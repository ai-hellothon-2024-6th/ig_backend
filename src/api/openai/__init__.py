from openai import OpenAI
from src.models.alice_ml import FilteredTextResponseDTO

client = OpenAI()


def generate_text(messages: list[dict]):
    return (
        client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=messages,
            response_format=FilteredTextResponseDTO,
        )
        .choices[0]
        .message.parsed
    )
