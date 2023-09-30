import os
import re
from pathlib import Path

from langchain.document_loaders import PyPDFLoader

SRC_DIR = Path(__file__).parents[1]
DATA_DIR = SRC_DIR / "data"


def read_raw_pdfs() -> None:
    """
    Read the raw pdf files and save them as text files in data/text_files folder.
    """
    # explore the raw data folder
    for file in os.listdir(DATA_DIR / "raw"):
        loader = PyPDFLoader(str(DATA_DIR / "raw" / file))
        pages = loader.load_and_split()
        # store all pages in a single string
        text = ""
        for page in pages:
            text += page.page_content.replace("•", "").replace("\u200aY", "")
            # delete everything after Credits
            text = text.split("Credits")[0]
            text = text.split("index")[0]

        # remove irregulat characters
        patterns_to_remove = [
            r"\n\d+",  # Remove '\n' followed by numbers
            r"\n\s*[A-Z]",
            # r'\n'  # Remove '\n' followed by any capital letter
        ]
        for pattern in patterns_to_remove:
            text = re.sub(pattern, "", text)

        # see if data/processed folder exists
        folder_to_save = "text_files"
        if not os.path.exists(DATA_DIR / folder_to_save):
            os.makedirs(DATA_DIR / folder_to_save)

        # save the text files
        with open(DATA_DIR / folder_to_save / file.replace(".pdf", ".txt"), "w") as f:
            f.write(text)


def main():
    read_raw_pdfs()


if __name__ == "__main__":
    main()
