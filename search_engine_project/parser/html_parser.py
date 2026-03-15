"""
Document Parser
Cleans HTML, tokenizes text, removes stop words, stems words.
"""

from bs4 import BeautifulSoup
import re

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for",
    "if", "in", "into", "is", "it", "no", "not", "of", "on", "or",
    "such", "that", "the", "their", "then", "there", "these",
    "they", "this", "to", "was", "will", "with"
}

def clean_html(html_content: str) -> str:
    """Removes HTML tags and returns plain text."""
    soup = BeautifulSoup(html_content, "html.parser")
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text(separator=" ")
    return text

def tokenize(text: str) -> list:
    """Extracts alphanumeric tokens from text and lowercases them."""
    return re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())

def simple_stem(word: str) -> str:
    """A very basic suffix-stripping stemmer."""
    if len(word) <= 3:
        return word
    if word.endswith("ing"):
        return word[:-3]
    if word.endswith("ly"):
        return word[:-2]
    if word.endswith("es"):
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    if word.endswith("ed"):
        return word[:-2]
    return word

def parse_document(html_content: str) -> list:
    """Full parsing pipeline: clean -> tokenize -> filter -> stem."""
    text = clean_html(html_content)
    tokens = tokenize(text)
    processed = []
    for token in tokens:
        if token not in STOP_WORDS:
            stemmed = simple_stem(token)
            processed.append(stemmed)
    return processed

if __name__ == "__main__":
    html = "<html><body><h1>Search Engines are amazing!</h1><p>They are indexing the web quickly.</p></body></html>"
    print("Parsed output:", parse_document(html))
