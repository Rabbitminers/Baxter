import json
import os

from discord.ext import commands
from discord.ext.commands import Context
import discord

import requests

from helpers import checks

class GitHub(commands.Cog, name="github"):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = os.environ.get('COMMIT_ALERT_CHANNEL')
        self.secret = os.environ.get('GITHUB_WEBHOOK_SECRET')

    @commands.Cog.listener()
    async def on_raw_receive(self, payload):
        print("Recieved")
        event = payload.headers.get('X-GitHub-Event')
        if event == "push":
            if payload.headers.get('X-Hub-Signature') != self.secret:
                print("Invalid signature.")
                return
            data = json.loads(payload.data)
            repository = data["repository"]["full_name"]
            commits = data["commits"]
            message = f"There are {len(commits)} new commits in {repository}:"
            for commit in commits:
                message += f"\n- {commit['message']} ({commit['url']})"
            channel = self.bot.get_channel(int(self.channel_id))
            await channel.send(message)

async def setup(bot):
    await bot.add_cog(GitHub(bot))
