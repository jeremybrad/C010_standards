# Model Bootstrap Checklist

Use this script notebook when preparing Houston’s inference fleet. Run commands on each host in descending priority so the cloud tier is ready first, followed by workstation and Mac backups.

## Directory Layout
```
~/models/
├── ollama/
│   ├── qwen-coder:480b               # cloud primary (managed remotely)
│   ├── qwen2.5-coder:32b-q4_K_M      # RTX workstation
│   ├── qwen3:72b-q4_K_M              # RTX workstation (general reasoning)
│   ├── qwen2.5-coder:14b-q4_K_M      # Mac fallback
│   ├── mistral:7b-q4_K_M             # lightweight fallback
│   └── fallbacks/
│       ├── deepseek:670b             # optional local mirror of cloud alt
│       └── gpt-oss:120b              # optional local mirror of cloud alt
└── config/
    └── houston-models.json           # use-case → model priority mapping
```

## Cloud Bootstrap (primary models)
```bash
# Run on cloud console (managed Ollama instance)
ollama pull qwen-coder:480b
ollama pull deepseek:670b
ollama pull gpt-oss:120b
```

## RTX Workstation
```bash
# Ensure Ollama daemon is running
ollama serve &

# Download high-capacity fallbacks
ollama pull qwen2.5-coder:32b-q4_K_M
ollama pull qwen3:72b-q4_K_M
```

## Local Mac
```bash
# Keep smaller models for offline work
ollama pull qwen2.5-coder:14b-q4_K_M
ollama pull mistral:7b-q4_K_M
```

## Config Sync
1. Edit `30_config/houston.json` to list all hosts, ordered by priority.
2. Update `~/models/config/houston-models.json` to map use cases.
3. Check both files into secure config storage (not this repo) and document hash receipts in `70_evidence/`.

## Validation Hooks
Once validators land in `validators/`, add checks that
- each configured model matches an installed tag (exact suffix), and
- fallback chains include at least one local model.
