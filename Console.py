import asyncio

import lmstudio as lms
import msgspec

import GameContext

class Console:
    currentInferenceResults: str = ""
    currentInput: asyncio.Task | None = None
    currentInference: asyncio.Task | None = None
    currentLineLength: int = 0

    @staticmethod
    def handle_prediction_fragment(fragment: lms.LlmPredictionFragment):
        if fragment.reasoning_type == "reasoning":
            pass
        elif fragment.reasoning_type == "reasoningEndTag":
            pass
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
