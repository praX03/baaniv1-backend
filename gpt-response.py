import openai
import os
from dotenv import load_dotenv
import json
import json
import openai
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

GPT_MODEL = "gpt-4-1106-preview"
load_dotenv()
### Utility functions
@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if tools is not None:
        json_data.update({"tools": tools})
    if tool_choice is not None:
        json_data.update({"tool_choice": tool_choice})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "tool": "magenta",
    }
    
    for message in messages:
        if message["role"] == "system":
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "tool":
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))

openai.api_key = os.getenv("OPENAI_API_KEY")
instructions=os.getenv("INSTRUCTIONS")
client = openai
messages = []
def post_deatils(post_content, post_date, post_platform):
    print(post_content, "\n",
          post_date, "\n",
          post_platform)
    return post_content, post_date, post_platform
# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
tools = [
    {
        "type": "function",
        "function": {
            "name": "extract_post_details",
            "description": "Use this function to extract the platform for posting content, the date for posting(in 'HH:MM,DD/MM/YYYY' format, '00:00,00/00/0000' if user say now) and the content for the post",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": """
                                The content generated for posting.
                                Content should be the final content after refinement.
                                Content should be confirmed by the user.
                                """,
                    },
                    "platform": {
                        "type": "string",
                        "description": """
                                The platform for posting the content as decided by the user(Instagram, Twitter, LinkedIn, Email, WhatsApp)
                                """,
                    },
                    "date": {
                        "type": "string",
                        "description": """
                                The date for posting the content in 'HH:MM, DD/MM/YYYY' format.
                                '00:00,00/00/0000' if user says anything related to now/immediately.
                                """,
                    }
                },
                "required": ["content", "platform", "date"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_image",
            "description": "generate image by Dall-E 3",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to generate image",
                    },
                    "size": {
                        "type": "string",
                        "enum": ["1024x1024", "other_sizes"],
                    },
                },
                "required": ["prompt"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send mail to a user",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "The subject for the mail",
                    },
                    "email-body": {
                        "type": "string",
                        "description": "The body content for the mail",
                    },
                },
                "required": ["subject", "email-body"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "make_post_linkedin",
            "description": "Make a post to linkedin",
            "parameters": {
                "type": "object",
                "properties": {
                    "linkedin_post": {
                        "type": "string",
                        "description": "The linkedin post text content",
                    },
                    "twitter_post": {
                        "type": "string",
                        "description": "The twitter post text content",
                    },
                    "image": {
                        "type": "string",
                        "description": "Image URL of the post generated by generate_image function",
                    },
                },
                "required": ["linkedin_post", "twitter_post"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_notion",
            "description": "add data to notion",
            "parameters": {
                "type": "object",
                "properties": {
                    "linkedin_post": {
                        "type": "string",
                        "description": "The linkedin post text content",
                    },
                    "linkedin_post_date": {
                        "type": "string",
                        "description": "date to post the content on linkedin in the format 'December 4, 2023'",
                    },
                    "twitter_post": {
                        "type": "string",
                        "description": "The twitter post text content",
                    },
                    "twitter_post_date": {
                        "type": "string",
                        "description": "date to post the content on twitter in the format 'December 4, 2023'",
                    },
                    "image": {
                        "type": "string",
                        "description": "Image URL of the post",
                    },
                },
                "required": [
                    "linkedin_post",
                    "linkedin_post_date",
                    "twitter_post",
                    "twitter_post_date",
                ],
            },
        },
                },
]
def execute_function_call(message):
    if message["tool_calls"][0]["function"]["name"] == "extract_post_details":
        content = json.loads(message["tool_calls"][0]["function"]["arguments"])["content"]
        date = json.loads(message["tool_calls"][0]["function"]["arguments"])["date"]
        platform = json.loads(message["tool_calls"][0]["function"]["arguments"])["platform"]
        results = post_deatils(content, date, platform)
    else:
        results = f"Error: function {message['tool_calls'][0]['function']['name']} does not exist"
    return results
def gpt_response(user_content):
    
    messages.append({"role": "system", "content": os.getenv("INSTRUCTIONS")})
    messages.append({"role": "user", "content": user_content})
    chat_response = chat_completion_request(messages, tools)
    assistant_message = chat_response.json()["choices"][0]["message"]
    print(assistant_message)
    if assistant_message.tool_calls[0] is not None:
        print(assistant_message.tool_calls[0].function)
        # pass
    # assistant_message['content'] = str(assistant_message.tool_calls[0].function)
    messages.append(assistant_message)
    if assistant_message.get("tool_calls"):
        results = execute_function_call(assistant_message)
        messages.append({"role": "tool", "tool_call_id": assistant_message["tool_calls"][0]['id'], "name": assistant_message["tool_calls"][0]["function"]["name"], "content": results})

        # assistant_message_2 = second_response.json()["choices"][0]["message"]
        # messages.append(assistant_message_2)
        # messages.append({"role": "assis", "content": "Create content for posting on twitter, now, the content should be about eiffel tower. /show"})
    pretty_print_conversation(messages)
while True:
    message = input("Prax: ")
    if message:
        messages.append({"role":"user", "content":message},)
        gpt_response(message)
