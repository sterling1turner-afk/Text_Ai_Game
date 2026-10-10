# This is a sample Python script.

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

        print("Generating adventure...\n")

        async for fragment in await model.respond_stream(prompt):
            print(fragment.content, end="", flush=False)

        print()


if __name__ == "__main__":
    asyncio.run(main())

