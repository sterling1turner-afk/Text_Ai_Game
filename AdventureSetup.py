import sys

import aioconsole
import lmstudio as lms

import GameContext
import Console

async def run_adventure_setup(model: lms.AsyncLLM, memory: GameContext.GameContext, config: lms.LlmPredictionConfigDict):
    print("WELCOME TO YOUR TEXT RPG ADVENTURE")

    theme: str = await aioconsole.ainput("Enter your adventure theme: ")
    character: str = await aioconsole.ainput("Describe your character?: ")
    objective: str = await aioconsole.ainput("What is your character's objective?: ")

    memory.set_adventure_context(theme, character, objective)

    start_prompt = (
        f"Begin the adventure based on the chosen theme: {theme}"
        f"The player character is: {character}"
        f"Their objective is: {objective}"
        f"Establish an opening scene and deliver the call to action:"
    )
    memory.add_player_action(start_prompt)

    print("Generating adventure...\n")

    await Console.Console.launch_inference(model, memory, config)
