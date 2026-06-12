"""

core mathematical engine of a Vector Database:

  1. MiniLM maps strings to 384-D coordinates.

  2. ChromaDB indexes and saves those coordinates.

  3. Query gets its own 384-D coordinate.

  4. Distance math finds the closest point and returns the original text.
"""



from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_chroma import Chroma

# 1. Load the "Translator" (This turns our English into math)
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Let's take a list of lines
text = ["Neurons transmit information using action potentials.",
        "Vijay is a great Actor.",
        "The capital of France is Paris.",
        "The mitochondria is the powerhouse of the cell.",
        "The Earth revolves around the Sun.",
        "Donald trump was the 45th president of the United States."]

# 3. Put them in our Vector Database (Chroma) as embeddings(numbers) instead of text. This is like putting the "translations" of our sentences into a special filing cabinet that can find similar "translations" when we ask it a question.
db = Chroma.from_texts(text, embedding=embedding_model)

# 4. Now we can ask questions! Let's ask "What is the capital of France?"
query = "How human cells produce energy from food we eat?"

print(db.similarity_search(query, k=1)) # k is how many results we want, we set it to 1 because we only want the most relevant result.)) 