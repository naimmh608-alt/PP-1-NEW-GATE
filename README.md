# 🔥 PayPal Charge Telegram Bot

A powerful Telegram bot for testing PayPal payment gateway with credit cards.

**Gateway:** PayPal Commerce (awwatersheds.org)  
**Amount:** $1.00 USD  
**No Captcha Required**

---

## 📋 Features

- ✅ Single card checking
- ✅ Real-time processing
- ✅ Detailed response messages
- ✅ Easy to use Telegram interface
- ✅ Railway.com ready for instant deployment

---

## 🚀 Quick Deploy to Railway.com

### Method 1: One-Click Deploy (Recommended)

1. **Fork this repository** to your GitHub account

2. **Go to [Railway.app](https://railway.app)**

3. Click **"New Project"** → **"Deploy from GitHub repo"**

4. **Select your forked repository**

5. **Add Environment Variables:**
   - Click on your deployment
   - Go to **"Variables"** tab
   - Add: `BOT_TOKEN` = `your_telegram_bot_token`

6. **Deploy!** Railway will automatically:
   - Detect Python project
   - Install dependencies from `requirements.txt`
   - Run the bot using `Procfile`

### Method 2: Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Add environment variables
railway variables set BOT_TOKEN=your_bot_token_here

# Deploy
railway up
```

---

## 🤖 Getting Telegram Bot Token

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Follow the instructions:
   - Choose a name for your bot (e.g., "PayPal Charge Bot")
   - Choose a username (must end with 'bot', e.g., "paypal_charge_bot")
4. **Copy the token** BotFather gives you
5. Use this token in Railway's environment variables

---

## 📦 Files Included

```
├── bot.py              # Main bot file with all logic
├── requirements.txt    # Python dependencies
├── Procfile           # Railway deployment configuration
├── runtime.txt        # Python version specification
├── .env.example       # Environment variables template
└── README.md          # This file
```

---

## 🎯 How to Use the Bot

### Commands

- `/start` - Start the bot and see welcome message
- `/help` - Show help and instructions
- `/chk CC|MM|YY|CVV` - Check a single card

### Card Format

**Format:** `CC|MM|YY|CVV`

**Examples:**
- `4185497154154915|11|33|461`
- `4532015112830366|12|2025|123`

### Quick Check (No Command Needed)

Just send the card directly to the bot:
```
4185497154154915|11|33|461
```

The bot will automatically detect and check it!

---

## 📊 Response Types

| Status | Emoji | Meaning |
|--------|-------|---------|
| **CHARGED** | ✅ | Card successfully charged $1.00 |
| **APPROVED** | ✅ | Payment approved (Insufficient Funds) |
| **LIVE** | 💰 | Card is valid but failed (CVV/Expiry issue) |
| **DECLINED** | ❌ | Card declined by processor |
| **ERROR** | ⚠️ | Technical error occurred |

---

## 🔧 Environment Variables

Create these in Railway.com dashboard:

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | ✅ Yes | Your Telegram bot token from @BotFather |
| `ADMIN_IDS` | ❌ No | Comma-separated admin user IDs (future use) |

---

## 💻 Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd <repo-name>
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set environment variable:**
```bash
# Linux/Mac
export BOT_TOKEN="your_bot_token_here"

# Windows (CMD)
set BOT_TOKEN=your_bot_token_here

# Windows (PowerShell)
$env:BOT_TOKEN="your_bot_token_here"
```

4. **Run the bot:**
```bash
python bot.py
```

---

## ⚙️ Technical Details

### Core Logic (Unchanged from Original)

All PayPal checking logic remains **100% intact**:
- ✅ Token scraping from awwatersheds.org
- ✅ Donation registration
- ✅ PayPal order creation
- ✅ Card charging via GraphQL
- ✅ Response analysis

### What Changed?

**Only the interface changed:**
- ❌ Removed: CLI menu system
- ❌ Removed: File-based mass checking (for now)
- ❌ Removed: Colorama terminal colors
- ✅ Added: Telegram bot integration
- ✅ Added: Async message handling
- ✅ Added: Railway deployment support

---

## 🛡️ Security Notes

- Bot token is stored securely in Railway environment variables
- No sensitive data is logged or stored
- All card checking logic runs in memory only

---

## 📝 To-Do / Future Features

- [ ] Mass checking with file upload
- [ ] Admin-only commands
- [ ] User statistics
- [ ] Proxy support via bot commands
- [ ] Export results to file

---

## 🙏 Credits

**Original Script:** @REALYASHVIRGAMING  
**Telegram Channel:** @THEYASHVIRGAMING  
**Converted for Railway:** Railway.com Compatible Version

---

## 📄 License

This project is for educational purposes only.

---

## ❓ Support

**Issues?** Create an issue on GitHub  
**Questions?** Contact: @REALYASHVIRGAMING  
**Channel:** t.me/THEYASHVIRGAMING

---

**⭐ Star this repo if you found it useful!**
