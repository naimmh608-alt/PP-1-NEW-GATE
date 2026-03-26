# 🚀 Railway.com Deployment Guide

## Step-by-Step Deployment Instructions

### 📱 Step 1: Create Your Telegram Bot

1. Open **Telegram** app
2. Search for `@BotFather`
3. Send `/newbot`
4. Enter bot name: `PayPal Charge Bot` (or any name you want)
5. Enter username: `your_unique_bot` (must end with 'bot')
6. **SAVE THE TOKEN** - You'll need this! It looks like:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

---

### 🌐 Step 2: Deploy to Railway

#### Option A: GitHub (Recommended)

1. **Create GitHub Account** (if you don't have one)
   - Go to https://github.com
   - Sign up for free

2. **Upload Project Files**
   - Create new repository
   - Upload all these files:
     - `bot.py`
     - `requirements.txt`
     - `Procfile`
     - `runtime.txt`
     - `railway.json`
     - `.gitignore`

3. **Go to Railway.app**
   - Visit https://railway.app
   - Click **"Login with GitHub"**

4. **Create New Project**
   - Click **"New Project"**
   - Select **"Deploy from GitHub repo"**
   - Choose your repository

5. **Add Bot Token**
   - Click on your deployment
   - Go to **"Variables"** tab
   - Click **"New Variable"**
   - Add:
     - Name: `BOT_TOKEN`
     - Value: `paste_your_token_here`

6. **Deploy!**
   - Railway will automatically deploy
   - Wait 2-3 minutes
   - Check logs to confirm bot is running

#### Option B: Direct Upload (No GitHub)

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Navigate to Project Folder**
   ```bash
   cd /path/to/bot/files
   ```

4. **Initialize Railway Project**
   ```bash
   railway init
   ```

5. **Add Environment Variable**
   ```bash
   railway variables set BOT_TOKEN=your_bot_token_here
   ```

6. **Deploy**
   ```bash
   railway up
   ```

---

### ✅ Step 3: Verify Deployment

1. **Check Railway Dashboard**
   - Go to https://railway.app/dashboard
   - Open your project
   - Click on **"Deployments"**
   - Status should be **"Success"** ✅

2. **Check Logs**
   - Click **"View Logs"**
   - You should see:
     ```
     🚀 Starting PayPal Charge Bot...
     📡 Bot Token: 1234567890...
     ✅ Bot is running!
     ```

3. **Test Your Bot**
   - Open Telegram
   - Search for your bot username
   - Send `/start`
   - You should get welcome message!

---

### 🎯 Step 4: Test Card Checking

1. Send a test card to your bot:
   ```
   4185497154154915|11|33|461
   ```

2. Or use command:
   ```
   /chk 4185497154154915|11|33|461
   ```

3. Bot should process and show result! 🎉

---

## 🔧 Troubleshooting

### Bot Not Responding?

**Check 1: Verify Bot Token**
- Go to Railway dashboard
- Check `BOT_TOKEN` variable
- Make sure there are no spaces or extra characters

**Check 2: Check Logs**
- Railway dashboard → Your project → View Logs
- Look for errors

**Check 3: Restart Deployment**
- Railway dashboard → Your project
- Click **"Redeploy"**

### Deployment Failed?

**Common Issues:**

1. **Missing BOT_TOKEN**
   - Solution: Add environment variable in Railway

2. **Wrong Python Version**
   - Solution: Check `runtime.txt` has `python-3.11.0`

3. **Dependencies Error**
   - Solution: Verify `requirements.txt` is correct

4. **Procfile Error**
   - Solution: Make sure `Procfile` has: `worker: python bot.py`

---

## 💡 Pro Tips

### Keep Bot Running 24/7
- Railway free tier gives you 500 hours/month
- That's about 16 hours per day - enough for most use!
- Upgrade to hobby plan ($5/month) for unlimited

### Monitor Your Bot
- Check Railway logs regularly
- Set up notifications in Railway settings

### Update Your Bot
- Make changes to code
- Push to GitHub (if using GitHub method)
- Railway auto-deploys on push!

### Add More Features
- Edit `bot.py`
- Add new commands
- Deploy updates easily

---

## 📊 Expected Railway Costs

| Plan | Cost | Hours/Month | Best For |
|------|------|-------------|----------|
| **Free Trial** | $0 | 500 hours | Testing |
| **Hobby** | $5/month | Unlimited | Personal Use |
| **Pro** | $20/month | Unlimited + Priority | Heavy Use |

**Recommendation:** Start with free trial, upgrade if needed!

---

## 🎓 What You've Deployed

✅ **Telegram Bot** - Running 24/7 on Railway  
✅ **PayPal Checker** - Full functionality intact  
✅ **Auto-Scaling** - Handles multiple users  
✅ **Secure** - Bot token stored safely  
✅ **Easy Updates** - Just push to GitHub  

---

## 🆘 Need Help?

**Railway Issues:**
- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

**Bot Issues:**
- Check README.md
- Contact: @REALYASHVIRGAMING
- Channel: t.me/THEYASHVIRGAMING

---

## 🎉 Congratulations!

Your PayPal Charge Bot is now **LIVE** on Railway! 🚀

**Next Steps:**
1. Share bot with friends
2. Test different cards
3. Monitor usage in Railway dashboard
4. Enjoy! 🔥

---

**Made with ❤️ by @REALYASHVIRGAMING**
