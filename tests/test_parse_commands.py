from simulate import extract_commands_from_text, Command


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
    expected_result = [Command('q', 0.0, 1.0, False)]
    assert result == expected_result, f"Expected {expected_result}, got {result}"

def test_quit_less_with_more_sleep():
    content = '''
```bash enter=false sleep=2 sleepBefore=1
q
```
'''
    result = extract_commands_from_text(content)
    expected_result = [Command('q', 1.0, 2.0, False)]
    assert result == expected_result, f"Expected {expected_result}, got {result}"

def test_run_ollama():
    content = '''
```bash
ollama run mistral --verbose
```
'''
    result = extract_commands_from_text(content)
    expected_result = [Command('ollama run mistral --verbose', 0.0, 1.0, True)]
    assert result == expected_result, f"Expected {expected_result}, got {result}"