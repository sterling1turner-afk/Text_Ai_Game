import asyncio
import sys

import lmstudio as lms
import msgspec

import GameContext
import GameState

class Console:
    currentInferenceResults: str = ""
    currentInput: asyncio.Task | None = None
    currentInference: asyncio.Task | None = None
    currentLineLength: int = 0

    @staticmethod
    def handle_prediction_fragment(fragment: lms.LlmPredictionFragment):
        if fragment.reasoning_type == "reasoning":
            print(fragment.content, end="", file=sys.stderr)
        elif fragment.reasoning_type == "reasoningEndTag":
            print()
        else:
            print(fragment.content, end = "", flush=True)
            Console.currentInferenceResults += fragment.content


    @staticmethod
    async def launch_inference(model: lms.AsyncLLM, memory: GameContext.GameContext, config: lms.LlmPredictionConfigDict):
        Console.currentInferenceResults = ""
        try:
            async for _ in await model.respond_stream(memory.get_chat_object(),
                                                      config=config,
                                                      on_prediction_fragment=lambda x: Console.handle_prediction_fragment(x)):
                pass
        except msgspec.ValidationError as _:
            pass
