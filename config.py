import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URL = os.getenv("DB_URL")
COOLDOWN = 60                       #Cooldown time for a user in minutes.
RUNNER = [1342588891227492485]      #any user role to run the bot commands.
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
    },
    1421724529759223878: {
        "level": "level_3",
        "role": 1420397400282894428,
        "question_count": 5,
        "embed": 2,
        "document": "https://medium.com/openxai/openxai-a-permissionless-ai-protocol-90b8934519f1"
    },
    1421724560012738690: {
        "level": "level_4",
        "role": 1420397555111694339,
        "question_count": 5,
        "embed": 3,
        "document": "https://medium.com/openxai/build-deploy-own-the-new-rules-of-ai-monetization-in-openxai-studio-d0459448ca01"
    },
    1421724595085508688: {
        "level": "level_5",
        "role": 1420397584710631546,
        "question_count": 5,
        "embed": 4,
        "document": "https://medium.com/openxai/openxai-developer-workshop-how-to-tokenize-ai-models-llms-ai-agents-2658917a434b"
    },
    1421724623745187893: {
        "level": "level_6",
        "role": 1420397658614530109,
        "question_count": 5,
        "embed": 5,
        "document": "https://medium.com/openxai/openxai-a-permissionless-ai-protocol-90b8934519f1"
    },
    1421724649150087208: {
        "level": "level_7",
        "role": 1420397653807730688,
        "question_count": 5,
        "embed": 6,
        "document": "https://medium.com/openxai/turning-ai-deployment-from-weeks-to-minutes-b7ce0bd32a3d"
    },
    1421724691076219014: {
        "level": "level_8",
        "role": 1420397649634529290,
        "question_count": 5,
        "embed": 7,
        "document": "https://medium.com/openxai/openxai-weekly-progress-update-april-19-2026-4f250061a37f"
    },
    1421724715956830218: {
        "level": "level_9",
        "role": 1420397644454301736,
        "question_count": 5,
        "embed": 8,
        "document": "https://medium.com/openxai/openxai-a-permissionless-ai-protocol-90b8934519f1"
    },
    1421724743329120348: {
        "level": "level_10",
        "role": 1420397637202346147,
        "question_count": 5,
        "embed": 9,
        "document": "https://medium.com/openxai/openxai-weekly-progress-update-april-19-2026-4f250061a37f"
    }
}

#Selector key is discord channel id, and role is the role id. 


