from openai import OpenAI
from src.models.alice_ml import OutputDTO

client = OpenAI()


def generate_text(messages: list[dict]):
    return (
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        .choices[0]
        .message.content
    )
