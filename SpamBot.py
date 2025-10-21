import discord
from discord import app_commands
from discord.ext import commands
import asyncio

#===============Setup intents===============
intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


#===============On bot ready===============
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

#===============Interactive Panel===============
class SpamView(discord.ui.View):
    def __init__(self, message_text: str):
        super().__init__(timeout=None)
        self.message_text = message_text

    @discord.ui.button(label="Spam", style=discord.ButtonStyle.danger)
    async def spam_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=True)
        for _ in range(5):
            await interaction.followup.send(self.message_text)
            await asyncio.sleep(0.1)

#===============Modal (Message input panel)===============
class MessageModal(discord.ui.Modal, title="Spam Message Panel"):
    message_input = discord.ui.TextInput(
        label="Enter the message you want to send",
        placeholder="Example: hi",
        required=True,
        max_length=100
    )

    async def on_submit(self, interaction: discord.Interaction):
        msg = self.message_input.value

        embed = discord.Embed(
            title="𝗞æ𝘇𝘇𝘆",
            description=msg,
            color=discord.Color.default()
        )

        view = SpamView(msg)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


#===============/spam command===============
@bot.tree.command(name="spam", description="Open a message input panel for spamming")
async def spam(interaction: discord.Interaction):
    await interaction.response.send_modal(MessageModal())

#===============Status===============
@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,  # watching / listening / competing / Playing
            name="/spam"
        ),
        status=discord.Status.idle  # online / idle / dnd
    )
    print(f"{bot.user} is ready!")

#===============Run the bot===============
bot.run("")





