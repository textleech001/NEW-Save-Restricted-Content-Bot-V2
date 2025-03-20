# ---------------------------------------------------
# File Name: start.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

from pyrogram import filters
from devgagan import app
from config import OWNER_ID
from devgagan.core.func import subscribe
import asyncio
from devgagan.core.func import *
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.raw.functions.bots import SetBotInfo
from pyrogram.raw.types import InputUserSelf

from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
 
@app.on_message(filters.command("set"))
async def set(_, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply("Owner ko karne do Bhai💀")
        return
     
    await app.set_bot_commands([
        BotCommand("start", "🚀 Start the bot"),
        BotCommand("batch", "🫠 Extract in bulk"),
        BotCommand("login", "🔑 Get into the bot"),
        BotCommand("logout", "🚪 Get out of the bot"),
        BotCommand("token", "🚨🏴‍☠️ Get 3 hours PREMIUM👑 FREE"),
        BotCommand("adl", "👻 Download audio from 30+ sites"),
        BotCommand("dl", "💀 Download videos from 30+ sites"),
        BotCommand("freez", "🧊 Remove all expired user (Owners Only😭)"),
        BotCommand("pay", "₹ Pay now to get subscription"),
        BotCommand("status", "⟳ Refresh Payment status"),
        BotCommand("transfer", "💘 Gift premium to your GirlFriend😉"),
        BotCommand("myplan", "⌛ Get your plan details"),
        BotCommand("add", "➕ Add user to premium(Ownres Only😭)"),
        BotCommand("rem", "➖ Remove from premium(Ownres Only😭)"),
        BotCommand("session", "🧵 Generate Pyrogramv2 session"),
        BotCommand("settings", "⚙️ Personalize things"),
        BotCommand("stats", "📊 Get stats of the bot(Ownres Only😭)"),
        BotCommand("plan", "🗓️ Check our premium plans"),
        BotCommand("terms", "📜 Terms and conditions"),
        BotCommand("speedtest", "🚅 Speed of server"),
        BotCommand("get", "🗄️ Get all user IDs(Ownres Only😭)"),
        BotCommand("lock", "🔒 Protect channel from extraction(Ownres Only😭)"),
        BotCommand("gcast", "⚡ Broadcast message to bot users(Ownres Only😭)"),
        BotCommand("help", "❓ If you're a noob, still!"),
        BotCommand("cancel", "🚫 Cancel batch process")
    ])
 
    await message.reply("✅ Commands configured successfully!")
 
 
 
 
help_pages = [
    (
        "✨➰**Bot Commands Overview (1/2)**:\n\n"
        "1. **/add userID**\n"
        "> Add user to Premium✔ (Owner only😭)\n\n"
        "2. **/rem userID**\n"
        "> Remove user from Premium❗ (Owner only😭)\n\n"
        "3. **/transfer userID**\n"
        "> Transfer premium to your GirlFriend 😉 (Premium members only👑)\n\n"
        "4. **/get**\n"
        "> Get all user IDs🎗 (Owner only😭)\n\n"
        "5. **/lock**\n"
        "> Lock channel from extraction🔏 (Owner only😭)\n\n"
        "6. **/dl link**\n"
        "> Download videos🎥 (💀use YT video link or any Download Link🤞)\n\n"
        "7. **/adl link**\n"
        "> Download audio🔊 (👻use YT Song link or any Download Link🤞)\n\n"
        "8. **/login**\n"
        "> Log in📎 for private channel🔏 access\n\n"
        "9. **/batch**\n"
        "> for Download Multi Post at once📜 (After login🔗)\n\n"
    ),
    (
        "✨➰ **Bot Commands Overview (2/2)**:\n\n"
        "10. **/logout**\n"
        "> Logout from the bot⛓⚔\n\n"
        "11. **/stats**\n"
        "> Get bot stats🃏\n\n"
        "12. **/plan**\n"
        "> Check premium plans👑\n\n"
        "13. **/speedtest**\n"
        "> Test the server speed🚀 \n\n"
        "14. **/terms**\n"
        "> Terms and conditions📜\n\n"
        "15. **/cancel**\n"
        "> Cancel ongoing batch process🚫❌\n\n"
        "16. **/myplan**\n"
        "> Get details about your plans📧\n\n"
        "17. **/session**\n"
        "> Generate Pyrogram V2 session🧵\n\n"
        "18. **/settings ⚙**\n"
        "> 1. SETCHATID : 🎗To directly upload in channel or group or user's dm use it with -100[chatID]🎗\n"
        "> 2. SETRENAME : 🔺To add custom Rename tag or username of your Channels🔻\n"
        "> 3. CAPTION : ➰To add custom caption➰\n"
        "> 4. REPLACEWORDS : 〽Can be used for words in deleted set via REMOVE WORDS〽\n"
        "> 5. RESET : ☣To Reset Settings⚙ Default☣\n\n"
        "> ⚜You can set ✔~CUSTOM THUMBNAIL~, ✔~PDF WATERMARK~, ✔~VIDEO WATERMARK~, ✔~SESSION-based login~, etc. from settings⚙\n\n"
        "**__Powered by 🏴‍☠️✨KING PROJECTS✨🏴‍☠️__**"
    )
]
 
 
async def send_or_edit_help_page(_, message, page_number):
    if page_number < 0 or page_number >= len(help_pages):
        return
 
     
    prev_button = InlineKeyboardButton("⬅ Previous", callback_data=f"help_prev_{page_number}")
    next_button = InlineKeyboardButton("Next ➡", callback_data=f"help_next_{page_number}")
 
     
    buttons = []
    if page_number > 0:
        buttons.append(prev_button)
    if page_number < len(help_pages) - 1:
        buttons.append(next_button)
 
     
    keyboard = InlineKeyboardMarkup([buttons])
 
     
    await message.delete()
 
     
    await message.reply(
        help_pages[page_number],
        reply_markup=keyboard
    )
 
 
@app.on_message(filters.command("help"))
async def help(client, message):
    join = await subscribe(client, message)
    if join == 1:
        return
 
     
    await send_or_edit_help_page(client, message, 0)
 
 
@app.on_callback_query(filters.regex(r"help_(prev|next)_(\d+)"))
async def on_help_navigation(client, callback_query):
    action, page_number = callback_query.data.split("_")[1], int(callback_query.data.split("_")[2])
 
    if action == "prev":
        page_number -= 1
    elif action == "next":
        page_number += 1
 
     
    await send_or_edit_help_page(client, callback_query.message, page_number)
 
     
    await callback_query.answer()
 
 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
 
@app.on_message(filters.command("terms") & filters.private)
async def terms(client, message):
    terms_text = (
        "> 📜 **Terms and Conditions** 📜\n\n"
        "✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.\n"
        "✨ Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. __Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.__\n"
        "✨ Payment to us **__does not guarantee__** authorization for the /batch command. All decisions regarding authorization are made at our discretion and mood.\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/BhardwajBhavit")],
        ]
    )
    await message.reply_text(terms_text, reply_markup=buttons)
 
 
