import os
import interactions

import sqlite3

# conn = sqlite3.connect('test.db')

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD = int(os.getenv('DISCORD_GUILD'))

bot = interactions.Client(token=DISCORD_TOKEN)
@bot.command(
    name="say_something",
    description="say something!",
    scope=DISCORD_GUILD,
    options = [
        interactions.Option(
            name="text",
            description="What you want to say",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def say_something(ctx: interactions.CommandContext, text: str):
    await ctx.send(f"You said '{text}'!")


bot.start()