# This is a sample Python script.
from lmstudio import Chat


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

import os
import asyncio

os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"
os.environ["no_proxy"] = "localhost,127.0.0.1,::1"

import lmstudio as lms


async def main():
    async with lms.AsyncClient("127.0.0.1:1234") as client:
        model = await client.llm.model("google/gemma-4-e4b")
        prompt = "Describe a mysterious fantasy dungeon in 3 sentences."
        chat = Chat.from_history({"messages": [
            {"role": "system", "content": "You are a gamemaster for a text adventure."},
            {"role": "user", "content": prompt},
        ]})
        prev_msgs = []

        print("Generating adventure...\n")
        async for fragment in await model.respond_stream(chat):
            print(fragment.content, end="")
            prev_msgs.append(fragment.content)
        print()

        prev_msg_str = "".join(prev_msgs)
        prev_msgs.clear()
        prompt = "Investigate the magically active parts of the surroundings."
        chat.add_user_message(prompt)
        chat = Chat.from_history({"messages": [
            {"role": "system", "content": "You are a gamemaster for a text adventure."},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": prev_msg_str},
        ]})
        async for fragment in await model.respond_stream(chat):
            print(fragment.content, end="")
            prev_msgs.append(fragment.content)
        print()


if __name__ == "__main__":
    asyncio.run(main())

