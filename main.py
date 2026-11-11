import asyncio
import time
import random
import re
from datetime import datetime
from collections import defaultdict
from telegram import Update
from telegram import ChatPermissions
from telegram.error import TelegramError
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.error import RetryAfter
# ========================= MULTI BOT CONFIG =========================
BOT_TOKENS = [
    
    "8396007535:AAHsXz5lLEVOxsyyAHEYSuNNWoPaDHLlJqw",
    "8711163627:AAE5TDdi3TwhY2g2R313mFZKF5C8B1Y6o1M",
    "8708602012:AAHQ2C7pdpizW6FXlUORt0P2zedr6SOFxck",
    
    "8966135886:AAHjHHcqbgAbGrye6Rw719onq_8lb8UE9y8",
    "8619906767:AAE9PueM4urRxAQRVk_j5XYyHBCReaHsVcQ",
    
    "8713482896:AAGcCB2dl-g505_J62iDSgasU7hLDdZK3YY",
    "8973335154:AAEoL_nkEPYO6lsMA_UqNmY9leqmPNUKGY0",
    "8891426631:AAGzyzi2_VXGHxlXwnJHsUcZKJGBGF-CBG8",
    "8668412803:AAHsSTpEaOe9RoHmJTXpNkSueIt5ONFUXSk",
    "8954295428:AAERPH4LVOz1tDCZgaf9GYmRvulWLEc2pUk",
    "8882126507:AAG4hKTY42lR62bhOHgS_wY2qC_qOW_1Agw",
    "8607054496:AAFU-0OlqJaleDxUk-CVJ8zNz7NSL8IXaa8",

]

OWNER_ID = 5066264920

# ====================== PHOTO STORAGE ======================
SAVED_PHOTOS = {}  # {group_id: [photo_file_ids]}
ACTIVE_PHOTO_LOOPS = {}  # {f"{group_id}_photo": asyncio.Task}

# ====================== GROUP TRACKING ======================
GROUP_TRACKER = {}  # {group_id: group_name}
TASK_START_TIMES = {}  # {task_key: start_time}
ACTIVE_GROUPS = set()  # Set of group IDs where bot is active

# ====================== ULTRA FAST CONFIG - NO DELAYS ======================
DELAYS = {
    'nc': 0,        # NO DELAY - INSTANT!
    'spam': 0,      # NO DELAY - MACHINE GUN!
    'swipe': 0,     # NO DELAY - LIGHTNING!
    'reply': 0,     # NO DELAY - SUPERSONIC!
}

# ====================== AUTO RESTART CONFIG ======================
AUTO_RESTART = False  # Disable auto restart - continuous loop is enough
RESTART_DELAY = 0    # Restart after 2 seconds

# ====================== 👥 FRIENDS & TEAM 👥 ======================
FRIENDS = {
    'creator': 'Sarwan',
    'team': ['Era', 'Of', 'Sarwan']
}

# ====================== TEXT LISTS ======================
NC_TEXTS = {
    'snc': [
        r"{target} 𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐊𝐀 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒,🥶᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄༺═──────────────═༻☟☜♻𓂃𓂃𓂃♻᳄᳄᳄᳄᳄᳄᳄༺═────(🌀)",
        r"{target} 𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐊𝐀 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒,🥶᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄༺═──────────────═༻☟☜♻𓂃𓂃𓂃♻᳄᳄᳄᳄᳄᳄᳄༺═────(🔥)",
        r"{target} 𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐊𝐀 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒,🥶᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄༺═──────────────═༻☟☜♻𓂃𓂃𓂃♻᳄᳄᳄᳄᳄᳄᳄༺═────(💀)",
        r"{target} 𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐊𝐀 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒,🥶᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄༺═──────────────═༻☟☜♻𓂃𓂃𓂃♻᳄᳄᳄᳄᳄᳄᳄༺═────(⚡)",
        r"{target} 𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐊𝐀 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒,🥶᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄༺═──────────────═༻☟☜♻𓂃𓂃𓂃♻᳄᳄᳄᳄᳄᳄᳄༺═────(😈)",
        r"{target} 𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐊𝐀 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒,🥶᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄༺═──────────────═༻☟☜♻𓂃𓂃𓂃♻᳄᳄᳄᳄᳄᳄᳄༺═────(☠️)",
        r"{target} 𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐊𝐀 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒,🤍᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄༺═──────────────═༻☟☜♻𓂃𓂃𓂃♻᳄᳄᳄᳄᳄᳄᳄༺═────(🌪️)",
        r"{target} 𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐊𝐀 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒,💢᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄༺═──────────────═༻☟☜♻𓂃𓂃𓂃♻᳄᳄᳄᳄᳄᳄᳄༺═────(👑)",
        r"{target} 𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐊𝐀 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒,🥶💢᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄༺═──────────────═༻☟☜♻𓂃𓂃𓂃♻᳄᳄᳄᳄᳄᳄᳄༺═────(💥)",
        r"{target} 𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐊𝐀 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒,🥶᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄᳄༺═──────────────═༻☟☜♻𓂃𓂃𓂃♻᳄᳄᳄᳄᳄᳄᳄༺═────(🚨)"
    ],
    'ssnc': [
        r"{target}﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷〘 𝐓𝐌𝐊𝐂 𝐂𝐇𝐔𝐏 𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 𝐒𝐀𝐑𝐖𝐀𝐍 𝐒𝐄 𝐒𝐄𝐓 𝐇 𝐎𝐊 👌🤗〙(🌀)",
        r"{target}﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷〘 𝘛𝘮𝘬𝘤 𝘙𝘢𝘯𝘥𝘪〙(🔥)",
        r"{target}﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷〘 𝘛𝘮𝘬𝘤 𝘙𝘢𝘯𝘥𝘪〙(💀)",
        r"{target}﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷〘 𝘛𝘮𝘬𝘤 𝘙𝘢𝘯𝘥𝘪〙(⚡)",
        r"{target}﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷〘 𝘛𝘮𝘬𝘤 𝘙𝘢𝘯𝘥𝘪〙(😈)",
        r"{target}﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷〘 𝘚𝘢𝘳𝘸𝘢𝘯 𝘬𝘰 𝘣𝘢𝘢𝘱 𝘣𝘰𝘭〙(☠️)",
        r"{target}﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷〘 𝘚𝘢𝘳𝘸𝘢𝘯 𝘬𝘰 𝘣𝘢𝘢𝘱 𝘣𝘰𝘭〙(🌪️)",
        r"{target}﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷〘 𝘚𝘢𝘳𝘸𝘢𝘯 𝘬𝘰 𝘣𝘢𝘢𝘱 𝘣𝘰𝘭〙(👑)",
        r"{target}﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷〘𝐂ʜʜᴀᴋᴀ ᴄᴜᴅᴀɪ ᴋʜᴀ〙(💥)",
        r"{target}﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷﷽﷽🩷〘 𝘚𝘢𝘳𝘸𝘢𝘯 𝘬𝘰 𝘣𝘢𝘢𝘱 𝘣𝘰𝘭〙(🚨)"
    ],
    'fnc': [
        r"˚⊱━━🍁━━⊰˚{target} Cʜᴜᴘ Cʜᴀᴘ Cʜᴜᴅ Rɴᴅʏᴋ\n꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅",
        r"˚⊱━━🔥━━⊰˚{target} Cʜᴜᴘ Cʜᴀᴘ Cʜᴜᴅ Rɴᴅʏᴋ\n꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅",
        r"˚⊱━━💀━━⊰˚{target} Cʜᴜᴘ Cʜᴀᴘ Cʜᴜᴅ Rɴᴅʏᴋ\n꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅",
        r"˚⊱━━⚡━━⊰˚{target} Cʜᴜᴘ Cʜᴀᴘ Cʜᴜᴅ Rɴᴅʏᴋ\n꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅",
        r"˚⊱━━😈━━⊰˚{target} Cʜᴜᴘ Cʜᴀᴘ Cʜᴜᴅ Rɴᴅʏᴋ\n꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅",
        r"˚⊱━━☠️━━⊰˚{target} Cʜᴜᴘ Cʜᴀᴘ Cʜᴜᴅ Rɴᴅʏᴋ\n꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅",
        r"˚⊱━━🌪️━━⊰˚{target} Cʜᴜᴘ Cʜᴀᴘ Cʜᴜᴅ Rɴᴅʏᴋ\n꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅",
        r"˚⊱━━👑━━⊰˚{target} Cʜᴜᴘ Cʜᴀᴘ Cʜᴜᴅ Rɴᴅʏᴋ\n꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅",
        r"˚⊱━━💥━━⊰˚{target} Cʜᴜᴘ Cʜᴀᴘ Cʜᴜᴅ Rɴᴅʏᴋ\n꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅",
        r"˚⊱━━🚨━━⊰˚{target} Cʜᴜᴘ Cʜᴀᴘ Cʜᴜᴅ Rɴᴅʏᴋ\n꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅꧅"
    ],
    'cnc': [
        r"˚⊱━━😛━━⊰˚{target} chote bhag rndice 𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨✨𒐫✨✨✨𒐫✨✨✨𒐫𒐫✨✨𒐫✨✨✨𒐫✨✨𒐫𒐫✨✨✨𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨𒐫𒐫𒐫✨𒐫✨✨𒐫𒐫✨✨𒐫✨✨𒐫𒐫𒐫✨🎀✨",
        r"˚⊱━━🔥━━⊰˚{target} chote bhag rndice 𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨✨𒐫✨✨✨𒐫✨✨✨𒐫𒐫✨✨𒐫✨✨✨𒐫✨✨𒐫𒐫✨✨✨𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨𒐫𒐫𒐫✨𒐫✨✨𒐫𒐫✨✨𒐫✨✨𒐫𒐫𒐫✨🎀✨",
        r"˚⊱━━💀━━⊰˚{target} chote bhag rndice 𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨✨𒐫✨✨✨𒐫✨✨✨𒐫𒐫✨✨𒐫✨✨✨𒐫✨✨𒐫𒐫✨✨✨𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨𒐫𒐫𒐫✨𒐫✨✨𒐫𒐫✨✨𒐫✨✨𒐫𒐫𒐫✨🎀✨",
        r"˚⊱━━⚡━━⊰˚{target} chote bhag rndice 𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨✨𒐫✨✨✨𒐫✨✨✨𒐫𒐫✨✨𒐫✨✨✨𒐫✨✨𒐫𒐫✨✨✨𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨𒐫𒐫𒐫✨𒐫✨✨𒐫𒐫✨✨𒐫✨✨𒐫𒐫𒐫✨🎀✨",
        r"˚⊱━━😈━━⊰˚{target} chote bhag rndice 𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨✨𒐫✨✨✨𒐫✨✨✨𒐫𒐫✨✨𒐫✨✨✨𒐫✨✨𒐫𒐫✨✨✨𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨𒐫𒐫𒐫✨𒐫✨✨𒐫𒐫✨✨𒐫✨✨𒐫𒐫𒐫✨🎀✨",
        r"˚⊱━━☠️━━⊰˚{target} chote bhag rndice 𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨✨𒐫✨✨✨𒐫✨✨✨𒐫𒐫✨✨𒐫✨✨✨𒐫✨✨𒐫𒐫✨✨✨𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨𒐫𒐫𒐫✨𒐫✨✨𒐫𒐫✨✨𒐫✨✨𒐫𒐫𒐫✨🎀✨",
        r"˚⊱━━🌪️━━⊰˚{target} chote bhag rndice 𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨✨𒐫✨✨✨𒐫✨✨✨𒐫𒐫✨✨𒐫✨✨✨𒐫✨✨𒐫𒐫✨✨✨𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨𒐫𒐫𒐫✨𒐫✨✨𒐫𒐫✨✨𒐫✨✨𒐫𒐫𒐫✨🎀✨",
        r"˚⊱━━👑━━⊰˚{target} chote bhag rndice 𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨✨𒐫✨✨✨𒐫✨✨✨𒐫𒐫✨✨𒐫✨✨✨𒐫✨✨𒐫𒐫✨✨✨𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨𒐫𒐫𒐫✨𒐫✨✨𒐫𒐫✨✨𒐫✨✨𒐫𒐫𒐫✨🎀✨",
        r"˚⊱━━💥━━⊰˚{target} chote bhag rndice 𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨✨𒐫✨✨✨𒐫✨✨✨𒐫𒐫✨✨𒐫✨✨✨𒐫✨✨𒐫𒐫✨✨✨𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨𒐫𒐫𒐫✨𒐫✨✨𒐫𒐫✨✨𒐫✨✨𒐫𒐫𒐫✨🎀✨",
        r"˚⊱━━🚨━━⊰˚{target} chote bhag rndice 𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨✨𒐫✨✨✨𒐫✨✨✨𒐫𒐫✨✨𒐫✨✨✨𒐫✨✨𒐫𒐫✨✨✨𒐫𒐫𒐫𒐫𒐫𒐫𒐫✨✨𒐫𒐫𒐫✨𒐫✨✨𒐫𒐫✨✨𒐫✨✨𒐫𒐫𒐫✨🎀✨"
    ],
    'bnc': [
        r"✨ {target} 𝐓ᴍᴋᴄ 𝐑Aɴᴅi 𝐊ᴇ𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑💫",
        r"🌟 {target} 𝐓ᴍᴋᴄ 𝐑Aɴᴅi 𝐊ᴇ𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑✨",
        r"🌀 {target} 𝐓ᴍᴋᴄ 𝐑Aɴᴅi 𝐊ᴇ𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑💫",
        r"🔱 {target} 𝐓ᴍᴋᴄ 𝐑Aɴᴅi 𝐊ᴇ𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑✨",
        r"🌈 {target} 𝐓ᴍᴋᴄ 𝐑Aɴᴅi 𝐊ᴇ𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑??👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑💫",
        r"⭐ {target} 𝐓ᴍᴋᴄ 𝐑Aɴᴅi 𝐊ᴇ𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑✨",
        r"🫧 {target} 𝐓ᴍᴋᴄ 𝐑Aɴᴅi 𝐊ᴇ𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑💫",
        r"🪩 {target} 𝐓ᴍᴋᴄ 𝐑Aɴᴅi 𝐊ᴇ𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑✨",
        r"🪷 {target}  𝐓ᴍᴋᴄ 𝐑Aɴᴅi 𝐊ᴇ𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑💫",
        r"🌙 {target} 𝐓ᴍᴋᴄ 𝐑Aɴᴅi 𝐊ᴇ𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑𒈙👑✨"
    ],
    'sgcnc': [
        r"{target} ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤ 𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤(💔)",
        r"{target} ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤ 𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤(❤️)",
        r"{target} ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤ 𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤(🧡)",
        r"{target} ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤ 𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤(💛)",
        r"{target} ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤ 𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤(💚)",
        r"{target} ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤ 𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤(🩶)",
        r"{target} ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤ 𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤(🤎)",
        r"{target} ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤ 𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤(💜)",
        r"{target} ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤ 𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤(💙)",
        r"{target} ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤ 𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤𒀱ꪳ🩵𒀱ꪳ💛𒀱ꪳ💚𒀱ꪳ❤(🩵)"
    ]
}

