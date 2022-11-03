import time
import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import Config
import telebot

from typing import Union
from vk_api.vk_api import VkApiMethod


TG = telebot.TeleBot(Config.TG_TOKEN)
VK_SESSION = vk_api.VkApi(token=Config.VK_TOKEN)
VK = VK_SESSION.get_api()


def vk_required(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs, vk=VK)
    return wrapper


def get_timestamp() -> None:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


@vk_required
def get_name_by_id(user_id: Union[int, str], vk: "VkApiMethod"=None) -> str:
    t = vk.users.get(user_ids=(user_id,), lang='ru')[0]
    return f"{t['first_name']} {t['last_name']}"


def prepare_message(raw_message: str) -> str:
    symbols_to_escape = "._*~()[]|-"
    for symbol in symbols_to_escape:
        raw_message = raw_message.replace(symbol, f"\{symbol}")
    return raw_message


if __name__ == '__main__':
    print(get_timestamp(), "ВК-Бот запущен!")
    longpoll = VkBotLongPoll(VK_SESSION, Config.VK_GROUP_ID)

    while True:
        try:
            for event in longpoll.listen():
                if event.from_chat:
                    from_id = event.obj.message["from_id"]
                    from_name = get_name_by_id(from_id)
                    text = prepare_message(event.obj.message["text"])
                    attachments = event.obj.message["attachments"]
                    # print(attachments)
                    
                    if attachments:
                        for attachment in attachments:
                            if attachment["type"] == "photo":
                                TG.send_photo(
                                    Config.TG_CHAT_ID, 
                                    caption=f"*{from_name}:*\n{text}",
                                    photo=attachment["photo"]["sizes"][-1]["url"],
                                    parse_mode="MarkdownV2"
                                )
                            elif attachment["type"] == "wall":
                                attach = f"https://vk.com/wall{attachment['wall']['from_id']}_{attachment['wall']['id']}"
                                attach = attach.replace(".", "\.").replace("-", "\-").replace("_", "\_")
                                TG.send_message(
                                    Config.TG_CHAT_ID, 
                                    f"*{from_name}:*\n{text}\n\n*Вложение:* {attach}",
                                    parse_mode="MarkdownV2"
                                )
                            elif attachment["type"] == "sticker":
                                TG.send_document(
                                    Config.TG_CHAT_ID,
                                    document=attachment["sticker"]["images"][3]["url"],
                                    caption=f"*{from_name}:*",
                                    parse_mode="MarkdownV2"
                                )
                    else:
                        TG.send_message(
                            Config.TG_CHAT_ID, 
                            f"*{from_name}:*\n{text}",
                            parse_mode="MarkdownV2"
                        )
        except Exception as e:
            print(e)
            continue