@app.on_message(filters.command("plan") & filters.private)
async def plan(client, message):
    plan_text = (
        "> 💰 **Premium Price**:\n\n 🤞Starting from **__~10₹~ or ~20₹~__**  accepted via **__all Payments Option__** (T&C apply).🤞\n\n"
        "📥 👻**Download Limit**: Users can download Multipel files in a single batch command.👻\n\n"
        "🛑 🌻**Batch**: You will get and /batch. mode🌻\n\n"
        "   🍂- Users are advised to wait for the process to automatically cancel before proceeding with any downloads or uploads.🍂\n\n"
        "📜 **Terms and Conditions**: For further details and complete terms and conditions, please send /terms.\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/BhardwajBhavit")],
        ]
    )
    await message.reply_text(plan_text, reply_markup=buttons)
 
 
@app.on_callback_query(filters.regex("see_plan"))
async def see_plan(client, callback_query):
    plan_text = (
        "> 💰**Premium Price**\n\n 🤞Starting from **__~10₹~ or ~20₹~__** accepted via **__all Payment Options__** (T&C apply).🤞\n\n"
        "📥 👻**Download Limit**: Users can download Multipel files in a single batch command.👻\n\n"
        "🛑 🌻**Batch**: You will get and /batch. mode🌻\n\n"
        "   🍂- Users are advised to wait for the process to automatically cancel before proceeding with any downloads or uploads.🍂\n\n"
        "📜 **Terms and Conditions**: For further details and complete terms and conditions, please send /terms or click See Terms👇\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/BhardwajBhavit")],
        ]
    )
    await callback_query.message.edit_text(plan_text, reply_markup=buttons)
 
 
@app.on_callback_query(filters.regex("see_terms"))
async def see_terms(client, callback_query):
    terms_text = (
        "> 📜 **Terms and Conditions** 📜\n\n"
        "✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.\n"
        "✨ Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. __Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.__\n"
        "✨ Payment to us **__does not guarantee__** authorization for the /batch command. All decisions regarding authorization are made at our discretion and mood.\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/BhardwajBhavit")],
        ]
    )
    await callback_query.message.edit_text(terms_text, reply_markup=buttons)
 
 
