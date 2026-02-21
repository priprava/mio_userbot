from aiogram import types, Router
from aiogram.filters import CommandStart
from ai import mio_litellm
from config import llms, nlp



start_router = Router()

@start_router.message(CommandStart())
async def start(message: types.Message):
    print(message.from_user.id)
    llm = llms.get(message.from_user.id)
    if llm == None:
        llm = mio_litellm(message.from_user.id)
        llms[message.from_user.id] = llm
    doc = nlp(await llm.ask(f"[{message.from_user.first_name}]: 👋"))
    sentences = [sent.text for sent in doc.sents]
    for sen in sentences:
        await message.bot.send_message(message.from_user.id, sen)
