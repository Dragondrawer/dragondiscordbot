import discord
import botdb
import os, random
from discord import Game
from discord.ext import commands

class Chris():
  def __init__(self, bot):
    self.bot = bot

##################
# Random/Testing #
##################
  @commands.command()
  async def summonmaster(self):
     await self.bot.say('mmmm~ you summoned the dungeon master~ heheheh... <@214472130627239946>')

  @commands.command()
  async def ping(self):
     await self.bot.say('PONG BITCH!')

  @commands.command()
  async def crazy(self):
    await self.bot.say('oh no~ theres nothing you can throw at me.. *you cant win against my kind of crazy~*')

  @commands.command()
  async def snap(self):
    possible_responses = [
      'JIMMY! IMMA GET THE MOB BOSS ON YOUR ASS!',
      'MELVIN! IMMA HACK YOUR ROUTER, BISH! UGUGUGUGUGUGUGUGUG',
      'JERRY! IMMA STUFF YO ASS WITH BEEEANNNSSS, YEAH',
      'JUDY! NOW GIVE ME MY FUKIN NEWPORTS BITCH!',
      'ALISTAIR! Get in the fucking Dungeon and prepare for the most pain you have ever felt~',
    ]
    await self.bot.say('hmm.. who shall I be today? >:D *snaps fingers* oh.. now im ' + random.choice(possible_responses))

#################
# Informational #
#################
  @commands.command()
  async def chrishelp(self):
    embed=discord.Embed(title="Chris Module Help (CMD Prefix: '!' or '$')", description="Available commands in this Personality Module", color=0x3e0913)
    embed.add_field(name="Random/Test CMDs", value="""
                      **ping** - Test Command
                      **summonmaster** - If you wish to summon Chris
                      **crazy** - Think you can throw anything at Chris?
                      **snap** - Go into character~""")
    embed.add_field(name="Currency/Gambling CMDs", value="""
                      **bal** - Check your balance
                      **resetbal** - Reset your balance
                      **slots** - If you wish to play slots""")
    await self.bot.say("", embed=embed)


############
# Currency #
############
  @commands.command(pass_context=True)
  async def bal(self, context):
    name=""
    desc=""
    key = context.message.author.name + "_" + context.message.author.discriminator + "_money"
    doc = botdb.get(key, "currency")
    if doc:
      name=context.message.author.name + "'s Currency card"
      desc="Card No/ID: **" + context.message.author.id + "**\nYou have **$%s**" % doc['bal']
    else:
      name="Error"
      desc="Account not found. Adding it. (type !bal again)"
      botdb.set(key, {'bal': 1000}, "currency")

    embed=discord.Embed(title="DragonScript Bank", description="User Balance Info", color=0x1abc9c)
    embed.set_thumbnail(url=context.message.author.avatar_url)
    embed.add_field(name=name, value=desc)
    await self.bot.say(context.message.author.mention, embed=embed)

#  @commands.command(pass_context=True)
#  async def testaddbal(self, context):
#    key = context.message.author.name + "_" + context.message.author.discriminator + "_money"
#    money = botdb.get(key, "currency")
#    money['bal'] += 150
#    botdb.set(key, money, "currency")
#    embed=discord.Embed(title="DragonScript Bank", description="User Balance Info", color=0x1abc9c)
#    embed.set_thumbnail(url=context.message.author.avatar_url)
#    embed.add_field(name=context.message.author.name + "'s Currency card", value="Card No/ID: **" + context.message.author.id + "**\nAdding **$150** to your account.")
#    await self.bot.say(context.message.author.mention, embed=embed)

  @commands.command(pass_context=True)
  async def resetbal(self, context):
    key = context.message.author.name + "_" + context.message.author.discriminator + "_money"
    botdb.set(key, {'bal': 1000}, "currency")
    embed=discord.Embed(title="DragonScript Bank", description="User Balance Info", color=0x1abc9c)
    embed.set_thumbnail(url=context.message.author.avatar_url)
    embed.add_field(name=context.message.author.name + "'s Currency card", value="Card No/ID: **" + context.message.author.id + "**\nAccount reset.")
    await self.bot.say(context.message.author.mention, embed=embed)

