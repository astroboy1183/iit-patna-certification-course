import os

from langchain_core.prompts import PromptTemplate

blog_prompt = PromptTemplate(
    input_variable=["topic", "audience", "tone"],
    template="You are a professional blog writer.\n"
    "write a short , engaging blog post about {topic} for {audience}."
    "Use a {tone} tone\n"
    "Include:\n"
    "-a catchy title\n"
    "-2 short paragraphs(2-3 sentences each)\n"
    "-A Closing line encouraging readers to comment and share\n",
)

os.makedirs("08_prompt_reuse_yaml", exist_ok=True)

save_path = "08_prompt_reuse_yaml/blog_prompt.yaml"
blog_prompt.save(save_path)

print(f"Prompt saved to {save_path}")
