[Ctrl+U]

[Ctrl+L]

```bash sleep=2
pygmentize \
  -O style=github-dark \
  -l Dockerfile \
  models/Modelfile-question-llama2-base | less
```

```bash enter=false
q
```

```bash sleep=2
ollama create \
  question-llama2-base \
  -f models/Modelfile-question-llama2-base
```
[Ctrl+L]

```bash sleep=2
pygmentize \
  -O style=github-dark \
  -l Dockerfile \
  models/Modelfile-question-llama2 | less
```

[j*10sleep=0.2]

```bash enter=false
q
```

```bash sleep=2
ollama create \
  question-llama2 \
  -f models/Modelfile-question-llama2
```
[Ctrl+L]
