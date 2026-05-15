from telethon import TelegramClient, events

api_id = 38395000
api_hash = '0d557f4d8c8887938851f1eb850b98a8'

KEYWORDS = ['прайс', 'расчет', 'фулик', 'фулфилмент', 'фф', 'стоимость', 
'рассчет']
TARGET_CHANNEL = 'zaifki1'

client = TelegramClient('session', api_id, api_hash)


@client.on(events.NewMessage)
async def handler(event):
    try:
        text = event.raw_text.lower()

        # 🔎 фильтр по ключевым словам
        if not any(word in text for word in KEYWORDS):
            return

        chat = await event.get_chat()
        sender = await event.get_sender()

        # ❌ исключаем ЛС (личные сообщения)
        if event.is_private:
            return

        # ✅ только группы и каналы
        if not (event.is_group or event.is_channel):
            return

        # username отправителя
        username = sender.username if sender and sender.username else "нет"

        # название чата
        chat_title = chat.title if hasattr(chat, 'title') else "ЛС"

        # ссылка на сообщение
        if hasattr(chat, 'username') and chat.username:
            link = f"https://t.me/{chat.username}/{event.id}"
        else:
            link = f"https://t.me/c/{str(event.chat_id)[4:]}/{event.id}"

        # сообщение
        message = f"""
🔥 Новая заявка

{text}

👤 @{username}
📍 Чат: {chat_title}

🔗 {link}
"""

        await client.send_message(TARGET_CHANNEL, message)

    except Exception as e:
        print("Ошибка:", e)


client.start()
print("Бот запущен 🚀")
client.run_until_disconnected()
