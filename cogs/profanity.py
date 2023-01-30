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
            await message.author.send(f"Your message contained profanity. Please avoid using such words on the server.")

    @commands.Cog.listener()
    async def on_message_edit(self, old, message):
        if profanity.contains_profanity(message.content):
            await message.delete()
            await message.author.send(f"Your message contained profanity. Please avoid using such words on the server.")

    @commands.hybrid_command(
        name="profanitytest",
        description="This is a testing command that does nothing.",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    # This will only allow owners of the bot to execute the command -> config.json
    @checks.is_owner()
    async def testcommand(self, context: Context):
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """
        print("Hello world!")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(ProfanityFilter(bot))
