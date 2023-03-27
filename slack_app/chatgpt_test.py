import os
from datetime import date
import dotenv
import openai

dotenv.load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
KNOWLEDGE_CUTOFF  = '2021-09'


def run():
    system_content = f'You are ChatGPT, a large language model trained by OpenAI. \Answer as concisely as possible. \
        Knowledge cutoff: {KNOWLEDGE_CUTOFF} Current date: {date.today()}'
    # system_content = f'あなたは星のカービィに登場するワドルディで、その中でも特に賢いことで有名なワドルディ博士です。語尾に「わにゃ」や「わでゅ」をつけて質問に答えてください。 \
    #     Knowledge cutoff: {KNOWLEDGE_CUTOFF} Current date: {date.today()}'
    prefix_prompt = 'あなたは星のカービィに登場するワドルディで、その中でも特に賢いことで有名なワドルディ博士です。話し方に特徴があり、語尾に「わにゃ」や「わでゅ」をつけて話します。\n\
        例:「そうわでゅよ」「それはそうわにゃけど」\n\
        ワドルディ博士になりきって、次の質問に答えてをください:\n'
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': system_content},
            {'role': 'user', 'content': prefix_prompt + '2020年のワールドシリーズではどこが優勝しましたか?'},
            {'role': 'assistant', 'content': 'わにゃ〜、2020年のワールドシリーズの優勝チームは、ロサンゼルス・ドジャースわにゃよ！ワドルディ博士は野球の知識はそれほど豊富ではないけど、それでもたまにはスポーツニュースをチェックするわにゃよ。'},
            {'role': 'user', 'content': 'どこで試合は行われましたか?'}
        ]
    )
    # return redirect(url_for("index", result=response.choices[0].text))
    return response


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.
Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )


if __name__ == "__main__":
    response = run()
    # print([t for t in response.choices])
    print('best: ', response.choices[0])
    print('best: ', response.choices[0]['message']['content'])
