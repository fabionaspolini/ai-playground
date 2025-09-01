from openai import OpenAI

print(".:: 2-analyze-images ::.")

client = OpenAI(base_url="http://localhost:1234/v1")

# fail
response = client.responses.create(
    model="openai/gpt-oss-20b",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "What teams are playing in this image?",
                },
                {
                    "type": "input_image",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3b/LeBron_James_Layup_%28Cleveland_vs_Brooklyn_2018%29.jpg"
                }
            ]
        }
    ],
    temperature=0.1
)

print(response.output_text)