SPAM_TEXTS = {
    'bspam': [
        r"✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Kᴀʟᴡɪ 「🎀」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Kᴀʟᴡɪ 「🤍」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Kᴀʟᴡɪ 「🎀」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Kᴀʟᴡɪ 「🤍」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Kᴀʟᴡɪ 「🎀」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Kᴀʟᴡɪ 「🤍」",
        r"✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Bᴀᴜɴɪ 「✨」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Bᴀᴜɴɪ 「🩷」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Bᴀᴜɴɪ 「✨」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Bᴀᴜɴɪ 「🩷」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Bᴀᴜɴɪ 「✨」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Bᴀᴜɴɪ 「🩷」",
        r"✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Hᴀᴋʟɪ 「💫」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Hᴀᴋʟɪ 「🩵」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Hᴀᴋʟɪ 「💫」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Hᴀᴋʟɪ 「🩵」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Hᴀᴋʟɪ 「💫」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Hᴀᴋʟɪ 「🩵」",
        r"✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Lᴀɴɢᴅɪ 「🌙」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Lᴀɴɢᴅɪ 「🖤」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Lᴀɴɢᴅɪ 「🌙」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Lᴀɴɢᴅɪ 「🖤」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Lᴀɴɢᴅɪ 「🌙」\n✫: ̗̀➛「{target}」────────Tᴇʀɪ Mᴀ Lᴀɴɢᴅɪ 「🖤」"
    ],
    'aspam': [
        r"🤍{target}  ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ   🤍",
        r" 🖤{target}  ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ   🖤",
        r" 🤎{target}  ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ   🤎",
        r" 💜{target}  ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ   💜",
        r" 💙{target}  ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ   💙",
        r" 🩵{target}  ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ   🩵",
        r" 💚{target}  ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ   💚",
        r" 💛{target}  ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ   💛",
        r" 🧡{target}  ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ   🧡",
        r" ❤️{target}  ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ   ❤️"
    ],
    'sspam': [
        r"{target}  CVR KR MC GAREEB 👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞 {target}  CVR KR MC GAREEB{target}  CVR KR MC GAREEB 👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞 {target}  CVR KR MC GAREEB {target}  CVR KR MC GAREEB 👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞👞 {target}  CVR KR MC GAREEB"
    ],
    'fspam': [
        r"💛 𓂃𓈒 {target} OYEEEEEEEEEEE  TEERRIIIIIII MAAA KIIIIIII CHUTTTTTTT  CHALLLLLLL BOLLLLLLL 🥷 𝗬𝗨𝗧𝗔  PAAAPPAAA GALTIIIIIIIII HO GYAAAAAA              YEEEEEE SPAMMMMM KRRRRKAAA TERIIIII MAAAA KIIIII CHUTTTTTT FARRRRR GUNGAAAAAAAA  BOLLLL 🥷 𝗬𝗨𝗧𝗔  PAPA SORRYYYYY                                TUUUUU LANDDDDD KAAAA BALLLLL 🥷 𝗬𝗨𝗧𝗔  KO H8 DEGAAAA TERIIII MAA KIIIIIIII CHUTTTTTTTTT  TUU 🥷 𝗬𝗨𝗧𝗔  KIIIII LUNDDDDD KAAAA BALLLLL HAI BSSSSSSS RO MATTTTTTTT ABBB AB KUCHHHHH NHIIIII HOO SKTAAAAA HAI ABB TU   CHUDI       KHAAAAAA BSSSSSSS  {target}"
    ],
    'gspam': [
        r"TERYYYYYYYYYYYY AMMMMIIII KIIIII BURRRR FADUUGAAAA MADHARXHODDDDD👀👀👀 RANDIKEEEEE PILLEEEE  RANDDDD TERYYYY BHENNNN KIIII SEALLLL TODUGAAAAA SAREYAMMMMM CHAURAHEEEEE PEEEEE🤣🤣🤣🤣🤣BHENNNN KEEEE TAKEEEE MADHARXHODDDDDDD🖕🖕TERYYYYY MAAAA KEEEE BHOSDEEEE MEEEE KHADAAA HATHIIII KAAAA LUNDDDD DALUGAAAA BHENNNN KEEE TAKKEEEEE MADHARXHODDDDD👀👀👀🤣🤣🤣 BHSDKKK BAAAPP KOOO FEELLL LEEE BHAGGG MATTTT MADHARXHODDDD BHSDKKKK TERYYY MAAA XHODNIIII HAIIII MEREEE KOOO AJAAA RANDIKEEEE OLADDD🤣🤣👅👅🙈🖕🩸\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n            𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ \n     ⠀⣴⣾⣿⣿⣶⡄\n⠀⠀⢸⣿⣿⣿⣿⣿⣿\n⠀⠀⠈⢿⣿⣿⣿⣿⠏\n⠀⠀⠀⠀⠈⣉⣩⣀⡀\n⠀⠀⠀⠀⣼⣿⣿⣿⣷⡀⠀\n⠀⠀⢀⣼⣿⣿⣿⣿⣿⡇\n⠀⢀⣾⣿⣿⣿⣿⣿⣿⣷. {target} TERY MAA\n⢠⣾⣿⣿⠉⣿⣿⣿⣿⣿⡄⠀⢀⣠⣤⣤⣀\n⠀⠙⣿⣿⣧⣿⣿⣿⣿⣿⡇⢠⣿⣿⣿⣿⣿⣧\n⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣷⠸⣿⣿⣿⣿⣿⡿\n⠀⠀⠀⠀⠘⠿⢿⣿⣿⣿⣿⡄⠙⠻⠿⠿⠛⠁\n⠀⠀⠀⠀⠀⠀⠀⡟⣩⣝⢿⠀⠀⣠⣶⣶⣦⡀\n⠀⠀⠀⠀⠀⠀⠀⣷⡝⣿⣦⣠⣾⣿⣿⣿⣿⣷⡀\n⠀⠀⠀⠀⠀⠀⠀⣿⣿⣮⢻⣿⠟⣿⣿⣿⣿⣿⣷⡀\n⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⠻⠿⠻⣿⣿⣿⣿⣦⡀\n⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⠇⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⡆\n⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⠇\n⠀⠀⠀⠀⠀⠀⢸⣿⣿⡿⠀⠀⠀⢀⣴⣿⣿⣿⣿⣟⣋⣁⣀⣀\n\n\nFEEL KARRRRRR BAAAPPPPPP KOOOOO MADRXHODDDDDDD :)(●*∩_∩*●)"
    ],
    'rspam': [
        r"{target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙 {target}𝐑ᴀɴᴅʏ 𝐊ᴀ 𝐁ᴀᴄʜᴀ ˏˋ°•*⁀➷ 𝑳𝑼𝑵𝑫 𝑪𝑯𝑶𝑶𝑺 🥷 𝗬𝗨𝗧𝗔  𝑲𝑨 कुतिया के 🥂🌙"
    ]
}

