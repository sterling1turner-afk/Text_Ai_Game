import asyncio
import sys

import aioconsole
import lmstudio as lms
import AdventureSetup
import GameContext
from Console import prompt_user, currentInferenceResults

SYSTEM_PROMPT = """ 
You are an expert Text RPG Game Master, Your tone is dark, atmospheric, and immersive

# RULES
1. Provide rich, 3-sentence descriptions of new locations, actions, and consequences, do not redescribe the same things you have already described or repeat the same descriptors over and over
2. Never speak, act, or make decisions on behalf of the player.
3. Try to follow the "Hero's journey" and maintain a story arc
4. End every turn by explaining the immediate surroundings and presenting a situation for the player, the situation should move the story forward in some way, not just "move left or move right"
"""


async def main():
    module = sys.modules[__name__]
    memory = GameContext.GameContext(system_prompt=SYSTEM_PROMPT)

    async with lms.AsyncClient("127.0.0.1:1234") as client:
        model = await client.llm.model(
            "google/gemma-4-e4b",
            config={
                "seed": 25
            }
        )
        prediction_config: lms.LlmPredictionConfigDict = {
            "temperature": 0.0,
            "maxTokens": 4096
        }

        await AdventureSetup.run_adventure_setup(model, memory, prediction_config)

        while True:
            player_action = await aioconsole.ainput("\nEnter your action: ")
            player_action = player_action.strip()

            if player_action.lower() == "quit":
                print("Thanks for playing!")
                break

            if not player_action:
                continue

            module.currentInferenceResults = ""

            memory.add_player_action(player_action)

            print("\nStory Teller: ", end="")

            await prompt_user(model, memory, prediction_config)

            memory.add_assistant_response(currentInferenceResults)




if __name__ == "__main__":
    asyncio.run(main())