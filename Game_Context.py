from lmstudio import Chat


class GameContext:
    def __init__(self, system_prompt: str) -> None:
        self.system_prompt = system_prompt
        self.theme = ""
        self._history_messages = []

    def set_adventure_theme(self, chosen_theme: str) -> None:
        self.theme = chosen_theme.strip()
        full_system_instructions = f"""
{self.system_prompt}

# ADVENTURE THEME
The genre, setting, and aesthetic of the game must strictly follow: {self.theme}
"""
        self._history_messages = [
            {"role": "system", "content": full_system_instructions.strip()},
        ]

    def add_player_action(self, action_text: str) -> None:
        self._history_messages.append({"role": "user", "content": action_text})

    def add_assistant_response(self, response_text: str) -> None:
        self._history_messages.append({"role": "assistant", "content": response_text})

    def get_chat_object(self) -> Chat:
        return Chat.from_history({"messages": self._history_messages})