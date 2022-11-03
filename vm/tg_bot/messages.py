import time
import vk_api
from vk_api.utils import get_random_id
from config import Config
import json
import random


def dump_data(data_):
    with open("data.json", "w") as file:
        json.dump(data_, file)


def get_msg():
    return random.choice(Config.PHRASES)


def work(token, owner, post):
    try:
        vk_session = vk_api.VkApi(token=token)
        vk = vk_session.get_api()

        vk.wall.createComment(
            owner_id=owner,
            post_id=post,
            message=get_msg()
        )
    except Exception:
        return


def start_work(owner, post, count=3):
    for token in random.choices(Config.ACCOUNTS, k=count):
        time.sleep(30 + random.random() * 22)
        work(token, owner, post)


def start():
    vk_session = vk_api.VkApi(token=Config.VK_TOKEN)
    vk = vk_session.get_api()
    # owner = "-211070446"
    owner = Config.OWNER
    with open("data.json", "r") as file:
        data = json.load(file)
    last = data["last"]

    while True:
        print("Checkin' for new posts...")
        post = vk.wall.get(
            # owner_id="-211070446"
            owner_id=owner
        )["items"][0]
        if post["id"] != last:
            last = post["id"]
            dump_data({"last": last})
            vk.messages.send(
                chat_id=Config.CHAT_ID, 
                random_id=get_random_id(),
                message=f"У тамарочки новый пост: https://vk.com/wall{post['owner_id']}_{post['id']}\nЗапускаем скам"
            )
            start_work(owner, post["id"], count=random.randint(3, 10))
        else:
            print("Nothing new...")
        time.sleep(Config.SLEEP_TIME)
