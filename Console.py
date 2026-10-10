import asyncio
import sys

import lmstudio as lms

import GameContext
import GameState

currentInferenceResults: str = ""
currentInput: asyncio.Task | None = None
currentInference: asyncio.Task | None = None
currentLineLength: int = 0

def handle_prediction_fragment(fragment: lms.LlmPredictionFragment, i: int):
    if fragment.reasoning_type == "reasoning":
        # print(fragment.content, end="", file=sys.stderr)
        pass
    elif fragment.reasoning_type == "reasoningEndTag":
        # print()
        pass
    else:
        print(fragment.content, end = "", flush=True)
        sys.modules[__name__].currentInferenceResults += fragment.content


async def prompt_user(model: lms.AsyncLLM, memory: GameContext.GameContext, config: lms.LlmPredictionConfigDict):
    await model.act(memory.get_chat_object(), tools=GameState.get_tools(), config=config, on_prediction_fragment=lambda x, i: handle_prediction_fragment(x, i))