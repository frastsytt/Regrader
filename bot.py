# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
from modules import gemInfo, ninjaCurrencyValue, gemPrice

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
primePrice = ninjaCurrencyValue('Prime Regrading Lens')
secondaryPrice = ninjaCurrencyValue('Secondary Regrading Lens')
exaltPrice = ninjaCurrencyValue('Exalted Orb')

primaryIcon = "<:PRL:946141140283957328>"
secondaryIcon = "<:SRL:946141140263006258>"
exaltedIcon = "<:Exalted:946141140342681650>"
chaosIcon = "<:chaos:946158278944096326>"

@bot.command(name='weight', help='Returns the weight of a gem')
async def weight(weight, *args):
    if not args:
        response = ":smile:"
        await weight.send(response)
    else:
        argumentString = ""
        for arg in args:
            argumentString += arg + " "
        argumentString = argumentString[:-1]
        print(argumentString)
        string = gemInfo(str(argumentString))

        if string == "Error":
            response=discord.Embed(title="Error", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description="Not a valid gem", color=0xF70404)
            response.set_thumbnail(url="https://cdn.discordapp.com/attachments/553615402941284353/911643857039532123/unknown.png")
        else:    
            #### Create the initial embed object ####
            response=discord.Embed(title="Sample Embed", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description=argumentString, color=0x109319)

            # Add author, thumbnail, fields, and footer to the embed
            response.set_author(name="Regrader", icon_url="https://static.wikia.nocookie.net/pathofexile_gamepedia/images/4/43/Prime_Regrading_Lens_inventory_icon.png/revision/latest/scale-to-width-down/78?cb=20201015024013")

            response.set_thumbnail(url=string[1])

            for key in string[0]:
                if key == "Superior":
                    response.add_field(name=key + "\t" + str(string[0][key]["value"]), value=str(string[0][key]["qualityBonus"]), inline=False) 
                else:
                    response.add_field(name=key + "\t" + str(string[0][key]["value"]) + "\t" + str(gemPrice(string[2], key)) + " " + chaosIcon, value=str(string[0][key]["qualityBonus"]), inline=False) 
            #response.add_field(name=" ", value=primePrice, url="https://static.wikia.nocookie.net/pathofexile_gamepedia/images/4/43/Prime_Regrading_Lens_inventory_icon.png", inline=True)
            #response.add_field(name=" ", value=secondaryPrice, url="https://www.poewiki.net/w/images/a/a4/Secondary_Regrading_Lens_inventory_icon.png", inline=True)
            response.add_field(name=exaltedIcon, value=exaltPrice, inline=True)
            response.add_field(name=secondaryIcon, value=secondaryPrice, inline=True)
            response.add_field(name=primaryIcon, value=primePrice, inline=True)
            #embed.add_field(name="Field 3 Title", value="It is inline with Field 2", inline=True)

            response.set_footer(text="This is the footer. It contains text at the bottom of the embed")
            
        await weight.send(embed=response)


# @bot.command(name='weight', help='Returns the weight of a gem')
# async def weight(weight, *args):
#     if not args:
#         response = "fuck you"
#     else:
#         argumentString = ""
#         for arg in args:
#             argumentString += arg + " "
#         argumentString = argumentString[:-1]
#         print(argumentString)
#         string = gemInfo(str(argumentString))
#         response = "```"
#         for key in string:
#             response += key + "\t" + str(string[key]["value"]) + "\t" + str(string[key]["qualityBonus"]) + "\n"
#         response += "```"
#     await weight.send(response)
bot.run(TOKEN)