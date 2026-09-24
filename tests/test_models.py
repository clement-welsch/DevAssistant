from openai import OpenAI

from config import LMSTUDIO_API_KEY, LMSTUDIO_BASE_URL


client = OpenAI(
    base_url=LMSTUDIO_BASE_URL,
    api_key=LMSTUDIO_API_KEY,
)

models = client.models.list()

for model in models.data:
    print(model.id)