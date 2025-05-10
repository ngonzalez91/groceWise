import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def compare_prices(items):
    prompt = "You are a shopping assistant. For the following receipt items, suggest cheaper alternatives or cost-saving tips.\n"
    for item in items:
        prompt += f"- {item['name']}: ${item['price']:.2f}\n"
    prompt += "Provide brief insights or tips."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{ "role": "user", "content": prompt }],
            max_tokens=150
        )
        suggestions = response['choices'][0]['message']['content']
        return suggestions.strip().split('\n')
    except Exception as e:
        return [f"Error generating insights: {e}"]
