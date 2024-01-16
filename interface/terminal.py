
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

def pretty_print_conversation(messages=None, message=None):
    role_to_color = {
        "user": "green",
        "assistant": "blue",
        "assistant_wo_fc": "magenta",
        "prompt": "yellow",
    }


    if messages:
        if messages[-1]["role"] == "assistant" and messages[-1].get("function_call"):
            print(colored(f"Baani: {messages[-1]['function_call']}\n", role_to_color["assistant"]))
        elif messages[-1]["role"] == "assistant" and not messages[-1].get("function_call"):
            print(colored(f"Baani: {messages[-1]['content']}\n", role_to_color["assistant_wo_fc"]))
    elif message:
        print(colored(f"{message}\n", role_to_color["prompt"]))
