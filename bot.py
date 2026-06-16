import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, MODERATOR_GROUP_ID, PAYMENT_PHONE, DB_PATH
from database import Database
from states import OrderStates, AdminStates
from keyboards import get_main_keyboard, get_admin_keyboard, get_cancel_keyboard

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота, диспетчера и БД
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
db = Database(DB_PATH)

# --- ХЕНДЛЕРЫ ПОЛЬЗОВАТЕЛЯ ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"👋 Привет! Я бот для пополнения игровой валюты Free Fire.\n\n"
        f"💳 Оплата принимается на номер: `{PAYMENT_PHONE}`\n"
        f"После оплаты создайте заказ и прикрепите скриншот чека.",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "make_order")
async def start_order(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(OrderStates.waiting_for_id)
    await callback.message.answer("Введите ваш игровой ID Free Fire:", reply_markup=get_cancel_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "cancel_order")
async def cancel_order(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Заказ отменен. Вы можете начать заново через /start")
    await callback.answer()

@dp.message(OrderStates.waiting_for_id)
async def process_id(message: types.Message, state: FSMContext):
    await state.update_data(game_id=message.text)
    await state.set_state(OrderStates.waiting_for_amount)
    await message.answer("Введите сумму пополнения (алмазы или валюта):", reply_markup=get_cancel_keyboard())

@dp.message(OrderStates.waiting_for_amount)
async def process_amount(message: types.Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await state.set_state(OrderStates.waiting_for_receipt)
    await message.answer(f"Отправьте скриншот чека об оплате на номер `{PAYMENT_PHONE}`:", reply_markup=get_cancel_keyboard(), parse_mode="Markdown")

@dp.message(OrderStates.waiting_for_receipt, F.photo)
async def process_receipt(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    data = await state.get_data()
    
    # Сохранение в БД
    order_id = db.add_order(
        user_id=message.from_user.id,
        username=message.from_user.username or "Unknown",
        game_id=data['game_id'],
        amount=data['amount'],
        receipt_file_id=photo_id
    )
    
    await state.clear()
    await message.answer(f"✅ Ваш заказ №{order_id} принят! Ожидайте подтверждения модератором.")
    
    # Уведомление модераторов
    admin_text = (
        f"🆕 **Новый заказ №{order_id}**\n"
        f"👤 Пользователь: @{message.from_user.username} (ID: {message.from_user.id})\n"
        f"🎮 Игровой ID: `{data['game_id']}`\n"
        f"💰 Сумма: {data['amount']}\n"
    )
    
    await bot.send_photo(
        chat_id=MODERATOR_GROUP_ID,
        photo=photo_id,
        caption=admin_text,
        reply_markup=get_admin_keyboard(order_id),
        parse_mode="Markdown"
    )

# --- ХЕНДЛЕРЫ МОДЕРАЦИИ ---

@dp.callback_query(F.data.startswith("admin_"))
async def handle_admin_actions(callback: types.CallbackQuery, state: FSMContext):
    action_data = callback.data.split("_")
    action = action_data[1]
    order_id = int(action_data[2])
    
    order = db.get_order(order_id)
    if not order:
        await callback.answer("Заказ не найден.")
        return

    user_id = order[1]

    if action == "accept":
        db.update_order_status(order_id, "accepted")
        await bot.send_message(user_id, f"✅ Ваш заказ №{order_id} выполнен! Алмазы зачислены.")
        await callback.message.edit_caption(caption=callback.message.caption + "\n\n✅ **СТАТУС: ВЫПОЛНЕН**", parse_mode="Markdown")
        await callback.answer("Заказ выполнен")

    elif action == "process":
        db.update_order_status(order_id, "processing")
        await bot.send_message(user_id, f"⏳ Ваш заказ №{order_id} принят в работу модератором.")
        await callback.message.edit_caption(caption=callback.message.caption + "\n\n⏳ **СТАТУС: В ПРОЦЕССЕ**", parse_mode="Markdown")
        await callback.answer("Статус обновлен: В процессе")

    elif action == "reject":
        await state.update_data(reject_order_id=order_id, admin_msg_id=callback.message.message_id)
        await state.set_state(AdminStates.waiting_for_rejection_reason)
        await callback.message.answer("Введите причину отказа:")
        await callback.answer()

@dp.message(AdminStates.waiting_for_rejection_reason)
async def process_rejection_reason(message: types.Message, state: FSMContext):
    data = await state.get_data()
    order_id = data['reject_order_id']
    reason = message.text
    
    order = db.get_order(order_id)
    user_id = order[1]
    
    db.update_order_status(order_id, "rejected", reason)
    await bot.send_message(user_id, f"❌ Ваш заказ №{order_id} отклонен.\nПричина: {reason}")
    
    # Обновление сообщения в группе модераторов (нужно знать ID сообщения)
    # Для простоты просто отправим новое уведомление или оставим как есть
    await message.answer(f"Заказ №{order_id} отклонен. Пользователь уведомлен.")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
