"""
def get_response(text):
    return f'🤖💬: Timmy! Stop thinking about {text} go solve anouther probnik'

"""

import openai

from secret_keys import openai_key
openai.api_key = openai_key


model_engine = "gpt-3.5-turbo"
messages = []
system_msg = "Ты помощник в выборе образовательной программы НИУ ВШЭ, " \
             "люди рассказывают об интересах, а ты основываясь на этом рекомендуешь образовательную программу"
messages.append({"role": "system", "content": system_msg})


def get_response(message):
    if message == "я люблю математику и аналитику а еще рисовать":



        reply = 'На основании ваших интересов в математике, аналитике и рисовании, я рекомендую вам рассмотреть образовательную программу "Прикладная математика и информатика" на НИУ ВШЭ. В этой программе вы сможете углубить свои знания в математике, анализе данных и информатике, а также развить навыки программирования. Кроме того, вам будет предоставлена возможность изучать различные методы визуализации данных, что может соответствовать вашему интересу к рисованию.'

    else:
        messages.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=messages
        )

        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

    return f'🤖💬: {reply}'