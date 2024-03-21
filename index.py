import logging
import io
import sys
from javascript import require, On
from mc.mine_chat import MineChat

logging.basicConfig(filename='index.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')
Vec3 = require('Vec3')

bot = mineflayer.createBot({
    'host': 'localhost',
    'port': 58917,
    'username': 'Claude3',
    'verbose': True,
    'checkTimeoutInterval': 60 * 10000,
})

bot.loadPlugin(pathfinder.pathfinder)
mine_chat = MineChat(prompt_file_path="meta_prompted.txt")

@On(bot, 'spawn')
def spawn(*args):
    logging.info("I spawned 👋")

def execute_arbitrary_code(code):
    """Executes arbitrary code, captures stdout and stderr, including errors."""
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    output_buffer = io.StringIO()
    sys.stdout = output_buffer
    sys.stderr = output_buffer

    result = ""

    try:
        exec(code)
        result = output_buffer.getvalue()
    except Exception as error:
        result = f"Error encountered: {error}"
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        output_buffer.close()
        return result

def process_feedback(player_name, message, depth=0, max_depth=6):
    if depth > max_depth:
        logging.info("Max recursion depth reached.")
        return
    else: 
        logging.info(f"Recursion depth {depth}.")
    
    if "<function_results>" in message:
        formatted_message = f"{message}"
    else: 
        formatted_message = f"<message>Player {player_name}, says \"{message}\"</message>"

    logging.info(f"{formatted_message}")

    feedback = mine_chat(formatted_message)
    
    logging.info(f"Feedback code: {feedback}")

    if feedback:
        logging.info(f"Executing feedback code: {feedback}")
        result = execute_arbitrary_code(feedback)
        if result.strip():
            result_formatted = f"<function_results>{result}<function_results>"
            logging.info(f"Feedback result: {result_formatted}")
            process_feedback(player_name, result_formatted, depth + 1, max_depth)
        else:
            logging.info("No feedback result.") 

@On(bot, "chat")
def handle_chat(_, player_name, message, *args):
    if player_name == bot.username:
        return

    process_feedback(player_name, message)

if __name__ == "__main__":
    # Any initialization or run code should go here
    pass
