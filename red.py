import json, tiktoken
from redis.asyncio import Redis
from config import SYSTEM_MESSAGE

r = Redis()

async def get_history(id: str):
    get = await r.get(f"{id}::messages")
    if get != None:
        data = json.loads(get)
        if num_tokens_from_string(str(data[1:])) > 10000:
            from ai import summerize
            sumer = {"role": "system", "content": "История диалога: " + await summerize(data[1:], )}
            data.clear()
            data.append({"role": "system", "content": SYSTEM_MESSAGE})
            data.append(sumer)

        return data
    else:
        from telegram.bot import get_info_about_user
        return [{"role": "system", "content": SYSTEM_MESSAGE}, {"role": "system", "content": "Информация о user: " + await get_info_about_user(id)}]

async def save_history(id: str, messages):
    await r.set(f"{id}::messages", json.dumps(messages, ensure_ascii=False))

async def clear_history(id: str):
    await r.delete(f"{id}::messages")

def num_tokens_from_string(string: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(string))

if __name__ == "__main__":
    pass