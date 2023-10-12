[Ctrl+U]

[Ctrl+L]

```bash sleep=3
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "What is the sentiment of this sentence: The situation surrounding the video assistant referee is at crisis point."
 }' 2>/dev/null | jq -Cc | less -R
```

[j*32sleep=0.1]

```bash enter=false
q
```