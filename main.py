#!/usr/bin/env python3
import discord


class AutoMod(discord.Client):
    async def send_message_to_mod_channel(self, guild: discord.Guild, text: str):
        if guild.system_channel and guild.system_channel.permissions_for(guild.me).send_messages:
            print(f"Sending message {text} in {guild.id} to system channel {guild.system_channel.id}")
            await guild.system_channel.send(text)
        else:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    print(f"Sending message {text} in {guild.id} to regular channel {channel.id}")
                    await channel.send(text)
                    break

    async def on_ready(self):
        print(f"Started up in {len(list(client.guilds))} guilds")

    async def on_guild_join(self, guild: discord.Guild):
        print(f"Joined guild {guild.id}")
        await self.send_message_to_mod_channel(guild, "This bot will automatically ban Honde bots")

    async def on_member_join(self, member: discord.Member):
        if "h0nde" in member.name.lower() and "twitter" in member.name.lower():
            try:
                await member.ban(reason="banned h0nde")
                print(f"Banned {member.id} in {member.guild.id}")
            except discord.Forbidden:
                await self.send_message_to_mod_channel(member.guild, f"Could not ban {member}, not enough permissions")


intents = discord.Intents.default()
intents.members = True
activity = discord.Activity(name='for Honde Bots', type=discord.ActivityType.watching)

client = AutoMod(intents=intents, activity=activity)
with open("TOKEN", "r") as f:
    client.run(f.readline())
