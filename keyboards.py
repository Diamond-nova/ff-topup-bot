from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    buttons = [
        [InlineKeyboardButton(text="💎 Сделать заказ Free Fire", callback_data="make_order")],
        [InlineKeyboardButton(text="📜 Мои заказы", callback_data="my_orders")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_admin_keyboard(order_id):
    buttons = [
        [
            InlineKeyboardButton(text="✅ Принять", callback_data=f"admin_accept_{order_id}"),
            InlineKeyboardButton(text="⏳ В процессе", callback_data=f"admin_process_{order_id}")
        ],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"admin_reject_{order_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_cancel_keyboard():
    buttons = [[InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_order")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
