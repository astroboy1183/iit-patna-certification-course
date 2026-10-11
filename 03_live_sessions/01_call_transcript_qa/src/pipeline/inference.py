"""Run the call-transcript QA pipeline: classify -> route -> evaluate -> report.

Two ways to use it, both run from the project root
(config and data paths are relative to it):

    # every transcript in a file, results saved to data/output.xlsx
    python -m src.pipeline.inference

    # a single transcript, results printed
    python -m src.pipeline.inference --transcript "Customer: I was charged twice. ..."
"""

import argparse
import json
import pprint

import pandas as pd

from src.components.classification import get_classification_prompt
from src.components.evaluation import (
    get_knowledge_chain,
    get_resolution_chain,
    get_tone_chain,
)
from src.components.reporting import get_final_report_chain
from src.components.router import apply_routing, route_call
from src.pipeline.pipeline import (
    apply_evaluations,
    apply_final_reports,
    generate_final_report,
    run_classification,
    run_evaluations,
)
from src.utils.config_loader import load_config
from src.utils.data_loader import load_transcripts
from src.utils.llm_loader import load_llm


def build_chains(llm, config):
    """Build every chain once, so steps reuse them instead of rebuilding per call."""
    return {
        "classification": get_classification_prompt(llm, config),
        "tone": get_tone_chain(llm),
        "knowledge": get_knowledge_chain(llm),
        "resolution": get_resolution_chain(llm),
        "final": get_final_report_chain(llm),
    }


def load_chains():
    config = load_config()
    llm = load_llm(config)
    return build_chains(llm, config)


def infer_transcript(transcript, chains):
    """Run the whole pipeline on one transcript and return a dict with every result."""
    classification = chains["classification"].invoke(transcript)
    evaluation_plan = route_call(classification.call_type)
    evaluation_outputs = run_evaluations(
        transcript,
        evaluation_plan,
        chains["tone"],
        chains["knowledge"],
        chains["resolution"],
    )
    report = generate_final_report(evaluation_outputs, chains["final"])

    return {
        "predicted_call_type": classification.call_type,
        "confidence": classification.confidence,
        "evaluation_plan": evaluation_plan,
        "evaluation_outputs": evaluation_outputs,
        "summary": report.get("summary"),
        "recommendation": report.get("recommendation"),
    }


def run_inference(data_path="data/transcripts.xlsx", output_path="data/output.xlsx"):
    """Run the pipeline on every transcript in data_path; save to output_path if given."""
    chains = load_chains()

    df = load_transcripts(data_path)
    df = run_classification(df, chains["classification"])
    df = apply_routing(df)
    df = apply_evaluations(
        df, chains["tone"], chains["knowledge"], chains["resolution"]
    )
    df = apply_final_reports(df, chains["final"])

    if output_path:
        save_results(df, output_path)
        print(f"Results saved to {output_path}")
    return df


def save_results(df, output_path):
    """Save to .xlsx or .csv.

    Excel can't store Python lists/dicts in a cell, so those are saved as JSON text.
    """
    out = df.copy()
    for col in out.columns:
        if out[col].map(lambda v: isinstance(v, (list, dict))).any():
            out[col] = out[col].map(
                lambda v: json.dumps(v) if isinstance(v, (list, dict)) else v
            )

    if str(output_path).endswith(".csv"):
        out.to_csv(output_path, index=False)
    else:
        out.to_excel(output_path, index=False)


def main():
    parser = argparse.ArgumentParser(
        description="Classify, evaluate and report on customer support calls."
    )
    parser.add_argument(
        "--data", default="data/transcripts.xlsx", help="transcripts file (.xlsx)"
    )
    parser.add_argument(
        "--output", default="data/output.xlsx", help="results file (.xlsx or .csv)"
    )
    parser.add_argument(
        "--transcript", help="evaluate one transcript instead of a file"
    )
    args = parser.parse_args()

    if args.transcript:
        result = infer_transcript(args.transcript, load_chains())
        pprint.pprint(result, sort_dicts=False, width=100)
    else:
        df = run_inference(args.data, args.output)
        with pd.option_context("display.max_columns", None, "display.width", 200):
            columns = [
                "call_id",
                "expected_call_type",
                "predicted_call_type",
                "summary",
            ]
            print(df[columns])


if __name__ == "__main__":
    main()
