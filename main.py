import asyncio

import lmstudio as lms

SYSTEM_PROMPT = """ 
You are an expert Text RPG Game Master, Your tone is dark, atmospheric, and immersive

# RULES
1. Provide rich, 3-sentence descriptions of locations, actions, and consequences.
2. Never speak, act, or make decisions on behalf of the player.
3. End every turn by explaining the immediate surroundings and presenting a situation for the player
"""



async def main():
    async with lms.AsyncClient("127.0.0.1:1234") as client:
        model = await client.llm.model(
            "google/gemma-4-e4b",
            config={
                "seed": 25
            }
        )
        prompt = "Describe a mysterious fantasy dungeon in 3 sentences."
        print("Generating adventure...\n")
        prediction_config: lms.LlmPredictionConfigDict = {
            "temperature": 0.0,
            "maxTokens": 4096
        }
        async for fragment in await model.respond_stream(prompt, config=prediction_config):
            print(fragment.content, end="")
        print()


if __name__ == "__main__":
    asyncio.run(main())