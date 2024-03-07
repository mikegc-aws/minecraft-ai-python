from .chat import Chat

class MineChat(Chat):
    def __init__(self, prompt_file_path='mine_prompt.txt', **kwargs):
        # Read system prompt from the specified file
        with open(prompt_file_path, 'r') as file:
            system_prompt = file.read().strip()

        # Now call the superclass's __init__ with the loaded system prompt
        super().__init__(system_prompt=system_prompt, **kwargs)

    def extract_substring(self, text, trigger_str, end_str):
        last_trigger_index = text.rfind(trigger_str)
        if last_trigger_index == -1:
            return ""
        next_end_index = text.find(end_str, last_trigger_index)
        if next_end_index == -1:
            return ""
        substring = text[last_trigger_index + len(trigger_str):next_end_index]
        return substring

    def parse_response(self, response: str):
        code = self.extract_substring(response, "<code>", "</code>")
        return code.strip()

    def prompt(self, prompt: str):
        response = super().prompt(prompt)
        return self.parse_response(response)
