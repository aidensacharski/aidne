if self.path.startswith("/search"):
    from urllib.parse import urlparse, parse_qs, quote
    parsed = urlparse(self.path)
    query = parse_qs(parsed.query).get("q", [""])[0]
    url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
    # Fetch and return the content using requests or urllib
