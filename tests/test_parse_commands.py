from simulate import extract_commands_from_text


def test_commands():
    content = '''
[Ctrl+U]
'''
    result = extract_commands_from_text(content)
    expected_result = [('Ctrl+U', 1, True)]
    assert result == expected_result, f"Expected {expected_result}, got {result}"

def test_commands_repeat():
    content = '''
[j*5sleep=0.1]
'''
    result = extract_commands_from_text(content)
    expected_result = [('j', 0.1, True), ('j', 0.1, True), ('j', 0.1, True), ('j', 0.1, True), ('j', 0.1, True)]
    assert result == expected_result, f"Expected {expected_result}, got {result}"

def test_quit_less():
    content = '''
```bash enter=false
q
```
'''
    result = extract_commands_from_text(content)
    expected_result = [('q', 1.0, False)]
    assert result == expected_result, f"Expected {expected_result}, got {result}"

def test_run_ollama():
    content = '''
```bash
ollama run mistral --verbose
```
'''
    result = extract_commands_from_text(content)
    expected_result = [('ollama run mistral --verbose', 1.0, True)]
    assert result == expected_result, f"Expected {expected_result}, got {result}"