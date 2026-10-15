"""Ask a Claude model whether one re:Invent rumor is true.

Usage: python check_claim.py [CLAIM_ID]   (default: C-02)
"""

import csv
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from langsmith import Client as LangSmithClient
from langsmith import traceable
from langsmith.run_helpers import get_current_run_tree

load_dotenv()

MODEL = "claude-opus-5-5"
CSV_PATH = Path(__file__).parent / "data" / "reinvent_candidates.csv"

client = anthropic.Anthropic()


def load_claim(claim_id: str) -> dict:
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["candidate_id"] == claim_id:
                return row
    raise SystemExit(f"Claim {claim_id} not found in {CSV_PATH}")


@traceable(name="check_claim", run_type="chain")
def check_claim(claim: dict) -> dict:
    prompt = (
        "You are fact-checking a rumor about AWS re:Invent 2025.\n\n"
        f"Claim: {claim['claim_text']}\n"
        f"Service: {claim['claimed_service']}\n"
        f"Source: {claim['origin_source_name']} ({claim['origin_source_url']}), "
        f"published {claim['origin_published_date']}\n\n"
        "Is this claim true, false, or unverified? Start your answer with one word "
        "(TRUE, FALSE, or UNVERIFIED), then give a short justification."
    )
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=16000,
        output_config={"effort": "medium"},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        messages=[{"role": "user", "content": prompt}],
    )
    if response.stop_reason == "refusal":
        answer = "REFUSED"
    else:
        answer = "".join(b.text for b in response.content if b.type == "text").strip()

    run = get_current_run_tree()
    return {"model": response.model, "answer": answer, "run_id": str(run.id) if run else None}


def main() -> None:
    claim_id = sys.argv[1] if len(sys.argv) > 1 else "C-02"
    claim = load_claim(claim_id)
    result = check_claim(claim)

    print(f"Claim {claim_id}: {claim['claim_text']}")
    print(f"Model: {result['model']}")
    print(f"Answer:\n{result['answer']}")

    if result["run_id"]:
        ls = LangSmithClient()
        ls.flush()
        print(f"Public LangSmith trace: {ls.share_run(result['run_id'])}")


if __name__ == "__main__":
    main()
