import discord, asyncio, sys, traceback
from discord.ext import commands
from Cogs.quiz import Startquiz
from config import BOT_TOKEN

discord.utils.setup_logging()

class MyClient(commands.Bot):

    def __init__(self):
        super().__init__(
        command_prefix=":::",
        intents=discord.Intents.all(),
        case_insensitive=True,
        strip_after_prefix=True,
        )

    async def on_ready(self):
        print(f"{self.user.name} is ready")

    async def setup_hook(self) -> None:
        try:
            await self.load_extension('Cogs.quiz')
            print("Quiz cog loaded successfully")
        except Exception as error:
            print(f"Error loading Quiz Cog", file=sys.stderr)
            traceback.print_exc()
        await self.tree.sync()
        self.add_view(Startquiz())

    async def start_client(self):
        await self.start(BOT_TOKEN)

asyncio.run(MyClient().start_client())