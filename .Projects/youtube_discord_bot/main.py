import os
import asyncio
import discord
from discord.ext import commands
from googleapiclient.discovery import build
from youtube_dl import YoutubeDL
from dotenv import load_dotenv
from collections import deque
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('music_bot')

# Load environment variables
load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

if not API_KEY or not DISCORD_TOKEN:
    raise ValueError("Missing API_KEY or DISCORD_TOKEN in .env file")

# YouTube API setup
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='y!', intents=intents)

# Youtube-dl configuration
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdl_format_options)

class Song:
    def __init__(self, url, title, duration, requester):
        self.url = url
        self.title = title
        self.duration = duration
        self.requester = requester

class MusicPlayer:
    def __init__(self, ctx):
        self.bot = ctx.bot
        self.guild = ctx.guild
        self.channel = ctx.channel
        self.queue = deque()
        self.current_song = None
        self.volume = 0.5
        self.paused = False
        self._volume_lock = asyncio.Lock()

    async def add_song(self, song):
        self.queue.append(song)
        if len(self.queue) == 1 and not self.current_song:
            await self.play_next()

    async def play_next(self):
        if not self.queue:
            self.current_song = None
            return

        try:
            self.current_song = self.queue.popleft()
            voice_client = self.guild.voice_client

            def get_url(url):
                info = ytdl.extract_info(url, download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                return info.get('url', None)

            audio_url = await asyncio.get_event_loop().run_in_executor(
                None, lambda: get_url(self.current_song.url)
            )

            if not audio_url:
                await self.channel.send("❌ Could not get audio URL")
                self.current_song = None
                await self.play_next()
                return

            if voice_client.is_playing():
                voice_client.stop()

            def after_playing(error):
                if error:
                    logger.error(f"Error playing audio: {error}")
                asyncio.run_coroutine_threadsafe(self.play_next(), bot.loop)

            voice_client.play(
                discord.FFmpegOpusAudio(audio_url, **ffmpeg_options),
                after=after_playing
            )

            await self.channel.send(f"🎵 Now playing: **{self.current_song.title}**")

        except Exception as e:
            logger.error(f"Error in play_next: {e}")
            await self.channel.send(f"❌ Error playing song: {str(e)}")
            self.current_song = None
            await self.play_next()

    async def set_volume(self, volume):
        async with self._volume_lock:
            self.volume = max(0.0, min(1.0, volume))
            if self.guild.voice_client and self.guild.voice_client.source:
                self.guild.voice_client.source.volume = self.volume

# Dictionary to store music players for each guild
players = {}

def get_player(ctx):
    if ctx.guild.id not in players:
        players[ctx.guild.id] = MusicPlayer(ctx)
    return players[ctx.guild.id]

@bot.command(name='search', help='Search for YouTube videos')
async def search(ctx, *, search_query):
    try:
        request = youtube.search().list(
            part='snippet',
            q=search_query,
            type='video',
            maxResults=5
        )
        response = request.execute()

        results = []
        for i, item in enumerate(response['items'], 1):
            video_title = item['snippet']['title']
            video_id = item['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            results.append(f'{i}. {video_title}: {video_url}')

        await ctx.send("🔎 Search results:\n" + "\n".join(results))
    except Exception as e:
        await ctx.send(f"❌ Error searching: {str(e)}")

@bot.command(name='play', help='Play a song from YouTube')
async def play(ctx, *, query):
    try:
        if not ctx.author.voice:
            return await ctx.send("❌ You must be in a voice channel to use this command!")

        # Connect to voice channel if not already connected
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()

        # Search for the video
        request = youtube.search().list(
            part='snippet',
            q=query,
            type='video',
            maxResults=1
        )
        response = request.execute()
        
        if not response['items']:
            return await ctx.send("❌ No results found!")

        video_id = response['items'][0]['id']['videoId']
        video_title = response['items'][0]['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={video_id}'

        # Create song object and add to queue
        song = Song(video_url, video_title, 0, ctx.author)
        player = get_player(ctx)
        await player.add_song(song)
        
        if len(player.queue) > 1:
            await ctx.send(f"➕ Added to queue: **{video_title}**")

    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name='queue', help='Show the current queue')
async def queue(ctx):
    player = get_player(ctx)
    if not player.current_song and not player.queue:
        return await ctx.send("📪 Queue is empty!")

    queue_list = []
    if player.current_song:
        queue_list.append(f"🎵 Now playing: **{player.current_song.title}**")
    
    for i, song in enumerate(player.queue, 1):
        queue_list.append(f"{i}. **{song.title}** (requested by {song.requester.name})")

    await ctx.send("\n".join(queue_list))

@bot.command(name='skip', help='Skip the current song')
async def skip(ctx):
    if ctx.voice_client and (ctx.voice_client.is_playing() or ctx.voice_client.is_paused()):
        ctx.voice_client.stop()
        await ctx.send("⏭️ Skipped")
    else:
        await ctx.send("❌ Nothing to skip!")

@bot.command(name='pause', help='Pause the current song')
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Paused")
    else:
        await ctx.send("❌ Nothing is playing!")

@bot.command(name='resume', help='Resume the current song')
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Resumed")
    else:
        await ctx.send("❌ Nothing is paused!")

@bot.command(name='stop', help='Stop playing and clear the queue')
async def stop(ctx):
    player = get_player(ctx)
    player.queue.clear()
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    await ctx.send("⏹️ Stopped playing and cleared the queue")

@bot.command(name='volume', help='Set the volume (0-100)')
async def volume(ctx, vol: int):
    if not 0 <= vol <= 100:
        return await ctx.send("❌ Volume must be between 0 and 100")
    
    player = get_player(ctx)
    await player.set_volume(vol / 100)
    await ctx.send(f"🔊 Volume set to {vol}%")

@bot.command(name='clear', help='Clear the queue')
async def clear(ctx):
    player = get_player(ctx)
    player.queue.clear()
    await ctx.send("🧹 Queue cleared")

@bot.command(name='disconnect', aliases=['leave'], help='Disconnect the bot from voice')
async def disconnect(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Disconnected from voice channel")
    else:
        await ctx.send("❌ Not connected to a voice channel")

# Run the bot
def main():
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

if __name__ == "__main__":
    main()