from crewai.tools import tool
from ddgs import DDGS

@tool("DuckDuckGo Web Search")
def duckduckgo_search(query: str) -> str:
    """Search the public web for current information. Input should be a concise search query."""
    query = (query or "").strip()
    if not query:
        return "No query was provided."
    try:
        results = DDGS().text(query, max_results=6)
        items = []
        for index, result in enumerate(results or [], start=1):
            title = result.get("title", "Untitled")
            url = result.get("href") or result.get("url") or ""
            body = result.get("body", "")
            items.append(f"{index}. {title}\nURL: {url}\nSnippet: {body}")
        if not items:
            return "No search results were returned. Try a shorter or more specific query."
        return "\n\n".join(items)
    except Exception as exc:
        return (
            "DuckDuckGo search temporarily failed. Do not invent sources. "
            f"Search error: {type(exc).__name__}: {exc}"
        )
