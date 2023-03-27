from datetime import date
import openai
from slack_app.util.routine import get_logger


DEFAULT_MODEL_NAME = 'gpt-3.5-turbo'
KNOWLEDGE_CUTOFF  = '2021-09'
SYSTEM_CONTENT = f'You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. \
Knowledge cutoff: {KNOWLEDGE_CUTOFF} Current date: {date.today()}'
BOT_USER_ID = '@U0504NZFL4S'

logger = get_logger(__name__)


class ChatGPT:
    def __init__(self, model_name: str = DEFAULT_MODEL_NAME) -> None:
        self.model_name = model_name

    def chat_request(self, model_name: str, messages: list[dict[str: str]]) -> str:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages
        )
        return response.choices[0]['message']['content']

    def run(self, messages: list[dict[str, str]]) -> str:
        chatgpt_messages = [
            {'role': 'system', 'content': SYSTEM_CONTENT},
        ]
        for message in messages:
            content = self._remove_mention(message['content'])
            role = 'assistant' if message['role'] == 'bot' or message['role'] == BOT_USER_ID[1:] else 'user'
            chatgpt_messages.append({'role': role, 'content': content})

        logger.info(f'chatgpt request: {chatgpt_messages}, with model {self.model_name}')
        res = self.chat_request(self.model_name, chatgpt_messages)
        logger.info(f'chatgpt response: {res}')
        return res
    
    def _remove_mention(self, content: str) -> str:
        return content.replace(f'<{BOT_USER_ID}>', '').strip()