SWIPE_TEXTS = {
    'aswipe': [
        r"𝐊ʏᴀ 𝐑ᴇ 𝐑ᴀɴᴅɪᴋᴇ 𝐂ᴏᴏʟ 𝐁ᴀɴᴇɢᴀ 𝐓ᴜ 𝐂ʜᴀʟ 𝐀ʙ 𝐂ʜᴜᴅ 𝐀ᴘɴᴇ 𝐁ᴀᴀᴘ 🥷 𝗬𝗨𝗧𝗔  𝐒ᴇ - 🦢💘",
        r"𝐊ɪ 𝐌ᴀᴀ 𝐌ᴀʀʀ 𝐆ᴀʏɪ 𝐘ᴀᴀʀ - 𝐉ᴀɪ 🥷 𝗬𝗨𝗧𝗔  ! 🌙",
        r"acha beta 😂🔥👊🏻 ? coi na me toh HATER codunga 😹💔🔥😆👊🏻💥",
        r"chudke bhaga kaise 😂💥🤣🤘🏻",
        r"ne toh 🥷 𝗬𝗨𝗧𝗔  ka lun muh me lelia 😂🙏🏻😂🙏🏻",
        r"try maa सूर्य☀ nikalte hi pel du 😹🔥💔",
        r"mkl lun te vaj 😂✊🏻💦",
        r"𝗧ᴍᴋ𝗕 pe 🥷 𝗬𝗨𝗧𝗔  ka hamla 😂⚔🔥💥",
        r"𝐂ʜʟ 𝐇ᴀʀᴍᴢᴀᴅ𝐈 𝐊ᴇ लड़के 💛🤍🩵",
        r"oi 𝐓ᴇʀɪ 𝐌‌ᴀᴀ गुलाम ₰🖤",
        r"chl rndyce chud ke dikha 😂💥🤣🔥",
        r"𝐊ɪ 𝐌ᴀᴀ 𝐌ᴀʀʀ 𝐆ᴀʏɪ naacho 💃🏻💃🏻🕺🏻🎶😂😆💞🔥 !",
        r"tera baap bass 🥷 𝗬𝗨𝗧𝗔  hai 😂🎀",
        r" try maa hagte hue paad mari -#😹🔥🥀",
        r"  𝐓ᴇʀɪ 𝐌ᴜᴍᴍʏ 𝐂ʜᴏᴅ 𝐃ɪ 🥷 𝗬𝗨𝗧𝗔  𝐍ᴇ 𝐁ᴡᴀʜᴀʜᴀʜᴀ ⚜",
        r"𝐊ʏᴀ 𝐑ᴇ 𝐑ᴀɴᴅɪᴋᴇ 𝐂ᴏᴏʟ 𝐁ᴀɴᴇɢᴀ 𝐓ᴜ 𝐂ʜᴀʟ 𝐀ʙ 𝐂ʜᴜᴅ 𝐀ᴘɴᴇ 𝐁ᴀᴀᴘ 🥷 𝗬𝗨𝗧𝗔  𝐒ᴇ - 🦢💘",
        r"𝐊ɪ 𝐌ᴀᴀ 𝐌ᴀʀʀ 𝐆ᴀʏɪ 𝐘ᴀᴀʀ - 𝐉ᴀɪ 🥷 𝗬𝗨𝗧𝗔  ! 🌙",
        r"acha beta 😂🔥👊🏻 ? coi na me toh HATER codunga 😹💔🔥😆👊🏻💥"
    ],
    'fswipe': [
        r"chudke bhaga kaise 😂💥🤣🤘🏻",
        r"ne toh 🥷 𝗬𝗨𝗧𝗔  ka lun muh me lelia 😂🙏🏻😂🙏🏻",
        r"try maa सूर्य☀ nikalte hi pel du 😹🔥💔",
        r"mkl lun te vaj 😂✊🏻💦",
        r"𝗧ᴍᴋ𝗕 pe 🥷 𝗬𝗨𝗧𝗔  ka hamla 😂⚔🔥💥",
        r"𝐂ʜʟ 𝐇ᴀʀᴍᴢᴀᴅ𝐈 𝐊ᴇ लड़के 💛🤍🩵",
        r"oi 𝐓ᴇʀɪ 𝐌‌ᴀᴀ गुलाम ₰🖤",
        r"chl rndyce chud ke dikha 😂💥🤣🔥",
        r"𝐊ɪ 𝐌ᴀᴀ 𝐌ᴀʀʀ 𝐆ᴀʏɪ naacho 💃🏻💃🏻🕺🏻🎶😂😆💞🔥 !",
        r"tera baap bass 🥷 𝗬𝗨𝗧𝗔  hai 😂🎀",
        r" try maa hagte hue paad mari -#😹🔥🥀",
        r"  𝐓ᴇʀɪ 𝐌ᴜᴍᴍʏ 𝐂ʜᴏᴅ 𝐃ɪ 🥷 𝗬𝗨𝗧𝗔  𝐍ᴇ 𝐁ᴡᴀʜᴀʜᴀʜᴀ ⚜"
    ],
    'rrswipe': [
        r"𓂃˖˳·˖ ִֶָ ⋆❤️͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚❤️ ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆🧡͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚🧡 ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆💛͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚💛 ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆💚͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚💚 ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆💙͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚💙 ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆💜͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚💜 ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆🖤͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚🖤 ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆🤍͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚🤍 ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆🤎͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚🤎 ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆💖͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚💖 ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆💗͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚💗 ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆💓͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚💓 ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆💞͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚💞 ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆💕͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚💕 ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆💘͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚💘 ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆💝͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚💝 ݁˖⭑.ᐟ",
        r"𓂃˖˳·˖ ִֶָ ⋆💟͙⋆ ִֶָ˖·˳˖𓂃 ִֶָ⁀➴༯ sꪶꪖꪜꫀ ִֶָ. ..𓂃 ࣪ ִֶָ🌈་༘࿐ 𝗟𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 -/- ⋆˚💟 ݁˖⭑.ᐟ"
    ],
    'cswipe': [
        r" 𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸 ⇝ ༼ 🍓༽ ",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍈༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🫜༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍒༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍐༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🥥༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍎༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🫛༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🥔༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍅༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🥬༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🧅༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🌶️༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🫑༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🫚༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍉༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍏༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🫘༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍑༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🥝༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🌰༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍊༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🥑༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🥜༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍐༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🫒༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍞༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🥭༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🥦༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🫓༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍍༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🥒༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🥯༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍌༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🫐༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🧇༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍋༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍇༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍳༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🌽༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍆༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🥩༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍋‍🟩༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍠༽",
        r"𝐾𝐵𝐴𝐷𝐼 𝑊𝐴𝐿𝐸  ⇝ ༼ 🍟༽"
    ]
}

