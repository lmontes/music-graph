import re
import string
import hashlib
from bs4 import BeautifulSoup


def extract_text_from_html(html_string):
    soup = BeautifulSoup(html_string, "html.parser")

    for tag_remove in soup(["script", "style", "meta", "link", "img"]):
        tag_remove.decompose()

    content = soup.find("div", {"id": "content"})

    text = content.get_text()

    return text.replace("\n", " ").replace("\r", " ").replace(";", " ").strip()


def clean_title(title):
    title = re.sub(r"\([^)]*\)", "", title)
    return title.replace("\"", "'").strip()


def id_from_url(url):
    return hashlib.md5(destination.encode("utf-8")).hexdigest()