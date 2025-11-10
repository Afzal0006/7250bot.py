from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import time

# === CONFIG ===
API_ID = 24526311
API_HASH = "717d5df262e474f88d86c537a787c98d"
STRING_SESSION = "BQF2PecANAmsjfKJkBv-PwZxQvinq0a7lcJ-6KCdyu13xnl8jeDV7YR9gk20ifB2M_7H2XqqUQMH0OAab9SXzfFqepsXHARqnp8JN7Iplo_5Odzwe6n5NBCFOyVP4Y3FGSdEQ4Y8UTM3VmCxTk8Jur_h9lCIKgxtLapFiiaYwgLwKWfP6W3XfsOs33FhjTEpHI8AOmZtqO4f5aAf3_2Mi032AHXKBDuzRqioX8RcG7JjYsjt-e8qnSudSpL20USBzR1FhGsYZjUx7W9_uPB7wjNH0P_6I3zJyynGPgdqIzkBi3sdZ2gRtgk7D-63t-jMbYuXIu5OfM6IZfCior4CVvRPu79nawAAAAHwVWW1AA"
ESCROW_BOT_USERNAME = "ris_bottetris_bottetris_bot"  # <-- apne escrow bot ka username (without @)
OWNER_ID = 7363327309  # <-- apna Telegram user id

# === START CLIENT ===
app = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

# === HANDLER ===
@app.on_message(filters.command("setup"))
async def create_group(client, message):
    # Sirf owner allow hoga
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("⛔ You are not authorized to use this command.")

    try:
        # Command ke baad naam hona chahiye
        if len(message.command) < 2:
            return await message.reply_text("⚠️ Usage: /setup GroupName")

        deal_name = " ".join(message.command[1:])  # /setup ke baad ka text
        chat_title = deal_name  # sirf wahi naam rakhenge

        # Step 1: Create private supergroup
        group = await client.create_supergroup(chat_title, "Private escrow group auto-created")

        # Step 2: Add Owner
        await client.add_chat_members(group.id, OWNER_ID)

        # Step 3: Add Escrow Bot
        await client.add_chat_members(group.id, ESCROW_BOT_USERNAME)

        # Step 4: Send default deal form
        form_message = f"""
**📑 DEAL INFO :**
👤 **BUYER :** (To be added)
👤 **SELLER :** (To be added)
💰 **DEAL AMOUNT :** (To be decided)
⏳ **TIME TO COMPLETE DEAL :** (To be decided)
"""
        sent_msg = await client.send_message(group.id, form_message)
        await client.pin_chat_message(group.id, sent_msg.id)

        # Step 5: Send Invite Link to Owner
        link = await client.export_chat_invite_link(group.id)
        await message.reply_text(f"✅ Group created successfully!\n**Name:** {chat_title}\n🔗 {link}")

    except FloodWait as e:
        time.sleep(e.value)
        await message.reply_text("⏳ Please try again later, Telegram rate limit reached.")

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

print("🚀 Userbot running...")
app.run()
