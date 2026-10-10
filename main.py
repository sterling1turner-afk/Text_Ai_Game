import asyncio

import aioconsole
import lmstudio as lms

import AdventureSetup
import GameContext
import Console


SYSTEM_PROMPT = """ 
# RULES
1. Provide good descriptions for actions, consequences and character introductions. 
2. Never speak, act, or make decisions on behalf of the player.
3. Follow the "Hero's journey" structure
5. End every turn by describing the immediate, changing situation or a new threat to the player to keep the story moving at a good pace.
7. Use tools throughout the game when necessary to keep inventory up to date.
8. Don't be cheesy, avoid AI slop dialogue, and write realistic character dialogue.
9. Use only plain text. Do not use markdown formatting.
"""

START_SYSTEM_PROMPT = """
You are an expert Text RPG Game Master, Your tone is immersive 

0.1 Provide a good description for the environment around the character currently
0.2 Use the update tool to give the player some starting items relevant to their character
0.3 Start the story with a call to action or equivalent for the player
"""


async def main():
    memory = GameContext.GameContext(system_prompt=SYSTEM_PROMPT, starting_system_prompt=START_SYSTEM_PROMPT)

    async with lms.AsyncClient("127.0.0.1:1234") as client:
        model = await client.llm.model(
            "google/gemma-4-e4b",
            config={
                "seed": 25
            }
        )
        prediction_config: lms.LlmPredictionConfigDict = {
            "temperature": 0.9,
            ## "maxTokens":
        }

        await AdventureSetup.run_adventure_setup(model, memory, prediction_config)

        memory.set_system_prompt()

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

            print("\nStory Teller: \n --------------------------------------------------------------------------------------------------------------\n", end="")

            await Console.Console.launch_inference(model, memory, prediction_config)

            memory.add_assistant_response(Console.Console.currentInferenceResults)




if __name__ == "__main__":
    asyncio.run(main())