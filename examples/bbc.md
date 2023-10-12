[Ctrl+L]

```
less bbc.txt
```

[j*32sleep=0.2]

```bash enter=false
q
```

```bash sleep=3
ollama run mistral --verbose \
"Please can you summarise this article: $(cat bbc.txt)"
```

[Ctrl+L]

```bash sleep=3
ollama run mistral --verbose \
"Can you pull out 5 bullet points from the following article: $(cat bbc.txt)"
```

[Ctrl+L]

```bash sleep=3
ollama run mistral --verbose \
"If you had to categorise this article, what tags would you use?: $(cat bbc.txt)"
```