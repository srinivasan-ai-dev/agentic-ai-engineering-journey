import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
 

 #workflow : Pdf -> chunks -> vector database

# --- Configuration ---
# Hardcoding paths is fine for scripts, but keep them at the top for easy editing
PDF_PATH = "./data/Neuroscience.pdf" # This is the PDF we want to ingest. You can change this to any PDF you like, just make sure to update the path.
DB_DIR = "./vector_vault" # This is where our vector database will be stored. You can change this to any directory you want, but make sure it exists or the script will throw an error.

def main():
      print("🚀 Starting Data Ingestion Pipeline...")


      #1. load the embedding model
      print("Loading embedding model (all-MiniLM-L6-v2)...")
      embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


      #2. load the PDF
      print("Loading PDF...")
      loader = PyPDFLoader(PDF_PATH) # This creates a loader object that knows how to read our PDF file. We will use this loader to extract the text from the PDF in the next step.
      pages = loader.load() # This actually reads the PDF and extracts the text, returning a list of "pages". Each page is an object that contains the text of that page, along with some metadata. The length of this list tells us how many pages were in the PDF.
      print(f"Loaded {len(pages)} pages.")


      #3. split the text into chunks
      #  textbooks have long paragraphs. We use a chunk size of 800 
      #  to capture full concepts, and a high overlap of 150 so sentences aren't cut in half.
      print("\nSplitting text into chunks...")
      text_splitting_function = RecursiveCharacterTextSplitter(
          chunk_size=800,
          chunk_overlap=150,
          length_function=len,
          is_separator_regex=False,# This tells the splitter to split based on character count, not on specific separators like newlines or punctuation. This is important for scientific texts where concepts may span multiple sentences.
      )

      chunks= text_splitting_function.split_documents(pages) # This takes the list of pages and splits the text of each page into smaller chunks based on the configuration we set. The result is a new list of "chunks", where each chunk is a smaller piece of text that is easier for our embedding model to process. The number of chunks will depend on the length of the original text and the chunk size we chose.
      print(f"Created {len(chunks)} chunks.")

      #4. create the vector database
      print("\nCreating vector database...")
      vector_db = Chroma.from_documents(
          documents=chunks,
          embedding=embedding_model,
          collection_name="neuro_textbook",
          persist_directory=DB_DIR
      ) # This creates a new vector database using Chroma. We pass in the list of chunks as the documents to be stored, the embedding model to convert those chunks into vectors, a name for the collection (which is like a table in a traditional database), and the directory where the database files will be stored. This step will take some time as it processes each chunk and creates the corresponding embeddings.

      print("✨ Data ingestion complete! Your vector database is ready for querying.")



if __name__ == "__main__": # This is a common Python idiom that checks if this script is being run directly (as the main program) rather than imported as a module in another script. If this condition is true, it will execute the code inside this block, which in this case is calling the main() function to start the data ingestion process.
    main()