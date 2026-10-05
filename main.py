import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
import sys
from prompts import system_prompt
from call_function import available_functions,call_function
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


for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )

    message = response.choices[0].message
    messages.append(message)
    if message.tool_calls:  
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            result_message = call_function(tool_call)
            messages.append(result_message)
            if not result_message['content']:
                raise Exception("Empty stuff!")
            else:
                if args.verbose:
                    print(f"-> {result_message['content']}")
    else:
        print(message.content)
        break
else:
    print("Maximum no of iterations reached!!")
    sys.exit(1)