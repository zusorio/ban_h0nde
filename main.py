#!/usr/bin/env python3
import discord
from dotenv import load_dotenv
import os


class AutoMod(discord.Client):
    async def send_message_to_mod_channel(self, guild: discord.Guild, text: str):
        if guild.system_channel and guild.system_channel.permissions_for(guild.me).send_messages:
            await guild.system_channel.send(text)
        else:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    await channel.send(text)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_member_join(self, member: discord.Member):
        name = member.name.lower()
        if "h0nde" in name and "twitter" in name:
            try:
                await member.ban(reason="banned h0nde")
                print(f"Banned {member.id} in {member.guild.id}")
            except discord.Forbidden:
                await self.send_message_to_mod_channel(member.guild, f"Could not ban {member}, not enough permissions")


def main():
    load_dotenv()

    intents = discord.Intents.default()
    intents.members = True

    client = AutoMod(intents=intents, status=discord.Status.invisible)

    client.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
    main()
