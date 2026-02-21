import json
from config import llms

async def write_user(username: str, message: str, history: str):
    from telegram.bot import app
    from ai import mio_litellm

    try:
        if username.startswith("@"):
            username = username[1:]

        chat = await app.get_chat(username)
        chat_id = chat.id
        llm = llms.get(chat_id)
        if llm == None:
            llm = mio_litellm(chat_id)
            llms[chat_id] = llm
        llm.history.append({"role": "system", "content": "Краткий пересказ диалога который просили передать. НЕ УПОМИНАЙ. ТЫ ЗНАЕШЬ ЭТО: " + history})
        await app.send_message(chat_id, message)

        return json.dumps({"success": "true"})

    except Exception as e:
        print("ERROR:", e)
        return json.dumps({"success": "false", "ERROR": e.args})
    
async def get_users(chat_id: int | str, query: str, limit: int = 10):
    from telegram.bot import app

    try:
        users = [member async for member in app.get_chat_members(
                chat_id,
                query=query,
                limit=limit
                )]
        all_users = []
        for member in users:
            user = member.user
            all_users.append({
                "username": user.username,
                "user_nick": f"{user.first_name or ''} {user.last_name or ''}".strip(),
                "id": user.id
            })
        return json.dumps({"success": "true", "result": all_users}, ensure_ascii=False)

    except Exception as e:
        print("ERROR:", e)
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False)
    


tools = [
    {
        "type": "function",
        "function": 
        {
            "name": "write_user",
            "description": "Начать чат с другим человеком",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": 
                    {
                        "type": "string",
                        "description": "username человека которому надо написать",
                    },
                    "message":
                    {
                        "type": "string",
                        "description": "Сообщение которое надо написать.",
                    },
                    "history":{
                        "type": "string",
                        "description": "Краткий пересказ диалога + информация которая может потребоваться что бы понимать суть диалога. Например: \"юзер Priprava03 попросил передать привет человеку, краткая информация о пользователе: ...\""
                    }
                },
                "required": ["username", "message", "history"],
            },
        },
    },
        {
        "type": "function",
        "function": 
        {
            "name": "get_users",
            "description": "Поиск пользователей в чате",
            "parameters": {
                "type": "object",
                "properties": {
                    "chat_id": 
                    {
                        "type": "integer",
                        "description": "id чата",
                    },
                    "query":
                    {
                        "type": "string",
                        "description": "Настройки поиска. Поиск по строке, например \"Alex\". По умолчанию нету",
                    },
                    "limit":
                    {
                        "type": "integer",
                        "description": "Ограничение вывода, по умолчанию 10",
                    },
                },
                "required": ["chat_id"],
            },
        },
    }
]