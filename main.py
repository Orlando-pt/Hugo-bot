import os
import interactions
import json

from web_scraper import WebScraper

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD = int(os.getenv('DISCORD_GUILD'))

scraper = WebScraper()

bot = interactions.Client(token=DISCORD_TOKEN)

@bot.command(
    name="todays_drops",
    description="Cardano drops for today.",
    scope=DISCORD_GUILD,
    options = [
        interactions.Option(
            name="day",
            description="Day you want to see",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
    ],
)
async def todays_drops(ctx: interactions.CommandContext, day: int = None):
    await ctx.send('This might take a little while. Have a coffee in the meantime :wink:')

    drops = scraper.drops_for_today(day)
    drops_json = '```json\n' + json.dumps(drops, indent=2) + '\n```'
    await ctx.send(f"Here are the drops you asked for:\n{drops_json}")


bot.start()