from aiogram import Router, F
from ai import mio_litellm
from config import llms, nlp

text_router = Router()

@text_router.message(F.text)
async def get_message(message):
    print(message.from_user.id)
    llm = llms.get(message.from_user.id)
    if llm == None:
        llm = mio_litellm(message.from_user.id)
        llms[message.from_user.id] = llm
    
    doc = nlp(await llm.ask(message.text))
    sentences = [sent.text for sent in doc.sents]
    for sen in sentences:
        await message.bot.send_message(message.from_user.id, sen)