REPLY_TEXTS = {
    'rreply': [
        r"⋆｡ﾟ☁︎｡𝐂ʏᴜ 𝐑ᴇ मदरचोद 🥷 𝗬𝗨𝗧𝗔  बाप के सामने 𝐅ʏᴛᴇʀ 𝐁ᴀɴᴇɢᴀ ⋆𓂃 ོ☼𓂃 😂🔥",
        r"नहीं नहीं तेरी मां को 𝐒ɪʀғ 🥷 𝗬𝗨𝗧𝗔  बाप चोद सकता है ִֶָ𓂃 ࣪ ִֶָ👑་༘࿐ sᴀᴍᴊʜᴀ ʀᴀɴᴅɪᴋᴇ ???",
        r"तेरी मां का 𝐒ᴛʏʟɪsʜ भोसड़ा 😱",
        r"𝑻𝒆𝒓𝒚 𝒎𝒂𝒂 𝒓𝒂𝒏𝒅𝒂𝒍 𝒉 𝒃𝒂𝒔 𝒃𝒂𝒂𝒕 𝒌𝒉𝒂𝒕𝒂𝒎 😡🔥",
        r"सोच तेरी बहन को 🥷 𝗬𝗨𝗧𝗔  बाप का गुलाम चोद रहा 😎🔥",
        r"Hello hello?? Oxygen aarahi है? रण्डी पुत्र 🧘🏻",
        r"Shut up रंडीके वरना दुनिया यही बोलेगी तेरी बहन 🥷 𝗬𝗨𝗧𝗔  /\~ 👑 बाप से सही chudi 🥵🔥"
    ],
    'breply': [
        r"ᴛᴜ ᴏʀ ᴛᴇʀɪ ᴍᴀᴀ ᴅᴏɴᴏ 🥷 𝗬𝗨𝗧𝗔  बाप के ʟɴᴅ sᴇ ᴋᴀʙʜɪ ᴜᴛʜ ɴʜɪ ᴘᴀʏᴇ 😂🔥",
        r"🇮🇳𝐵𝐻𝐴𝑅𝐴𝑇 𝐻𝐴𝑀𝐴𝑅𝐴 𝐷𝐸𝑆𝐻 𝐻 𝐴𝑈𝑅 𝑈𝑆 𝐷𝐸𝑆𝐻 𝑀𝐸 तेरी मां घर घर जाके MOAN करती है ! 🛐",
        r"⋆｡ﾟ☁︎｡𝐂ʏᴜ 𝐑ᴇ मदरचोद 🥷 𝗬𝗨𝗧𝗔  बाप के सामने 𝐅ʏᴛᴇʀ 𝐁ᴀɴᴇɢᴀ ⋆𓂃 ོ☼𓂃 😂🔥",
        r"नहीं नहीं तेरी मां को 𝐒ɪʀғ 🥷 𝗬𝗨𝗧𝗔  बाप चोद सकता है ִֶָ𓂃 ࣪ ִֶָ👑་༘࿐ sᴀᴍᴊʜᴀ ʀᴀɴᴅɪᴋᴇ ???",
        r"तेरी मां का 𝐒ᴛʏʟɪsʜ भोसड़ा 😱",
        r"𝑻𝒆𝒓𝒚 𝒎𝒂𝒂 𝒓𝒂𝒏𝒅𝒂𝒍 𝒉 𝒃𝒂𝒔 𝒃𝒂𝒂𝒕 𝒌𝒉𝒂𝒕𝒂𝒎 😡🔥",
        r"सोच तेरी बहन को 🥷 𝗬𝗨𝗧𝗔  बाप का गुलाम चोद रहा 😎🔥",
        r"Hello hello?? Oxygen aarahi है? रण्डी पुत्र 🧘🏻",
        r"Shut up रंडीके वरना दुनिया यही बोलेगी तेरी बहन 🥷 𝗬𝗨𝗧𝗔  /\~ 👑 बाप से सही chudi 🥵🔥",
        r"ᴛᴜ ᴏʀ ᴛᴇʀɪ ᴍᴀᴀ ᴅᴏɴᴏ 🥷 𝗬𝗨𝗧𝗔  बाप के ʟɴᴅ sᴇ ᴋᴀʙʜɪ ᴜᴛʜ ɴʜɪ ᴘᴀʏᴇ 😂🔥",
        r"🇮🇳𝐵𝐻𝐴𝑅𝐴𝑇 𝐻𝐴𝑀𝐴𝑅𝐴 𝐷𝐸𝑆𝐻 𝐻 𝐴𝑈𝑅 𝑈𝑆 𝐷𝐸𝑆𝐻 𝑀𝐸 तेरी मां घर घर जाके MOAN करती है ! 🛐",
        r"⋆｡ﾟ☁︎｡𝐂ʏᴜ 𝐑ᴇ मदरचोद 🥷 𝗬𝗨𝗧𝗔  बाप के सामने 𝐅ʏᴛᴇʀ 𝐁ᴀɴᴇɢᴀ ⋆𓂃 ོ☼𓂃 😂🔥"
    ],
    'creply': [
        r"नहीं नहीं तेरी मां को 𝐒ɪʀғ 🥷 𝗬𝗨𝗧𝗔  बाप चोद सकता है ִֶָ𓂃 ࣪ ִֶָ👑་༘࿐ sᴀᴍᴊʜᴀ ʀᴀɴᴅɪᴋᴇ ???",
        r"तेरी मां का 𝐒ᴛʏʟɪsʜ भोसड़ा 😱",
        r"𝑻𝒆𝒓𝒚 𝒎𝒂𝒂 𝒓𝒂𝒏𝒅𝒂𝒍 𝒉 𝒃𝒂𝒔 𝒃𝒂𝒂𝒕 𝒌𝒉𝒂𝒕𝒂𝒎 😡🔥",
        r"सोच तेरी बहन को 🥷 𝗬𝗨𝗧𝗔  बाप का गुलाम चोद रहा 😎🔥",
        r"Hello hello?? Oxygen aarahi है? रण्डी पुत्र 🧘🏻",
        r"Shut up रंडीके वरना दुनिया यही बोलेगी तेरी बहन 🥷 𝗬𝗨𝗧𝗔  /\~ 👑 बाप से सही chudi 🥵🔥",
        r"ᴛᴜ ᴏʀ ᴛᴇʀɪ ᴍᴀᴀ ᴅᴏɴᴏ 🥷 𝗬𝗨𝗧𝗔  बाप के ʟɴᴅ sᴇ ᴋᴀʙʜɪ ᴜᴛʜ ɴʜɪ ᴘᴀʏᴇ 😂🔥",
        r"🇮🇳𝐵𝐻𝐴𝑅𝐴𝑇 𝐻𝐴𝑀𝐴𝑅𝐴 𝐷𝐸𝑆𝐻 𝐻 𝐴𝑈𝑅 𝑈𝑆 𝐷𝐸𝑆𝐻 𝑀𝐸 तेरी मां घर घर जाके MOAN करती है ! 🛐",
        r"⋆｡ﾟ☁︎｡𝐂ʏᴜ 𝐑ᴇ मदरचोद 🥷 𝗬𝗨𝗧𝗔  बाप के सामने 𝐅ʏᴛᴇʀ 𝐁ᴀɴᴇɢᴀ ⋆𓂃 ོ☼𓂃 😂🔥",
        r"नहीं नहीं तेरी मां को 𝐒ɪʀғ 🥷 𝗬𝗨𝗧𝗔  बाप चोद सकता है ִֶָ𓂃 ࣪ ִֶָ👑་༘࿐ sᴀᴍᴊʜᴀ ʀᴀɴᴅɪᴋᴇ ???",
        r"तेरी मां का 𝐒ᴛʏʟɪsʜ भोसड़ा 😱",
        r"𝑻𝒆𝒓𝒚 𝒎𝒂𝒂 𝒓𝒂𝒏𝒅𝒂𝒍 𝒉 𝒃𝒂𝒔 𝒃𝒂𝒂𝒕 𝒌𝒉𝒂𝒕𝒂𝒎 😡🔥"
    ]
}

# ====================== STATE ======================
active_tasks = {}
sudo_users = {OWNER_ID}
sudo_list = [OWNER_ID]
start_time = time.time()

def is_sudo(user_id: int) -> bool:
    # Direct check for owner - no sudo_users dependency
    if user_id == OWNER_ID:
        return True
    if user_id in sudo_users:
        return True
    return False

