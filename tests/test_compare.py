from difflib import SequenceMatcher

import re

def count_leading_spaces(s):
    match = re.match(r'\s*', s)
    return len(match.group()) if match else 0

def compute_line_diff(before, after):
    commands = []

    i = 0
    while i < len(before) and i < len(after) and before[i] == after[i]:
        i += 1
    chars_to_delete = len(before) - i

    if chars_to_delete > 0:
        commands.append(f"[Backspace*{chars_to_delete}sleep=0.1]")

        leading_spaces = count_leading_spaces(after[i:])
        if leading_spaces > 0:
            commands.append(f"[Space*{chars_to_delete}sleep=0.1]")

        commands.append(f"""```sql
{after[i:].strip()}
```""")

    return commands

def compute_multi_line_diff(before, after): 
    before_rows = before.split("\n")
    after_rows = after.split("\n")

    commands = []
    for b, a in zip(before_rows, after_rows):
        commands += compute_line_diff(b, a)

    return commands

def test_compute_diff_simple():
    before = "FROM foo SELECT *;"
    after = "FROM foo SELECT field1;"

    result = compute_line_diff(before, after)
    expected_result = [
        "[Backspace*2sleep=0.1]",
        """```sql
field1;
```"""
    ]
    assert result == expected_result, f"Expected {expected_result}, got {result}"

def test_compute_diff_wrap_function():
    before = "FROM foo SELECT field1;"
    after = "FROM foo SELECT splitByString('/', field1)[1];"
    result = compute_line_diff(before, after)
    expected_result = [
        "[Backspace*7sleep=0.1]",
        """```sql
splitByString('/', field1)[1];
```""",
]
    assert result == expected_result, f"Expected {expected_result}, got {result}"

def test_compute_diff_append():
    before = "FROM foo SELECT field2;"
    after = "FROM foo SELECT field2 LIMIT 10;"
    result = compute_line_diff(before, after)
    expected_result = [
        "[Backspace*1sleep=0.1]",
         "[Space*1sleep=0.1]",
        """```sql
LIMIT 10;
```""",
]
    assert result == expected_result, f"Expected {expected_result}, got {result}"

def test_compute_multi_line_diff_append():
    before = """FROM foo
SELECT field2;"""
    after = """FROM foo 
SELECT field2 LIMIT 10;"""
    result = compute_multi_line_diff(before, after)
    expected_result = [
        "[Backspace*1sleep=0.1]",
        "[Space*1sleep=0.1]",
        """```sql
LIMIT 10;
```""",
]
    # for item in expected_result:
    #     print(item)
    #     print("")
    assert result == expected_result, f"Expected {expected_result}, got {result}"
    # assert False
    