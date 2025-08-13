import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary_script(paper_text: str, length: str = "medium") -> str:
    if length == "short":
        prompt_length = "Provide a very brief summary (2-3 sentences) highlighting the main ideas."
    elif length == "long":
        prompt_length = "Provide a detailed summary with examples and explanations."
    else:  # medium or default
        prompt_length = "Provide a clear and concise summary covering the key points."

    prompt = (
        "You are a skilled explainer. Summarize the following research paper text "
        "into a clear, beginner-friendly explanation that could be narrated in a video:\n\n"
        f"{paper_text}\n\n{prompt_length}\n\nSummary:"
    )
    try:
        response = client.chat.completions.create(
            #model="gpt-4o-mini",
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=600,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "Failed to generate summary."