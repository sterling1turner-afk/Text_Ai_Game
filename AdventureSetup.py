import sys

import aioconsole
import lmstudio as lms

import GameContext
import Console

async def run_adventure_setup(model: lms.AsyncLLM, memory: GameContext.GameContext, config: lms.LlmPredictionConfigDict):
    print("WELCOME TO YOUR TEXT RPG ADVENTURE")

    theme: str = await aioconsole.ainput("Enter your adventure theme: ")

    memory.set_adventure_theme(theme)

    start_prompt = f"Begin the adventure based on the chosen theme: {theme}"
    memory.add_player_action(start_prompt)

    print("Generating adventure...\n")

    await Console.Console.launch_inference(model, memory, config)
