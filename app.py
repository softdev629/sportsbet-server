from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredURLLoader
from langchain import OpenAI, LLMChain, PromptTemplate

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/api/get-article")
def getArticle(address: str = Body(embed=True)):
    loader = UnstructuredURLLoader(urls=[
        address
    ])
    data = loader.load()
    prompt_template = """Don't return empty results. You must write an interesting long article based on the following text and try to avoid using and copying same words from the text.

    {text}
    """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
    llm = OpenAI(temperature=0, max_tokens=1000)
    llm_chain = LLMChain(prompt=PROMPT, llm=llm)
    result = llm_chain.run(data[0].page_content)
    return {"output": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=9000, reload=True)
