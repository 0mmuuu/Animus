#packages necessary for the discord bot to run
import discord
from discord.ext import commands
import responses
# packages that can tinker with websites
import requests 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = "MTAyMjUyMzk4OTIzMjQ3MjA2NQ.GD_p1E.-ek4BSYKRk0hz0dhgCq3Mdal-D1iJYm-OXVQHQ"
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    bot = commands.Bot(command_prefix='>>', intents=intents)

    #BOT COMMANDS:

    # Command for >>quote, the command will output a random quote
    @bot.command()
    async def quote(rq):
        """Gives ya a random quote"""
        recieved = requests.get("https://api.quotable.io/random")
        data = recieved.json()
        quote = data["content"]
        author = data["author"]
        reponse = str("```fix\n"+ "‟"+ quote +"”" + " - " + author +"\n```")
        await rq.send(reponse)

    # Command for >>weather, the command will output the weather of the given area
    @bot.command()
    async def weather(weather, *info):
        """Weather of the given location (Street Address,Zip)"""
        if len(info) == 0:
            await weather.send("Please type in a valid street name and zip after the command, as such: ```fix\n !weather Street, Zip\n```")
        else:
            #Setting up the user input to go into the link
            address = " ".join(info)
            if ',' not in address:
                await weather.send("Please try again, but with a comma this time.")
            else:
                split_address = address.split(',')
                street = split_address[0].replace(" ", "+")
                zip = split_address[1]

                #Putting user input into the link to get json details
                recieved_coords = requests.get("https://geocoding.geo.census.gov/geocoder/locations/address?street="+street+"&zip="+zip+"&benchmark=Public_AR_Census2020&format=json")
                data_coords = recieved_coords.json()
                # print("\n\n\n COORDS: ", data_coords, "\n\n\n")
                
                #time to get coordinates...or not
                if len(data_coords.get("result").get("addressMatches")) == 0:
                    await weather.send("Please enter a ***VALID*** street name and zip.")
                else:
                    longitude = str(data_coords.get("result").get("addressMatches")[0].get("coordinates").get("x"))
                    latitude = str(data_coords.get("result").get("addressMatches")[0].get("coordinates").get("y"))
                    coordinates = str(latitude+","+longitude)

                    #Now to get the weather
                    recieved_weather = requests.get("https://api.weather.gov/points/"+coordinates)
                    data_weather = recieved_weather.json()
                    link = str(data_weather.get("properties").get("forecast"))
                    recieved_forecast = requests.get(link)
                    data_forecast = recieved_forecast.json()

                    #Formatting the output
                    description = str(data_forecast.get("properties").get("periods")[0].get("detailedForecast"))
                    place = ("```"+address+" ("+longitude+","+latitude+")```")
                    forecast = ("```fix\nToday:\n"+description+"\n```")
                    output = str(place+forecast)
                    await weather.send(output)
        await weather.send("I hope you have a ~~horrible~~ great day ¬‿¬ ")
                    

    # >>genki, made a command that gives me the JPNS textbook answers to a certain page
    @bot.command(name = "genki")
    async def random_quote(genki,*numbers):
        """Send the answers of the given page (Chapter#,Lesson#)"""
        print(numbers[0],numbers[1])
        lesson = str(numbers[0])
        workbook = str(numbers[1])
        link = "https://sethclydesdale.github.io/genki-study-resources/lessons-3rd/lesson-"+lesson+"/workbook-"+workbook+"/"
        driver = webdriver.Firefox()
        driver.get(link)

        # This lets my click on the button on the site to access the answers
        prompt_1 = driver.find_element(By.XPATH,"//button[text()= 'Check Answers']")
        prompt_1.click()
        prompt_2 = driver.find_element(By.XPATH,"//button[text()= 'Yes, check my answers!']")
        prompt_2.click()

        # Sends me the output (screenshot or textbox)
        driver.save_full_page_screenshot("answers.png")
        # main = driver.find_element(By.ID,"quiz-zone")
        # problems = main.find_element(By.CLASS_NAME,"count-problems")
        # question = problems.find_element(By.CLASS_NAME,"problem")
        # print(question.text)
        # await genki.send(question.text)

        # Send the screenshot to discord
        with open("answers.png","rb") as f:
            picture = discord.File(f)
            await genki.send(file=picture)
        driver.quit()

    bot.run(TOKEN)

    #CLIENT SIDE
    @client.event
    async def on_ready():
        print(f"{client.user} is now running!")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print (f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == "?":
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)

