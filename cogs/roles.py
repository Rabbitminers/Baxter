from discord.ext import commands
from discord.ext.commands import Context

import random

import discord

from helpers import checks

class RoleSelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.role = None
        self.added = None

    @discord.ui.button(label="Updates & Announcements", style=discord.ButtonStyle.blurple)
    async def updates(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.role = discord.utils.get(interaction.guild.roles, name="Update Pings")
        self.added = await self.add_or_remove_role(self.role, interaction.user)
        self.stop()

    @discord.ui.button(label="Beta Releases", style=discord.ButtonStyle.blurple)
    async def beta(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.role = discord.utils.get(interaction.guild.roles, name="Beta Release Pings")
        self.added = await self.add_or_remove_role(self.role, interaction.user)
        self.stop()

    @discord.ui.button(label="Progress & Events", style=discord.ButtonStyle.blurple)
    async def events(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.role = discord.utils.get(interaction.guild.roles, name="Progress Pings")
        self.added = await self.add_or_remove_role(self.role, interaction.user)
        self.stop()

    async def add_or_remove_role(self, role, user):
        added: bool = role in user.roles
        if added: await user.remove_roles(role) 
        else: await user.add_roles(role)
        return added

# Here we name the cog and create a new class for the cog.
class RoleAssignment(commands.Cog, name="roles"):
    def __init__(self, bot):
        self.bot = bot
        self.message_id = 1074821220945637456

        self.roles = {
            '🎡': "Beta Release Pings",
            '⬆️': "Update Pings",
            '🚋': "Progress Pings"
        }
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        message_id = payload.message_id
        emoji = payload.emoji
        guild_id = payload.guild_id
        user_id = payload.user_id

        print(emoji)

        if (message_id != self.message_id):
            return

        guild = self.bot.get_guild(guild_id)
        user = guild.get_member(user_id)

        role_name: str = self.roles.get(str(emoji))
        role = discord.utils.get(guild.roles, name=role_name)

        if role is None:
            return

        await user.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        message_id = payload.message_id
        emoji = payload.emoji
        guild_id = payload.guild_id
        user_id = payload.user_id

        print(emoji)

        if (message_id != self.message_id):
            return
            
        guild = self.bot.get_guild(guild_id)
        user = guild.get_member(user_id)

        role_name: str = self.roles.get(str(emoji))
        role = discord.utils.get(guild.roles, name=role_name)

        if role is None:
            return

        await user.remove_roles(role)

    async def add_or_remove_role(self, role, user):
        added: bool = role in user.roles
        if added: await user.remove_roles(role) 
        else: await user.add_roles(role)
        return added

async def setup(bot):
    await bot.add_cog(RoleAssignment(bot))
