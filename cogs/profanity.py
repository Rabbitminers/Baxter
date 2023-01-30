from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks
from better_profanity import profanity

# Here we name the cog and create a new class for the cog.
class ProfanityFilter(commands.Cog, name="profanity"):
    def __init__(self, bot):
        with open("censor_list.txt", "r") as f:
            lines = [line.strip() for line in f]
        profanity.load_censor_words(lines)
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if profanity.contains_profanity(message.content):
            await message.delete()

    @commands.Cog.listener()
    async def on_message_edit(self, old, message):
        if profanity.contains_profanity(message.content):
            await message.delete()

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(ProfanityFilter(bot))
