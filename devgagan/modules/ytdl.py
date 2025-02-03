import yt_dlp
import os
import tempfile
import time
import asyncio
import random
import string
import requests
import logging
import cv2
from devgagan import sex as client
from pyrogram import Client, filters
from telethon import events
from telethon.sync import TelegramClient
from telethon.tl.types import DocumentAttributeVideo
from devgagan.core.func import screenshot, video_metadata
from telethon.tl.functions.messages import EditMessageRequest
from devgagantools import fast_upload
from concurrent.futures import ThreadPoolExecutor
import aiohttp
from mutagen.id3 import ID3, TIT2, TPE1, COMM, APIC
from mutagen.mp3 import MP3

logger = logging.getLogger(__name__)

thread_pool = ThreadPoolExecutor()
ongoing_downloads = {}

# Path to cookies.txt
COOKIES_PATH = os.path.join(os.getcwd(), 'devgagan', 'modules', 'cookies.txt')

def d_thumbnail(thumbnail_url, save_path):
    try:
        response = requests.get(thumbnail_url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return save_path
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download thumbnail: {e}")
        return None

async def download_thumbnail_async(url, path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(path, 'wb') as f:
                    f.write(await response.read())

async def extract_audio_async(ydl_opts, url):
    def sync_extract():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=True)
    return await asyncio.get_event_loop().run_in_executor(thread_pool, sync_extract)

def get_random_string(length=7):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

async def process_audio(client, event, url, cookies_path=None):
    start_time = time.time()
    random_filename = f"@team_spy_pro_{event.sender_id}"
    download_path = f"{random_filename}.mp3"
    
    if cookies_path is None:
        cookies_path = COOKIES_PATH  # Use the fixed path for cookies
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{random_filename}.%(ext)s",
        'cookiefile': cookies_path,
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'quiet': False,
        'noplaylist': True,
    }
    prog = None

    progress_message = await event.reply("**__Starting audio extraction...__**")

    try:
        info_dict = await extract_audio_async(ydl_opts, url)
        title = info_dict.get('title', 'Extracted Audio')

        await progress_message.edit("**__Editing metadata...__**")
        if os.path.exists(download_path):
            def edit_metadata():
                audio_file = MP3(download_path, ID3=ID3)
                try:
                    audio_file.add_tags()
                except Exception:
                    pass
                audio_file.tags["TIT2"] = TIT2(encoding=3, text=title)
                audio_file.tags["TPE1"] = TPE1(encoding=3, text="Pragyan")
                audio_file.tags["COMM"] = COMM(encoding=3, lang="eng", desc="Comment", text="Processed by Pragyan")
                thumbnail_url = info_dict.get('thumbnail')
                if thumbnail_url:
                    thumbnail_path = os.path.join(tempfile.gettempdir(), "thumb.jpg")
                    asyncio.run(download_thumbnail_async(thumbnail_url, thumbnail_path))
                    with open(thumbnail_path, 'rb') as img:
                        audio_file.tags["APIC"] = APIC(
                            encoding=3, mime='image/jpeg', type=3, desc='Cover', data=img.read()
                        )
                    os.remove(thumbnail_path)
                audio_file.save()

            await asyncio.to_thread(edit_metadata)

        chat_id = event.chat_id
        if os.path.exists(download_path):
            await progress_message.delete()
            prog = await client.send_message(chat_id, "**__Starting Upload...__**")
            uploaded = await fast_upload(
                client, download_path,
                reply=prog,
                name=None,
                progress_bar_function=lambda done, total: progress_callback(done, total, chat_id)
            )
            await client.send_file(chat_id, uploaded, caption=f"**{title}**\n\n**__Powered by Pragyan__**")
            if prog:
                await prog.delete()
        else:
            await event.reply("**__Audio file not found after extraction!__**")

    except Exception as e:
        logger.exception("Error during audio extraction or upload")
        await event.reply(f"**__An error occurred: {e}__")
    finally:
        if os.path.exists(download_path):
            os.remove(download_path)

