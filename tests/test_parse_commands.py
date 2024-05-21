from simulate import extract_commands_from_text, extract_attributes_from_info, Command


def test_commands():
    content = '''
[Ctrl+U]
'''
    result = extract_commands_from_text(content)
    expected_result = [Command('Ctrl+U', 0, 1, True)]
    assert result == expected_result, f"Expected {expected_result}, got {result}"

def test_commands_repeat():
    content = '''
[j*5sleep=0.1]
'''
    result = extract_commands_from_text(content)
    expected_result = [Command('j', 0.0, 0.1, True), Command('j', 0.0, 0.1, True), Command('j', 0.0, 0.1, True), Command('j', 0.0, 0.1, True), Command('j', 0.0, 0.1, True)]
    assert result == expected_result, f"Expected {expected_result}, got {result}"

def test_quit_less():
    content = '''
```bash enter=false
q
```
'''
    result = extract_commands_from_text(content)
    expected_result = [Command('q\n', 0.0, 1.0, False, wait_for_prompt=True)]
    assert result == expected_result, f"Expected {expected_result}, got {result}"

def test_quit_less_with_more_sleep():
    content = '''
```bash enter=false sleep=2 sleepBefore=1
q
```
'''
    result = extract_commands_from_text(content)
    expected_result = [Command('q\n', 1.0, 2.0, False, wait_for_prompt=True)]
    assert result == expected_result, f"Expected {expected_result}, got {result}"

def test_run_ollama():
    content = '''
```bash
ollama run mistral --verbose
```
'''
    result = extract_commands_from_text(content)
    expected_result = [Command('ollama run mistral --verbose\n', 0.0, 1.0, True, wait_for_prompt=True)]
    assert result == expected_result, f"Expected {expected_result}, got {result}"

def test_soft_enter():
    content = '''
```bash soft_enter=true
import logging
import sys
```
'''
    result = extract_commands_from_text(content)
    expected_result = [
        Command('import logging', wait_for_prompt=False, press_enter=False),
        Command('Ctrl+Q', 0.0, 1.0, True),
        Command('Ctrl+J', 0.0, 1.0, True),
        Command('import sys', wait_for_prompt=True, press_enter=True)
    ]
    assert result == expected_result, f"Expected {expected_result}, got {result}"

def test_extract_attributes():
    result = extract_attributes_from_info("bash soft_enter=true")
    expected_result = {
        "soft_enter": "true"
    }
    assert result == expected_result, f"Expected {expected_result}, got {result}"