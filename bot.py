import dotenv
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db import conn, cursor
import os
from dotenv import load_dotenv

dotenv.load_dotenv()

# создаем экземпляр бота с помощью токена
BOT = os.getenv("BOT")

# создаем экземпляр диспетчера, который будет обрабатывать сообщения
bot = Bot(token=BOT)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(massage: types.Message):
    await massage.answer('Привет! Это твой туду лист. /help для инструкций')


@dp.message_handler(commands=['add_task'])
async def add_task_command(message: types.Message):
# сообщение с запросом задачи
    await message.answer('Напиши задачу')

# добавляем обработчик для следующего сообщения
    dp.register_message_handler(process_new_task)


async def process_new_task(message: types.Message):
    # сохраняем задачу в базу данных
    task = message.text
    cursor.execute("INSERT INTO task (task, done) VALUES (?, ?)", (task, 0))
    conn.commit()
    await message.answer(f'Задача "{task}" успешно добавлена')


@dp.message_handler(commands=['list_tasks'])
async def list_tasks_command(message: types.Message):
    # удаляем выполненные задачи из базы данных
    cursor.execute("DELETE FROM task WHERE done=1")
    conn.commit()

    # получаем список невыполненных задач из базы данных и отправляем его пользователю
    cursor.execute("SELECT task FROM task WHERE done=0")
    undone_tasks = cursor.fetchall()
    response = ''
    if len(undone_tasks) > 0:
        response += 'Список невыполненных задач:\n'
        for index, task in enumerate(undone_tasks):
            response += f'{index+1}. {task[0]}\n'
    else:
        response += 'Нет невыполненных задач\n'
    await message.answer(response)


@dp.message_handler(commands=['done_task'])
async def done_task_command(message: types.Message):
    # получаем индекс выполненной задачи из сообщения пользователя
    task_index = message.text.split(' ')[1]
    cursor.execute("UPDATE task SET done=1 WHERE task_id=?", (task_index,))
    conn.commit()
    # удаляем выполненную задачу из базы данных
    cursor.execute("DELETE FROM task WHERE task_id=? AND done=1", (task_index,))
    conn.commit()

    await message.answer(f'Задача с индексом {task_index} отмечена как выполненная')

# запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

