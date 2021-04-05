from qbittorrent import Client
from secret import *
import telebot

bot = telebot.TeleBot(token=TOKEN)
list_torrent = []


def download_book(magnet_link):
    qb = Client('http://localhost:8080/')
    qb.login()  # https://pypi.org/project/python-qbittorrent/
    len_1 = len(qb.torrents())
    qb.download_from_link(magnet_link, savepath=Save_location)
    len_2 = len(qb.torrents())
    if len_2 > len_1:
        print('Скачивается')
        return "Скачивается"
    else:
        print('Не корректная ссылка')
        return 'Не корректная ссылка'


def download_greed(torrent_magnet_message):
    while True:
        qb = Client('http://localhost:8080/')
        qb.login()  # https://pypi.org/project/python-qbittorrent/
        list_torrent_qb = qb.torrents()
        for tor in list_torrent_qb:
            if torrent_magnet_message[0] in tor["magnet_uri"]:
                if tor['state'] == "stalledUP":
                    print('Download')
                    qb._delete(tor['hash'])
                    return "Скачалось"


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.reply_to(message, "Добро пожаловать\n"
                          "Чтобы скачать книгу\n"
                          "Напишите слово 'Скачать' пробел\n"
                          "и вставьте magnet ссылку\n")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    cmd, *args = message.text.split()
    cmd.lower()
    if cmd == 'скачать':
        list_torrent.append([args[0][0:40], message])
        bot.send_message(message.from_user.id, download_book(args))
    else:
        bot.send_message(message.from_user.id, "Нет такой команды")
        return

    torrent_magnet_message = list_torrent.pop(0)
    bot.reply_to(torrent_magnet_message[1], download_greed(torrent_magnet_message))


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=2)