async def replace_target(text: str, target: str = "") -> str:
    if target:
        text = text.replace("{target}", target).replace("<target>", target).replace("<TARGET>", target.upper())
    return text

# ====================== SUPER FAST LOOPS ======================
async def nc_loop(context, bot_id, chat_id, loop_type, target):
    key = f"{bot_id}_{chat_id}_{loop_type}"
    texts = NC_TEXTS.get(loop_type, NC_TEXTS['snc'])
    i = 0
    
    error_skip = 0
    while key in active_tasks:
        try:
            title = await replace_target(texts[i % len(texts)], target)
            try:
                await context.bot.set_chat_title(chat_id, title)
                i += 1
                error_skip = 0
            except Exception as send_err:
                if "FloodWait" in str(send_err):
                    wait_match = re.search(r'retry after (\d+)', str(send_err))
                    wait_time = int(wait_match.group(1)) if wait_match else 1
                    await asyncio.sleep(wait_time)
                else:
                    # Skip error, continue to next text
                    i += 1
                    error_skip += 1
                    if error_skip > 50:
                        error_skip = 0
                    await asyncio.sleep(0.001) if error_skip > 10 else None
        except asyncio.CancelledError:
            break
        except:
            # Silently skip any other error
            i += 1
            await asyncio.sleep(0.001)
    
    # AUTO RESTART FUNCTIONALITY
    if AUTO_RESTART and key in active_tasks:
        print(f"🔄 Auto-Restarting {loop_type}...")
        await asyncio.sleep(RESTART_DELAY)
        if key in active_tasks:
            asyncio.create_task(nc_loop(context, bot_id, chat_id, loop_type, target))

async def spam_loop(context, bot_id, chat_id, loop_type, target):
    key = f"{bot_id}_{chat_id}_{loop_type}"
    texts = SPAM_TEXTS.get(loop_type, SPAM_TEXTS['bspam'])
    i = 0
    
    while key in active_tasks:
        try:
            msg = await replace_target(texts[i % len(texts)], target)
            try:
                await context.bot.send_message(chat_id, msg)
                i += 1
            except Exception as send_err:
                if "FloodWait" in str(send_err):
                    wait_match = re.search(r'retry after (\d+)', str(send_err))
                    wait_time = int(wait_match.group(1)) if wait_match else 1
                    await asyncio.sleep(wait_time)
                else:
                    i += 1
                    await asyncio.sleep(0.001)
        except asyncio.CancelledError:
            break
        except:
            i += 1
    
    # AUTO RESTART FUNCTIONALITY
    if AUTO_RESTART and key in active_tasks:
        print(f"🔄 Auto-Restarting {loop_type}...")
        await asyncio.sleep(RESTART_DELAY)
        if key in active_tasks:
            asyncio.create_task(spam_loop(context, bot_id, chat_id, loop_type, target))

async def swipe_loop(context, bot_id, chat_id, reply_to, loop_type, target, is_reply=False):
    key = f"{bot_id}_{chat_id}_{reply_to}_{loop_type}"
    texts = SWIPE_TEXTS.get(loop_type) if not is_reply else REPLY_TEXTS.get(loop_type)
    if not texts:
        return
    i = 0
    
    while key in active_tasks:
        try:
            text = await replace_target(texts[i % len(texts)], target)
            try:
                await context.bot.send_message(chat_id, text, reply_to_message_id=reply_to)
                i += 1
            except Exception as send_err:
                if "FloodWait" in str(send_err):
                    wait_match = re.search(r'retry after (\d+)', str(send_err))
                    wait_time = int(wait_match.group(1)) if wait_match else 1
                    await asyncio.sleep(wait_time)
                else:
                    i += 1
                    await asyncio.sleep(0.001)
        except asyncio.CancelledError:
            break
        except:
            i += 1
    
    # AUTO RESTART FUNCTIONALITY
    if AUTO_RESTART and key in active_tasks:
        print(f"🔄 Auto-Restarting {loop_type}...")
        await asyncio.sleep(RESTART_DELAY)
        if key in active_tasks:
            asyncio.create_task(swipe_loop(context, bot_id, chat_id, reply_to, loop_type, target, is_reply))

# ====================== GAME OVER (FIXED) ======================

async def gameover(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not is_sudo(user.id):
        await update.message.reply_text("𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐒ᴇ sᴜᴅᴏ ᴍᴀɴɢ ᴘᴇʜʟᴇ ᴛᴍᴋᴄ🌀🌀")
        return

    text = update.message.text or ""

    #!gameover <target>
    parts = text.split(" ", 1)
    target = parts[1].strip() if len(parts) > 1 else "Bhai"

    now = datetime.now()

    game_msg = f"""
==========================
  GAME OVER BY  𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡  🌀 
==========================
{target} ᴛᴇʀɪ ᴄʜᴜᴅɪ ᴅ𝟿 ʙʏ sᴀʀᴡᴀɴ 
Date :- {now.strftime("%d %b %Y")}
Time :- {now.strftime("%H:%M:%S")}
Day :- {now.strftime("%A")}
==========================
ᴀʙ ɴᴏ ʙʜᴀᴡ ʀᴏᴛᴀ ʀᴇʜ ʀɴᴅɪᴄᴇ
==========================
""".strip()

    await update.message.reply_text(game_msg)

# ====================== PIN COMMANDS ======================
async def pin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pin the replied message"""
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐒ᴇ sᴜᴅᴏ ᴍᴀɴɢ ᴘᴇʜʟᴇ ᴛᴍᴋᴄ🌀🌀")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply to a message to pin it!\nExample: Reply to a message and type !pin")
        return
    
    try:
        await update.message.reply_to_message.pin()
        await update.message.reply_text("📌 Message pinned successfully!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}\nMake sure bot has admin rights!")

async def unpin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unpin the replied message"""
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐒ᴇ sᴜᴅᴏ ᴍᴀɴɢ ᴘᴇʜʟᴇ ᴛᴍᴋᴄ 🌀🌀")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply to a message to unpin it!\nExample: Reply to a message and type !unpin")
        return
    
    try:
        await update.message.reply_to_message.unpin()
        await update.message.reply_text("📌 Message unpinned successfully!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}\nMake sure bot has admin rights!")

