

class GameMemory:
    def __init__(self, system_prompt: str, seed: int) -> None:
        self.system_prompt = system_prompt
        self.SEED = seed

        self._history_messages = [
            {"role": "system", "content": self.system_prompt},
        ]

    def add_player_action(self, action_text: str) -> None:
        self._history_messages.append({"role": "player", "content": action_text})

    def add_assistant_response(self, response_text: str) -> None:
        self._history_messages.append({"role": "assistant", "content": response_text})

