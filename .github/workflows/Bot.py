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
INITIAL_BRAWL_STARS_API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkxZWZjZjczLWNmMGYtNDc3YS05Zjg3LTQ4ODdmYTFjZWU1NCIsImlhdCI6MTc0Mjg3NzczMiwic3ViIjoiZGV2ZWxvcGVyL2RjYmNlNjM4LTk1MjctODRjMC1iYjc3LTBlM2RkZDM5NzQxZSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTUyLjU4LjQ1Ljc1Il0sInR5cGUiOiJjbGllbnQifV19.ZkEYzBQwfop88EGW8lvo5pvoQqnIzAERX7HeLdwtj98l2zvPW7u19F7a33DHlcyrcfUrsjgjixP7D7dhwOMpcQ'
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

def is_valid_player_tag(player_tag: str) -> bool:
    return re.match(r'^[0289PYLQGRJCUV]+$', player_tag) is not None

async def fetch_player_data(player_tag: str) -> dict:
    if not is_valid_player_tag(player_tag):
        logger.error(f"Invalid player tag format: {player_tag}")
        return None
    
    encoded_tag = f"%23{player_tag}"
    url = f"{BRAWL_STARS_API_URL}{encoded_tag}"
    headers = {
        'Authorization': f'Bearer {BRAWL_STARS_API_TOKEN[0]}',  # Access the mutable token
        'Accept': 'application/json'
    }
    
    try:
        logger.info(f"Fetching data for player tag: {player_tag}, URL: {url}")
        response = requests.get(url, headers=headers)
        logger.info(f"API response status: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"API error: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
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
    if not is_valid_player_tag(player_tag):
        await update.message.reply_text(f'❌ The provided player tag #{player_tag} is invalid.')
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
    if not is_valid_player_tag(player_tag):
        await update.message.reply_text(f'❌ The provided player tag #{player_tag} is invalid.')
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
        # Show current API token
        current_token = BRAWL_STARS_API_TOKEN[0]
        await update.message.reply_text(f"🔑 Current Brawl Stars API Token:\n`{current_token}`\n\nTo update, use: `/api <new_token>`")
    else:
        # Update API token
        new_token = ' '.join(context.args).strip()
        old_token = BRAWL_STARS_API_TOKEN[0]
        BRAWL_STARS_API_TOKEN[0] = new_token
        await update.message.reply_text(f"🔑 API Token Updated!\nOld: `{old_token}`\nNew: `{new_token}`\n\nUse `/info` or `/ban` to test the new token.")

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
    application.add_handler(CommandHandler("api", api))  # New API command handler
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
