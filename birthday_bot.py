import discord
import asyncio
import datetime
import pytz
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = "MTMzNTQ1OTEwMzkxNjY4NzQ2MA.GwfAbl.LN2EqYwPDANy8cXQ8EszTQbjYyvptpExieG-CQ"
GUILD_ID = 1271205831685177385  # ID server Discord
CHANNEL_ID = 1272686221977456781  # ID channel untuk kirim pesan ulang tahun

# Data ulang tahun (Format: {'UserID': 'MM-DD'})
birthday_data = {
    480574654927601675: "02-02",  #Reou
    291878279781285888: "11-22",  #Panda dan Batu
    1072542796591943774: "09-04", #Deri
    416187604644659200: "06-29", #Geralodon
    267929521657741322: "05-17", #mas mei
    310456410863435776: "01-30", #Ka je
    724508393531899946: "09-02", #lyu
    329593201323147264: "04-22", #andre
    1176399002292453470: "09-18", #mas ijun
    903258255357255680: "09-08", #Achi
    414668432420634627: "08-16", #papahh
    1105860816047190066: "07-01", #ka hikar
    483599107689152512: "", #ple
    1016167721743962203: "12-06", #tante
    712782452866678827: "", #ruu
    401007640853086211: "", #renn
    1209656640597655695: "", #thalas
    704884655710797824: "", #mbiqs
    838459680908640320: "", #TJ
    421922511018786827: "", #hela
    659765472258162709: "", #izi
    924716078725226517: "", #rann
    536447679711150090: "", #ric
    276344072057257984: "", #eruu
    385649895002079241: "", #valivid
    1089810781350150165: "", #opang
    756853440541622313: "", #latte
    904251554545143848: "" #bang sui
}

intents = discord.Intents.default()
intents.members = True  # Pastikan ini diaktifkan di Discord Developer Portal

bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler()

def check_birthdays():
    """Cek ulang tahun dan kembalikan list user ID yang berulang tahun hari ini."""
    today = datetime.datetime.now(pytz.timezone("Asia/Jakarta")).strftime("%m-%d")
    print(f"🔍 Tanggal hari ini: {today}")  # Debugging, cek tanggal hari ini
    
    birthday_users = []
    for user_id, birth_date in birthday_data.items():
        print(f"🎉 Mengecek ulang tahun untuk {user_id}: {birth_date}")  # Debugging ulang tahun yang tersimpan
        if birth_date == today:
            print(f"🎉 Ulang tahun ditemukan: {user_id}")  # Debugging, melihat user yang cocok
            birthday_users.append(user_id)
    
    if not birthday_users:
        print("❌ Tidak ada ulang tahun hari ini.")  # Debugging jika tidak ada ulang tahun
    return birthday_users

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} sudah online!")
    # Debugging scheduler
    scheduler.add_job(send_birthday_message, "cron", hour=00, minute=00, timezone="Asia/Jakarta")
    print("⏰ Scheduler dimulai untuk pukul 00.00 WIB.")
    scheduler.start()

    # Cek apakah channel ada
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        print(f"🛠 Channel ditemukan: {channel.name}")
    else:
        print(f"❌ Channel dengan ID {CHANNEL_ID} tidak ditemukan!")

async def send_birthday_message():
    """Kirim pesan ke channel jika ada yang ulang tahun."""
    guild = bot.get_guild(GUILD_ID)
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("❌ Channel tidak ditemukan!")  # Debugging jika channel tidak ditemukan
        return
    
    birthday_users = check_birthdays()
    if birthday_users:
        # Buat list mention untuk semua user yang berulang tahun
        mentions = [guild.get_member(user_id).mention for user_id in birthday_users if guild.get_member(user_id)]
        if not mentions:
            print("⚠ Tidak ada user yang ditemukan di server.")
            return
        
        # Gabungkan semua mention dengan koma
        mentions_str = ", ".join(mentions)
        
        # Kalimat announcement yang sudah dibuat
        msg = (
            f"🎉 **Hari Spesial!** 🎉\n"
            f"Hari ini adalah hari ulang tahun **{mentions_str}**! 🎂\n"
            f"Mari kita semua berikan ucapan selamat dan doa terbaik! 🎊\n"
            f"@everyone, jangan lupa kirimkan pesan manis ya! 🎈"
        )
        await channel.send(msg)
    else:
        print("❌ Tidak ada ulang tahun hari ini.")

@bot.command()
async def add_birthday(ctx, member: discord.Member, date: str):
    """Tambahkan ulang tahun member dengan format MM-DD."""
    try:
        datetime.datetime.strptime(date, "%m-%d")  # Validasi format tanggal (hanya bulan & tanggal)
        birthday_data[member.id] = date
        await ctx.send(f"✅ Ulang tahun {member.mention} telah ditambahkan pada {date}.")
    except ValueError:
        await ctx.send("❌ Format tanggal salah! Gunakan format: `MM-DD` (contoh: `02-15`).")

bot.run(TOKEN)