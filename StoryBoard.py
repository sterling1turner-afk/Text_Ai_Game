
import lmstudio as lms

class Storyboard:
    _storyboard: list[str] = []
    _notes: list[str] = []
    _event = 0

    @staticmethod
    def get_tools() -> list[lms.ToolFunctionDef]:
        return [
            lms.ToolFunctionDef.from_callable(
                Storyboard.create_story_board,
                name="createStoryBoard",
                description="Create a new story board. With a current event. The story board should contain the current event given with the future event planned out and the past event if available. This works as a reference moving forward in the story",
            ),
            lms.ToolFunctionDef.from_callable(
                Storyboard.finish_story_event,
                name="finishStoryEvent",
                description="End the current event and move the plot forward into the next event. Use the note input to keep important information relevant to that plot point that will impact the plot moving forward and that you might need to reference.",
            ),
            lms.ToolFunctionDef.from_callable(
                Storyboard.get_surrounding_story_board_events,
                name="getPastPresentAndFutureStoryBoardEvents",
                description="Returns information about the most recent, current, and next events. Your notes for the most recent event will appear here, so use them to inform your future self about what happened in that plot point, how plot points were resolved, and where the story currently sits.",
            )
        ]



    @staticmethod
    def create_story_board(story: str):
        Storyboard._storyboard = story.split("---")

    @staticmethod
    def finish_story_event(notes: str):
        Storyboard._notes.append(notes)
        Storyboard._event += 1

    @staticmethod
    def get_surrounding_story_board_events() -> dict[str, str | tuple[str, str]]:
        var = {"current event": Storyboard._storyboard[Storyboard._event]}
        if Storyboard._event > 0:
            var.update({"last event": (Storyboard._storyboard[Storyboard._event - 1], Storyboard._notes[Storyboard._event - 1])})
        elif Storyboard._event < len(Storyboard._storyboard):
            var.update({"next event": Storyboard._storyboard[Storyboard._event + 1]})
        return var