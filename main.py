import os
import signal

import telegram.error
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup
from mutagen.mp3 import MP3
from musicfunctions import get_random_music, get_current_music, get_music_by_genre, get_music_by_artist
from musicfunctions import get_music_by_name, get_music_by_name_and_artist


keyboard = [['Найти песню'], ['Найти по жанру']]


def start_command(update: Update, _: CallbackContext):
    update.effective_chat.send_message(text='Привет!', reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


def send_audio(update: Update, music_name: str):
    update.effective_chat.send_audio(
        audio=open(music_name, 'rb'),
        duration=int(MP3(music_name).info.length)
    )


def send_random_audio_command(update: Update, _: CallbackContext):
    name = get_random_music(full_path=True)
    print(name)
    send_audio(update, name)


def get_current_music_command(update: Update, _: CallbackContext):
    message = update.effective_message.text
    result = get_current_music(message, full_path=True)
    if result is None:
        update.effective_chat.send_message(text='Такой песни нет')
    else:
        send_audio(update, result)
    return ConversationHandler.END


def get_music_by_genre_command(update: Update, _: CallbackContext):
    message = update.effective_message.text
    get_music = get_music_by_genre(message, full_path=True)
    if len(get_music) == 0:
        update.effective_chat.send_message(text='Песен с таким жанром нет')
    else:
        for i in get_music:
            send_audio(update, i)
    return ConversationHandler.END


def current_music_command(update: Update, _: CallbackContext):
    update.effective_chat.send_message(text='Отправь название песни')
    return 1


def music_by_genre_command(update: Update, _: CallbackContext):
    update.effective_chat.send_message(text='Отправь название жанра')
    return 2


def send_error(update: Update, _: CallbackContext):
    raise telegram.error.NetworkError("Hello i am test error")


def unknown_command_handler(update: Update, _: CallbackContext):
    update.effective_chat.send_message(text='Такой комманды нет')


def error_handler(update: Update, context: CallbackContext):
    error = context.error
    print(error)
    if isinstance(error, telegram.error.NetworkError):
        os.kill(os.getpid(), signal.SIGINT)


def get_by_id_command(update:Update, context: CallbackContext):
    id_music = int(update.effective_message.text.split(' ')[1])
    music_path = get_current_music(id_music, full_path=True)
    send_audio(update, music_path)


def get_by_name_command(update:Update, context: CallbackContext):
    name = update.effective_message.text.split(' ')[1]
    music_path = get_music_by_name(name, full_path=True)
    send_audio(update, music_path)


def get_by_artist_command(update:Update, context: CallbackContext):
    artist = update.effective_message.text.split(' ')[1]
    music_paths = get_music_by_artist(artist, full_path=True)
    for i in music_paths:
        send_audio(update, i)


def get_by_genre_command(update:Update, context: CallbackContext):
    genre = update.effective_message.text.split(' ')[1]
    music_paths = get_music_by_artist(genre, full_path=True)
    for i in music_paths:
        send_audio(update, i)


def get_music_by_name_and_artist_command(update: Update, context: CallbackContext):
    name_artist = update.effective_message.text.split(' ')[1]
    music_path = get_music_by_artist(name_artist, full_path=True)
    send_audio(update, music_path)


def main(token: str) -> None:
    updater = Updater(token=token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('send_random_audio', send_random_audio_command))
    dispatcher.add_handler(CommandHandler('test_err', send_error))
    dispatcher.add_error_handler(error_handler)
    dispatcher.add_handler(CommandHandler('get_by_id', get_by_id_command))
    dispatcher.add_handler(CommandHandler('get_by_artist', get_by_artist_command))
    dispatcher.add_handler(CommandHandler('get_by_name', get_by_name_command))
    dispatcher.add_handler(CommandHandler('get_by_genre', get_by_genre_command))
    dispatcher.add_handler(CommandHandler('get_music_by_name_and_artist', get_music_by_name_and_artist_command))

    get_current_music_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Найти песню'), current_music_command)],
        states={
            1: [MessageHandler(Filters.text, get_current_music_command)],
        },
        fallbacks=[]
    )
    get_music_by_genre_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Найти по жанру'), music_by_genre_command)],
        states={
            2: [MessageHandler(Filters.text, get_music_by_genre_command)]
        },
        fallbacks=[]
    )

    dispatcher.add_handler(get_current_music_handler)
    dispatcher.add_handler(get_music_by_genre_handler)
    dispatcher.add_handler(MessageHandler(Filters.regex('/.*'), unknown_command_handler))

    print(updater.bot.get_me())
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    with open('token.txt', 'r') as t:
        m = t.read()

    main(m)
