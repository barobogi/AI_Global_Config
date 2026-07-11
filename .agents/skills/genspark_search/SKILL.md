---
name: genspark_search
description: "Perform parallel, fast web research using multiple asynchronous streams. Use this when you need comprehensive data, multiple perspectives, or deep analysis without manually searching one by one."
---

# Genspark Search Skill

This skill provides you with a python script (`genspark_search.py`) that performs parallel web searches to simulate a Genspark-style "Super Agent" search. It uses `duckduckgo_search` and `asyncio` to fetch multiple streams of information concurrently, bypassing traditional API costs.

## When to use this skill
- When Barobogi (the user) asks you to research a complex topic, trend, or deep technical concept.
- When you need a wide variety of sources quickly (e.g., news, general web, and documentation).
- When a single web search might not give you the full picture.

## How to use this skill
Run the python script located at `D:\AI\.agents\skills\genspark_search\genspark_search.py`.
Pass your search query as an argument.

Example:
```powershell
python "D:\AI\.agents\skills\genspark_search\genspark_search.py" "UiPath Maestro AI agent configuration"
```

## How it works
The script will internally launch 3 parallel asynchronous searches:
1. **General Web Search**: Grabs the top general results.
2. **News Search**: Grabs the most recent news articles related to the topic.
3. **Deep Search**: Appends specific keywords (like "documentation", "github", "reddit") to find technical discussions.

It then aggregates the text into a single standard output.
Your job is to read this combined output and synthesize a single, highly insightful report for the user, much like Genspark does.
