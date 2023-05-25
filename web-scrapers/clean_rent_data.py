import re
import openai
import tiktoken
import numpy as np
import pandas as pd

openai.api_key = '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'

encoding = tiktoken.get_encoding("cl100k_base")

# Read Data From JSON File
data = pd.read_json("./data/houses-for-rent.json")

# Remove KSH and Spaces From price Column
def clean_price(value):
    cleaned_value = re.sub('[^\d,]', '', value)
    cleaned_value = cleaned_value.replace(',', '')
    try:
        return int(cleaned_value)  # Convert to int
    except ValueError:
        return 0  # Return default value (0) for invalid values

data['price'] = data['price'].apply(clean_price)

data = data[["title", "location", "size", "price"]]

data["summarized"] = (
    "title: " + data.title.str.strip() + "; location: " + data.location.str.strip() + "; size: " +
    data["size"].astype(str).str.strip() + "; price: " + data.price.astype(str)
)

data["tokens"] = data.summarized.apply(lambda x: len(encoding.encode(x)))


def get_text_embedding(text, embeddingMode="text-embedding-ada-002"):
    result = openai.Embed.create(
        model=embeddingMode,
        documents=[text]
    )

    return result["embeddings"][0]["value"]


def get_data_embedding(data):
    return {
        (idx, r.title): get_text_embedding(r.summarized)
        for idx, r in data.iterrows()
    }


document_embeddings = get_data_embedding(data)
print(document_embeddings)
