import pytest
import GameState


@pytest.fixture(autouse=True)
def clear_state():
    """Resets the global GameState._dict state before and after each test."""
    GameState._dict.clear()
    yield
    GameState._dict.clear()


# ==========================================
# 1. Tests for update_variable
# ==========================================

def test_update_variable_flat():
    """Test setting a simple top-level variable."""
    GameState.update_variable("/name", "Hero")
    assert GameState._dict == {"name": "Hero"}


def test_update_variable_nested_object():
    """Test creating and updating nested dictionaries."""
    GameState.update_variable("/player/stats/hp", "100")
    assert GameState._dict == {"player": {"stats": {"hp": "100"}}}


def test_update_variable_auto_extend_array():
    """Test that arrays are created and auto-extended correctly based on index."""
    GameState.update_variable("/inventory/0", "Potion")
    GameState.update_variable("/inventory/2", "Shield")

    # Check that indices map correctly and unassigned gaps resolve safely
    assert GameState.resolve_pointer("/inventory/0") == "Potion"
    assert GameState.resolve_pointer("/inventory/2") == "Shield"


# ==========================================
# 2. Tests for resolve_pointer
# ==========================================

def test_resolve_pointer_success():
    """Test resolving pointers from nested objects and lists."""
    GameState._dict.update({
        "world": {
            "zones": ["forest", "cave", "castle"]
        }
    })

    assert GameState.resolve_pointer("/world/zones/1") == "cave"


def test_resolve_pointer_missing_key_raises_error():
    """Test that resolving a non-existent pointer path raises a KeyError/IndexError/TypeError."""
    GameState.update_variable("/status", "active")

    with pytest.raises((KeyError, IndexError, TypeError)):
        GameState.resolve_pointer("/nonexistent")


# ==========================================
# 3. Tests for list_variables
# ==========================================

def test_list_variables_dictionary_keys():
    """Test that listing variables on a dictionary returns its keys."""
    GameState.update_variable("/stats/strength", "15")
    GameState.update_variable("/stats/agility", "12")

    keys = GameState.list_variables("/stats")
    assert sorted(keys) == ["agility", "strength"]


def test_list_variables_array_length():
    """Test that listing variables on a list/array returns its integer length."""
    GameState.update_variable("/party/0", "Mage")
    GameState.update_variable("/party/1", "Warrior")

    assert GameState.list_variables("/party") == 2


def test_list_variables_primitive_value():
    """Test that listing a primitive leaf node returns its string representation."""
    GameState.update_variable("/player/name", "Arthur")

    assert GameState.list_variables("/player/name") == "Arthur"


# ==========================================
# 4. Tests for remove_variable
# ==========================================

def test_remove_variable_from_object():
    """Test removing a property key from an object dictionary."""
    GameState.update_variable("/config/theme", "dark")
    GameState.update_variable("/config/sound", "off")

    GameState.remove_variable("/config/sound")

    assert "sound" not in GameState._dict["config"]
    assert GameState.resolve_pointer("/config/theme") == "dark"


def test_remove_variable_from_array():
    """Test popping/removing an element from an array by index."""
    GameState.update_variable("/log/0", "Event A")
    GameState.update_variable("/log/1", "Event B")

    GameState.remove_variable("/log/0")

    # Index 0 is popped, shifting Event B to index 0
    assert GameState.resolve_pointer("/log/0") == "Event B"
    assert GameState.list_variables("/log") == 1