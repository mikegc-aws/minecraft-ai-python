import boto3
import json
from javascript import require, On
from context.reason_two import prompt
from helper.direction import *

from time import sleep

mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')


bot = mineflayer.createBot({
  'host': 'localhost',
  'port': 58917,
  'username':'Claude',
  'verbose': True,
  'checkTimeoutInterval': 60 * 10000,
})

bot.loadPlugin(pathfinder.pathfinder)

mcData = require('minecraft-data')(bot.version)

def extract_substring(text, trigger_str, end_str):
    last_trigger_index = text.rfind(trigger_str)
    
    if last_trigger_index == -1:
        return ""
    
    next_end_index = text.find(end_str, last_trigger_index)
    
    if next_end_index == -1:
        return ""
    
    substring = text[last_trigger_index + len(trigger_str):next_end_index]
    
    return substring

@On(bot, 'spawn')
def spawn(*args):
  print("I spawned 👋")
  

@On(bot, "chat")
def handle(this, player_name, message, *args):
    if player_name == bot.username:
        return
    else:
        bedrock = boto3.client(service_name="bedrock-runtime")

        # In the prompt string replace the [[MESSAGE]] string with the message
        message_prompt = prompt.replace("[[MESSAGE]]", message)

        query = "\n\nHuman: {} \n\nAssistant:".format(message_prompt)
        print(query)
        body = json.dumps(
            {
                "prompt": query,
                "max_tokens_to_sample": 1000,
                "temperature": 0.2,
                "stop_sequences": ["\n<end/>"],
                "anthropic_version": "bedrock-2023-05-31"
            }
        )
        response = bedrock.invoke_model(body=body, modelId="anthropic.claude-v2:1")
        response_body = json.loads(response.get("body").read())
        response = response_body.get("completion")
        print(f"-----------\n{response}\n-----------\n:")
        try:
            # WARNING: this is a very dangerous way to execute code! Do you trust AI?
            # Note: the code is executed in the context of the bot entity

            code = extract_substring(response, "<code>", "</code>")

            print(f"Found code:{code}")

            if code != "":
                code = code.strip()
                for code_line in code.split('\n'):
                    print(f"Running: {code_line}")
                    eval("{}".format(code_line))

        except Exception as error:
            print("error: {}".format(error))
            print("{}".format(response))
            bot.chat("I could not execute that: {}".format(code_line))
