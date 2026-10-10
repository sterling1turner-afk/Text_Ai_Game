import asyncio

import lmstudio as lms
import aioconsole

from adventure_setup import run_adventure_setup
from Game_Context import GameContext

SYSTEM_PROMPT = """ 
You are an expert Text RPG Game Master, Your tone is dark, atmospheric, and immersive

# RULES
1. Provide rich, 3-sentence descriptions of locations, actions, and consequences.
2. Never speak, act, or make decisions on behalf of the player.
3. End every turn by explaining the immediate surroundings and presenting a situation for the player
"""

async def main():
    chosen_seed = 25
    memory = GameContext(system_prompt=SYSTEM_PROMPT)

    async with lms.AsyncClient("127.0.0.1:1234") as client:
        model = await client.llm.model(
            "google/gemma-4-e4b",
            config={
                "seed": chosen_seed
            }
        )
        prediction_config: lms.LlmPredictionConfigDict = {
            "temperature": 0.0,
            "maxTokens": 4096
        }

        await run_adventure_setup(model, memory, prediction_config)

if __name__ == "__main__":
    asyncio.run(main())