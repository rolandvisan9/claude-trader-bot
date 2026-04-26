import os
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    response = requests.post(url, json=payload, timeout=20)
    response.raise_for_status()
    return response.json()


def send_file_summary(filepath, header):
    path = PROJECT_ROOT / filepath
    if not path.exists():
        send_message(f"{header}\n\nArchivo no encontrado: {filepath}")
        return
    content = path.read_text(encoding="utf-8")
    # Telegram tiene límite de 4096 caracteres por mensaje
    message = f"{header}\n\n{content[:3800]}"
    send_message(message)


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "brief"
    if mode == "premarket":
        send_file_summary("memory/premarket_summary.md", "🤖 ClaudeTrader - Pre-Market")
    elif mode == "eod":
        send_file_summary("memory/eod_summary.md", "🤖 ClaudeTrader - End of Day")
    else:
        send_file_summary("memory/daily_brief.md", "🤖 ClaudeTrader - Daily Brief")
    print("Mensaje enviado a Telegram.")
