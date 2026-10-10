import sys

import aioconsole
import lmstudio as lms

import GameContext
import Console

def handle_prediction_fragment(fragment: lms.LlmPredictionFragment):
    if fragment.reasoning_type == "reasoning":
        print(fragment.content, end="", file=sys.stderr)
    elif fragment.reasoning_type == "reasoningEndTag":
        print()
    else:
        print(fragment.content, end="")

async def run_adventure_setup(model: lms.AsyncLLM, memory: GameContext.GameContext, config: lms.LlmPredictionConfigDict):
    print("WELCOME TO YOUR TEXT RPG ADVENTURE")

    theme: str = await aioconsole.ainput("Enter your adventure theme: ")

    memory.set_adventure_theme(theme)

    start_prompt = f"Begin the adventure based on the chosen theme: {theme}"
    memory.add_player_action(start_prompt)

    print("Generating adventure...\n")

    ##full_response = ""

    await Console.prompt_user(model, memory, config)

    ## async for fragment in await model.respond_stream(memory.get_chat_object(), config=config, on_prediction_fragment=handle_prediction_fragment):
    ##    full_response += fragment.content
    ## print()

    ##memory.add_assistant_response(full_response)
