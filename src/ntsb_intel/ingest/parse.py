import html

def clean_narrative(text):
    if text is None:
        return ""
    unescaped = html.unescape(text)
    return " ".join(unescaped.split())

