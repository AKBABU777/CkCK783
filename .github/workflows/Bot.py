import logging
import asyncio
import re
import requests
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import BadRequest
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
TELEGRAM_BOT_TOKEN = '8139449951:AAHYdQskTW3EAXmbhcY-UQR5IvIydaR_7Gg'
INITIAL_BRAWL_STARS_API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjI4MDFjZjRlLTFhMDctNDI4MS04N2YwLTBjYzE1MzEwZmM0YSIsImlhdCI6MTc0Mjg5NzczMCwic3ViIjoiZGV2ZWxvcGVyL2RjYmNlNjM4LTk1MjctODRjMC1iYjc3LTBlM2RkZDM5NzQxZSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTUyLjU4LjQ1LjE4NiJdLCJ0eXBlIjoiY2xpZW50In1dfQ.rvPPSX9xc4OSe71Uz8tsDP-UK2JcsYCjPR0FuUnw8l5L9891Q16AOvXrix6l8QU8d78-m8ChwjxWKwpG5SKKtA'
BRAWL_STARS_API_URL = 'https://api.brawlstars.com/v1/players/'
OWNER_LINK = 'https://t.me/ytgaming_on'
GLOBAL_CHAT_ID_ENDPOINT = 'https://yourusername.pythonanywhere.com/chat_ids'  # Replace with your server URL
ADMIN_CHAT_ID = 7138310520  # Admin chat ID

# Use a list to make the API token mutable
BRAWL_STARS_API_TOKEN = [INITIAL_BRAWL_STARS_API_TOKEN]

# Global counters and storage
user_count = random.randint(50, 100)
banned_count = random.randint(20, 50)
local_chat_ids = set()
last_api_response = None  # To store the last API response or error
custom_players = {}  # Dictionary to store custom player data

# Fake server messages
SERVER_MESSAGES = [
    "🌐 Server 1: Online | Load: 87%",
    "⚡ Server 2: Boosting attack speed...",
    "🔒 Server 3: Encrypting data...",
    "🛠️ Server 4: Maintenance in progress",
    "📡 Server 5: Scanning for targets..."
]

# Social media links
WHATSAPP_LINK = 'https://api.whatsapp.com/send/?phone=994402638009'
INSTAGRAM_LINK = 'https://www.instagram.com/ytgaming_on?igsh=MTdzbmlrMGszbWI5dw=='
TELEGRAM_CHANNEL_LINK = 'https://t.me/ytgaming_on'

def is_valid_api_player_tag(player_tag: str) -> bool:
    # Strict validation for real Brawl Stars API tags
    return re.match(r'^[0289PYLQGRJCUV]+$', player_tag) is not None

def is_valid_custom_player_tag(player_tag: str) -> bool:
    # Relaxed validation for custom tags: any uppercase letters and numbers
    return re.match(r'^[A-Z0-9]+$', player_tag) is not None

async def fetch_player_data(player_tag: str) -> dict:
    global last_api_response
    
    if not is_valid_api_player_tag(player_tag):
        logger.error(f"Invalid player tag format for API: {player_tag}")
        return None
    
    encoded_tag = f"%23{player_tag}"
    url = f"{BRAWL_STARS_API_URL}{encoded_tag}"
    headers = {
        'Authorization': f'Bearer {BRAWL_STARS_API_TOKEN[0]}',
        'Accept': 'application/json'
    }
    
    try:
        logger.info(f"Fetching data for player tag: {player_tag}, URL: {url}")
        response = requests.get(url, headers=headers)
        logger.info(f"API response status: {response.status_code}")
        
        if response.status_code == 200:
            last_api_response = {
                "status": response.status_code,
                "data": response.json()
            }
            return response.json()
        else:
            error_details = {
                "status": response.status_code,
                "reason": response.json().get("reason", "Unknown"),
                "message": response.json().get("message", "No message provided")
            }
            last_api_response = error_details
            logger.error(f"API error: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        last_api_response = {
            "status": "network_error",
            "message": str(e)
        }
        logger.error(f"Network error fetching player data: {e}")
        return None

async def sync_chat_ids(chat_id):
    try:
        requests.post(GLOBAL_CHAT_ID_ENDPOINT, json={'chat_id': chat_id})
    except Exception as e:
        logging.error(f"Failed to sync chat ID {chat_id}: {e}")