async def unpin_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove all pinned messages"""
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐒ᴇ sᴜᴅᴏ ᴍᴀɴɢ ᴘᴇʜʟᴇ ᴛᴍᴋᴄ 🌀🌀")
        return
    
    chat = update.effective_chat
    
    try:
        await chat.unpin_all_messages()
        await update.message.reply_text("📌 All pinned messages removed!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}\nMake sure bot has admin rights!")

# ====================== MUTE/UNMUTE COMMANDS ======================
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐒ᴇ sᴜᴅᴏ ᴍᴀɴɢ ᴘᴇʜʟᴇ ᴛᴍᴋᴄ 🌀🌀")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to user message.")
        return

    chat_id = update.effective_chat.id
    user_id = update.message.reply_to_message.from_user.id

    try:
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            )
        )
        await update.message.reply_text("✅ MUTED")

    except Exception as e:
        await update.message.reply_text(f"❌ {e}")


# ---------------- UNMUTE ----------------
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐒ᴇ sᴜᴅᴏ ᴍᴀɴɢ ᴘᴇʜʟᴇ ᴛᴍᴋᴄ 🌀🌀")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to user message.")
        return

    chat_id = update.effective_chat.id
    user_id = update.message.reply_to_message.from_user.id

    try:
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False
            )
        )
        await update.message.reply_text("✅ UNMUTED")

    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def gcmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("No access")
        return

    chat_id = update.effective_chat.id

    perms = ChatPermissions(
        can_send_messages=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False
    )

    await context.bot.set_chat_permissions(
        chat_id=chat_id,
        permissions=perms
    )

    await update.message.reply_text("🔇 GC MUTED")


# ---------------- GROUP UNMUTE ----------------
async def gcunmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("No access")
        return

    chat_id = update.effective_chat.id

    perms = ChatPermissions(
        can_send_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_change_info=False,
        can_invite_users=True,
        can_pin_messages=False
    )

    await context.bot.set_chat_permissions(
        chat_id=chat_id,
        permissions=perms
    )

    await update.message.reply_text("🔊 GC UNMUTED")

# ====================== OTHER COMMANDS ======================
async def stopall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐒ᴇ sᴜᴅᴏ ᴍᴀɴɢ ᴘᴇʜʟᴇ ᴛᴍᴋᴄ 🌀🌀")
        return
    chat_id = update.effective_chat.id
    removed = 0
    for key in list(active_tasks.keys()):
        if str(chat_id) in key:
            task = active_tasks.pop(key, None)
            if task and not task.done():
                task.cancel()
                removed += 1
    await update.message.reply_text(f"✅ All Tasks Stopped! ({removed} loops)")

async def add_sudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("Only Owner can give sudo!")

    # Reply se user
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id

    # Argument se user ID
    elif context.args:
        try:
            user_id = int(context.args[0])
        except ValueError:
            return await update.message.reply_text("❌ Invalid ID!")

    else:
        return await update.message.reply_text(
            "Usage:\n"
            "• !sudo <user_id>\n"
            "• Reply to a user's message with !sudo"
        )

    if user_id in sudo_users:
        return await update.message.reply_text("Already sudo!")

    sudo_users.add(user_id)

    if user_id not in sudo_list:
        sudo_list.append(user_id)

    await update.message.reply_text(f"✅ Sudo added: `{user_id}`", parse_mode="Markdown")

async def remove_sudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id

    elif context.args:
        try:
            user_id = int(context.args[0])
        except ValueError:
            return await update.message.reply_text("❌ Invalid ID!")

    else:
        return await update.message.reply_text(
            "Usage:\n"
            "• !dsudo <user_id>\n"
            "• Reply to a sudo user's message with !dsudo"
        )

    sudo_users.discard(user_id)

    if user_id in sudo_list:
        sudo_list.remove(user_id)

    await update.message.reply_text(f"❌ Sudo removed: `{user_id}`", parse_mode="Markdown")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await ban_unban(update, context, True)

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await ban_unban(update, context, False)

async def ban_unban(update: Update, context: ContextTypes.DEFAULT_TYPE, ban_action: bool = True):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐒ᴇ sᴜᴅᴏ ᴍᴀɴɢ ᴘᴇʜʟᴇ ᴛᴍᴋᴄ 🌀🌀")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a message!")
        return
    user = update.message.reply_to_message.from_user
    chat = update.effective_chat
    try:
        if ban_action:
            await chat.ban_member(user.id)
            await update.message.reply_text(f"✅ {user.first_name} BANNED!")
        else:
            await chat.unban_member(user.id)
            await update.message.reply_text(f"✅ {user.first_name} UNBANNED!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def delmsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐒ᴇ sᴜᴅᴏ ᴍᴀɴɢ ᴘᴇʜʟᴇ ᴛᴍᴋᴄ 🌀🌀")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a message!")
        return
    try:
        await update.message.reply_to_message.delete()
        await update.message.reply_text("✅ Message deleted!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def sudolist_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        return
    if sudo_users:
        await update.message.reply_text(f"**Sudo List** ({len(sudo_users)})\n" + "\n".join(map(str, sudo_users)))
    else:
        await update.message.reply_text("No sudo users.")

async def adminlist_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        return
    try:
        admins = await update.effective_chat.get_administrators()
        admin_names = [f"{admin.user.first_name} (ID: {admin.user.id})" for admin in admins]
        await update.message.reply_text(f"**Admin List**\n" + "\n".join(admin_names))
    except Exception as e:
        await update.message.reply_text(f"Cannot fetch: {str(e)}")

async def banlist_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        return
    await update.message.reply_text("**Ban List** - Check manually.")

async def refreshsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        return
    global sudo_users, sudo_list
    sudo_users = {OWNER_ID}
    sudo_list = [OWNER_ID]
    await update.message.reply_text("✅ Sudo refreshed! Only Owner is sudo now.")

async def refresh_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        return
    global active_tasks, sudo_users, sudo_list, start_time
    for key, task in list(active_tasks.items()):
        if not task.done():
            task.cancel()
    active_tasks.clear()
    sudo_users = {OWNER_ID}
    sudo_list = [OWNER_ID]
    start_time = time.time()
    await update.message.reply_text("✅ Bot refreshed! All tasks stopped.")

async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nc = sum(1 for k in active_tasks if "nc_" in k)
    spam = sum(1 for k in active_tasks if "spam_" in k)
    swipe = sum(1 for k in active_tasks if "swipe_" in k)
    reply = sum(1 for k in active_tasks if any(x in k for x in ['rreply', 'breply', 'creply']))
    
    await update.message.reply_text(
        f"**📊 BOT STATUS**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🔹 NC: {nc}\n"
        f"🔹 Spam: {spam}\n"
        f"🔹 Swipe: {swipe}\n"
        f"🔹 Reply: {reply}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📌 Total: {len(active_tasks)}"
    )

# ====================== MENU ======================
MENU_TEXT = """
𓆩🕷️𓆪━━━ 🥷 𝗬𝗨𝗧𝗔  𝐅ᴀsᴛ 𝐁ᴏᴛ ━━━𓆩🕷️𓆪
          𓆩💗𓆪 𝐔𝐋𝐓𝐑𝐀 𝐌𝐄𝐍𝐔 𓆩💗𓆪

╰┈➤ 𓆩🕷️𓆪 𝐍𝐂 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒
   ◈ ~snc       ⟿ 𝐒ᴛᴀʀᴛ
   ◈ ~ssnc      ⟿ 𝐒𝐒𝐍𝐂
   ◈ ~fnc       ⟿ 𝐅ᴀsᴛ
   ◈ ~cnc       ⟿ 𝐂ᴏᴏʟ
   ◈ ~bnc       ⟿ 𝐁ᴜɪʟᴛ
   ◈ ~sgcnc     ⟿ 𝐒ᴘᴇᴄɪᴀʟ
   ◈ ~dnc       ⟿ 𝐃ᴇʟᴇᴛᴇ
   ◈ ~dallnc    ⟿ 𝐂ʟᴇᴀʀ 𝐀ʟʟ

╰┈➤ 𓆩💗𓆪 𝐒𝐏𝐀𝐌 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒
   ◈ ~bspam     ⟿ 𝐁ᴏʟᴅ
   ◈ ~aspam     ⟿ 𝐀ʀᴛɪsᴛɪᴄ
   ◈ ~sspam     ⟿ 𝐒ᴛʀᴏɴɢ
   ◈ ~fspam     ⟿ 𝐅ᴀsᴛ
   ◈ ~gspam     ⟿ 𝐆ʟᴏᴡ
   ◈ ~rspam     ⟿ 𝐑ɪᴄʜ
   ◈ ~dbspam    ⟿ 𝐃ᴇʟᴇᴛᴇ
   ◈ ~dallspam  ⟿ 𝐂ʟᴇᴀʀ 𝐀ʟʟ

╰┈➤𓆩🔥𓆪 𝐒𝐋𝐈𝐃𝐄 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒
   ◈ ~aswipe     ⟿ 𝐀 sᴡɪᴘᴇ
   ◈ ~fswipe     ⟿ 𝐅ᴀsᴛ
   ◈ ~rrswipe    ⟿ 𝐑ᴀɪᴅ
   ◈ ~cswipe     ⟿ 𝐂ᴏᴏʟ
   ◈ ~daswipe    ⟿ 𝐃ᴇʟᴇᴛᴇ
   ◈ ~dallswipe  ⟿ 𝐂ʟᴇᴀʀ 𝐀ʟʟ

╰┈➤ 𓆩💬𓆪 𝐑𝐄𝐏𝐋𝐘 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒
   ◈ ~rreply      ⟿ 𝐑ɪᴄʜ
   ◈ ~breply      ⟿ 𝐁ɪɢ
   ◈ ~creply      ⟿ 𝐂ᴏᴏʟ
   ◈ ~drreply     ⟿ 𝐒ᴛᴏᴘ
   ◈ ~dallreply   ⟿ 𝐂ʟᴇᴀʀ 𝐀ʟʟ

╰┈➤ 𓆩👑𓆪 𝐀𝐃𝐌𝐈𝐍 𝐏𝐎𝐖𝐄𝐑
   ◈ ~sudo        ⟿ 𝐀ᴅᴅ
   ◈ ~dsudo       ⟿ 𝐑ᴇᴍᴏᴠᴇ
   ◈ ~sudolist    ⟿ 𝐋ɪsᴛ
   ◈ ~refreshsudo ⟿ 𝐑ᴇғʀᴇsʜ
   ◈ ~ban         ⟿ 𝐁ᴀɴ
   ◈ ~unban       ⟿ 𝐔ɴʙᴀɴ
   ◈ ~adminlist   ⟿ 𝐀ᴅᴍɪɴ 𝐋ɪsᴛ
   ◈ ~banlist     ⟿ 𝐁ᴀɴ 𝐋ɪsᴛ

╰┈➤ 𓆩🛡️𓆪 𝐌𝐔𝐓𝐄 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒
   ◈ ~mute      ⟿ 𝐌ᴜᴛᴇ
   ◈ ~unmute    ⟿ 𝐔ɴᴍᴜᴛᴇ
   ◈ ~gcmute    ⟿ 𝐆ʀᴏᴜᴘ 𝐌ᴜᴛᴇ
   ◈ ~gcunmute  ⟿ 𝐆ʀᴏᴜᴘ 𝐔ɴᴍᴜᴛᴇ
   ◈ ~delmsg    ⟿ 𝐃ᴇʟᴇᴛᴇ

╰┈➤ 𓆩📡𓆪 𝐒𝐓𝐀𝐓𝐔𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒
   ◈ ~status    ⟿ 𝐒ᴛᴀᴛᴜs
   ◈ ~ping      ⟿ 𝐏ɪɴɢ
   ◈ ~uptime    ⟿ 𝐔ᴘᴛɪᴍᴇ
   ◈ ~refresh   ⟿ 𝐑ᴇғʀᴇsʜ
   ◈ ~pin       ⟿ 𝐏ɪɴ
   ◈ ~unpin     ⟿ 𝐔ɴᴘɪɴ
   ◈ ~revpin    ⟿ 𝐑ᴇᴍᴏᴠᴇ 𝐏ɪɴ

