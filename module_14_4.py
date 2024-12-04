from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from crud_function import initiate_db, add_product, get_all_products
import os

# 1. Token bot
API_TOKEN = ''

# 2. Создаём экземпляры бота, хранилища и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# 3. Главная клавиатура
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рассчитать')],
        [KeyboardButton(text='Информация')],
        [KeyboardButton(text='Купить')]
    ],
    resize_keyboard=True
)

# 4. Обработчики
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Приветственное сообщение
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=main_menu_kb)

@dp.message_handler(lambda message: message.text == 'Купить')
async def get_buying_list(message: types.Message):
    # Получаем продукты из базы данных
    products = get_all_products()

    # Пути к фотографиям
    product_images = [
        "files/image1.jpeg",
        "files/image2.jpeg",
        "files/image3.jpeg",
        "files/image4.jpeg"
    ]

    if not products:
        await message.answer("Продукты отсутствуют.")
        return

    for idx, product in enumerate(products):
        product_id, title, description, price = product

        # Формируем текст
        product_text = f"Название: {title}\nОписание: {description}\nЦена: {price} руб."
        await message.answer(product_text)

        # Отправляем фотографию, если она существует
        try:
            with open(product_images[idx], "rb") as photo:
                await message.answer_photo(photo=photo)
        except (FileNotFoundError, IndexError):
            await message.answer("Фотография отсутствует.")

# Запуск бота
if __name__ == '__main__':
    # Инициализация базы данных
    initiate_db()

    # Добавление продуктов, если база пустая
    if not get_all_products():
        initial_products = [
            ("Product1", "Описание 1", 100),
            ("Product2", "Описание 2", 200),
            ("Product3", "Описание 3", 300),
            ("Product4", "Описание 4", 400),
        ]
        for product in initial_products:
            add_product(*product)

    executor.start_polling(dp, skip_updates=True)
