import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import urllib
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import youtube_dl
from selenium.webdriver.firefox.options import Options as FirefoxOptions

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='y!', intents=intents)



def printVariable(variable):
    print(f': {variable}\n')


async def playByUrl(ctx, url):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel.")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        voice_client = await channel.connect()
    elif ctx.voice_client.channel != channel:
        await ctx.voice_client.move_to(channel)
        voice_client = ctx.voice_client
    else:
        voice_client = ctx.voice_client

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'noplaylist': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        audio_url = info_dict['formats'][0]['url']

        try:
            voice_client.play(FFmpegPCMAudio(audio_url))
        except Exception as e:
            print(e)
            await ctx.send("Error playing the video.")






"""@bot.command()
async def play(ctx, *search_query):
    spacing = '                 '

    search_query = ' '.join(search_query)

    print(f'> Initated search for')
    print(f'{spacing}:. {search_query}')


    search_url = f'https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}'


    response = requests.get(search_url)

    soup = BeautifulSoup(response.text, 'html.parser')
    #print(f'{spacing}{str(soup)[:2000]}')

    results = soup.select('.yt-lockup-title a')
    #results = soup.find_all('a', id='video-title')
    #results = soup.find_all('a', href=lambda href: href and href.startswith('/watch?v='))
    

    if results:
        
        url = 'https://www.youtube.com' + results[0]['href']
        

        await playByUrl(ctx, url)


        await ctx.send(f'Playing: {urllib.parse.unquote(results[0].text)}')

    else:

        await ctx.send('No results found.')"""

@bot.command()
async def play(ctx, *search_query):
    search_query = ' '.join(search_query)
    search_url = f'https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}'

    driver=None

    try:
        # Set up Firefox options
        options = FirefoxOptions()
        options.headless = True  # Run in headless mode for faster execution

        # Initialize the Firefox driver with the specified options
        driver = webdriver.Firefox(options=options)
        driver.get(search_url)

        wait = WebDriverWait(driver, 20)
        results = wait.until(EC.presence_of_all_elements_located((By.ID, 'video-title')))

        if results:
            url = 'https://www.youtube.com' + results[0].get_attribute('href')
            await playByUrl(ctx, url)
            await ctx.send(f'Playing: {urllib.parse.unquote(results[0].text)}')
        else:
            await ctx.send('No results found.')

    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.send("There was an error during the search process.")

    finally:
        if driver is not None:
            driver.quit()





@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not connected to a voice channel.")



@bot.command()
async def list(ctx, *search_query):
    search_query = ' '.join(search_query)
    num_results = 5  # Default number of results
    if search_query[-1].isdigit():
        num_results = int(search_query[-1])
        search_query = ' '.join(search_query[:-1])
    
    url = f'https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.select('.yt-lockup-title a')
    
    result_list = [f'{i+1}. {unquote(result.text)}' for i, result in enumerate(results[:num_results])]
    await ctx.send('\n'.join(result_list))



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')





bot.run('MTI3MTEzMzU3NTczMDk1NDM1MQ.G7XTj1.TseZpQTbcUJPdp8-Q9-qkN5SFFtkFIyrXBWotQ')
