from ollama import chat


def ask_llm(context, question):
    prompt = f"""
You are answering questions ONLY using the provided REDCap data.

REDCap Data:
{context}

Question:
{question}

If the answer cannot be found in the data, say:
"I cannot answer based on the provided REDCap records."
"""

    response = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]