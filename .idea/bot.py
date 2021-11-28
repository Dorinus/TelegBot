import telebot
import config
import random

from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('res/falloutcaps.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Random Nr")
    item2 = types.KeyboardButton("How are you?")

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Greetings from Fall Out Universe {0.first_name}! I am - <b>{1.first_name}</b>, a bot made for tests!".format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def response(message):
    if message.chat.type == 'private':
        if message.text == "Random Nr":
            bot.send_message(message.chat.id, str(random.randint(0, 1000)))
        elif message.text == "How are you?":

            bot.send_message(message.chat.id, "Good, how are you?")
        else:
            sticker = open('res/cryingviking.webp', 'rb')
            bot.send_sticker(message.chat.id, sticker)

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Sorry", callback_data="good")
            item2 = types.InlineKeyboardButton("I don't care", callback_data="bad")
            markup.add(item1, item2)

            bot.send_message(message.chat.id, "I don't know what to answer  :(", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, ":*")
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, "You are dead!")

            # # remove inline buttons
            #
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            #                       text="I don't know what to answer  :(", reply_markup=None)
            #
            #
            # # alert
            # bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
            #                           text="This is a test message!")
    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
