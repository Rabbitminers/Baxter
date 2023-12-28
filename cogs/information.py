from discord.ext import commands
from discord.ext.commands import Context
import discord
from discord import message, channel

from readthefaq import ReadTheFAQ

class Information(commands.Cog, name="information"):
    def __init__(self, bot):
        self.bot = bot
        self.rtf = ReadTheFAQ()
        self.channel_id: int = 1069327918385348688

    @commands.Cog.listener()
    async def on_message(self, message: message.Message):
        channel: discord.abc.MessageableChannel = message.channel
        if not self.is_same_channel(channel.id):
            return
        if self.rtf.predict([message.content])[0]:
            embed = discord.Embed(
                description=f"Your question might be answered by the FAQ in <#1069396544379428984>\n\n(This message is based on a prediction of youre message if this is incorrect please tell us)",
                color=0x9C84EF
            )
            await message.channel.send(embed=embed)

    def is_same_channel(self, channel_id: int) -> bool:
        return channel_id == self.channel_id

async def setup(bot):
    await bot.add_cog(Information(bot))
