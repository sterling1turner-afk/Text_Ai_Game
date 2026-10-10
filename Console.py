import asyncio
import sys

import lmstudio as lms
import msgspec

import GameContext
import GameState
import StoryBoard


class Console:
    currentInferenceResults: str = ""
    currentInput: asyncio.Task | None = None
    currentInference: asyncio.Task | None = None
    currentLineLength: int = 0

    @staticmethod
    def handle_prediction_fragment(fragment: lms.LlmPredictionFragment, _: int, should_print: bool):
        if fragment.reasoning_type == "reasoningStartTag":
            pass
        elif fragment.reasoning_type == "reasoning":
            # print(fragment.content, end="", file=sys.stderr)
            pass
        elif fragment.reasoning_type == "reasoningEndTag":
            # print()
            pass
        else:
            if should_print:
                print(fragment.content, end = "", flush=True)
            Console.currentInferenceResults += fragment.content


    @staticmethod
    async def launch_inference(model: lms.AsyncLLM, memory: GameContext.GameContext, config: lms.LlmPredictionConfigDict, should_print: bool=True):
        Console.currentInferenceResults = ""
        try:
            await model.act(memory.get_chat_object(),
                            [*GameState.get_tools(), *StoryBoard.Storyboard.get_tools()],
                            config=config,
                            on_prediction_fragment=lambda x, i: Console.handle_prediction_fragment(x, i, should_print))
        except msgspec.ValidationError as _:
            pass
