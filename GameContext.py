from lmstudio import Chat


class GameContext:
    def __init__(self, system_prompt: str, starting_system_prompt: str) -> None:
        self.system_prompt = system_prompt
        self.starting_system_prompt = starting_system_prompt
        self.theme = ""
        self.character = ""
        self.objective = ""
        self._history_messages = []

    def set_adventure_context(self, chosen_theme: str, chosen_character: str, character_goal: str) -> None:
        self.theme = chosen_theme.strip()
        self.character = chosen_character.strip()
        self.objective = character_goal.strip()
        self.system_instructions = f"""
{self.system_prompt}

# ADVENTURE THEME
The genre, setting, and aesthetic of the game must strictly follow: {self.theme}

# PLAYER CHARACTER
The player character is roleplaying as: {self.character}

# MAIN OBJECTIVE
The original goal the character is working towards is: {self.objective}
"""
        start_game = self.system_instructions + self.starting_system_prompt
        self._history_messages = [
            {"role": "system", "content": start_game.strip()},
        ]

    def add_player_action(self, action_text: str) -> None:
        self._history_messages.append({"role": "user", "content": action_text})

    def add_assistant_response(self, response_text: str) -> None:
        self._history_messages.append({"role": "assistant", "content": response_text})

    def get_chat_object(self) -> Chat:
        return Chat.from_history({"messages": self._history_messages})

    def set_system_prompt(self) -> None:
        self._history_messages[0]["content"] = self.system_instructions.strip()