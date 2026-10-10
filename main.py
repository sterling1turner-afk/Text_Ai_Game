import asyncio
from os import MFD_ALLOW_SEALING

import aioconsole
import lmstudio as lms

import AdventureSetup
import GameContext
import Console


SYSTEM_PROMPT = """ 
You are an expert Text RPG Game Master, Your tone is dark, atmospheric, and immersive

# RULES
1. Provide rich detailed descriptions of NEW locations (not old locations that were already described in a previous response), actions, and consequences
2. Never speak, act, or make decisions on behalf of the player.
3. Try to follow the "Hero's journey" and maintain a story arc, start the first adventure generation with a call to action
4. End every turn by explaining the immediate surroundings and presenting an impactful situation to the player that should move the story along at a good pace
"""


async def main():
    memory = GameContext.GameContext(system_prompt=SYSTEM_PROMPT)

    async with lms.AsyncClient("127.0.0.1:1234") as client:
        model = await client.llm.model(
            "google/gemma-4-e4b",
            config={
                "seed": 25
            }
        )
        prediction_config: lms.LlmPredictionConfigDict = {
            "temperature": 0.9,
            "maxTokens": False
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

            Console.Console.currentInferenceResults = ""

            memory.add_player_action(player_action)

            print("\nStory Teller: ", end="")

            await Console.Console.launch_inference(model, memory, prediction_config)

            memory.add_assistant_response(Console.Console.currentInferenceResults)




if __name__ == "__main__":
    asyncio.run(main())