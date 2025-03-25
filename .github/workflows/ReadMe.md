# 🤖 Brawl Stars Info Bot 🚀

Welcome to the **Brawl Stars Info Bot**! 🎉 This Telegram bot is your ultimate companion for checking out Brawl Stars player stats, launching fake "attacks" (just for fun, of course), and even creating custom players! 👾 Built with Python and a dash of creativity, it’s loaded with awesome features and a slick interface. Let’s dive in! 🌟

---

## ✨ Features

- **Player Info Lookup** ℹ️  
  Use `/info <player_tag>` to get detailed stats about any Brawl Stars player:  
  - 👤 Name  
  - 🏆 Trophies  
  - 🥇 Highest Trophies  
  - 🎓 Experience Level  
  - 🔓 Brawlers Unlocked  

- **Attack Mode** ⚔️  
  Launch a mock attack with `/ban <player_tag>`! Watch the progress bar fill up with epic messages like "⚡ Overloading servers..." or "✅ Servers Successfully Freezed!"  
  - ⏳ **Cooldown:** Normal users can attack once every 3 hours (bot’s not *that* strong yet!). Admin bypasses this!  

- **Server Status** 📡  
  Check the bot’s "server status" with `/ping` and see a live-updating progress bar with random pings (20-150ms). Pure sci-fi vibes! 🌐  

- **Broadcast Power** 📢  
  Admin (chat ID: `7138310520`) can send messages to all users with `/broadcast <message> [btn name:link]`. Spread the word like a boss!  

- **API Management** 🔑  
  - `/api`: View or update the Brawl Stars API token (admin only).  
  - `/chkapi`: Check the last API response or error (e.g., IP issues) to troubleshoot like a pro! 🛠️  

- **Custom Players** 🎨  
  Create fake players with `/addplayer <tag> <name> <trophies> <highestTrophies> <expLevel> <brawlers>` (admin only). Use any uppercase letters and numbers for tags (e.g., `JBEIOEOS1` or `FAKEPLAYER`)!  
  - Displays as "(Custom Player)" in `/info` and `/ban`.  
  - No API conflicts—purely in-bot fun!  

- **Social Connections** 📞  
  Click the "Owner 👑" button to reveal:  
  - 📱 WhatsApp  
  - 📸 Instagram  
  - 📢 Telegram Channel  
  - 🔙 Back to welcome screen  

- **Stats at a Glance** 📊  
  See live-updated "Users Using 👥" and "Accounts Banned ⛔" stats right in the welcome message!  

---

## 🎮 How to Use

1. **Start the Bot**  
   Type `/start` to get this epic welcome message:
   🤖 Welcome to the Brawl Stars Info Bot! 🎉
🌟 This bot provides info about Brawl Stars players! 🚀
👾 Use /ban <player_tag> to attack a player (3-hour cooldown).
ℹ️ Use /info <player_tag> for info without attacking.
✨ Example: /ban VLQPVPY or /info VLQPVPY
📲 Click below to contact the owner! 👇

2. **Check Player Info**  
Example: `/info VLQPVPY`  

3. **Launch an Attack**  
Example: `/ban VLQPVPY` → Click "Start Attack 🚀" → Watch the magic!  

4. **Ping the Server**  
Type `/ping` for a cool status update!  

5. **Manage the API**  
- Check token: `/api`  
- Check last API response: `/chkapi` (e.g., fix "accessDenied.invalidIp" errors)  

6. **Add a Custom Player**  
Example: `/addplayer JBEIOEOS1 FakePlayer 1000 1500 50 20`  
Then try `/info JBEIOEOS1` or `/ban JBEIOEOS1`!  

7. **Contact the Owner**  
Click "Owner 👑" to see social links, then "Back 🔙" to return.  

---

## 🛠️ Setup

### Prerequisites
- 🐍 Python 3.7+  
- 📱 Telegram app (to interact with the bot)  
- 🌐 A Brawl Stars API token (included, but grab your own [here](https://developer.brawlstars.com) if needed)  

### Installation
1. **Clone the Repo**
git clone https://github.com/AKBABU777/bot.git
cd bot
2. **Install Dependencies**
pip install -r requirements.txt
3. **Update Config**  
- Replace `GLOBAL_CHAT_ID_ENDPOINT` with your server URL (e.g., `https://yourusername.pythonanywhere.com/chat_ids`).  
- Update social links in the code:  
  - `WHATSAPP_LINK`  
  - `INSTAGRAM_LINK`  
  - `TELEGRAM_CHANNEL_LINK`  

4. **Run the Bot**
python bot.py

5. **Deploy (Optional)**  
Host on [PythonAnywhere](https://www.pythonanywhere.com) or [Replit](https://replit.com) for 24/7 uptime! 🌍  

---

## ⚙️ Technical Details

- **Language:** Python 🐍  
- **Framework:** `python-telegram-bot` for Telegram magic!  
- **API:** Brawl Stars API for real player data 📈  
- **Custom Players:** Stored in-memory via `custom_players` dictionary—no API calls needed! 🎨  
- **Cooldown:** 3-hour limit for attacks (stored in `context.user_data`) ⏰  
- **Admin:** Chat ID `7138310520` gets unlimited power! 👑  

---

## 🌟 Contributing

Got ideas? Found a bug? Feel free to:  
- 📩 Open an issue  
- 🛠️ Submit a pull request  
Let’s make this bot even cooler together! 🚀  

---

## 📜 License

This project is open-source under the [MIT License](LICENSE). Feel free to fork and tweak it! 🎉  

---

## 👋 Say Hi!

Follow me on:  
- 📱 [WhatsApp](https://wa.me/your-number)  
- 📸 [Instagram](https://instagram.com/your-profile)  
- 📢 [Telegram Channel](https://t.me/ytgaming_on)  

Happy banning (safely, of course) and enjoy creating your own players! 😄  
