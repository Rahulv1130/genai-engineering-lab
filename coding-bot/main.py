from dotenv import load_dotenv
from openai import OpenAI
import json
from tools import tools, list_files, read_file, write_file, run_terminal_command

load_dotenv()

client = OpenAI()


SYSTEM_PROMPT = """
You are running on Windows git bash terminal. So use commands related to that only.
If the output of the run_terminal_command tool contains return_code 0, then it shows that the command executed successfully
"""


messages = []

messages.append({"role": "system", "content": SYSTEM_PROMPT})


def get_response(message):
    response = client.chat.completions.create(
        messages=messages, model="gpt-4o-mini", tools=tools
    )

    return response


def perform_tool_calls(tool_calls):
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        if tool_name == "read_file":
            result = read_file(**tool_args)

        elif tool_name == "write_file":
            result = write_file(**tool_args)

        elif tool_name == "list_files":
            result = list_files(**tool_args)

        elif tool_name == "run_terminal_command":
            result = run_terminal_command(**tool_args)

        else:
            result = {"error": f"Unknown tool {tool_name}"}

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            }
        )


while True:
    query = input("You ->  ")

    messages.append({"role": "user", "content": query})

    while True:
        res = get_response(query)

        if res.choices[0].finish_reason != "tool_calls":
            print(f"AI -> {res.choices[0].message.content}")
            break

        messages.append(
            {
                "role": "assistant",
                "content": res.choices[0].message.content,
                "tool_calls": res.choices[0].message.tool_calls,
            }
        )

        tool_calls = res.choices[0].message.tool_calls

        perform_tool_calls(tool_calls)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]
