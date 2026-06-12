from langchain_huggingface import HuggingFaceEmbeddings

# 1. Load the "Translator" (This turns our English into math)
# We are using a free, highly efficient open-source model from HuggingFace
print("Loading embedding model...")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Let's take a simple biological sentence
text = "Neurons transmit information using action potentials."

# 3. Translate the text into an embedding (a vector of numbers)
vector = embedding_model.embed_query(text)

# 4. Prove that it worked
print("\nSuccess! The text was translated into math.")
print(f"Your sentence was turned into a list of {len(vector)} numbers.")
print(f"Here are the first 5 numbers: {vector[:5]}")