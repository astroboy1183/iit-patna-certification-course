def route_call(call_type):
    if call_type == "billing" or call_type == "claims":
        return ["knowledge_accuracy", "resolution_quality"]
    elif call_type == "complaint":
        return ["tone_empathy", "resolution_quality"]
    elif call_type == "general_query":
        return ["knowledge_accuracy"]
    else:
        return ["knowledge_accuracy"]


def apply_routing(df):
    df["evaluation_plan"] = df["predicted_call_type"].apply(route_call)
    return df
