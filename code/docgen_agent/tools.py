"""Tools for the report generation workflow."""

import asyncio
import logging
import os
import requests
from typing import Literal

from langchain_core.tools import tool

_LOGGER = logging.getLogger(__name__)

# Initialize Tavily client only if API key is available
tavily_client = None
try:
    from tavily import AsyncTavilyClient
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if tavily_api_key:
        tavily_client = AsyncTavilyClient(api_key=tavily_api_key)
        _LOGGER.info("Tavily API initialized successfully.")
    else:
        _LOGGER.warning("TAVILY_API_KEY not set. Web search functionality will be disabled.")
except ImportError:
    _LOGGER.warning("Tavily package not installed. Web search functionality will be disabled.")

# GitHub API setup
github_token = os.getenv("GITHUB_TOKEN")
github_headers = {"Authorization": f"token {github_token}"} if github_token else {}

INCLUDE_RAW_CONTENT = False
MAX_TOKENS_PER_SOURCE = 1000
MAX_RESULTS = 5
SEARCH_DAYS = 30


def _deduplicate_and_format_sources(
    search_response, max_tokens_per_source, include_raw_content=True
):
    """
    Takes either a single search response or list of responses from Tavily API and formats them.
    Limits the raw_content to approximately max_tokens_per_source.
    include_raw_content specifies whether to include the raw_content from Tavily in the formatted string.

    Args:
        search_response: Either:
            - A dict with a 'results' key containing a list of search results
            - A list of dicts, each containing search results

    Returns:
        str: Formatted string with deduplicated sources
    """
    # Convert input to list of results
    if isinstance(search_response, dict):
        sources_list = search_response["results"]
    elif isinstance(search_response, list):
        sources_list = []
        for response in search_response:
            if isinstance(response, dict) and "results" in response:
                sources_list.extend(response["results"])
            else:
                sources_list.extend(response)
    else:
        raise ValueError(
            "Input must be either a dict with 'results' or a list of search results"
        )

    # Deduplicate by URL
    unique_sources = {}
    for source in sources_list:
        if source["url"] not in unique_sources:
            unique_sources[source["url"]] = source

    # Format output
    formatted_text = "Sources:\n\n"
    for i, source in enumerate(unique_sources.values(), 1):
        formatted_text += f"Source {source['title']}:\n===\n"
        formatted_text += f"URL: {source['url']}\n===\n"
        formatted_text += (
            f"Most relevant content from source: {source['content']}\n===\n"
        )
        if include_raw_content:
            # Using rough estimate of 4 characters per token
            char_limit = max_tokens_per_source * 4
            # Handle None raw_content
            raw_content = source.get("raw_content", "")
            if raw_content is None:
                raw_content = ""
                print(f"Warning: No raw_content found for source {source['url']}")
            if len(raw_content) > char_limit:
                raw_content = raw_content[:char_limit] + "... [truncated]"
            formatted_text += f"Full source content limited to {max_tokens_per_source} tokens: {raw_content}\n\n"

    return formatted_text.strip()


@tool(parse_docstring=True)
async def search_tavily(
    queries: list[str],
    topic: Literal["general", "news", "finance"] = "news",
) -> str:
    """Search the web using the Tavily API.

    Args:
        queries: List of queries to search.
        topic: The topic of the provided queries.
          general - General search.
          news - News search.
          finance - Finance search.

    Returns:
        A string of the search results.
    """
    if not tavily_client:
        return "Web search is not available. Please set TAVILY_API_KEY environment variable."
    
    _LOGGER.info("Searching the web using the Tavily API")

    days = None
    if topic == "news":
        days = SEARCH_DAYS

    search_results = []
    for query in queries:
        try:
            result = await tavily_client.search(
                query=query,
                search_depth="basic",
                include_domains=[],
                exclude_domains=[],
                include_answer=True,
                include_raw_content=INCLUDE_RAW_CONTENT,
                max_results=MAX_RESULTS,
                include_images=False,
                search_type=topic,
                days_back=days,
            )
            search_results.append(result)
        except Exception as e:
            _LOGGER.error(f"Error searching for query '{query}': {e}")
            search_results.append({"results": []})

    return _deduplicate_and_format_sources(
        search_results, MAX_TOKENS_PER_SOURCE, INCLUDE_RAW_CONTENT
    )


