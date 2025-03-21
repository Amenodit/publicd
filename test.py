import openai
from openai import AuthenticationError  # Correct error import

# Replace with your actual API key
openai.api_key = "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"

try:
    response = openai.models.list()
    print("✅ API Key is valid. Models available:")
    for model in response:
        print(model.id)
except AuthenticationError:
    print("❌ Invalid API key!")
except Exception as e:
    print(f"⚠️ Some other error occurred: {e}")
response = openai.images.generate(
    prompt="A futuristic city at sunset with flying cars",
    n=1,
    size="512x512"
)
print(response.data[0].url)
