from ai.modules import write_user
import asyncio
from telegram.bot import start_bot
import logging, time

logging.basicConfig(level=logging.INFO)

start_bot()

print(asyncio.run(write_user("Priprava03", "Попросили передать привет")))


# from pyrogram import Client, filters
# from pyrogram.types import Message
# from dotenv import load_dotenv
# import os, re
# from ai import mio_litellm

# load_dotenv()

# API_ID=30582976
# API_HASH="f671ec1fbe4929fce5d49accb011b05b"
# PHONE = "16573626597"
# LOGIN="Ne_zapomnai"

# app = Client(LOGIN, API_ID, API_HASH, phone_number=PHONE)

# print("запущен")

# x = mio_litellm("1801855220")

# @app.on_message(filters.private & ~filters.command("reset"))
# async def start(client: Client, message: Message):
#     answ = await x.ask(message.text)
#     await client.send_message(message.chat.id, answ)
    
# @app.on_message(filters.command("reset"))
# async def reset(client: Client, message: Message):
#     await red.clear_history(message.from_user.id)

# app.run()




# import litellm, asyncio
# import red, json
# from config import API_KEY, MODEL, BASE_URL
# with open(r"ai\mio_prompt1.txt", encoding="utf-8") as txt_prompt:
#     SYSTEM_MESSAGE = txt_prompt.read().strip()



# def get_current_test(location):
#         return json.dumps({"location": location})

# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_current_test",
#             "description": "Тестовая функция. Вызови её",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "location": {
#                         "type": "string",
#                         "description": "Любая строка",
#                     },
#                     "unit": {"type": "string"},
#                 },
#                 "required": ["location"],
#             },
#         },
#     }
# ]




# class mio_litellm():
#     def __init__(self, id: str):
#         super().__init__()
#         self.id = id
#         self.history = [{"role": "system", "content": SYSTEM_MESSAGE}]

    
#     async def ask(self, prompt: str) -> str:
#         self.history.append({"role": "user", "content": prompt})
#         req = await litellm.acompletion(
#         model=MODEL,
#         base_url=BASE_URL,
#         api_key=API_KEY,
#         messages=self.history,
#         tools=tools,
#         tool_choice="auto"
#         )
#         answer = req.choices[0].message.content
#         print(answer)
#         print(req.choices[0].message.tool_calls)
#         self.history.append({"role": "assistant", "content": answer})
#         return answer
    
# l = mio_litellm(123)
# asyncio.run(l.ask(input()))