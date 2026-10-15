# fact-checker

Asks a Claude model (via OpenRouter) whether a rumor from `data/reinvent_candidates.csv` (re:Invent candidate items, collected 27 Oct – 2 Nov 2025) is true.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then fill in the keys; MODEL picks the model
python check_claim.py C-02
```

## Result for C-02

**Claim:** AWS will launch a managed quantum computing Region in us-east-1 at re:Invent 2025.

- **Model id:** `anthropic/claude-sonnet-5.5` (OpenRouter)
- **Answer:** **UNVERIFIED, and probably false as worded.** The model knows of no AWS announcement or credible report of a "managed quantum computing Region" in us-east-1. AWS offers quantum computing through Amazon Braket, which runs inside existing Regions, so a "quantum Region" doesn't match any AWS construct.
- **Official AWS page named:** No, the model's answer does not name any aws.amazon.com page (or any URL at all).
- **Public LangSmith trace:** https://smith.langchain.com/public/d188b9bc-27d2-4931-8170-79ab2666ba9a/r
