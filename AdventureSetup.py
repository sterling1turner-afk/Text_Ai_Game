import aioconsole
import lmstudio as lms

import GameContext
import Console
import StoryBoard

STORY_PROMPT = """Please generate a unique story plot. It should have distinct story beats, separated by horizontal rule lines (make these by adding a line space and --- in Markdown). Please make a story that won't be seen as generic. Focus mainly on a single storyline, and try to keep the story outline concise and under 600 words. Give the main antagonist consistent, realistic motives that make sense from their perspective but are evidently detrimental to the general public. Don't be too fanciful with unnecessary details - create atmospheric but grounded environments. Keep story elements consistent throughout the entire outline."""

async def run_adventure_setup(model: lms.AsyncLLM, memory: GameContext.GameContext, config: lms.LlmPredictionConfigDict):
    print("WELCOME TO YOUR TEXT RPG ADVENTURE")

    theme: str = await aioconsole.ainput("Enter your adventure theme: ")
    character: str = await aioconsole.ainput("Describe your character?: ")
    objective: str = await aioconsole.ainput("What is your character's objective?: ")

    print("Writing story ...\n")

    ctx = GameContext.GameContext("", "")
    ctx._history_messages.append({"role": "system", "content": f"{STORY_PROMPT} Protagonist: {character}. Objective: {objective}. Theme: {theme}."})
    await Console.Console.launch_inference(model, ctx, config, False)
    StoryBoard.Storyboard.create_story_board(Console.Console.currentInferenceResults)

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