╰┈➤ 𓆩🌐𓆪 𝐆𝐑𝐎𝐔𝐏 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒
   ◈ ~groups    ⟿ 𝐀ʟʟ 𝐆ʀᴏᴜᴘs
   ◈ ~statusg   ⟿ 𝐆ʀᴏᴜᴘ 𝐒ᴛᴀᴛᴜs
   ◈ ~overg     ⟿ 𝐎ᴠᴇʀᴠɪᴇᴡ
   ◈ ~leaveg    ⟿ 𝐋ᴇᴀᴠᴇ

𓆩💗𓆪━━━━━━━━━━━━━━━━ 𓆩💗𓆪
        🥷 𝗬𝗨𝗧𝗔  𝐏ᴏᴡᴇʀ 𝐁ᴏᴛ
𓆩💗𓆪━━━━━━━━━━━━━━━━ 𓆩💗𓆪
"""

# ====================== PHOTO COMMAND FUNCTIONS ======================
async def savephoto_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save photos from the group"""
    msg = update.message
    chat_id = msg.chat_id
    
    # Check if replying to a message with photo
    if msg.reply_to_message and msg.reply_to_message.photo:
        if chat_id not in SAVED_PHOTOS:
            SAVED_PHOTOS[chat_id] = []
        
        photo = msg.reply_to_message.photo[-1]  # Get highest quality
        file_id = photo.file_id
        
        SAVED_PHOTOS[chat_id].append(file_id)
        await msg.reply_text(f"✅ Photo Saved! Total: {len(SAVED_PHOTOS[chat_id])} photos\n📸 Use ~startphoto to start changing DP!")
    else:
        await msg.reply_text("❌ Reply to a photo with ~savephoto to save it!")

async def startphoto_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start changing group DP with saved photos in loop"""
    msg = update.message
    chat_id = msg.chat_id
    
    if chat_id not in SAVED_PHOTOS or not SAVED_PHOTOS[chat_id]:
        return await msg.reply_text("❌ No photos saved! Use ~savephoto first!")
    
    # Check if already running
    task_key = f"{chat_id}_photo"
    if task_key in ACTIVE_PHOTO_LOOPS:
        return await msg.reply_text("⚠️ Photo loop already running! Use ~stopphoto to stop!")
    
    async def photo_loop():
        idx = 0
        while task_key in ACTIVE_PHOTO_LOOPS:
            try:
                photo_list = SAVED_PHOTOS.get(chat_id, [])
                if not photo_list:
                    await asyncio.sleep(0.1)
                    continue
                
                file_id = photo_list[idx % len(photo_list)]
                try:
                    # Get file from file_id
                    file = await context.bot.get_file(file_id)
                    # Download the file
                    photo_file = await file.download_to_memory()
                    # Set as chat photo
                    await context.bot.set_chat_photo(chat_id=chat_id, photo=photo_file)
                    idx += 1
                    await asyncio.sleep(0.5)  # Small delay between changes
                except Exception as photo_err:
                    if "FloodWait" in str(photo_err):
                        wait_match = re.search(r'retry after (\d+)', str(photo_err))
                        wait_time = int(wait_match.group(1)) if wait_match else 5
                        await asyncio.sleep(wait_time)
                    else:
                        idx += 1
                        await asyncio.sleep(1)
            except asyncio.CancelledError:
                break
            except:
                idx += 1
                await asyncio.sleep(1)
    
    task = asyncio.create_task(photo_loop())
    ACTIVE_PHOTO_LOOPS[task_key] = task
    await msg.reply_text(f"🔄 Started changing DP! Full speed mode! 🚀\n📸 {len(SAVED_PHOTOS[chat_id])} photos rotating!")

async def stopphoto_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stop the photo DP changing loop"""
    msg = update.message
    chat_id = msg.chat_id
    
    task_key = f"{chat_id}_photo"
    if task_key not in ACTIVE_PHOTO_LOOPS:
        return await msg.reply_text("❌ No photo loop running!")
    
    task = ACTIVE_PHOTO_LOOPS.pop(task_key, None)
    if task and not task.done():
        task.cancel()
        await msg.reply_text("⛔ Photo loop stopped!")
    else:
        await msg.reply_text("❌ Could not stop loop!")

async def dphoto_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete saved photos and show menu"""
    msg = update.message
    chat_id = msg.chat_id
    
    # Stop if running
    task_key = f"{chat_id}_photo"
    if task_key in ACTIVE_PHOTO_LOOPS:
        task = ACTIVE_PHOTO_LOOPS.pop(task_key)
        if task and not task.done():
            task.cancel()
    
    # Delete saved photos
    if chat_id in SAVED_PHOTOS:
        count = len(SAVED_PHOTOS[chat_id])
        del SAVED_PHOTOS[chat_id]
    else:
        count = 0
    
    # Show menu
    menu_text = f"""🎬 PHOTO MANAGER MENU 📸

━━━━━━━━━━━━━━━━━━━━
✅ Deleted {count} photos!

📋 Commands:
• ~savephoto - Save photo (reply to it)
• ~startphoto - Start DP changes 🚀
• ~stopphoto - Stop the loop ⛔
• ~dphoto - Delete all & show menu
━━━━━━━━━━━━━━━━━━━━

✨ All photos deleted! Photo loop stopped!"""
    
    await msg.reply_text(menu_text)

# ====================== GROUP MANAGEMENT COMMANDS ======================
async def groups_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all groups where bot is active"""
    msg = update.message
    
    if not ACTIVE_GROUPS:
        return await msg.reply_text("❌ Bot kisi bhi group mein active nahi hai!")
    
    text = f"📊 BOT ACTIVE GROUPS: {len(ACTIVE_GROUPS)}\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for i, group_id in enumerate(ACTIVE_GROUPS, 1):
        group_name = GROUP_TRACKER.get(group_id, f"Group {group_id}")
        text += f"{i}. {group_name}\n"
    
    text += "\n━━━━━━━━━━━━━━━━━━━━━━━━"
    await msg.reply_text(text)

async def statusg_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show status of all commands in each group"""
    msg = update.message
    
    if not active_tasks:
        return await msg.reply_text("❌ Koi bhi command chal nahi rahi!")
    
    text = "📈 GROUP-WISE COMMAND STATUS:\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    group_commands = defaultdict(list)
    
    # Organize tasks by group
    for task_key in active_tasks:
        parts = task_key.rsplit('_', 1)
        if len(parts) == 2:
            group_id = int(parts[1])
            cmd_type = parts[0]
            
            if group_id in GROUP_TRACKER:
                start_time = TASK_START_TIMES.get(task_key, time.time())
                elapsed = int(time.time() - start_time)
                mins = elapsed // 60
                secs = elapsed % 60
                
                group_commands[group_id].append(f"  • {cmd_type.upper()} ({mins}m {secs}s)")
    
    if not group_commands:
        return await msg.reply_text("❌ Koi active command nahi!")
    
    for group_id in sorted(group_commands.keys()):
        group_name = GROUP_TRACKER.get(group_id, f"Group {group_id}")
        text += f"🔹 {group_name}\n"
        for cmd in group_commands[group_id]:
            text += cmd + "\n"
        text += "\n"
    
    text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    await msg.reply_text(text)

async def overg_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stop all commands in a specific group"""
    msg = update.message
    args = msg.text.split()[1:]
    
    if not args:
        return await msg.reply_text("❌ Group name likho! Format: !overg <group_name>")
    
    group_name = ' '.join(args)
    
    # Find group by name
    target_group_id = None
    for gid, gname in GROUP_TRACKER.items():
        if group_name.lower() in gname.lower():
            target_group_id = gid
            break
    
    if not target_group_id:
        return await msg.reply_text(f"❌ Group '{group_name}' nahi mila!")
    
    # Stop all tasks in this group
    removed = 0
    for task_key in list(active_tasks.keys()):
        if str(target_group_id) in task_key:
            task = active_tasks.pop(task_key, None)
            if task and not task.done():
                task.cancel()
                removed += 1
    
    # Send "over" message to that group
    try:
        await context.bot.send_message(
            chat_id=target_group_id,
            text="⚠️ OVER ⚠️\n\nSab commands stop ho gaye!"
        )
    except:
        pass
    
    await msg.reply_text(f"✅ Group '{GROUP_TRACKER.get(target_group_id)}' ka {removed} command stop!")

