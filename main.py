import asyncio

import lmstudio as lms


async def main():
    async with lms.AsyncClient("127.0.0.1:1234") as client:
        model = await client.llm.model("google/gemma-4-e4b")
        prompt = "Describe a mysterious fantasy dungeon in 3 sentences."
        print("Generating adventure...\n")
        async for fragment in await model.respond_stream(prompt):
            print(fragment.content, end="")
        print()


if __name__ == "__main__":
    asyncio.run(main())