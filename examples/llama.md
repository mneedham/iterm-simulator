[Ctrl+L]

```
less pyproject.toml
```

```bash enter=false
q
```


```
poetry run python
```

[Ctrl+L]

```bash sleep=1
from llama_index.llms import Ollama
```

```bash sleep=1
llm = Ollama(model="mistral:instruct")
```

```python
with open('bbc.txt', 'r') as bbc_file:
  text = bbc_file.read()
```

[Enter]

```python sleep=2
text[:500]
```

[Ctrl+L]

```python sleep=2
response = llm.complete(f"""
Which people are mentioned in this article: {text}
""")
```

```python sleep=1
response
```

[Ctrl+L]

```python sleep=3
print(response.text)
```


```bash sleep=3
exit()
```