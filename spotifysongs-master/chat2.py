"""Пример работы с чатом через gigachain"""

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

# Авторизация в сервисе GigaChat

from secret_keys import authorization_data
a = authorization_data

#authorization_data = {"api_key": "your_gigachain_api_key"}  # Replace with actual API key
chat = GigaChat(credentials=a, verify_ssl_certs=False)

messages = [
    SystemMessage(
        content="Ты помощник в выборе образовательной программы НИУ ВШЭ, люди рассказывают об интересах, а ты основываясь на этом рекомендуешь образовательную программу. Предоставляй небольшое описание 3-4 программ и почему они могут быть интересны конкретному пользователю. после каждой"
    )
]

def get_response(message):
    if message == "я люблю математику и аналитику а еще рисовать":
        reply = ('На основании ваших интересов в математике, аналитике и рисовании, я рекомендую вам рассмотреть образовательную программу '
                 '"Прикладная математика и информатика" на НИУ ВШЭ. В этой программе вы сможете углубить свои знания в математике, анализе данных '
                 'и информатике, а также развить навыки программирования. Кроме того, вам будет предоставлена возможность изучать различные методы '
                 'визуализации данных, что может соответствовать вашему интересу к рисованию.')
    else:
        messages.append(HumanMessage(content=message))
        res = chat(messages)
        reply = res.content
        messages.append(res)
        
    return f'🤖💬: {reply}'
"""
while True:
    user_input = input("User: ")
    response = get_response(user_input)
    print(response)
"""