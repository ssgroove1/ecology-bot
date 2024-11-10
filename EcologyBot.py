import telebot, requests
import random, time, threading, schedule
from bot_logic import gen_pass
import os

TOKEN = "TOKEN"

bot = telebot.TeleBot(TOKEN)
    
@bot.message_handler(commands=['start', "hello"])
def start(message):
    bot.send_message(message.chat.id, "Привет, я твой личный бот помощник.")

def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text='Таймер истек!')

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "У меня есть команды такие как: /gen_pass /set /mem /animals /ecology .Есть ещё и текстовые: Орел и решка, Привет, Пока")

@bot.message_handler(commands=['mem'])
def send_mem(message):
    path = os.path.abspath("images") # Абсолютный путь к папке с изображениями
    meme_list = os.listdir(path) # Список изображений
    random_meme = random.choice(meme_list) # выбираем случайное изображение
    meme_path = os.path.join(path, random_meme) # Абсолютный путь к изображению
    bot.send_message(message.chat.id, "Путь к мему: "+ meme_path) # отправляем абсолютный путь к изображению
    with open(meme_path, 'rb') as f:  # Открываем файл
        bot.send_photo(message.chat.id, f) # Отправляем файл

@bot.message_handler(commands=['ecology'])
def send_problem(message):
    bot.send_message(message.chat.id, "Выкидывайте мусор правильно!")
    with open("instruction/tfda.jpg", "rb") as h:
        bot.send_photo(message.chat.id, h)

@bot.message_handler(commands=['animals'])
def send_mem(message):
    h = random.randint(1,6)
    if h == 1 or h == 2:
        bot.send_message(message.chat.id, "Вы нашли редкую картинку!")
        with open("animals/animal1.jpg", "rb") as g:
            bot.send_photo(message.chat.id, g)
    elif h == 3 or h == 4 or h == 5: 
        bot.send_message(message.chat.id, "Вы нашли обычную картинку!")
        with open("animals/animal2.png", "rb") as j:
            bot.send_photo(message.chat.id, j)
    else:
        bot.send_message(message.chat.id, "Вы нашли легендарную картинку!")
        with open("animals/animal3.png", "rb") as k:
            bot.send_photo(message.chat.id, k)

@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        schedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)
    else:
        bot.reply_to(message, 'Введите: /set <seconds>')


def get_duck_image_url():    
        url = 'https://random-d.uk/api/random'
        res = requests.get(url)
        data = res.json()
        return data['url']
    
    
@bot.message_handler(commands=['duck'])
def duck(message):
    '''По команде duck вызывает функцию get_duck_image_url и отправляет URL изображения утки'''
    image_url = get_duck_image_url()
    bot.reply_to(message, image_url)


@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)

@bot.message_handler(commands=["gen_pass"])
def gen_pass1(message):
    bot.send_message(message.chat.id, gen_pass(10))


@bot.message_handler(content_types=["text"])
def send_text(message):
    if message.text == "привет":
        bot.send_message(message.chat.id, "Привет!")
    elif message.text == "пока":
        bot.send_message(message.chat.id, "Пока!")
    elif message.text == "Орел и решка":
        bot.send_message(message.chat.id, "Подбрасываю монетку!")
        time.sleep(3)
        this222 = random.randint(1,2)
        if this222 == 1:
            bot.send_message(message.chat.id, "Выпал орел!")
        if this222 == 2:
            bot.send_message(message.chat.id, "Выпала решка!")


if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
