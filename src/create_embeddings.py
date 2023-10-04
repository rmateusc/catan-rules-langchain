import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from langchain.vectorstores import Pinecone

from langchain.document_loaders import TextLoader

# load environment variables
load_dotenv()

# set paths
SRC_DIR = Path(__file__).parents[1]
DATA_DIR = SRC_DIR / "data"
DATA_TXT = DATA_DIR / "text_files"

def main():
    # read all text files
    for txt_files in os.listdir(DATA_TXT):
        loader = TextLoader(str(DATA_TXT / txt_files))
        # load each file as a document
        documents = loader.load_and_split()

        # add title of Game Rules
        title = "Catan"
        if "base" in txt_files.lower():
            title += " Base Game"
        elif "seafarers" in txt_files.lower():
            title += " Seafarers"
        elif "cities" in txt_files.lower():
            title += " Cities & Knights"
        # add 5-6 players diffentiation
        if "expansion" in txt_files.lower():
            title += " Expansion 5 & 6 players"
        title += " Game Rules: \n "

        # append the title to each document to differentiate sets of rules
        for doc in documents[1:]:
            doc.page_content = title.upper() + doc.page_content


        # get OpenAI embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])

        # save in pinecone as a vector store
        # initialize pinecone
        pinecone.init(
            api_key=os.environ["PINECONE_API_KEY"],
            environment=os.environ["PINECONE_ENV"],
        )

        Pinecone.from_texts(
            [doc.page_content for doc in documents],
            embeddings,
            index_name=os.environ["PINECONE_INDEX"],
        )

if __name__ == "__main__":
    main()
