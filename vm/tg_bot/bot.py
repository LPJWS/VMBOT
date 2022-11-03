import time
import telebot
from config import Config
import vk_api
from vk_api.utils import get_random_id
from io import BytesIO, BufferedReader
import requests


TG = telebot.TeleBot(Config.TG_TOKEN)
VK_SESSION = vk_api.VkApi(token=Config.VK_TOKEN)
VK = VK_SESSION.get_api()


def get_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


@TG.message_handler(content_types=['text'])
def get_text_messages(message):
    VK.messages.send(
        chat_id=Config.VK_CHAT_ID, 
        random_id=get_random_id(), 
        message=message.text
    )


@TG.message_handler(content_types=['photo'])
def get_photo_messages(message: telebot.types.Message):
    file = TG.get_file(message.photo[-1].file_id)
    ba = TG.download_file(file.file_path)

    server = VK.photos.getMessagesUploadServer()['upload_url']
    pfile = requests.post(server, files={'photo': ("file.png", ba)}).json()
    photo = VK.photos.saveMessagesPhoto(server=pfile['server'], photo=pfile['photo'], hash=pfile['hash'])[0]
    attachments = ['photo%s_%s' % (photo['owner_id'], photo['id'])]

    VK.messages.send(
        chat_id=Config.VK_CHAT_ID, 
        random_id=get_random_id(), 
        attachment=",".join(attachments)
    )


@TG.message_handler(content_types=['sticker'])
def get_sticker_messages(message: telebot.types.Message):
    file = TG.get_file(message.sticker.file_id)
    ba = TG.download_file(file.file_path)

    server = VK.docs.getMessagesUploadServer(peer_id=f"{2000000000 + int(Config.VK_CHAT_ID)}")['upload_url']
    pfile = requests.post(server, files={'file': (file.file_path.split("/")[1], ba)}).json()
    doc = VK.docs.save(file=pfile['file'], title=file.file_path.split("/")[1])
    attachments = ['doc%s_%s' % (doc['doc']['owner_id'], doc['doc']['id'])]

    VK.messages.send(
        chat_id=Config.VK_CHAT_ID, 
        random_id=get_random_id(), 
        attachment=",".join(attachments)
    )


if __name__ == '__main__':
    print(get_timestamp(), "ТГ-Бот запущен!")
    TG.polling(none_stop=True, interval=0)