async def leaveg_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot leaves a specific group"""
    msg = update.message
    args = msg.text.split()[1:]
    
    if not args:
        return await msg.reply_text("❌ Group name likho! Format: !leaveg <group_name>")
    
    group_name = ' '.join(args)
    
    # Find group by name
    target_group_id = None
    for gid, gname in GROUP_TRACKER.items():
        if group_name.lower() in gname.lower():
            target_group_id = gid
            break
    
    if not target_group_id:
        return await msg.reply_text(f"❌ Group '{group_name}' nahi mila!")
    
    # Stop all tasks in this group
    for task_key in list(active_tasks.keys()):
        if str(target_group_id) in task_key:
            task = active_tasks.pop(task_key, None)
            if task and not task.done():
                task.cancel()
    
    # Send goodbye message
    try:
        await context.bot.send_message(
            chat_id=target_group_id,
            text="👋 Bye bye! Bot leave ho raha hai!"
        )
    except:
        pass
    
    # Leave the group
    try:
        await context.bot.leave_chat(chat_id=target_group_id)
        ACTIVE_GROUPS.discard(target_group_id)
        if target_group_id in GROUP_TRACKER:
            del GROUP_TRACKER[target_group_id]
        await msg.reply_text(f"✅ Bot '{group_name}' se leave ho gaya!")
    except Exception as e:
        await msg.reply_text(f"❌ Error: {e}")

# ====================== MAIN HANDLER ======================
async def make_handler(bot_id: str):
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.text:
            return
        
        text = update.message.text
        if not text.startswith('~'):
            return

        msg = update.message
        cmd_parts = text.lower().strip().split()
        cmd = cmd_parts[0][1:] if cmd_parts else ""
        args = cmd_parts[1:] if len(cmd_parts) > 1 else []

        # PUBLIC COMMANDS
        if cmd == "menu":
            return await msg.reply_text(MENU_TEXT)
        
        if cmd == "whoami":
            user_id = update.effective_user.id
            is_owner = "✅ YES! Tu OWNER hai!" if user_id == OWNER_ID else f"❌ Nahi. Owner ID: {OWNER_ID}, Tera ID: {user_id}"
            return await msg.reply_text(f"🔍 **Your ID:** {user_id}\n{is_owner}")
        
        if cmd == "ping":
            start = time.time()
            await msg.reply_text("🏓 Pong!")
            end = time.time()
            await msg.reply_text(f"⚡ Response: {round((end-start)*1000)}ms")
            return
        
        if cmd == "uptime":
            up = int(time.time() - start_time)
            hours = up // 3600
            minutes = (up % 3600) // 60
            seconds = up % 60
            await msg.reply_text(f"⏱️ Uptime: {hours}h {minutes}m {seconds}s")
            return

        # SUDO ONLY COMMANDS
        if not is_sudo(update.effective_user.id):
            return await msg.reply_text("𝐎𝐘𝐄 𐙚⋆🥷 𝗬𝗨𝗧𝗔  𝐏ᴀ𝐏𝐀~♡ 𝐒ᴇ sᴜᴅᴏ ᴍᴀɴɢ ᴘᴇʜʟᴇ ᴛᴍᴋᴄ 🌀🌀")

        chat_id = msg.chat.id

        # GAME OVER
        if cmd == "gameover":
            return await gameover(update, context)
        
        if cmd == "stopall":
            return await stopall(update, context)
        
        # PIN COMMANDS
        if cmd == "pin":
            return await pin_message(update, context)
        
        if cmd == "unpin":
            return await unpin_message(update, context)
        
        if cmd == "revpin":
            return await unpin_all_messages(update, context)

        # START COMMANDS
        if cmd in NC_TEXTS or cmd in SPAM_TEXTS or cmd in SWIPE_TEXTS or cmd in REPLY_TEXTS:
            target = " ".join(args) if args else msg.from_user.first_name
            is_swipe = cmd in SWIPE_TEXTS
            is_reply = cmd in REPLY_TEXTS
            
            if is_swipe or is_reply:
                if not msg.reply_to_message:
                    return await msg.reply_text("Reply to a message!")
                reply_to = msg.reply_to_message.message_id
                target_name = msg.reply_to_message.from_user.first_name if msg.reply_to_message.from_user else target
                key = f"{bot_id}_{chat_id}_{reply_to}_{cmd}"
                if key in active_tasks:
                    return await msg.reply_text("⚠️ Already Running!")
                task = asyncio.create_task(swipe_loop(context, bot_id, chat_id, reply_to, cmd, target_name, is_reply))
            elif cmd in SPAM_TEXTS:
                key = f"{bot_id}_{chat_id}_{cmd}"
                if key in active_tasks:
                    return await msg.reply_text("⚠️ Already Running!")
                task = asyncio.create_task(spam_loop(context, bot_id, chat_id, cmd, target))
            else:
                key = f"{bot_id}_{chat_id}_{cmd}"
                if key in active_tasks:
                    return await msg.reply_text("⚠️ Already Running!")
                task = asyncio.create_task(nc_loop(context, bot_id, chat_id, cmd, target))
            
            active_tasks[key] = task
            
            # Track group and task start time
            ACTIVE_GROUPS.add(chat_id)
            if chat_id not in GROUP_TRACKER:
                group_name = msg.chat.title or f"Group_{chat_id}"
                GROUP_TRACKER[chat_id] = group_name
            TASK_START_TIMES[key] = time.time()
            
            await msg.reply_text(f"✅ {cmd.upper()} Started!")

        # STOP COMMANDS
        elif cmd.startswith('d'):
            removed = 0
            base_cmd = cmd.replace('d', '', 1)
            
            if cmd in ['dallnc', 'dallspam', 'dallswipe', 'dallreply']:
                category = cmd.replace('dall', '')
                for key in list(active_tasks.keys()):
                    if category in key and str(chat_id) in key:
                        task = active_tasks.pop(key, None)
                        TASK_START_TIMES.pop(key, None)
                        if task and not task.done():
                            task.cancel()
                            removed += 1
            else:
                for key in list(active_tasks.keys()):
                    if key.endswith(f"_{base_cmd}") and str(chat_id) in key:
                        task = active_tasks.pop(key, None)
                        TASK_START_TIMES.pop(key, None)
                        if task and not task.done():
                            task.cancel()
                            removed += 1
            
            await msg.reply_text(f"✅ Stopped {removed} loop(s)!")

        # DELAY SET
        elif cmd.startswith("setdelay"):
            try:
                if not args:
                    return await msg.reply_text("Usage: ~setdelaync 0.001")
                sec = float(args[0])
                if sec < 0:
                    sec = 1
                dtype = cmd.replace("setdelay", "")
                if dtype in DELAYS:
                    DELAYS[dtype] = sec
                    await msg.reply_text(f"✅ {dtype.upper()} Delay = {sec}s")
                else:
                    await msg.reply_text(f"❌ Invalid! Use: nc, spam, swipe, reply")
            except:
                await msg.reply_text("❌ Invalid number!")

        # SUDO MANAGEMENT
        elif cmd == "sudo":
            await add_sudo(update, context)
        elif cmd == "dsudo":
            await remove_sudo(update, context)
        elif cmd == "sudolist":
            await sudolist_cmd(update, context)
        elif cmd == "refreshsudo":
            await refreshsudo(update, context)

        # BAN/UNBAN
        elif cmd == "ban":
            await ban(update, context)
        elif cmd == "unban":
            await unban(update, context)

        # MUTE/UNMUTE
        elif cmd == "mute":
            await mute(update, context)
        elif cmd == "unmute":
            await unmute(update, context)
        elif cmd == "gcmute":
            await gcmute(update, context)
        elif cmd == "gcunmute":
            await gcunmute(update, context)

        # MESSAGE MANAGEMENT
        elif cmd == "delmsg":
            await delmsg(update, context)

        # LISTS
        elif cmd == "adminlist":
            await adminlist_cmd(update, context)
        elif cmd == "banlist":
            await banlist_cmd(update, context)

        # TOOLS
        elif cmd == "status":
            await status_cmd(update, context)
        elif cmd == "refresh":
            await refresh_cmd(update, context)
        
        # PHOTO COMMANDS 📸
        elif cmd == "savephoto":
            await savephoto_cmd(update, context)
        elif cmd == "startphoto":
            await startphoto_cmd(update, context)
        elif cmd == "stopphoto":
            await stopphoto_cmd(update, context)
        elif cmd == "dphoto":
            await dphoto_cmd(update, context)
        
        # GROUP MANAGEMENT COMMANDS
        elif cmd == "groups":
            await groups_cmd(update, context)
        elif cmd == "statusg":
            await statusg_cmd(update, context)
        elif cmd == "overg":
            await overg_cmd(update, context)
        elif cmd == "leaveg":
            await leaveg_cmd(update, context)

    return handler

# ====================== RUN MULTI BOT ======================
async def run_multibot():
    applications = []
    
    for i, token in enumerate(BOT_TOKENS):
        if not token or "YOUR_BOT_TOKEN" in token:
            continue
        
        try:
            app = Application.builder().token(token).build()
            handler = await make_handler(str(i))
            app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & filters.Regex(r'^~'), handler))
            
            await app.initialize()
            await app.start()
            await app.updater.start_polling()
            
            applications.append(app)
            print(f"🚀 Bot {i+1} Started - {token[-8:]}")
            
        except Exception as e:
            print(f"❌ Bot {i+1} failed: {e}")

    if applications:
        print("\n✅ Bot is running! Press Ctrl+C to stop.\n")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Stopping...")
            for app in applications:
                await app.updater.stop()
                await app.stop()
                await app.shutdown()
            print("✅ Stopped!")
    else:
        print("❌ No bots started!")

if __name__ == '__main__':
    print("🔥 🥷 𝗬𝗨𝗧𝗔  ULTRA FAST BOT 🔥")
    print("⚡ SPEED: 0.1ms - MACHINE GUN MODE!")
    print("🚀 AUTO RESTART: ENABLED")
    print("💨 INSANE VELOCITY - FASTER THAN LIGHT!")
    print("="*50)
    
    try:
        asyncio.run(run_multibot())
    except KeyboardInterrupt:
        print("\n👋 Stopped!")
    except Exception as e:
        print(f"❌ Error: {e}")