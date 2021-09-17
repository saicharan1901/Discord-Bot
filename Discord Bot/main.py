import discord
from discord.ext import commands
import os
import aiohttp
import random
import json

bot = commands.Bot(command_prefix = ["g!"])

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game(name="g!help"))
  print('Logged in Succesfully')

determine_flip = ['h', 't']

@bot.command()
async def coinflip(ctx,message,message1:int):
  await open_account(ctx.author)
  users = await get_bank_data()
  user = ctx.author


  money = message1

  
  if random.choice(determine_flip) == message:
        embed = discord.Embed(title="Toss", description=f"{ctx.author.mention} Flipped coin, YOU **WONN**! **{money} coins**")
        users[str(user.id)]["Wallet"] += money
        await ctx.send(embed=embed)

  else:
        embed = discord.Embed(title="Toss", description=f"{ctx.author.mention} Flipped coin, YOU **LOST**! **{money} coins**")
        users[str(user.id)]["Wallet"] -= money
        await ctx.send(embed=embed)    

  with open("bank.json","w") as f:
        json.dump(users,f)

async def open_account(user):
     
     users = await get_bank_data()
    
     if str(user.id) in users:
        return False
     else:
        users[str(user.id)] = {}
        users[str(user.id)]["Wallet"] = 0
        users[str(user.id)]["Bank"] = 0    

     with open("bank.json","w") as f:
       json.dump(users,f) 
     return True

async def get_bank_data():
     with open("bank.json","r") as f:
        users = json.load(f)
    
     return users

@bot.command(case_insensitive=True, aliases = ["p"])
@commands.guild_only()
async def profile(ctx, user: discord.Member = None):

    if user is None:
      await open_account(ctx.author)
      user = ctx.author
      users = await get_bank_data()
      _id = str(user.id)
      coins_amt = users[_id]["Wallet"]
      bank_amt =  users[_id]["Bank"]

      em = discord.Embed(title = f"{ctx.author.name}'s profile", color = discord.Color.green())
      em.add_field(name = "MONEY",value =f":moneybag: **Wallet**: {coins_amt}"+"\n"+f':bank: **Bank**: {bank_amt}')
      em.set_thumbnail(url = user.avatar_url)

      await ctx.send(embed = em)

    else:
      await open_account(user)
      users = await get_bank_data()
      coins_amt = users[str(user.id)]["Wallet"]
      bank_amt =  users[str(user.id)]["Bank"]

      em = discord.Embed(title = f"{user.name}'s profile", color = discord.Color.green())
      em.add_field(name = "MONEY",value =f":moneybag: **Wallet**: {coins_amt}"+"\n"+f':bank: Bank: {bank_amt}')
      em.set_thumbnail(url = user.avatar_url)
      await ctx.send(embed = em)
      await user.send(f"**{ctx.author.name}** has viewed your profile in **{ctx.guild.name}**")


@bot.command(case_insensitive=True)
@commands.guild_only()
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Withdraw what lol?? Enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[1]:
        await ctx.send("You don't have that much money!")
        return 
    if amount<0:
        await ctx.send("Oh!! come on! Check what you're typing.")
        return
    
    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,"Bank")

    await ctx.send(f"You withdrew {amount} coins")

@bot.command(case_insensitive=True, aliases = ["dep"])
@commands.guild_only()
async def deposit(ctx,amount = None):
    await open_account(ctx.author)
    
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[0]:
        await ctx.send("You don't have that much money!")
        return 
    if amount<0:
        await ctx.send("Seriously dude?! Check what you typed.")
        return
    
    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,"Bank")

    await ctx.send(f"You deposited {amount} coins")

@bot.command(case_insensitive=True, aliases = ["send"])
@commands.guild_only()
async def give(ctx,member: discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)
    
    if amount == None:
        await ctx.send("Duhh! Enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[1]:
        await ctx.send("Duhhh! Check your coins first lol.")
        return 
    if amount<0:
        await ctx.send("That doesn't even make sense!")
        return
    if amount==0:
      await ctx.send("Bruhhh.. why use this command if u wanna give nothing")
      return
    
    await update_bank(ctx.author,-1*amount)
    await update_bank(member,amount)

    await ctx.send("You gave"+ " "+"<@"+f"{member.id}"+">"+" "+ f"{amount} coins")

async def update_bank(user, change = 0,mode = "Wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("bank.json","w") as f:
        json.dump(users,f)
     
    bal = [users[str(user.id)]["Wallet"],users[str(user.id)]["Bank"]]
    return bal


@bot.command(case_insensitive=True)
@commands.cooldown(1, 100, commands.BucketType.user)
async def loot(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()

    user = ctx.author

    earning = random.randrange(0,1000)
    

    if earning<=50:
      await ctx.send(f"**You got {earning} coins.** Couldn't loot more. Try again Next time."+ " "+ "<@"+ f"{ctx.author.id}"+ ">")

    else:
      await ctx.send(f"You found a chest containing **{earning} coins :money_mouth:**" + " " + "<@"+ f"{ctx.author.id}"+ ">")
    
    users[str(user.id)]["Wallet"] += earning
    

    with open("bank.json","w") as f:
        json.dump(users,f)

@bot.event
async def on_command_error(ctx,error):
       if isinstance(error, commands.CommandOnCooldown):
             msg = '**Still on cooldown**, please try again in {:.2f} seconds'.format(error.retry_after)
             await ctx.send(msg)


bot.run('ODg4Mzc4MDUyNjkyODA3NzIw.YUR0iQ.gevlZ-6eCHGen1ZoSBfvonkjht8')
