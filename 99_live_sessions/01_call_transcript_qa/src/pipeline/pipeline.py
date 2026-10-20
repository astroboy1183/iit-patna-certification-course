import pandas as pd
from tqdm import tqdm


def run_classification(df: pd.DataFrame, classification_chain):
    results = []

    for i, row in tqdm(df.iterrows(), total=len(df), desc="Classifying Calls"):
        try:
            response = classification_chain.invoke(row["transcript"])
            results.append(
                {
                    "call_id": row["call_id"],
                    "predicted_call_type": response.call_type,
                    "confidence": response.confidence,
                }
            )

        except Exception as e:
            print(f"Error classifying call {row['call_id']}: {e}")
            results.append(
                {
                    "call_id": row["call_id"],
                    "predicted_call_type": None,
                    "confidence": None,
                }
            )

    results_df = pd.DataFrame(results)
    df = df.merge(results_df, on="call_id")

    return df


def run_evaluations(
    transcript, eval_plan, tone_chain, knowledge_chain, resolution_chain
):
    results = {}

    if "tone_empathy" in eval_plan:
        try:
            tone_result = tone_chain.invoke({"transcript": transcript})
            results["tone"] = tone_result.model_dump()
        except Exception as e:
            results["tone"] = {"error": str(e)}

    if "knowledge_accuracy" in eval_plan:
        try:
            knowledge_result = knowledge_chain.invoke({"transcript": transcript})
            results["knowledge"] = knowledge_result.model_dump()
        except Exception as e:
            results["knowledge"] = {"error": str(e)}

    if "resolution_quality" in eval_plan:
        try:
            resolution_result = resolution_chain.invoke({"transcript": transcript})
            results["resolution"] = resolution_result.model_dump()
        except Exception as e:
            results["resolution"] = {"error": str(e)}

    return results


def apply_evaluations(df, tone_chain, knowledge_chain, resolution_chain):

    evaluation_outputs = []

    for i, row in tqdm(df.iterrows(), total=len(df), desc="Running Evaluations"):
        output = run_evaluations(
            row["transcript"],
            row["evaluation_plan"],
            tone_chain,
            knowledge_chain,
            resolution_chain,
        )

        evaluation_outputs.append(
            {"call_id": row["call_id"], "evaluation_outputs": output}
        )

    eval_df = pd.DataFrame(evaluation_outputs)
    df = df.merge(eval_df, on="call_id")

    return df


def generate_final_report(evaluation_report, final_chain):
    try:
        report = final_chain.invoke({"evaluation_outputs": evaluation_report})
        return {"summary": report.summary, "recommendation": report.recommendation}
    except Exception as e:
        return {"summary": None, "recommendation": None, "error": str(e)}


def apply_final_reports(df, final_chain):
    final_reports = []

    for i, row in tqdm(df.iterrows(), total=len(df), desc="Generating Final Reports"):
        final_report = generate_final_report(row["evaluation_outputs"], final_chain)
        final_reports.append(
            {
                "call_id": row["call_id"],
                "summary": final_report.get("summary"),
                "recommendation": final_report.get("recommendation"),
            }
        )

    final_df = pd.DataFrame(final_reports)
    df = df.merge(final_df, on="call_id")

    return df
