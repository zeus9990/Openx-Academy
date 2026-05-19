import discord, asyncio, config
from discord.ext import commands
from discord import app_commands
from typing import Literal
from db import add_question, get_question, update_level_status
from embeds import embed_list

user_data = {}
level_choices = [
    app_commands.Choice(name=value["level"].capitalize(), value=value["level"])
    for value in config.SELECTOR.values()
]

class Takequiz(discord.ui.View):
    def __init__(self, msg):
        super().__init__(timeout=60)
        self.msg = msg

    async def option_handler(self, interaction: discord.Interaction, selected_label: str):
        answer = user_data[interaction.user.id][0]['answer']
        level = user_data[interaction.user.id][0]['level']
        if answer == selected_label:
            channel_id = user_data[interaction.user.id][0]['channel_id']
            del user_data[interaction.user.id][0]
            if len(user_data[interaction.user.id]) == 0:
                role_id = config.SELECTOR[channel_id]['role']
                role = interaction.guild.get_role(role_id)
                await interaction.response.edit_message(embed=discord.Embed(description=f"**Congratulations, {interaction.user.mention} You have successfully passed the test, and {role.mention} role has been assigned to you.**", color=0x90EE90), view=None)
                self.stop()
                await interaction.user.add_roles(role)
                await update_level_status(user_id=interaction.user.id, level=level, status=True)
                del user_data[interaction.user.id]
                
            else:
                embed = discord.Embed(description="**Awesome that's correct answer next question coming in 10 seconds.**", color=0x90EE90)
                await interaction.response.edit_message(embed=embed, view=None)
                self.stop()
                await asyncio.sleep(10)

                embed=discord.Embed(
                                    title=f"Question No: {user_data[interaction.user.id][0]['question_no']} out of {user_data[interaction.user.id][0]['total_questions']}",
                                    description=f"{user_data[interaction.user.id][0]['question']}\n\n**• A.** {user_data[interaction.user.id][0]['options']['A']}\n**• B.** {user_data[interaction.user.id][0]['options']['B']}\n**• C.** {user_data[interaction.user.id][0]['options']['C']}\n**• D.** {user_data[interaction.user.id][0]['options']['D']}",
                                    color=0xFFFFFF
                                    )
                embed.set_footer(text="You have 60 seconds to answer.", icon_url="https://i.postimg.cc/tJkT3LM3/P-P.jpg")
                await interaction.followup.edit_message(message_id=self.msg.id, embed=embed, view=Takequiz(self.msg))
        else:
            await interaction.response.edit_message(embed=discord.Embed(description=f"**Unfortunately this is not the right answer {interaction.user.mention} Better luck next time.**", color=0xFF0000), view=None)
            del user_data[interaction.user.id]
            self.stop()
            return

    @discord.ui.button(label='Option A', style=discord.ButtonStyle.blurple)
    async def option_a(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.option_handler(interaction, 'A')

    @discord.ui.button(label='Option B', style=discord.ButtonStyle.blurple)
    async def option_b(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.option_handler(interaction, 'B')

    @discord.ui.button(label='Option C', style=discord.ButtonStyle.blurple)
    async def option_c(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.option_handler(interaction, 'C')

    @discord.ui.button(label='Option D', style=discord.ButtonStyle.blurple)
    async def option_d(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.option_handler(interaction, 'D')

    async def on_timeout(self) -> None:
        try:
            await self.msg.edit(embed=discord.Embed(description="**Response timed out, you took longer than a minute.**"), view=None)
        except:
            pass


class Startquiz(discord.ui.View):
    def __init__(self, channel=None):
        super().__init__(timeout=None)
        self.channel = channel
        
        link_button = discord.ui.Button(
            label="Read Chapter",
            style=discord.ButtonStyle.link,
            url=config.SELECTOR.get(self.channel, {}).get('document', 'https://www.example.com')
        )
        self.add_item(link_button)

        test_button = discord.ui.Button(
            label="Take test",
            style=discord.ButtonStyle.blurple,
            emoji="🎓",
            custom_id="start_quiz"
        )
        test_button.callback = self.on_take_test_click
        self.add_item(test_button)

    async def on_take_test_click(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        msg = await interaction.followup.send(embed=discord.Embed(description="**Preparing questions for you..**", color=0xFFFFFF), ephemeral=True)
        level = config.SELECTOR[interaction.channel.id]['level']
        question_count = config.SELECTOR[interaction.channel.id]['question_count']
        status, data = await get_question(user_id=interaction.user.id, level=level, question_count=question_count)
        if not status:
            await interaction.followup.edit_message(embed=discord.Embed(description=data, color=0xFF0000), message_id=msg.id)
        else:
            for idx, item in enumerate(data, start=1):
                item['question_no'] = idx
                item['channel_id'] = interaction.channel.id
                item['total_questions'] = question_count
            user_data[interaction.user.id] = data
            embed=discord.Embed(
                                title=f"Question No: {user_data[interaction.user.id][0]['question_no']} out of {user_data[interaction.user.id][0]['total_questions']}",
                                description=f"{user_data[interaction.user.id][0]['question']}\n\n**• A.** {user_data[interaction.user.id][0]['options']['A']}\n**• B.** {user_data[interaction.user.id][0]['options']['B']}\n**• C.** {user_data[interaction.user.id][0]['options']['C']}\n**• D.** {user_data[interaction.user.id][0]['options']['D']}",
                                color=0xFFFFFF
                                )
            embed.set_footer(text="You have 60 seconds to answer.", icon_url="https://i.postimg.cc/tJkT3LM3/P-P.jpg")
            await interaction.followup.edit_message(embed=embed, view=Takequiz(msg), message_id=msg.id)

class Question_Confirm(discord.ui.View):
    def __init__(self, question, option_A, option_B, option_C, option_D, answer, level):
        self.question = question
        self.option_A = option_A
        self.option_B = option_B
        self.option_C = option_C
        self.option_D = option_D
        self.answer = answer
        self.level = level
        super().__init__(timeout=180)

    @discord.ui.button(label='Yes !', style=discord.ButtonStyle.green, custom_id='yes')
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = await add_question(self.question, self.option_A, self.option_B, self.option_C, self.option_D, self.answer, self.level)
        if data:
            embed = discord.Embed(title=f"Question uploaded to database.")
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(title="This question is already present in the database.")
            await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label='No !', style=discord.ButtonStyle.red, custom_id='no')
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Alright! let's try again.")
        await interaction.response.edit_message(embed=embed, view=None)


class Quiz(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    async def check_permissions(self, interaction):
        return any(role.id in config.RUNNER for role in interaction.user.roles)

    @app_commands.command(
            name="quiz_panel",
            description="Initiate quiz panel in selected channel.")
    @app_commands.describe(
            channel="Channel where the quiz panel will be visible.")
    @app_commands.guild_only()
    async def quiz_panel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if not await self.check_permissions(interaction):
            await interaction.response.send_message(content="> **You don't have permission to send the quiz panel.**", ephemeral=True)
            return
        if channel.id in [key for key in config.SELECTOR.keys()]:
            url = self.client.user.display_avatar.url
            embed_code = config.SELECTOR[channel.id]['embed']
            await channel.send(embed=embed_list[embed_code], view=Startquiz(channel.id))
            await interaction.response.send_message(content=f"> **Quiz panel sent in {channel.mention}.**", ephemeral=True)
        else:
            await interaction.response.send_message(content="> **Please select a valid channel.**", ephemeral=True)

    @app_commands.command(
        name="add_question",
        description="Add questions for the quiz."
    )
    @app_commands.describe(
        question="the academy test question.",
        option_a="option number A of the question.",
        option_b="option number B of the question.",
        option_c="option number C of the question.",
        option_d="option number D of the question.",
        answer="choose the option number for the right answer.",
        level ="choose the level for which you are adding this question."
    )
    @app_commands.choices(level=level_choices)
    @app_commands.guild_only()
    async def add_question(self, interaction: discord.Interaction, question: str, option_a: str, option_b: str, option_c: str, option_d: str, answer: Literal['A','B','C','D'], level: app_commands.Choice[str]):
        if await self.check_permissions(interaction):
            url = self.client.user.display_avatar.url
            embed = discord.Embed(title="**Is this correct ?**",
                                  description=f'**Q:** {question}\n\n'
                                              f'**Option A:** {option_a}\n'
                                              f'**Option B:** {option_b}\n'
                                              f'**Option C:** {option_c}\n'
                                              f'**Option D:** {option_d}\n\n'
                                              f'**Correct Answer:** Option {answer}',
                                  color=0xFFFFFF)
            embed.set_footer(text="if it is correct click Yes to upload else click No.", icon_url=url)
            await interaction.response.send_message(embed=embed, view=Question_Confirm(question, option_a, option_b, option_c, option_d, answer, level.value))


async def setup(client):
    await client.add_cog(Quiz(client))