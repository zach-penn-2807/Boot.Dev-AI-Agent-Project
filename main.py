import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key == None:
    raise RuntimeError("No API Key found")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


parser = argparse.ArgumentParser(description="CLI Agent")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()



messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]


def main():
    
    print("Hello from ai-agent!")
    for i in range(20):
        response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
)
        if response.usage == None:
            raise RuntimeError("Failed API request")
        message = response.choices[0].message
        messages.append(message)
        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
            print("Response:")
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    result_message = call_function(tool_call, args.verbose)
                    if result_message["content"] == "":
                        raise Exception("Error: Empty Content")
                    print(f"-> {result_message['content']}")
                    if i == 19:
                        print("Iterations limit exceeded without result")
                        exit(1)
                    messages.append(result_message)
            else:
                print(response.choices[0].message.content)
                break
        else:
            print("Response:")
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    result_message = call_function(tool_call, args.verbose)
                    if result_message["content"] == "":
                        raise Exception("Error: Empty Content")
                    messages.append(result_message)
                    if i == 19:
                        print("Iterations limit exceeded without result")
                        exit(1)
            else:
                print(response.choices[0].message.content)
                break
        


if __name__ == "__main__":
    main()
