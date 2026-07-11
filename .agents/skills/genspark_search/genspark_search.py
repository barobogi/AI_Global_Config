import sys
import asyncio
import argparse
import json

try:
    from duckduckgo_search import AsyncDDGS
except ImportError:
    print("ERROR: duckduckgo_search library is not installed.")
    print("Please run: pip install duckduckgo-search")
    sys.exit(1)

async def search_task(ddgs: AsyncDDGS, task_name: str, query: str, max_results: int = 5):
    try:
        results = await ddgs.text(query, max_results=max_results)
        return {"task": task_name, "query": query, "results": results, "error": None}
    except Exception as e:
        return {"task": task_name, "query": query, "results": [], "error": str(e)}

async def search_news_task(ddgs: AsyncDDGS, task_name: str, query: str, max_results: int = 5):
    try:
        results = await ddgs.news(query, max_results=max_results)
        return {"task": task_name, "query": query, "results": results, "error": None}
    except Exception as e:
        return {"task": task_name, "query": query, "results": [], "error": str(e)}

async def main():
    parser = argparse.ArgumentParser(description="Genspark Parallel Search Script for 3AI")
    parser.add_argument("query", type=str, help="The search query")
    args = parser.parse_args()

    query = args.query
    print(f"🚀 [Genspark Parallel Search Initiated] Query: '{query}'")

    async with AsyncDDGS() as ddgs:
        # Define 3 parallel tasks: General Web, News, and Deep Tech/Forums
        tasks = [
            search_task(ddgs, "General Web", query, max_results=5),
            search_news_task(ddgs, "Recent News", query, max_results=3),
            search_task(ddgs, "Tech Forums & Docs", f"{query} site:reddit.com OR site:github.com OR documentation", max_results=3)
        ]
        
        results = await asyncio.gather(*tasks)

    print("\n" + "="*50)
    print("🔍 [Search Results]")
    print("="*50)

    for res in results:
        task_name = res["task"]
        actual_query = res["query"]
        items = res["results"]
        error = res["error"]
        
        print(f"\n--- 📌 Source: {task_name} (Query: '{actual_query}') ---")
        if error:
            print(f"Error occurred: {error}")
            continue
            
        if not items:
            print("No results found.")
            continue
            
        for idx, item in enumerate(items, 1):
            title = item.get("title", "No Title")
            href = item.get("href") or item.get("url") or "No URL"
            body = item.get("body") or item.get("summary") or "No Description"
            
            print(f"{idx}. {title}")
            print(f"   URL: {href}")
            print(f"   Snippet: {body}\n")

if __name__ == "__main__":
    asyncio.run(main())
