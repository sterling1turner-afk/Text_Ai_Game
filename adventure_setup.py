import aioconsole
import lmstudio as lms
from Game_Context import GameContext

## input string, output string

async def run_adventure_setup(model: lms.AsyncLLM, memory: GameContext, config: lms.LlmPredictionConfigDict):
    print("WELCOME TO YOUR TEXT RPG ADVENTURE")

    theme: str = await aioconsole.ainput("Enter your adventure theme: ")

    memory.set_adventure_theme(theme)

    start_prompt = f"Begin the adventure based on the chosen theme: {theme}"
    memory.add_player_action(start_prompt)

    print("Generating adventure...\n")

    full_response = ""

    async for fragment in await model.respond_stream(memory.get_chat_object(), config=config):
        print(fragment.content, end="", flush=True)
        full_response += fragment.content
    print()

    memory.add_assistant_response(full_response)