async def update_counters():
    global user_count, banned_count
    while True:
        await asyncio.sleep(random.uniform(5, 30))
        if random.random() < 0.7:
            user_increment = random.randint(0, 3)
            user_count += user_increment
            if user_increment > 0 and random.random() < 0.4:
                banned_count += random.randint(0, 2)
        if random.random() < 0.1:
            await asyncio.sleep(random.uniform(30, 60))

async def server_status_updates(application, message_id, chat_id):
    while True:
        ping = random.randint(20, 150)
        status = random.choice(SERVER_MESSAGES)
        progress_bar = '┃ [' + '■' * random.randint(3, 10) + '▯' * (10 - random.randint(3, 10)) + f'] Ping: {ping}ms'
        full_message = f"🌐 Network Status: {status}\n{progress_bar}"
        try:
            await application.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=full_message)
        except Exception as e:
            logger.error(f"Failed to update server status: {e}")
        await asyncio.sleep(random.uniform(5, 15))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global user_count
    user_count += 1
    chat_id = update.effective_chat.id
    local_chat_ids.add(chat_id)
    asyncio.create_task(sync_chat_ids(chat_id))
    message = (
        "🤖 Welcome to the Brawl Stars Info Bot! 🎉\n\n"
        "🌟 This bot provides info about Brawl Stars players! 🚀\n"
        "👾 Use `/ban <player_tag>` to attack a player (3-hour cooldown).\n"
        "ℹ️ Use `/info <player_tag>` for info without attacking.\n\n"
        "✨ Example: `/ban VLQPVPY` or `/info VLQPVPY`\n"
        "⛔ Don't Try To Ban Accounts Whch Has Trophies Above 60-80k 🚫"
    )
    keyboard = [
        [InlineKeyboardButton("Owner 👑", callback_data='show_owner_contacts')],
        [InlineKeyboardButton(f"Users Using: {user_count} 👥", callback_data='user_count'),
         InlineKeyboardButton(f"Accounts Banned: {banned_count} ⛔", callback_data='banned_count')]
    ]
    await update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    local_chat_ids.add(chat_id)
    asyncio.create_task(sync_chat_ids(chat_id))
    ping = random.randint(20, 150)
    status = random.choice(SERVER_MESSAGES)
    progress_bar = '┃ [' + '■' * random.randint(3, 10) + '▯' * (10 - random.randint(3, 10)) + f'] Ping: {ping}ms'
    full_message = f"🌐 Network Status: {status}\n{progress_bar}"
    sent_message = await update.message.reply_text(full_message)
    asyncio.create_task(server_status_updates(application=context.application, chat_id=sent_message.chat_id, message_id=sent_message.message_id))

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    local_chat_ids.add(chat_id)
    asyncio.create_task(sync_chat_ids(chat_id))
    if not context.args:
        await update.message.reply_text('❌ Please provide a player tag. Usage: /info <player_tag>')
        return
    player_tag = context.args[0].strip('#').upper()
    
    # Check if it's a custom player first
    if player_tag in custom_players:
        player_data = custom_players[player_tag]
        message = (
            f'🔍 Player Info for #{player_tag} (Custom Player):\n'
            f'👤 Name: {player_data.get("name", "Unknown")}\n'
            f'🏆 Trophies: {player_data.get("trophies", 0)}\n'
            f'🥇 Highest Trophies: {player_data.get("highestTrophies", 0)}\n'
            f'🎓 Experience Level: {player_data.get("expLevel", 0)}\n'
            f'🔓 Brawlers Unlocked: {player_data.get("brawlers", 0)}'
        )
        await update.message.reply_text(message)
        return
    
    # If not custom, validate for API and fetch
    if not is_valid_api_player_tag(player_tag):
        await update.message.reply_text(f'❌ The provided player tag #{player_tag} is invalid for real players.')
        return
    
    player_data = await fetch_player_data(player_tag)
    if player_data:
        message = (
            f'🔍 Player Info for #{player_tag}:\n'
            f'👤 Name: {player_data.get("name", "Unknown")}\n'
            f'🏆 Trophies: {player_data.get("trophies", 0)}\n'
            f'🥇 Highest Trophies: {player_data.get("highestTrophies", 0)}\n'
            f'🎓 Experience Level: {player_data.get("expLevel", 0)}\n'
            f'🔓 Brawlers Unlocked: {len(player_data.get("brawlers", []))}'
        )
        await update.message.reply_text(message)
    else:
        await update.message.reply_text(f'❌ Could not retrieve data for player #{player_tag}.')

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    local_chat_ids.add(chat_id)
    asyncio.create_task(sync_chat_ids(chat_id))
    
    if not context.args:
        await update.message.reply_text('❌ Please provide a player tag. Usage: /ban <player_tag>')
        return
    
    player_tag = context.args[0].strip('#').upper()
    
    # Check if it's a custom player first
    if player_tag in custom_players:
        player_data = custom_players[player_tag]
        message = (
            f'🔍 Player Info for #{player_tag} (Custom Player):\n'
            f'👤 Name: {player_data.get("name", "Unknown")}\n'
            f'🏆 Trophies: {player_data.get("trophies", 0)}\n'
            f'🥇 Highest Trophies: {player_data.get("highestTrophies", 0)}\n'
            f'🎓 Experience Level: {player_data.get("expLevel", 0)}\n'
            f'🔓 Brawlers Unlocked: {player_data.get("brawlers", 0)}\n\n'
            '⚠️ Ready to initiate attack?'
        )
        keyboard = [
            [InlineKeyboardButton("Start Attack 🚀", callback_data=f'start_attack_{player_tag}')],
            [InlineKeyboardButton("Terminate ❌", callback_data=f'terminate_{player_tag}')]
        ]
        await update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    # If not custom, validate for API and fetch
    if not is_valid_api_player_tag(player_tag):
        await update.message.reply_text(f'❌ The provided player tag #{player_tag} is invalid for real players.')
        return
    
    if chat_id != ADMIN_CHAT_ID:
        last_attack_time = context.user_data.get('last_attack_time')
        if last_attack_time:
            time_since_last_attack = datetime.now() - last_attack_time
            if time_since_last_attack < timedelta(hours=3):
                remaining_time = timedelta(hours=3) - time_since_last_attack
                hours, remainder = divmod(remaining_time.seconds, 3600)
                minutes = remainder // 60
                await update.message.reply_text(
                    f"⏳ Bot is not that strong yet! You can only attack once every 3 hours.\n"
                    f"Please wait {hours}h {minutes}m before your next attack.\n"
                    f"ℹ️ Use `/info {player_tag}` to get player info without attacking."
                )
                return
    
    player_data = await fetch_player_data(player_tag)
    if player_data:
        message = (
            f'🔍 Player Info for #{player_tag}:\n'
            f'👤 Name: {player_data.get("name", "Unknown")}\n'
            f'🏆 Trophies: {player_data.get("trophies", 0)}\n'
            f'🥇 Highest Trophies: {player_data.get("highestTrophies", 0)}\n'
            f'🎓 Experience Level: {player_data.get("expLevel", 0)}\n'
            f'🔓 Brawlers Unlocked: {len(player_data.get("brawlers", []))}\n\n'
            '⚠️ Ready to initiate attack?'
        )
        keyboard = [
            [InlineKeyboardButton("Start Attack 🚀", callback_data=f'start_attack_{player_tag}')],
            [InlineKeyboardButton("Terminate ❌", callback_data=f'terminate_{player_tag}')]
        ]
        await update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(f'❌ Could not retrieve data for player #{player_tag}.')