# Slots emotes; :spades: :clubs: :hearts: :diamonds: :dragon: 
############
# Gambling #
############
  @commands.command(pass_context=True)
  async def slots(self, context, am : int = 0):
    key = context.message.author.name + "_" + context.message.author.discriminator + "_money"
    doc = botdb.get(key, "currency")

    if am == 0:
      eremb=discord.Embed(title="DragonBot Slots [ERROR]", description="Please place a bet. (ex: !slots 100)", color=0xFF0000)
      await self.bot.say(context.message.author.mention, embed=eremb)
      return 
    if am < 50:
      eremb=discord.Embed(title="DragonBot Slots [ERROR]", description="You cannot bet any lower than **$50**", color=0xFF0000)
      await self.bot.say(context.message.author.mention, embed=eremb)
      return    
    if am > 200:
      eremb=discord.Embed(title="DragonBot Slots [ERROR]", description="You cannot bet any higher than **$200**", color=0xFF0000)
      await self.bot.say(context.message.author.mention, embed=eremb)
      return        

    spadesvalue=am*3
    clubsvalue=am*4
    heartsvalue=am*5
    diamondsvalue=am*6
    dragonsvalue=am*8 # Jackpot

    slot1=""
    slot2=""
    slot3=""

    result=""

    rescol=0x1abc9c

    possible_slots = [
      ':spades:',
      ':clubs:',
      ':hearts:',
      ':diamonds:',
      ':dragon:',
      ':clubs:',
      ':spades:',
      ':hearts:',
      ':clubs:',
      ':hearts:',
      ':clubs:',
      ':hearts:',
      ':diamonds:',
      ':dragon:',
      ':spades:',
      ':diamonds:',
      ':dragon:',
      ':spades:',
      ':diamonds:',
      ':clubs:',
      ':hearts:',
      ':diamonds:',
      ':spades:',
      ':hearts:',
      ':dragon:',
    ]

    slot1=random.choice(possible_slots)
    slot2=random.choice(possible_slots)
    slot3=random.choice(possible_slots)

    money = botdb.get(key, "currency")


    if doc['bal'] >= am:
      money['bal'] -= am
      botdb.set(key, money, "currency")

      if slot1 == possible_slots[0] and slot2 == possible_slots[0] and slot3 == possible_slots[0]:
        # won 1 slot
        rescol=0xed3d17
        money['bal'] += spadesvalue
        botdb.set(key, money, "currency")
        result="Winner! You won **$" + spadesvalue.__str__() + "**!"
      elif slot1 == possible_slots[1] and slot2 == possible_slots[1] and slot3 == possible_slots[1]:
        # won 2 slot
        rescol=0xaa3b23
        money['bal'] += clubsvalue
        botdb.set(key, money, "currency")
        result="Winner! You won **$" + clubsvalue.__str__() + "**!"
      elif slot1 == possible_slots[2] and slot2 == possible_slots[2] and slot3 == possible_slots[2]:
        # won 3 slot
        rescol=0xde1515
        money['bal'] += heartsvalue
        botdb.set(key, money, "currency")
        result="Winner! You won **$" + heartsvalue.__str__() + "**!"
      elif slot1 == possible_slots[3] and slot2 == possible_slots[3] and slot3 == possible_slots[3]:
        # won 4 slot
        rescol=0x15dede
        money['bal'] += diamondsvalue
        botdb.set(key, money, "currency")
        result="Winner! You won **$" + diamondsvalue.__str__() + "**!"
      elif slot1 == possible_slots[4] and slot2 == possible_slots[4] and slot3 == possible_slots[4]:
        # won 5 slot -- jackpot
        rescol=0xecff00
        money['bal'] += dragonsvalue
        botdb.set(key, money, "currency")
        result="JACKPOT!! You won **$" + dragonsvalue.__str__() + "**!"
      else:
        rescol=0xFF0000
        result="BUST! You won nothing! You lost **$" + am.__str__() + "**!"
    else:
      eremb=discord.Embed(title="DragonBot Slots [ERROR]", description="You need at least **$50** or more to use slots.", color=0xFF0000)
      await self.bot.say(context.message.author.mention, embed=eremb)
      return
    slotsemb=discord.Embed(title="DragonScript Slots", description="You bet **$" + am.__str__() + "** and..", color=rescol)
    slotsemb.add_field(name="Result", value=slot1 + " | " + slot2 + " | " + slot3)
    slotsemb.add_field(name="Rewards", value=":spades: - **$" + spadesvalue.__str__() + "**\n:clubs: - **$" + clubsvalue.__str__() + "**\n:hearts: - **$" + heartsvalue.__str__() + "**\n:diamonds: - **$" + diamondsvalue.__str__() + "**\n:dragon: - **JACKPOT $" + dragonsvalue.__str__() + "**")
    slotsemb.add_field(name="And..", value=result, inline=False)
    await self.bot.say(context.message.author.mention, embed=slotsemb)

def setup(bot):
  bot.add_cog(Chris(bot))
