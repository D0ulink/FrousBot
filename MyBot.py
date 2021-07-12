import discord
from discord.ext import commands

import sqlite3
from config import settings
from Cybernator import Paginator as pag

bot = commands.Bot(command_prefix = settings['PREFIX'], intents = discord.Intents.all())
bot.remove_command('help')
connection = sqlite3.connect('server.db')
cursor = connection.cursor()

@bot.event
async def on_ready():
    global coin, score, right, wrong
    coin = str(bot.get_emoji(858345716552040478))
    score = str(bot.get_emoji(858962817163460640))
    right = str(bot.get_emoji(858345644300173312))
    wrong = str(bot.get_emoji(858960951125999617))
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        id INT,
        cash BIGINT,
        scores BIGINT,
        server_id INT
    )""")
    for guild in bot.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, {guild.id})")
                connection.commit()
                print('Бот подключился к базе данных!')
            else:
                pass
    connection.commit()

@bot.event
async def on_member_join(member):
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, {member.guild.id})")
        connection.commit()
        print('Всё готово!')
    else:
        pass

@bot.command(aliases=['bal', 'balance', 'cash'])
async def _cash(ctx, member: discord.Member = None):
    if member == None:
            embed = discord.Embed(description = f"Место в рейтинге:", colour = discord.Colour.from_rgb(100, 74, 200), timestamp = ctx.message.created_at)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.add_field(name = 'Монеты:', value = f"""{coin} {cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}""")
            embed.add_field(name = 'Баллы:', value = f"""{score} {cursor.execute("SELECT scores FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}""")

    else:
            embed = discord.Embed(description = f'Место в рейтинге: {cursor.execute("SELECT cash, name FROM users WHERE server_id")}', colour = discord.Colour.from_rgb(100, 74, 200))
            embed.set_author(name=member, icon_url=member.avatar_url)
            embed.add_field(name = 'Монеты:', value = f"""{coin} {cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]}""")
            embed.add_field(name = 'Баллы:', value = f"""{score} {cursor.execute("SELECT scores FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}""")

    await ctx.send(embed = embed)

@bot.command(aliases = ['score-add', 'add-score', 'score+', '+score'])
@commands.has_guild_permissions(administrator = True)
async def _add_scores(ctx, member: discord.Member = None, amount: int = None):
    if member is None:
        embed = discord.Embed(description = f'{wrong} Команда введена неправильно.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(255, 10, 10))
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        embed.add_field(name = 'Используйте:\n', value = '`score+ <участник> <кол-во>`')
        await ctx.send(embed = embed)
        await ctx.message.add_reaction('')
    else:
        if amount is None:
            embed = discord.Embed(description = f'{wrong} Команда введена неправильно.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(255, 10, 10))
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            embed.add_field(name = 'Используйте:\n', value = '`score+ <участник> <кол-во>`')
            await ctx.send(embed = embed)
            await ctx.message.add_reaction('')
        elif amount < 1:
            embed = discord.Embed(description = f'{wrong} Команда введена неправильно.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(255, 10, 10))
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            embed.add_field(name = 'Используйте:\n', value = '`score+ <участник> <кол-во>`')
            await ctx.send(embed = embed)
            await ctx.message.add_reaction('')
        elif amount > 999999999:
            embed = discord.Embed(description = f'{wrong} Команда введена неправильно.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(255, 10, 10))
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            embed.add_field(name = 'Используйте:\n', value = '`score+ <участник> <кол-во>`')
            await ctx.send(embed = embed)
            await ctx.message.add_reaction('')
        else:
            cursor.execute(f"UPDATE users SET scores = scores + {amount} WHERE id = {member.id}")
            connection.commit()
            await ctx.message.add_reaction(f'{right}')

@bot.command(aliases = ['score-remove', 'remove-score', 'score-', '-score'])
@commands.has_guild_permissions(administrator = True)
async def _remove_scores(ctx, member: discord.Member = None, amount: int = None):
    if member is None:
        embed = discord.Embed(description = f'{wrong} Команда введена неправильно.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(255, 10, 10))
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        embed.add_field(name = 'Используйте:\n', value = '`score- <участник> <кол-во>`')
        await ctx.send(embed = embed)
        await ctx.message.add_reaction('')
    else:
        if amount is None:
            embed = discord.Embed(description = f'{wrong} Команда введена неправильно.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(255, 10, 10))
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            embed.add_field(name = 'Используйте:\n', value = '`score- <участник> <кол-во>`')
            await ctx.send(embed = embed)
            await ctx.message.add_reaction('')
        elif amount < 1:
            embed = discord.Embed(description = f'{wrong} Команда введена неправильно.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(255, 10, 10))
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            embed.add_field(name = 'Используйте:\n', value = '`score- <участник> <кол-во>`')
            await ctx.send(embed = embed)
            await ctx.message.add_reaction('')
        elif amount > 999999999:
            embed = discord.Embed(description = f'{wrong} Команда введена неправильно.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(255, 10, 10))
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            embed.add_field(name = 'Используйте:\n', value = '`score- <участник> <кол-во>`')
            await ctx.send(embed = embed)
            await ctx.message.add_reaction('')
        else:
            cursor.execute(f"UPDATE users SET scores = scores - {amount} WHERE id = {member.id}")
            connection.commit()
            await ctx.message.add_reaction(f'{right}')

@bot.command(aliases = ['cash-add', 'add-cash', 'cash+', '+cash'])
@commands.has_guild_permissions(administrator = True)
async def _add_money(ctx, member: discord.Member = None, amount: int = None):
    if member is None:
        embed = discord.Embed(description = f'{wrong} Команда введена неправильно.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(227, 38, 54))
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        embed.add_field(name = 'Используйте:\n', value = '`cash+ <участник> <сумма>`')
        await ctx.send(embed = embed)
        await ctx.message.add_reaction('')
    else:
        if amount is None:
            embed = discord.Embed(description = f'{wrong} Команда введена неправильно.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(227, 38, 54))
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            embed.add_field(name = 'Используйте:\n', value = '`cash+ <участник> <сумма>`')
            await ctx.send(embed = embed)
            await ctx.message.add_reaction('')
        elif amount < 1:
            embed = discord.Embed(description = f'{wrong} Команда введена неправильно.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(227, 38, 54))
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            embed.add_field(name = 'Используйте:\n', value = '`cash+ <участник> <сумма>`')
            await ctx.send(embed = embed)
            await ctx.message.add_reaction('')
        elif amount > 9999999999:
            embed = discord.Embed(description = f'{wrong} Вы ввели слишком большую сумму. Введите сумму меньше 1,000,000,000.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(227, 38, 54))
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            embed.add_field(name = 'Используйте:\n', value = '`cash+ <участник> <сумма>`')
            await ctx.send(embed = embed)
            await ctx.message.add_reaction('')
        else:
            cursor.execute(f"UPDATE users SET cash = cash + {amount} WHERE id = {member.id}")
            connection.commit()
            await ctx.message.add_reaction(f'{right}')

@bot.command(aliases = ['cash-remove', 'remove-cash', 'cash-', '-cash'])
@commands.has_guild_permissions(administrator = True)
async def _remove_money(ctx, member: discord.Member = None, amount: int = None):
    if member is None:
        embed = discord.Embed(description = f'{wrong} Команда введена неправильно.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(255, 10, 10))
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        embed.add_field(name = 'Используйте:\n', value = '`cash- <участник> <сумма>`')
        await ctx.send(embed = embed)
        await ctx.message.add_reaction('')
    else:
        if amount is None:
            embed = discord.Embed(description = f'{wrong} Команда введена неправильно.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(255, 10, 10))
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            embed.add_field(name = 'Используйте:\n', value = '`cash- <участник> <сумма>`')
            await ctx.send(embed = embed)
            await ctx.message.add_reaction('')
        elif amount < 1:
            embed = discord.Embed(description = f'{wrong} Команда введена неправильно.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(255, 10, 10))
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            embed.add_field(name = 'Используйте:\n', value = '`cash-<участник> <сумма>`')
            await ctx.send(embed = embed)
            await ctx.message.add_reaction('')
        elif amount > 999999999:
            embed = discord.Embed(description = f'{wrong} Вы ввели слишком большую сумму. Введите сумму меньше 1,000,000,000.\n⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣', colour = discord.Colour.from_rgb(255, 10, 10))
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            embed.add_field(name = 'Используйте:\n', value = '`cash- <участник> <сумма>`')
            await ctx.send(embed = embed)
            await ctx.message.add_reaction('')
        else:
            cursor.execute(f"UPDATE users SET cash = cash - {amount} WHERE id = {member.id}")
            connection.commit()
            await ctx.message.add_reaction(f'{right}')

@_remove_money.error
async def _remove_money_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description = f'{wrong} У вас недостаточно прав, что бы использовать эту команду!\n⁣⁣⁣', colour = discord.Colour.from_rgb(227, 38, 54))
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        embed.add_field(name = 'Требуемые права:', value = '`Administrator`')
        await ctx.send(embed = embed)

@_remove_scores.error
async def _remove_scores_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description = f'{wrong} У вас недостаточно прав, что бы использовать эту команду!\n')
        await ctx.send(embed = embed)

@_add_scores.error
async def _add_scores_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description = f'{wrong} У вас недостаточно прав, что бы использовать эту команду!\n')
        embed.add_field(name = 'Нужные права:\n⁣⁣⁣⁣⁣', value = '`Administrator`')
        await ctx.send(embed = embed)

@_add_money.error
async def _add_money_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description = f'{wrong} У вас недостаточно прав, что бы использовать эту команду!\n')
        await ctx.send(embed = embed)

@bot.command(aliases  = ['help', 'хелп'])
async def _help(ctx):
    embed = discord.Embed(title = 'Все доступные команды:', colour = discord.Colour.from_rgb(100, 74, 200), timestamp = ctx.message.created_at)
    embed.set_footer(text = f'Вызвал {ctx.author.name}', icon_url = ctx.author.avatar_url)
    embed.add_field(name = '.balance - Показывает ваш баланс, или баланс упомянутого участника.\n.top - Показывает лидеров по монетам или баллам на серверею.\n', value = '⁣')
    await ctx.send(embed = embed)

@bot.command(aliases = ['top', 'leaderboard', 'leaders', 'lb'])
async def _top(ctx):
    embed1 = discord.Embed(title = "🏛 Таблица Лидеров По Монетам", colour = discord.Colour.from_rgb(100, 74, 200), timestamp = ctx.message.created_at)
    counter = 0

    for row in cursor.execute("SELECT cash, name FROM users WHERE server_id = {} ORDER BY cash DESC LIMIT 10".format(ctx.guild.id)):
        counter += 1
        embed1.add_field(name = f'**{counter}.** {row[1]}', value = f'{coin} {row[0]}', inline = False)
        embed1.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

    embed2 = discord.Embed(title = "🏛 Таблица Лидеров По Баллам", colour = discord.Colour.from_rgb(100, 74, 200), timestamp = ctx.message.created_at)
    counter = 0

    for row in cursor.execute("SELECT scores, name FROM users WHERE server_id = {} ORDER BY scores DESC LIMIT 10".format(ctx.guild.id)):
        counter += 1
        embed2.add_field(name = f'**{counter}.** {row[1]}', value = f'{coin} {row[0]}', inline = False)
        embed2.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

    embeds = [embed1, embed2]
    reactions = ["👈", "👉"]

    message = await ctx.send(embed = embed1)
    page = pag(bot, message, only=ctx.author, use_more=False, embeds=embeds, reactions= reactions)
    await page.start()

print('Бот работает в полную силу❗')
bot.run(settings['TOKEN'])