async def addplayer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id != ADMIN_CHAT_ID:
        await update.message.reply_text('❌ Only the bot owner can use this command.')
        return
    
    if len(context.args) < 5:
        await update.message.reply_text(
            '❌ Usage: /addplayer <player_tag> <name> <trophies> <highestTrophies> <expLevel> <brawlers>\n'
            'Example: /addplayer JBEIOEOS1 FakePlayer 1000 1500 50 20'
        )
        return
    
    player_tag = context.args[0].strip('#').upper()
    if not is_valid_custom_player_tag(player_tag):
        await update.message.reply_text(f'❌ The provided player tag #{player_tag} is invalid. Use only uppercase letters and numbers.')
        return
    
    # Check if the tag already exists as a custom player
    if player_tag in custom_players:
        await update.message.reply_text(f'❌ Custom player with tag #{player_tag} already exists.')
        return
    
    # Check if the tag exists in the real API (only if it matches API format)
    if is_valid_api_player_tag(player_tag):
        real_player_data = await fetch_player_data(player_tag)
        if real_player_data:
            await update.message.reply_text(f'❌ Player tag #{player_tag} already exists in the real Brawl Stars API. Choose a different tag.')
            return
    
    try:
        name = context.args[1]
        trophies = int(context.args[2])
        highest_trophies = int(context.args[3])
        exp_level = int(context.args[4])
        brawlers = int(context.args[5])
        
        custom_players[player_tag] = {
            "name": name,
            "trophies": trophies,
            "highestTrophies": highest_trophies,
            "expLevel": exp_level,
            "brawlers": brawlers
        }
        
        await update.message.reply_text(
            f'✅ Custom player #{player_tag} added successfully!\n'
            f'👤 Name: {name}\n'
            f'🏆 Trophies: {trophies}\n'
            f'🥇 Highest Trophies: {highest_trophies}\n'
            f'🎓 Experience Level: {exp_level}\n'
            f'🔓 Brawlers Unlocked: {brawlers}'
        )
    except ValueError:
        await update.message.reply_text('❌ Invalid numeric values provided. Trophies, highestTrophies, expLevel, and brawlers must be integers.')

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    owner_id = ADMIN_CHAT_ID
    if update.effective_chat.id != owner_id:
        await update.message.reply_text('❌ Only the bot owner can use this command.')
        return
    if not context.args:
        await update.message.reply_text('❌ Usage: /broadcast <message> [btn name:link]')
        return
    args = ' '.join(context.args)
    button = None
    if ':' in args.split()[-1]:
        button_part = args.split()[-1]
        btn_name, btn_link = button_part.split(':', 1)
        message = ' '.join(args.split()[:-1])
        button = InlineKeyboardButton(btn_name, url=btn_link)
    else:
        message = args
    reply_markup = InlineKeyboardMarkup([[button]]) if button else None
    successful, failed = 0, 0
    for chat_id in local_chat_ids:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)
            successful += 1
            await asyncio.sleep(0.05)
        except Exception as e:
            logger.error(f"Failed to send broadcast to {chat_id}: {e}")
            failed += 1
    await update.message.reply_text(f'📤 Broadcast completed!\n✅ Sent to {successful} users\n❌ Failed for {failed} users')

