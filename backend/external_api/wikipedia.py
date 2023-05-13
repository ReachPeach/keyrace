import wikipediaapi


class WikipediaClient:
    def __init__(self):
        self._client = wikipediaapi.Wikipedia('ru')

    def page_text(self, title: str) -> str:
        return self._client.page(title).text.replace("«", "\"").replace("»", "\"").replace("—", '-')
