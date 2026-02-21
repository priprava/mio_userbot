from pyrogram import Client, filters
from pyrogram.types import Message
from config import LOGIN, API_ID, HASH_ID, PHONE, llms, nlp
import red, random
from ai import mio_litellm
from pyrogram.errors import PeerFlood, Flood, FloodWait
import asyncio

app = Client(LOGIN, API_ID, HASH_ID, phone_number=PHONE)

def start_bot():
    app.run()
    print("Бот запущен!")

@app.on_message(filters.private & filters.command("reset"))
async def reset(client: Client, message: Message):
    await red.clear_history(message.from_user.id)
    await client.send_message(message.chat.id, "История очищена")

@app.on_message(filters.private & filters.command("new"))
async def reset(client: Client, message: Message):
    llm = llms.get(message.from_user.id)
    if llm is None:
        llm = mio_litellm(message.from_user.id)
        llms[message.from_user.id] = llm

    # Получаем текст после команды
    if len(message.command) > 1:
        new_prompt = " ".join(message.command[1:])
    else:
        await message.reply("После /new нужно написать текст.")
        return

    await llm.add_to_history({
        "role": "system",
        "content": "Твой новый промпт: " + new_prompt
    })

    await message.reply("Новый промпт установлен ✅")

@app.on_message(filters.private & ~filters.me)
async def start(client: Client, message: Message):
    llm = llms.get(message.from_user.id)
    if llm == None:
        llm = mio_litellm(message.from_user.id)
        llms[message.from_user.id] = llm
    doc = nlp(await llm.ask(message.text))
    sentences = [sent.text for sent in doc.sents]
    for sen in sentences:
        await client.send_message(message.from_user.id,
                                   sen,
                                   parse_mode=None)
        await asyncio.sleep(random.randint(3, 7))

    

@app.on_message(filters.group & (filters.reply | filters.mentioned))
async def start(client: Client, message: Message):
        if message.chat.id == -1002264832322: return
        mess = ""
        if message.reply_to_message != None:
            if message.reply_to_message.from_user.id == 7820667543: 
                mess += f"[Ответ на: {message.reply_to_message.text}] "
            else: return
        mess += f"[{message.from_user.first_name}]: {message.text if message.text else message.caption}]"
        llm = llms.get(message.chat.id)
        if llm == None:
            llm = mio_litellm(message.chat.id)
            llms[message.chat.id] = llm
        try:
            await client.send_message(message.chat.id,
                                       await llm.ask(mess),
                                         reply_to_message_id=message.id,
                                         parse_mode=None)
            await asyncio.sleep(random.randint(3, 7))
        except PeerFlood or FloodWait or Flood:
            await asyncio.sleep(random.randint(3, 7))

    

async def get_info_about_user(id):
    try:
        info = await app.get_users(id)
        return f"""
    Имя: {info.first_name} {info.last_name}
    username: {info.username}
    """
    except:
        info = await app.get_chat(id)
        
        return f"""
    Чат: {info.title}
    username: {info.username}
    id: {info.id}
    """
        


if __name__ == "__main__":
    pass