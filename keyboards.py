from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    buttons = [
        [InlineKeyboardButton(text="💎 Сделать заказ Free Fire", callback_data="make_order")],
        [InlineKeyboardButton(text="📜 Мои заказы", callback_data="my_orders")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_diamonds_keyboard():
    diamonds = [
        ("100 + 10 бонус🔥 - 10 сомони", "100_10"),
        ("310 + 15 бонус🔥 - 29 сомони", "310_29"),
        ("520 + 24 бонус🔥 - 49 сомони", "520_49"),
        ("1060 + 53 бонус🔥 - 98 сомони", "1060_98"),
        ("2180 + 240 бонус🔥 - 210 сомони", "2180_210"),
        ("5600 + 560 бонус🔥 - 480 сомони", "5600_480"),
        ("Ваучер на неделю +450💎 - 16 сомони", "week_16"),
        ("Ваучер на месяц - 99 сомони", "month_99")
    ]
    buttons = []
    for text, callback in diamonds:
        buttons.append([InlineKeyboardButton(text=text, callback_data=f"diamond_{callback}")])
    
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_order")])
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
