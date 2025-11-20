import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URL = os.getenv("DB_URL")
COOLDOWN = 60 #Cooldown time for a user in minutes.
RUNNER = [1342588891227492485] #any user role to run the bot commands.
SELECTOR = {
    1420373848280403968: {
        "level": "level_1",
        "role": 1420384956508799172,
        "question_count": 5,
        "embed": 0,
        "document": "https://docs.openxai.org/"
    },
    1421724073263759471: {
        "level": "level_2",
        "role": 1420397364782432267,
        "question_count": 5,
        "embed": 1,
        "document": "https://medium.com/openxai/openxai-a-permissionless-ai-protocol-90b8934519f1"
    }
}

#Selector key is discord channel id, and role is the role id. 

