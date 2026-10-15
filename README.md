# fact-checker

Asks a Claude model (via OpenRouter) whether a rumor from `data/reinvent_candidates.csv` (re:Invent candidate items, collected 27 Oct – 2 Nov 2025) is true.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then fill in OPENROUTER_API_KEY and LANGSMITH_API_KEY
python check_claim.py C-02
```

## Result for C-02

**Claim:** AWS will launch a managed quantum computing Region in us-east-1 at re:Invent 2025.

- **Model id:** `anthropic/claude-opus-5.5` (OpenRouter)
- **Answer:** _TBD — run `python check_claim.py C-02`_
- **Public LangSmith trace:** _TBD_
