import os


class Config:
    VK_TOKEN = os.getenv("VK_TOKEN")
    VK_CHAT_ID = os.getenv("VK_CHAT_ID")
    VK_GROUP_ID = os.getenv("VK_GROUP_ID")
    VK_SERVICE = os.getenv("VK_SERVICE")
    TG_TOKEN = os.getenv("TG_TOKEN")
    TG_CHAT_ID = os.getenv("TG_CHAT_ID")
