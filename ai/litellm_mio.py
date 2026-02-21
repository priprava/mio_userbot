import litellm, json
import red
from config import API_KEY, MODEL, BASE_URL
from ai.modules import tools, write_user, get_users

class mio_litellm():
    def __init__(self, id: str):
        super().__init__()
        self.id = id
        self.history = []

    
    async def ask(self, prompt: str) -> str:
        self.history = await red.get_history(self.id)
        self.history.append({"role": "user", "content": prompt})
        req = await litellm.acompletion(
                model=MODEL,
                base_url=BASE_URL,
                api_key=API_KEY,
                messages=self.history,
                tools=tools,
                tool_choice="auto",
            )
        print(self.history)
        if req.choices[0].message.tool_calls:
            available_functions = {
                "write_user": write_user,
                "get_users": get_users
            }  # only one function in this example, but you can have multiple
            self.history.append({
            "role": "assistant",
            "content": req.choices[0].message.content,
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
                for tool_call in req.choices[0].message.tool_calls
            ],
            })
            for tool_call in req.choices[0].message.tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                if function_name == "write_user":
                    function_response = await function_to_call(
                        username=function_args.get("username"),
                        message=function_args.get("message"),
                        history=function_args.get("history")
                    )
                if function_name == "get_users":
                    function_response = await function_to_call(
                        chat_id=function_args.get("chat_id"),
                        query=function_args.get("query"),
                        limit=function_args.get("limit"),
                    )
                
                self.history.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            req = await litellm.acompletion(
                model=MODEL,
                base_url=BASE_URL,
                api_key=API_KEY,
                messages=self.history,
                tools=tools,
                tool_choice="none"
            )

        answer = req.choices[0].message.content
        self.history.append({"role": "assistant", "content": answer})
        await red.save_history(self.id, self.history)
        return answer
        
    async def add_to_history(self, message):
            await red.clear_history(self.id)
            self.history = []
            self.history.append(message)
            await red.save_history(self.id, self.history)

async def summerize(text: dict) -> str:
    data = []
    data.append({"role": "system", "content": """
    Сделай краткое, но информативное резюме следующего диалога. Выдели только ключевые идеи и факты, убери второстепенные детали. Сохрани логическую структуру и основной смысл. Объём — 3–6 предложений. Пиши ясно и нейтрально, без личных комментариев.
    """})
    data.extend(text)

    req = litellm.completion(
        model=MODEL,
        base_url=BASE_URL,
        api_key=API_KEY,
        messages=data
        )
    return req.choices[0].message.content

if __name__ == "__main__":
    pass