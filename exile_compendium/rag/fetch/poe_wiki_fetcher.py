import re
from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup
from haystack.nodes.base import BaseComponent
from haystack.schema import Document


class WikiFetcher(BaseComponent):
    base_url = "https://www.poewiki.net/api.php"
    header = ["title", "content"]

    outgoing_edges = 1

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
        soup = BeautifulSoup(html, features="html.parser")
        return soup.get_text()

    def run(self) -> Tuple[Dict[str, List[Document]], str]:
        documents: List[Document] = []

        pages_response = self.request_pages(None)
        i = 0
        while "continue" in pages_response and i < 50:
            pages_response = self.request_pages(
                pages_response["continue"]["apcontinue"]
            )
            for page in pages_response["query"]["allpages"]:
                title = page["title"]
                print(title)
                i += 1
                extract_response = self.get_page_extract(title)
                for extract in extract_response["query"]["pages"]:
                    extract_html = re.sub(
                        "<!--.*?-->", "", extract["extract"], flags=re.DOTALL
                    )
                    documents.append(
                        Document(
                            content=self.html_to_text(extract_html),
                            meta={"title": title},
                        )
                    )

        results = {"documents": documents}
        return results, "output_1"

    def run_batch(self):
        return self.run()
