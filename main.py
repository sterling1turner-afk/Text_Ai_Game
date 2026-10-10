# This is a sample Python script.
import aioconsole
from aioconsole import aprint

import os
import asyncio

os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"
os.environ["no_proxy"] = "localhost,127.0.0.1,::1"

import lmstudio as lms


async def main():
    async with lms.AsyncClient("127.0.0.1:1234") as client:
        model = await client.llm.model("google/gemma-4-e4b")

        print("WELCOME TO TEXT LINE ADVENTURE")
        theme: str = await aioconsole.ainput("Enter your adventure theme: ")
        print("Generating adventure...\n")

        async for fragment in await model.respond_stream(theme):
            print(fragment.content, end="", flush=False)
        print()


if __name__ == "__main__":
    asyncio.run(main())

