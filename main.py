import asyncio
import sys

import lmstudio as lms
import aioconsole

import GameState

SYSTEM_PROMPT = """ 
You are an expert Text RPG Game Master, Your tone is dark, atmospheric, and immersive

# RULES
1. Provide rich, 3-sentence descriptions of locations, actions, and consequences.
2. Never speak, act, or make decisions on behalf of the player.
3. End every turn by explaining the immediate surroundings and presenting a situation for the player
"""

def handle_prediction_fragment(fragment: lms.LlmPredictionFragment, _: int):
    if fragment.reasoning_type == "reasoning":
        print(fragment.content, end="", file=sys.stderr)
    elif fragment.reasoning_type == "reasoningEndTag":
        print()
    else:
        print(fragment.content, end="")

async def main():
    async with lms.AsyncClient("127.0.0.1:1234") as client:
        model = await client.llm.model(
            "google/gemma-4-e4b",
            config={
                "seed": 25
            }
        )

        print("WELCOME TO TEXT LINE ADVENTURE")
        # theme: str = await aioconsole.ainput("Enter your adventure theme: ")
        theme: str = "Test the tools provided. Include at least three nested levels. Include at least six total variables. Include at lease one array in the nested structure."
        print("Generating adventure...\n")

        prediction_config: lms.LlmPredictionConfigDict = {
            "temperature": 0.0,
            "maxTokens": 4096
        }
        await model.act(theme, tools=GameState.get_tools(), config=prediction_config, on_prediction_fragment=handle_prediction_fragment)
        print(GameState._dict)

if __name__ == "__main__":
    asyncio.run(main())