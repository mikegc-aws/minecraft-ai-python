import boto3
import json
from javascript import require, On
from mc.mine_chat import MineChat
from time import sleep

mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')
Vec3 = require('vec3').Vec3

bot = mineflayer.createBot({
  'host': 'localhost',
  'port': 58917,
  'username':'Claude3',
  'verbose': True,
  'checkTimeoutInterval': 60 * 10000,
})

bot.loadPlugin(pathfinder.pathfinder)
mcData = require('minecraft-data')(bot.version)
mine_chat = MineChat(prompt_file_path="mine_prompt.txt")
max_try = 5
current_try = 0

@On(bot, 'spawn')
def spawn(*args):
  print("I spawned 👋")
  
@On(bot, "chat")
def handle(this, player_name, message, *args):
    
    global current_try
    global max_try

    if player_name == bot.username:
        return
    
    else:
        code = mine_chat.prompt(message)
        try:
            
            current_try += 1
            
            print(f"Try: {current_try}")
            print("-"*20)
            print("code: {}".format(code))

            # WARNING: this is a very dangerous way to execute code! Do you trust AI?
            # Note: the code is executed in the context of the bot entity
            exec(code)

            current_try = 0

        except Exception as error:
            print("*"*20)
            print("error: {}".format(error))

            if current_try < max_try:
                bot.chat("There was an error running the code I came up with, I will try again.")
                message_error = f"There was an error running that code. Here is the error:\n{error}\n\nFix the code and try again."
                handle(this, player_name, message_error, *args)

            else:
                bot.chat("Error - giving up.")