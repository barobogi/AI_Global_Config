# 3AI 공통 병렬 리서치 스킬 — ddgs 기반 비동기 검색 + Wikipedia 보강
import sys
import json
import asyncio
import argparse
import time
import warnings
import urllib.request
import urllib.parse
from typing import List, Dict, Any

warnings.filterwarnings("ignore")

if sys.stdout is not None and getattr(sys.stdout, "encoding", None) is not None:
    if sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError as e:
        print(json.dumps({"status": "error", "message": f"ImportError: {str(e)}. Run: pip install ddgs"}))
        sys.exit(1)


def _fetch_wikipedia_summary(title: str) -> str:
    encoded = urllib.parse.quote(title.replace(" ", "_"))
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "3AI-parallel-search/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("extract", "")
    except Exception:
        return ""


def _enrich_with_wikipedia(results: List[Dict]) -> List[Dict]:
    enriched = []
    for r in results:
        if "wikipedia.org/wiki/" in r.get("href", ""):
            title = r["href"].split("/wiki/")[-1]
            summary = _fetch_wikipedia_summary(urllib.parse.unquote(title))
            if summary:
                r = dict(r)
                r["wikipedia_extract"] = summary[:1000]
        enriched.append(r)
    return enriched


def fetch_with_retry(ddgs: DDGS, query: str, max_results: int, retries: int = 3) -> Dict[str, Any]:
    delay = 1.0
    for attempt in range(retries):
        try:
            results = ddgs.text(query, max_results=max_results)
            return {"query": query, "results": _enrich_with_wikipedia(results), "error": None}
        except Exception as e:
            if "Ratelimit" in str(e) or "202" in str(e):
                if attempt < retries - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue
            return {"query": query, "results": [], "error": str(e)}
    return {"query": query, "results": [], "error": "Max retries exceeded"}


async def run_parallel_search(queries: List[str], max_results: int) -> Dict[str, Any]:
    start_time = time.time()

    with DDGS(timeout=5) as ddgs:
        tasks = [asyncio.to_thread(fetch_with_retry, ddgs, q, max_results) for q in queries]
        gathered = await asyncio.gather(*tasks)

    results_dict = {}
    for res in gathered:
        q = res["query"]
        if res["error"]:
            results_dict[q] = {"error": res["error"]}
        else:
            results_dict[q] = res["results"]

    elapsed = round(time.time() - start_time, 2)
    return {
        "status": "success",
        "results": results_dict,
        "elapsed_sec": elapsed
    }


def main():
    parser = argparse.ArgumentParser(description="Parallel Search Script for 3AI")
    parser.add_argument("--queries", nargs="+", help="List of queries to search")
    parser.add_argument("--max", type=int, default=5, help="Max results per query")
    parser.add_argument("--json-input", type=str, help="Path to JSON input file")

    args = parser.parse_args()

    queries = []
    max_results = args.max
    save_to_file = None

    if args.json_input:
        try:
            with open(args.json_input, 'r', encoding='utf-8') as f:
                data = json.load(f)
                queries = data.get("queries", [])
                max_results = data.get("max_results", 5)
                save_to_file = data.get("save_to_file")
        except Exception as e:
            print(json.dumps({"status": "error", "message": f"Failed to read json-input: {e}"}))
            sys.exit(1)
    elif args.queries:
        queries = args.queries
    else:
        print(json.dumps({"status": "error", "message": "Provide --queries or --json-input"}))
        sys.exit(1)

    if not queries:
        print(json.dumps({"status": "error", "message": "No queries provided"}))
        sys.exit(1)

    output = asyncio.run(run_parallel_search(queries, max_results))

    if save_to_file:
        try:
            with open(save_to_file, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print(json.dumps({"status": "success", "message": f"Saved to {save_to_file}", "elapsed_sec": output["elapsed_sec"]}))
        except Exception as e:
            output["status"] = "error"
            output["message"] = f"Failed to write to file: {e}"
            print(json.dumps(output, ensure_ascii=False))
    else:
        print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
