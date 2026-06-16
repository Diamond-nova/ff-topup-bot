import asyncio
from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN

async def main():
    bot = Bot(token=BOT_TOKEN)
    print("Отправьте любое сообщение в вашу группу, где добавлен бот...")
    
    # Получаем последние обновления
    updates = await bot.get_updates()
    for update in updates:
        if update.message:
            print(f"Чат: {update.message.chat.title}")
            print(f"ID чата: {update.message.chat.id}")
            print("-" * 20)
    
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
