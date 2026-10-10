import asyncio
import sys

import lmstudio as lms

import GameContext

currentInferenceResults: str = ""
currentInput: asyncio.Task | None = None
currentInference: asyncio.Task | None = None
currentLineLength: int = 0

def handle_prediction_fragment(fragment: lms.LlmPredictionFragment):
    if fragment.reasoning_type == "reasoning":
        print(fragment.content, end="", file=sys.stderr)
    elif fragment.reasoning_type == "reasoningEndTag":
        print()
    else:
        print(fragment.content, end = "", flush=True)
        sys.modules[__name__].currentInferenceResults += fragment.content


async def prompt_user(model: lms.AsyncLLM, memory: GameContext.GameContext, config: lms.LlmPredictionConfigDict):
    async for fragment in await model.respond_stream(
            memory.get_chat_object(), config=config, on_prediction_fragment=lambda x: handle_prediction_fragment(x)
    ):
        pass