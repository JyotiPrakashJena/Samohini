import requests


# Telegram Chatbot Info.
chat_id = -1001974682838
bot_token = "6482240864:AAHRPAfzw8JNgNMLSSKUh_TBQQJnhrY1psg"


def broadcast_msg(message: str):
    """Helper Function to Send message to Telegram."""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        params = {"chat_id": chat_id, "text": message}
        requests.post(url, json=params)
    except Exception as exp:
        print("Exception: ", exp)
