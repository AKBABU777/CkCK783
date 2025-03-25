# 🤖 Brawl Stars Info Bot 🚀

Welcome to the **Brawl Stars Info Bot**! 🎉 This Telegram bot is your ultimate companion for checking out Brawl Stars player stats and launching fake "attacks" (just for fun, of course)! 👾 Built with Python and a sprinkle of creativity, it’s packed with cool features and a sleek interface. Let’s dive in! 🌟

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

5. **Contact the Owner**  
Click "Owner 👑" to see social links, then "Back 🔙" to return.  

---

## 🛠️ Setup

### Prerequisites
- 🐍 Python 3.7+  
- 📱 Telegram app (to interact with the bot)  
- 🌐 A Brawl Stars API token (already included, but you can get your own [here](https://developer.brawlstars.com))  

### Installation
1. **Clone the Repo**
git clone https://github.com/yourusername/brawl-stars-info-bot.git
cd brawl-stars-info-bot
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
- **API:** Brawl Stars API for player data 📈  
- **Cooldown:** 3-hour limit for attacks (stored in memory via `context.user_data`) ⏰  
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

Happy banning (safely, of course)! 😄  
