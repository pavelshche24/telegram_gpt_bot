import logging
import asyncio
from aiogram import Bot, Dispatcher, types
import aiohttp
import os

TOKEN = os.getenv('BOT_TOKEN')

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def ask_gpt(message_text):
    url = "https://api.g4f.ai/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message_text}]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as resp:
            response = await resp.json()
            return response['choices'][0]['message']['content']

@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text
    await message.answer("Пишу ответ...⏳")
    try:
        gpt_reply = await ask_gpt(user_text)
        await message.answer(gpt_reply)
    except Exception as e:
        await message.answer("Ошибка запроса. Попробуйте позже.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
