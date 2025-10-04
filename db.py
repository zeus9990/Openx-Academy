import motor.motor_asyncio
from config import DB_URL, COOLDOWN
import random
from datetime import datetime, timedelta, timezone

database = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
db = database['openxAI']
questions = db['questions']
progress = db['progress']


def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or len(parts) == 0:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return ' '.join(parts)


async def add_question(question, option_A, option_B, option_C, option_D, answer, level):
    data = await questions.find_one({'question': question})
    if not data:
        await questions.insert_one(
            {
            'level': level, 'question': question,
                'options': {
                    "A": option_A,
                    "B": option_B,
                    "C": option_C,
                    "D": option_D
                },
                'answer': answer
            }
        )
        return True
    else:
        return False


async def get_random_questions_for_level(level, limit):
    question_list = await questions.find({"level": level}).to_list(length=None)
    for item in question_list:
        item.pop('_id', None)
    random.shuffle(question_list)
    random_questions = question_list[:limit]
    return random_questions


async def get_question(user_id, level, question_count):
    current_time = datetime.now(timezone.utc)
    user = await progress.find_one({'user_id': user_id})

    # Case 1: First attempt ever
    if not user:
        doc = {
            'user_id': user_id,
            f'{level}': False,
            f'{level}_last_attempt': current_time
        }
        await progress.insert_one(doc)
        questions = await get_random_questions_for_level(level=level, limit=question_count)
        return True, questions

    # Case 2: User exists
    current_status = user.get(level, False)
    if not current_status:
        last_attempt = user.get(f'{level}_last_attempt')
        if last_attempt:
            if last_attempt.tzinfo is None:
                last_attempt = last_attempt.replace(tzinfo=timezone.utc)
            elapsed = current_time - last_attempt
            if elapsed < timedelta(minutes=COOLDOWN):
                remaining = timedelta(minutes=COOLDOWN) - elapsed
                formatted_time = format_timedelta(remaining)
                return False, f'> **Hey <@{user_id}>, you already attempted this test. Try again in {formatted_time}.**'

        # Either no last attempt or cooldown expired
        await progress.update_one(
            {'user_id': user_id},
            {'$set': {f'{level}_last_attempt': current_time}},
            upsert=True
        )
        questions = await get_random_questions_for_level(level=level, limit=question_count)
        return True, questions

    # Case 3: Already completed the level
    return False, f'> **Hey <@{user_id}>, you already completed this Level.**'


async def update_level_status(user_id, level, status):
    await progress.update_one(
        {'user_id': user_id},
        {'$set': {level: status}},
        upsert=True
    )
