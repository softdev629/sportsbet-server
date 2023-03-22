from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredURLLoader
from langchain import OpenAI, LLMChain, PromptTemplate
import aiohttp
import asyncio
from datetime import datetime
import json

load_dotenv()

app = FastAPI()

origins = [
    "https://goldfish-app-y5srr.ondigitalocean.app/",
    "http://localhost:3000",
    "http://localhost:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def generate_article(url, title, description):
    loader = UnstructuredURLLoader(urls=[
        url
    ])
    try:
        data = loader.load()

        prompt_template = """Don't return empty results. You must write an interesting long article based on the 
        following text and try to avoid using and copying same words from the text. Divide result article into 
        several paragraphs. 
    
            {text}
            """
        prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
        llm = OpenAI(temperature=0, max_tokens=1000)
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        content = llm_chain.run(data[0].page_content)

        prompt_template = """Below is given article title.
        
        {title}
    
        Generate new article title which is very different from above title but similar in meaning."""

        prompt = PromptTemplate(template=prompt_template, input_variables=["title"])
        llm = OpenAI(temperature=0, max_tokens=100)
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        title = llm_chain.run(title)

        if description is not None:
            prompt_template = """Below is new given article description.
        
            {description}
        
            Generate new article description which is very different from above description but similar in meaning.
            """
            prompt = PromptTemplate(template=prompt_template, input_variables=["description"])
            llm = OpenAI(temperature=0, max_tokens=200)
            llm_chain = LLMChain(prompt=prompt, llm=llm)
            description = llm_chain.run(description)

        return {"title": title, "description": description, "content": content}
    except Exception:
        # print("Connection Error")
        return {"title": "", "description": "", "content": ""}


@app.post("/api/get-article")
def get_article(address: str = Body(embed=True), title: str = Body(embed=True), description: str = Body(embed=True)):
    return generate_article(address, title, description)


async def generate_tsx():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey"
                               "=9ff67f7da667487f846f3ae91cadb25f") as resp:
            data = await resp.json()
            for idx, article in enumerate(data["articles"]):
                article = generate_article(article["url"], article["title"], article["description"])
                f = open("./template.tsx", "r")
                template_tsx = f.read()
                article_dom_list = article["content"].split("\n\n")
                article_dom_content = ""
                for article_dom in article_dom_list:
                    article_dom = article_dom.replace("\n", "")
                    article_dom_content += "<p className=\"mb-6 font-secondary\">" + article_dom + "</p>"

                template_tsx = template_tsx.replace("<<TITLE>>",
                                                    article["title"].replace("\"", "").replace("\n", "")).replace(
                    "<<DESCRIPTION>>", article["description"].replace("\n", "")).replace("<<ARTICLEDOM>>",
                                                                                         article_dom_content).replace(
                    "<<DATETIME>>", datetime.now().astimezone().strftime("%B %d, %Y at %I:%M %p %Z"))
                if data["articles"][idx]["urlToImage"] is not None:
                    template_tsx = template_tsx.replace("<<URLIMAGE>>", data["articles"][idx]["urlToImage"])
                f.close()
                f = open(f"./templates/template_{idx}.tsx", "w")
                f.write(template_tsx)
                print(f"{100 / len(data['articles']) * (idx + 1)}%")
                f.close()


# def generate_tsx():
#     f = open("./top-headlines.json")
#     data = json.load(f)
#     f.close()
#
#     for idx, article in enumerate(data["articles"]) :
#         article = generate_article(article["url"], article["title"], article["description"])
#         f = open("./template.tsx", "r")
#         template_tsx = f.read()
#         article_dom_list = article["content"].split("\n\n")
#         article_dom_content = ""
#         for article_dom in article_dom_list :
#              article_dom = article_dom.replace("\n", "")
#              article_dom_content += "<p className=\"mb-6 font-secondary\">" + article_dom + "</p>"
#
#         template_tsx = template_tsx.replace("<<TITLE>>", article["title"].replace("\"", "").replace("\n", "")).replace("<<DESCRIPTION>>", article["description"].replace("\n", "")).replace("<<ARTICLEDOM>>", article_dom_content).replace("<<DATETIME>>", datetime.now().astimezone().strftime("%B %d, %Y at %I:%M %p %Z"))
#         if(data["articles"][idx]["urlToImage"] is not None):
#             template_tsx = template_tsx.replace("<<URLIMAGE>>", data["articles"][idx]["urlToImage"])
#         f.close()
#         f = open(f"./templates/template_{idx}.tsx", "w")
#         f.write(template_tsx)
#         print(f"{100 / len(data['articles']) * (idx + 1)}%")
#         f.close()

if __name__ == "__main__":
    # asyncio.run(generate_tsx())

    # generate_tsx()

    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=9000, reload=True)
