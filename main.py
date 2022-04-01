import discord
import os

from query import queries

class HugoBot(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to the server!')

        self.prefix = '$ask '

    async def on_message(self, message):

        # don't responde to ourselves
        if message.author == self.user:
            return

        if message.content.startswith(self.prefix):
            
            query = message.content[len(self.prefix):]

            if queries[query.lower()] == 0:
                await message.channel.send('É um borro')


if __name__ == "__main__":
    client = HugoBot()
    client.run(os.getenv('DISCORD_TOKEN'))