@tool(parse_docstring=True)
async def search_legal_precedents(
    legal_issue: str,
    jurisdiction: str = "US"
) -> str:
    """Search for legal precedents and similar cases related to the legal issue.

    Args:
        legal_issue: The specific legal issue to search for (e.g., "data selling terms of service")
        jurisdiction: The legal jurisdiction to focus on (default: US)

    Returns:
        A string containing relevant legal precedents and case information.
    """
    if not tavily_client:
        return "Legal research is not available. Please set TAVILY_API_KEY environment variable."
    
    _LOGGER.info(f"Searching for legal precedents: {legal_issue}")
    
    queries = [
        f"{legal_issue} legal cases {jurisdiction}",
        f"{legal_issue} court decisions {jurisdiction}",
        f"{legal_issue} consumer protection {jurisdiction}",
        f"{legal_issue} regulatory compliance {jurisdiction}"
    ]
    
    search_results = []
    for query in queries:
        try:
            result = await tavily_client.search(
                query=query,
                search_depth="advanced",
                include_domains=["law.justia.com", "casetext.com", "supreme.justia.com", "scholar.google.com"],
                include_answer=True,
                include_raw_content=True,
                max_results=3,
                search_type="news",
                days_back=365,  # Look back 1 year for recent cases
            )
            search_results.append(result)
        except Exception as e:
            _LOGGER.error(f"Error searching for legal precedents '{query}': {e}")
            search_results.append({"results": []})

    return _deduplicate_and_format_sources(
        search_results, MAX_TOKENS_PER_SOURCE, True
    )


@tool(parse_docstring=True)
def extract_github_document(
    repo_url: str,
    file_path: str = "README.md"
) -> str:
    """Extract a document from a GitHub repository.

    Args:
        repo_url: The GitHub repository URL (e.g., "https://github.com/user/repo")
        file_path: The path to the file in the repository (default: README.md)

    Returns:
        The content of the file as a string.
    """
    if not github_token:
        return "GitHub access is not available. Please set GITHUB_TOKEN environment variable."
    
    try:
        # Parse repository URL
        if "github.com" in repo_url:
            parts = repo_url.split("github.com/")[-1].split("/")
            owner = parts[0]
            repo = parts[1]
        else:
            return "Invalid GitHub URL format. Please provide a valid GitHub repository URL."
        
        # GitHub API endpoint
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
        
        response = requests.get(api_url, headers=github_headers)
        response.raise_for_status()
        
        content_data = response.json()
        if content_data.get("type") == "file":
            import base64
            content = base64.b64decode(content_data["content"]).decode("utf-8")
            return content
        else:
            return f"Path {file_path} is not a file in the repository."
            
    except requests.exceptions.RequestException as e:
        return f"Error accessing GitHub: {str(e)}"
    except Exception as e:
        return f"Error extracting document: {str(e)}"


@tool(parse_docstring=True)
def search_github_legal_documents(
    query: str,
    language: str = "markdown"
) -> str:
    """Search for legal documents in GitHub repositories.

    Args:
        query: Search query for legal documents (e.g., "terms of service", "privacy policy")
        language: File language to search for (default: markdown)

    Returns:
        A string containing information about found legal documents.
    """
    if not github_token:
        return "GitHub search is not available. Please set GITHUB_TOKEN environment variable."
    
    try:
        # GitHub search API
        search_url = "https://api.github.com/search/code"
        params = {
            "q": f"{query} language:{language}",
            "sort": "updated",
            "order": "desc"
        }
        
        response = requests.get(search_url, headers=github_headers, params=params)
        response.raise_for_status()
        
        results = response.json()
        items = results.get("items", [])
        
        if not items:
            return f"No legal documents found for query: {query}"
        
        # Format results
        formatted_results = f"Found {len(items)} legal documents for '{query}':\n\n"
        for i, item in enumerate(items[:5], 1):  # Show top 5
            repo_name = item["repository"]["full_name"]
            file_path = item["path"]
            file_url = item["html_url"]
            
            formatted_results += f"{i}. Repository: {repo_name}\n"
            formatted_results += f"   File: {file_path}\n"
            formatted_results += f"   URL: {file_url}\n\n"
        
        return formatted_results
        
    except requests.exceptions.RequestException as e:
        return f"Error searching GitHub: {str(e)}"
    except Exception as e:
        return f"Error in GitHub search: {str(e)}"
