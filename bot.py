import discord
from discord.ext import commands

## ***Additional libraries to make the commands work:*** 
import random
import os
import json
##

client = commands.Bot(command_prefix = 'bork ')

botName = 'DogeBot'
token = 'NzkxNzY4MTk0NDg1ODQ2MDM2.X-T9lw.sd-3yQXMkaEQOkGp1INcwTHlg5I'
status = '[bork]'

## ***EVENTS:***

@client.event
async def on_ready():
    print('Bot is ready and online.')
    await client.change_presence(activity=discord.Game(status))

@client.event
async def on_message(message):
    start_coins = 500
    increment_coins = 5
    json_filename = 'json/users.json'
    with open(json_filename, 'r') as f:
        users = json.load(f)
        id = str(message.author.id)
        if message.author.bot == True:
            return
        if not id in users:
            users[id] = { 'dogeCoins': start_coins,'name': message.author.name}
        else:
            user = users[id] 
            user['dogeCoins'] += increment_coins
            if random.randint(1,20) == 5:
                await message.channel.send(f'🎁 {str(message.author.mention)} a random giftbox appears! You open it to get {increment_coins*10} DogeCoins!')
                user['dogeCoins'] += increment_coins*5
    with open(json_filename, 'w') as f:
        json.dump(users,f,indent=4)
    await client.process_commands(message)

# @client.event
# async def on_command_error(ctx, error):
#     await ctx.send('Huh? What the heck does that mean!? Pls spell that correctly!')

## ***COMMANDS:***

@client.command()
async def ping(ctx):
    await ctx.send(f"Hey! Don't ping me! Here's my ping if that's what u wanted: {round(client.latency * 1000)}ms")

@client.command(pass_context=True, aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['My doge senses say no.','n o p e','YES','My friend said yes.',"Maybe...","bork bork bork","Bruh - definitely","yesn't","idk","no no no","I think that's a no."]
    await ctx.send(f'{ctx.message.author.mention}\nQuestion: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def bruh(ctx):
    await ctx.send("BRUH IN THE CHAT")

@client.command()
async def image(ctx):
    await ctx.send('cute doge:')
    file = discord.File("images/doge1.jpg", filename="doge1.jpg")
    embed = discord.Embed()
    embed.set_image(url="attachment://images/doge1.jpg")
    await ctx.send(file=file, embed=embed)

## ***ECONEMY COMMANDS:***

@client.command(pass_context = True, aliases=['bal'])
async def balance(ctx, member: discord.Member=None):
    if member == None:
        member = ctx.message.author
    json_filename = 'json/users.json'
    with open(json_filename, 'r') as f:
        users = json.load(f)
        id = str(member.id)
        userCoins = users[id]['dogeCoins']
    await ctx.send(f"{member.mention} your balance is {str(userCoins)} DogeCoins!")

@client.command(aliases=['rank'])
async def ranks(ctx):
    output = ""
    userInfos = []
    def sortUsers(a, lessThan):
        for i in range(1, len(a)):
            j = i
            while j > 0 and lessThan(a[j], a[j - 1]):
                a[j], a[j - 1] = a[j - 1], a[j]
                j -= 1
    class UserInfo():
        def __init__(self, name, coins):
            self.name = name
            self.coins = coins
    with open('json/users.json', 'r') as f:
        users = json.load(f)
        for user in users:
            userInfos.append(UserInfo(users[user]['name'], users[user]["dogeCoins"]))
    sortUsers(userInfos, lambda a, b: a.coins > b.coins)
    for i in range(len(userInfos)):
        if not i > 10:
            output += f"{userInfos[i].coins}: {userInfos[i].name}\n"
        else:
            break
    embedMes = discord.Embed(title="**Ranks for this Server**", description="These are the top 10 Ranks for this Server", color=0x025b8)
    embedMes.set_author(name='Doge Bot',icon_url='https://i.kym-cdn.com/profiles/icons/big/000/234/278/573.jpg')
    embedMes.add_field(name="**Top 10:**\n", value=output, inline=False)
    await ctx.send(embed=embedMes)
    
@client.command(pass_context = True, aliases=['box'])
async def boxes(ctx):
    correct = random.randint(1,3)
    await ctx.send(f'{ctx.author.mention} Here are three boxes, guess which one has the doge (reply with 1 2 or 3): 📦 📦 📦')
    response = await client.wait_for('message')
    response = int(response.content)
    if response == correct:
        json_filename = 'json/users.json'
        with open(json_filename, 'r') as f:
            users = json.load(f)
        with open(json_filename, 'w') as f:
            id = str(ctx.author.id)
            prize = random.randint(50,80)
            users[id]['dogeCoins'] += prize
            json.dump(users,f)
        await ctx.send(f'{ctx.author.mention} YES! You got {prize} DogeCoins')
    else:
        await ctx.send(f'{ctx.author.mention} n o p e it was box {str(correct)}.')

@client.command(pass_context=True)
async def party(funding):
    if int(funding) < 100:
        ctx.send("You need to put more DogeCoins in, bork bork bork!")
    ctx.send(f'{ctx.author.mention} has started a party! Type ***party*** in the chat to get {int(funding)/10}')
    response = await client.wait_for('message')
    while funding > 0
        if response == "party":
            with open('json/users.json','r'):
                users = json.load(f)
                users[response.author.id]['dogeCoins'] += int(funding)/10
            with open('json/users.json','w'):
                json.dump(users,f)
            int(funding) -= int(funding)/10

## ***ADMIN COMMANDS:***

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason); print(f'{member} has been kicked from the server.')

@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason); ctx.send(f'Banned {member.mention}')

@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {member.mention}')
            return

client.run(token)