async def api(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id != ADMIN_CHAT_ID:
        await update.message.reply_text('❌ Only the bot owner can use this command.')
        return
    
    if not context.args:
        current_token = BRAWL_STARS_API_TOKEN[0]
        await update.message.reply_text(f"🔑 Current Brawl Stars API Token:\n`{current_token}`\n\nTo update, use: `/api <new_token>`")
    else:
        new_token = ' '.join(context.args).strip()
        old_token = BRAWL_STARS_API_TOKEN[0]
        BRAWL_STARS_API_TOKEN[0] = new_token
        await update.message.reply_text(f"🔑 API Token Updated!\nOld: `{old_token}`\nNew: `{new_token}`\n\nUse `/info` or `/ban` to test the new token.")

async def chkapi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id != ADMIN_CHAT_ID:
        await update.message.reply_text('❌ Only the bot owner can use this command.')
        return
    
    if last_api_response is None:
        await update.message.reply_text("ℹ️ No API requests have been made yet.")
        return
    
    if last_api_response.get("status") == 200:
        message = (
            "✅ Last API Request Successful\n"
            f"Status: {last_api_response['status']}\n"
            "Response: Player data retrieved successfully"
        )
    elif last_api_response.get("status") == "network_error":
        message = (
            "❌ Last API Request Failed (Network Error)\n"
            f"Error: {last_api_response['message']}"
        )
    else:
        message = (
            "❌ Last API Request Failed\n"
            f"Status: {last_api_response['status']}\n"
            f"Reason: {last_api_response['reason']}\n"
            f"Message: {last_api_response['message']}\n\n"
            "🔧 Use this info to generate a new API key at https://developer.brawlstars.com\n"
            "Then update with: `/api <new_token>`"
        )
    
    await update.message.reply_text(message)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global banned_count
    query = update.callback_query
    data = query.data
    
    if data.startswith('start_attack_'):
        player_tag = data.split('_')[2]
        attack_messages = ["🔍 Scanning Bots...", "💾 Starting Mass Report...", "⚡ Overloading servers...", "⛔ Mass Traffic Generating...", "Servers Successfully Freezed✅!"]
        await query.edit_message_text(f'🚀⚠️ Launching attack on player #{player_tag}...\n\n┃ [▯▯▯▯▯▯▯▯▯▯] 0%\nInitializing...')
        await asyncio.sleep(1)
        for i in range(1, 11):
            progress_bar = '┃ [' + '■' * i + '▯' * (10 - i) + f'] {i * 10}%'
            message = random.choice(attack_messages) if i % 2 == 0 else ""
            await query.edit_message_text(f'⚠️ Launching attack on player #{player_tag}...\n\n{progress_bar}\n{message}')
            await asyncio.sleep(random.uniform(0.3, 0.7))
        banned_count += 1
        ban_time = random.randint(10, 30)
        await query.edit_message_text(f'🛡️ Attack on player #{player_tag} completed successfully!\n✅ Target neutralized.\n⏳ Expected time to ban this account: {ban_time} days')
        
        if update.effective_chat.id != ADMIN_CHAT_ID:
            context.user_data['last_attack_time'] = datetime.now()
    
    elif data.startswith('terminate_'):
        player_tag = data.split('_')[1]
        await query.edit_message_text(f'❌ Attack on player #{player_tag} has been terminated.')
    
    elif data == 'show_owner_contacts':
        message = "📞 Contact the Owner \n\nIf Bot Gets High Traffic It Automaticaly Starts Queue System! 📑\n\nDon't Forget Give Feedback On My Insta Page Videos If It Worked For U !"
        keyboard = [
            [InlineKeyboardButton("WhatsApp 📱", url=WHATSAPP_LINK),
             InlineKeyboardButton("Instagram 📸", url=INSTAGRAM_LINK)],
            [InlineKeyboardButton("Telegram Channel 📢", url=TELEGRAM_CHANNEL_LINK),
             InlineKeyboardButton("Back 🔙", callback_data='back_to_welcome')]
        ]
        await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data == 'back_to_welcome':
        message = (
            "🤖 Welcome to the Brawl Stars Info Bot! 🎉\n\n"
            "🌟 This bot provides info about Brawl Stars players! 🚀\n"
            "👾 Use `/ban <player_tag>` to attack a player (3-hour cooldown).\n"
            "ℹ️ Use `/info <player_tag>` for info without attacking.\n\n"
            "✨ Example: `/ban VLQPVPY` or `/info VLQPVPY`\n"
            "👇Click below to contact the owner! "
        )
        keyboard = [
            [InlineKeyboardButton("Owner 👑", callback_data='show_owner_contacts')],
            [InlineKeyboardButton(f"Users Using: {user_count} 👥", callback_data='user_count'),
             InlineKeyboardButton(f"Accounts Banned: {banned_count} ⛔", callback_data='banned_count')]
        ]
        await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data in ['user_count', 'banned_count']:
        keyboard = [
            [InlineKeyboardButton("Owner 👑", callback_data='show_owner_contacts')],
            [InlineKeyboardButton(f"Users Using: {user_count} 👥", callback_data='user_count'),
             InlineKeyboardButton(f"Accounts Banned: {banned_count} ⛔", callback_data='banned_count')]
        ]
        new_markup = InlineKeyboardMarkup(keyboard)
        try:
            current_text = query.message.text
            current_markup = query.message.reply_markup
            if current_text == query.message.text and current_markup == new_markup:
                await query.answer()
            else:
                await query.edit_message_text(query.message.text, reply_markup=new_markup)
        except BadRequest as e:
            if "Message is not modified" in str(e):
                await query.answer()
            else:
                logger.error(f"Error editing message: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in button handler: {e}")

def main():
    loop = asyncio.get_event_loop()
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ban", ban))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("api", api))
    application.add_handler(CommandHandler("chkapi", chkapi))
    application.add_handler(CommandHandler("addplayer", addplayer))
    application.add_handler(CallbackQueryHandler(button))
    
    loop.create_task(update_counters())
    
    try:
        loop.run_until_complete(application.run_polling())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        loop.run_until_complete(application.shutdown())

if __name__ == '__main__':
    main()