async def process_video(client, event, url, cookies_path=None, check_duration_and_size=False):
    start_time = time.time()
    logger.info(f"Received link: {url}")

    if cookies_path is None:
        cookies_path = COOKIES_PATH  # Use the fixed path for cookies

    random_filename = get_random_string() + ".mp4"
    download_path = os.path.abspath(random_filename)
    logger.info(f"Generated random download path: {download_path}")

    thumbnail_file = None
    metadata = {'width': None, 'height': None, 'duration': None, 'thumbnail': None}

    ydl_opts = {
        'outtmpl': download_path,
        'format': 'best',
        'cookiefile': cookies_path,
        'writethumbnail': True,
        'verbose': True,
    }
    prog = None
    progress_message = await event.reply("**__Starting download...__**")
    logger.info("Starting the download process...")
    try:
        info_dict = await fetch_video_info(url, ydl_opts, progress_message, check_duration_and_size)
        if not info_dict:
            return

        await asyncio.to_thread(download_video, url, ydl_opts)
        title = info_dict.get('title', 'Powered by Pragyan')
        k = video_metadata(download_path)
        W = k['width']
        H = k['height']
        D = k['duration']
        metadata['width'] = info_dict.get('width') or W
        metadata['height'] = info_dict.get('height') or H
        metadata['duration'] = int(info_dict.get('duration') or 0) or D
        thumbnail_url = info_dict.get('thumbnail', None)
        THUMB = None

        if thumbnail_url:
            thumbnail_file = os.path.join(tempfile.gettempdir(), get_random_string() + ".jpg")
            downloaded_thumb = d_thumbnail(thumbnail_url, thumbnail_file)
            if downloaded_thumb:
                logger.info(f"Thumbnail saved at: {downloaded_thumb}")

        if thumbnail_file:
            THUMB = thumbnail_file
        else:
            THUMB = await screenshot(download_path, metadata['duration'], event.sender_id)

        chat_id = event.chat_id
        if os.path.exists(download_path):
            await progress_message.delete()
            prog = await client.send_message(chat_id, "**__Starting Upload...__**")
            uploaded = await fast_upload(
                client, download_path,
                reply=prog,
                progress_bar_function=lambda done, total: progress_callback(done, total, chat_id)
            )
            await client.send_file(
                event.chat_id,
                uploaded,
                caption=f"**{title}**",
                attributes=[
                    DocumentAttributeVideo(
                        duration=metadata['duration'],
                        w=metadata['width'],
                        h=metadata['height'],
                        supports_streaming=True
                    )
                ],
                thumb=THUMB if THUMB else None
            )
            if prog:
                await prog.delete()
        else:
            await event.reply("**__File not found after download. Something went wrong!__**")
    except Exception as e:
        logger.exception("An error occurred during download or upload.")
        await event.reply(f"**__An error occurred: {e}__")
    finally:
        if os.path.exists(download_path):
            os.remove(download_path)
        if thumbnail_file and os.path.exists(thumbnail_file):
            os.remove(thumbnail_file)

# Other methods like fetch_video_info, progress_callback, download_video, and others remain unchanged
# Ensure that you update your event handlers below

@client.on(events.NewMessage(pattern="/adl"))
async def handler(event):
    user_id = event.sender_id
    if user_id in ongoing_downloads:
        await event.reply("**You already have an ongoing download. Please wait until it completes!**")
        return

    if len(event.message.text.split()) < 2:
        await event.reply("**Usage:** /adl <video-link>\n\nPlease provide a valid video link!")
        return    

    url = event.message.text.split()[1]
    ongoing_downloads[user_id] = True

    try:
        await process_audio(client, event, url)
    except Exception as e:
        await event.reply(f"**An error occurred:** {e}")
    finally:
        ongoing_downloads.pop(user_id, None)

@client.on(events.NewMessage(pattern="/dl"))
async def handler(event):
    user_id = event.sender_id

    if user_id in ongoing_downloads:
        await event.reply("**You already have an ongoing ytdlp download. Please wait until it completes!**")
        return

    if len(event.message.text.split()) < 2:
        await event.reply("**Usage:** /dl <video-link>\n\nPlease provide a valid video link!")
        return    

    url = event.message.text.split()[1]

    try:
        await process_video(client, event, url)
    except Exception as e:
        await event.reply(f"**An error occurred:** {e}")
    finally:
        ongoing_downloads.pop(user_id, None)

