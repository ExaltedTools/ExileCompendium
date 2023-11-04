import re
from typing import List

import requests
from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader


class WikiLoader(BaseLoader):
    base_url = "https://www.poewiki.net/api.php"
    header = ["title", "content"]

    def request_pages(self, apfrom):
        params = {
            "action": "query",
            "format": "json",
            "list": "allpages",
            "apfilterredir": "nonredirects",
            "apnamespace": 0,
            "aplimit": 500,
        }
        if apfrom is not None:
            params["apfrom"] = apfrom
        return requests.get(self.base_url, params=params).json()

    def get_page_extract(self, title):
        params = {
            "action": "query",
            "prop": "extracts",
            "format": "json",
            "formatversion": 2,
            "titles": title,
        }
        return requests.get(self.base_url, params=params).json()

    def get_page_parse(self, title):
        params = {"action": "parse", "page": title, "format": "json"}
        return requests.get(self.base_url, params=params).json()

    def html_to_text(self, html):
        extract_html = re.sub("<!--.*?-->", "", html, flags=re.DOTALL)
        soup = BeautifulSoup(extract_html, features="html.parser")
        return soup.get_text()

    def load(self) -> List[Document]:
        documents: List[Document] = []

        pages_response = self.request_pages(None)
        while "continue" in pages_response:
            pages_response = self.request_pages(
                pages_response["continue"]["apcontinue"]
            )
            for page in pages_response["query"]["allpages"]:
                title = page["title"]
                print(title)
                extract_response = self.get_page_extract(title)
                for extract_obj in extract_response["query"]["pages"]:
                    extract = extract_obj["extract"]
                    documents.append(
                        Document(
                            page_content=self.html_to_text(extract),
                            metadata={"title": title},
                        )
                    )

        return documents
