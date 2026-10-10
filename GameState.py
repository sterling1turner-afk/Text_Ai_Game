import json

import lmstudio as lms

def get_tools() -> list[lms.ToolFunctionDef]:
    return [
        lms.ToolFunctionDef.from_callable(
            update_variable,
            name="updateVariable",
            description="Set the value of the given variable to the given data value."
        ),
        lms.ToolFunctionDef.from_callable(
            list_variables,
            name="listVariables",
            description="List all the recorded variables."
        ),
        lms.ToolFunctionDef.from_callable(
            resolve_pointer,
            name="resolvePointer",
            description="Dereferences a JSON pointer and returns the value."
        ),
        lms.ToolFunctionDef.from_callable(
            remove_variable,
            name="removeVariable",
            description="Remove the variable pointed to by the given JSON pointer."
        )

    ]

# Variable name: JSON object
_dict: dict = {}

def update_variable(pointer: str, data: str) -> None:
    arr: list[str] = pointer.lstrip('/').split('/')
    d: dict = _dict
    for item in range(len(arr) - 1):
        if isinstance(d, list):
            if int(arr[item]) < len(d): d = d[int(arr[item])]
            else:
                d.extend([[] if arr[item + 1].isdecimal() else {}] * (int(arr[item]) - len(d) + 1))
                d = d[int(arr[item])]
        else:
            if arr[item] in d:
                d = d[arr[item]]
            else:
                d[arr[item]] = [] if arr[item + 1].isdecimal() else {}
                d = d[arr[item]]
    if isinstance(d, list):
        if int(arr[-1]) < len(d):
            d[int(arr[-1])] = data
        else:
            d.extend([""] * (int(arr[-1]) - len(d) + 1))
            d[int(arr[-1])] = data
    else: d[arr[-1]] = data

def list_variables(pointer: str) -> list[str] | int | str:
    arr: list[str] = pointer.lstrip('/').split('/')
    d: dict = _dict
    for item in arr:
        if isinstance(d, list): d = d[int(item)]
        else: d = d[item]
    if isinstance(d, list): return len(d)
    elif isinstance(d, dict): return list(d.keys())
    else: return str(d)

def resolve_pointer(pointer: str) -> str:
    arr: list[str] = pointer.lstrip('/').split('/')
    d: dict = _dict
    for item in arr:
        if isinstance(d, list): d = d[int(item)]
        else: d = d[item]
    return str(d)

def remove_variable(pointer: str) -> None:
    arr: list[str] = pointer.lstrip('/').split('/')
    d: dict = _dict
    for item in range(len(arr) - 1):
        if isinstance(d, list): d = d[int(arr[item])]
        else: d = d[arr[item]]
    if isinstance(d, list): d.pop(int(arr[-1]))
    else: d.pop(arr[-1])

