#for api keys
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


#prompt for AI
prompt= [
  ("system", "You are a helpful assistant that gives a 1 line answer to a question"),
  ("human", "Who is Nikola Tesla?")]


# calling gemini
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=2) #temperatue sets creativity of the response, higher is more creative. Ranges from 0 to 2, default is 1.
response = llm.invoke(prompt)
print('Gemini:', response.content)


#calling groq
from langchain_groq import ChatGroq
llm = ChatGroq(model ="qwen/qwen3-32b", reasoning_format="parsed")
response = llm.invoke(prompt)
print('Groq:', response.content)