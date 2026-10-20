from llm_factory import get_llm


def main():
    print("Langchain llm component demo:")
    llm = get_llm()
    prompt = "Explain Langchain in a suitable way for a 10 year old."
    print(f"Sending prompt to: {type(llm).__name__}\n")

    response = llm.invoke(prompt)
    print("llm's response:\n", response.content)


if __name__ == "__main__":
    main()
