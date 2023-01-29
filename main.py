import telebot
from telebot import types
from network import *
from functions import *

bot = telebot.TeleBot('Bot Token')

model = Net(ngf=128)
model.load_state_dict(torch.load('pretrained.model'), False)

content_flag = False
style_flag = False


def do_it(content_root, style_root, im_size):
    content_image = load_image(content_root, size=im_size, is_content=True)
    style = load_image(style_root, size=im_size)

    style_v = Variable(style)
    content_image = Variable(content_image)

    model.setTarget(style_v)
    output = model(content_image)
    save_image(output.data[0], 'result.jpg')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('Помощь')
    markup.add(btn)
    bot.send_message(message.chat.id, 'Привет! Я - бот, который переносит стиль с одной фотографии на другую.\n'
                                      'Ты можешь нажать на кнопку "Помощь" и получить инструкцию.', parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def help(message):
    if message.text == 'Помощь':
        bot.send_message(message.chat.id, '1. Пришлите фотографию, на которую желаете нанести стиль (Чем меньше контраст цветов, тем лучше ляжет стиль).\n'
                                          '2. Пришлите фотографию, с которой хотите перенести стиль (Желательно максимально контрастную).\n'
                                          '3. Ожидайте 5-15 секунд.'
                                          'Примечание: не отправляйте больше одной фотографии в одном сообщении.', parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Я больше ничего не умею(((.', parse_mode='html')


@bot.message_handler(content_types=['photo'])
def change_style(message):

    global content_flag
    global style_flag

    if not content_flag:
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = 'C:/Users/Vadim/PycharmProjects/ChangeStyleBot/content.jpg'
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
        except Exception as e:
            print(e)

        bot.send_message(message.chat.id, 'Изображение получено. Пришлите изображение стиля.', parse_mode='html')
        content_flag = True
    else:
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = 'C:/Users/Vadim/PycharmProjects/ChangeStyleBot/style.jpg'
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
        except Exception as e:
            print(e)

        bot.send_message(message.chat.id, text='Изображение стиля получено. Ожидайте...', parse_mode='html')
        style_flag = True

    if content_flag and style_flag:
        do_it('content.jpg', 'style.jpg', 512)
        with open('result.jpg', 'rb') as file:
            bot.send_photo(message.chat.id, file, caption='Изображение готово.')
        content_flag = False
        style_flag = False


bot.polling(none_stop=True)
