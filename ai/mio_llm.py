from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from .. import config, red
import json

llm = ChatOpenAI(
    model=config.MODEL,
    api_key=config.API_KEY,
    base_url=config.BASE_URL
)

prompt = ChatPromptTemplate([
    ("system", "Ты полезный ассистент"),
    ("user", "{input}")
])

def get_session_history(session_id: str):
    data = red.get_messages_for_user(session_id)
    history = InMemoryChatMessageHistory()

    messages = json.loads(data)
    for mes in messages:
        history.add_message(mes["role"], mes["content"])
    
    return history

chain = prompt | llm

store = {}

chat = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input"
)

result = chat.invoke(
    {"input": "Привет, теперь тебя зовут Иван Дикпик"},
    config={"configurable": {"session_id": "1"}}
    ).content

print(result)

result = chat.invoke(
    {"input": "Какая у тебя фамилия"},
    config={"configurable": {"session_id": "1"}}
    )

print(result)
