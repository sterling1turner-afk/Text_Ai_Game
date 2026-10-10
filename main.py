import asyncio

import lmstudio as lms
from typing import Any
import aioconsole

async def main():
    async with lms.AsyncClient("127.0.0.1:1234") as client:
        model = await client.llm.model("google/gemma-4-e4b")

        print("WELCOME TO TEXT LINE ADVENTURE")
        theme: str = await aioconsole.ainput("Enter your adventure theme: ")
        print("Generating adventure...\n")

        prediction_config: Any = {
            "temperature": 0.0,
            "seed": 25,
            "maxTokens": 4096
        }
        async for fragment in await model.respond_stream(theme, config=prediction_config):
            print(fragment.content, end="")
        print()


if __name__ == "__main__":
    asyncio.run(main())
