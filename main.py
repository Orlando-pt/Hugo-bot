import discord

class HugoBot(discord.Client):
    async def on_ready(self):
        pass

    async def on_message(self, message):

        # don't responde to ourselves
        if message.author == self.user:
            return

        pass

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True

    client = HugoBot(intents=intents)
    client.run('OTU5NTA1NzA4NDE0NTM3ODY4.Ykc3Uw.S6kFnnYQ3YD5iOV0E7OTBZ5F6WE')
