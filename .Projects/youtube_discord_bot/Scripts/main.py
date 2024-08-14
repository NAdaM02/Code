import discord
from discord.ext import commands
from googleapiclient.discovery import build
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

# Set up the YouTube Data API service
API_KEY = 'AIzaSyDY47Va_h3sUqnBb851fmc4iEBc6144iZ8'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='y!', intents=intents)

@bot.command()
async def search(ctx, *search_query):
    search_query = ' '.join(search_query)

    result_count = 5

    if '-' in search_query:
        search_query, result_count = search_query.split('-')
        search_query = search_query[:-1]
    
    request = youtube.search().list(
        part='snippet',
        q=search_query,
        type='video',
        maxResults=result_count  # Number of results to retrieve
    )
    response = request.execute()

    videos = []
    for item in response['items']:
        video_title = item['snippet']['title']
        video_id = item['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        videos.append(f'{video_title}: {video_url}')

    await ctx.send('\n'.join(videos))


@bot.command()
async def play(ctx, *search_query):
    search_query = ' '.join(search_query)

    result_count = 1

    if '#' in search_query:
        search_query, result_count = search_query.split('#')
        search_query = search_query[:-1]

    request = youtube.search().list(
        part='snippet',
        q=search_query,
        type='video',
        maxResults=result_count
    )
    response = request.execute()

    video_id = response['items'][result_count-1]['id']['videoId']
    video_url = f'https://www.youtube.com/watch?v={video_id}'

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'noplaylist': True,
        'verbose': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        audio_url = info_dict['formats'][result_count-1]['url']

    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    voice_client.play(FFmpegPCMAudio(audio_url))

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client:
        await voice_client.disconnect()
    else:
        await ctx.send("I'm not connected to a voice channel.")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run the bot
bot.run('MTI3MTEzMzU3NTczMDk1NDM1MQ.G7XTj1.TseZpQTbcUJPdp8-Q9-qkN5SFFtkFIyrXBWotQ')