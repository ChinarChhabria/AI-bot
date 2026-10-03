import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions
import json

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError("API key not found!!")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key = api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]


response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
)

message = response.choices[0].message
if message.tool_calls:  
    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")
else:
    if args.verbose:
        answer = response.choices[0].message.content
        print(answer)
        if not response.usage:
            raise RuntimeError("usage not found!")
        print(f"User prompt: {args.user_prompt}")
        print("Prompt tokens:",response.usage.prompt_tokens)
        print("Response tokens:",response.usage.completion_tokens)
    else:
        print(response.choices[0].message.content)
