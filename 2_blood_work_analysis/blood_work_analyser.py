from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


from langchain_groq import ChatGroq
llm = ChatGroq (model ="qwen/qwen3-32b")

with open('blood_work.txt', 'r') as f:
    input = f.read()

prompt_1 = [
    ("system", "You are a professional highly trained physician that gives accurate summary of blood work results in 50 words. You only answer the question asked and do not provide any additional information.",),
    ("human", "Here are the blood work results: " + input + " What is the summary of these blood work results?"),
]

summary = llm.invoke(prompt_1)
print(summary.content)

prompt_2 = [
    ("system", "You are a professional highly trained physician that gives accurate Indian Diet plan based on blood work results. You only answer the question asked and do not provide any additional information.",),
    ("human", "Here are the blood work summary: " + summary.content + " What is the Indian diet plan based on this summary?"),
]
diet_plan = llm.invoke(prompt_2)
print(diet_plan.content)