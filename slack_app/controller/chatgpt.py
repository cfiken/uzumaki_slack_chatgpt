from slack_bolt import App
from slack_app.model.chatgpt import ChatGPT
from slack_app.controller.base import Controller


DEFAULT_MODEL_NAME = 'gpt-3.5-turbo'


class ChatGPTController(Controller):
    def __init__(self, app: App) -> None:
        super().__init__()
        self.app = app
        self.chatgpt = ChatGPT()

    def handle(self, *args, **kwargs) -> str:
        thread_ts = kwargs.get('thread_ts')
        channel = kwargs.get('channel')
        say = kwargs.get('say')
        messages = self.get_thread_messages(channel, thread_ts)
        if not messages:
            return 'Please input content.'
        res = self.chatgpt.run(messages)
        say(res, thread_ts=thread_ts, reply_broadcast=True)
        return res
    
    def get_thread_messages(self, channel: str, thread_ts: str) -> list[dict[str, str]]:
        res = self.app.client.conversations_replies(channel=channel, ts=thread_ts)
        return [{'role': message.get('user', 'bot'), 'content': message['text']} for message in res['messages']]
    