import requests


def send_telegram_message(
    token,
    chat_id,
    message
):

    url = (
        f"https://api.telegram.org/"
        f"bot{token}/sendMessage"
    )

    data = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.post(
        url,
        data=data
    )

    return response.json()