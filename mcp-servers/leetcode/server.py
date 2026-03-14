#!/usr/bin/env python3
"""
LeetCode MCP Server

Provides tools to interact with LeetCode problems:
- Get problem by ID or slug
- Search problems by difficulty/topic
- Get daily challenge
- Submit and test solutions
- Track progress
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional
from datetime import datetime
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("leetcode-mcp")

# LeetCode GraphQL API endpoint
LEETCODE_API = "https://leetcode.com/graphql"
LEETCODE_BASE = "https://leetcode.com"


class LeetCodeClient:
    """Client for interacting with LeetCode API."""

    def __init__(self):
        self.session = httpx.AsyncClient(
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (compatible; LeetCode-MCP/1.0)"
            },
            timeout=30.0
        )

    async def get_problem(self, title_slug: str) -> Dict[str, Any]:
        """Get problem details by title slug."""
        query = """
        query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                title
                titleSlug
                content
                difficulty
                likes
                dislikes
                categoryTitle
                topicTags {
                    name
                    slug
                }
                codeSnippets {
                    lang
                    langSlug
                    code
                }
                sampleTestCase
                exampleTestcases
                hints
                solution {
                    id
                    canSeeDetail
                }
                stats
            }
        }
        """

        response = await self.session.post(
            LEETCODE_API,
            json={"query": query, "variables": {"titleSlug": title_slug}}
        )
        data = response.json()

        if "errors" in data:
            raise ValueError(f"Error fetching problem: {data['errors']}")

        return data["data"]["question"]

    async def get_daily_challenge(self) -> Dict[str, Any]:
        """Get today's daily challenge."""
        query = """
        query questionOfToday {
            activeDailyCodingChallengeQuestion {
                date
                link
                question {
                    questionId
                    questionFrontendId
                    title
                    titleSlug
                    difficulty
                    topicTags {
                        name
                    }
                }
            }
        }
        """

        response = await self.session.post(
            LEETCODE_API,
            json={"query": query}
        )
        data = response.json()

        if "errors" in data:
            raise ValueError(f"Error fetching daily challenge: {data['errors']}")

        return data["data"]["activeDailyCodingChallengeQuestion"]

    async def search_problems(
        self,
        difficulty: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for problems by difficulty and/or tags."""
        query = """
        query problemsetQuestionList($categorySlug: String, $limit: Int, $filters: QuestionListFilterInput) {
            problemsetQuestionList: questionList(
                categorySlug: $categorySlug
                limit: $limit
                filters: $filters
            ) {
                questions: data {
                    questionId
                    questionFrontendId
                    title
                    titleSlug
                    difficulty
                    topicTags {
                        name
                        slug
                    }
                    acRate
                    likes
                    dislikes
                }
            }
        }
        """

        filters = {}
        if difficulty:
            filters["difficulty"] = difficulty.upper()
        if tags:
            filters["tags"] = tags

        response = await self.session.post(
            LEETCODE_API,
            json={
                "query": query,
                "variables": {
                    "categorySlug": "",
                    "limit": limit,
                    "filters": filters
                }
            }
        )
        data = response.json()

        if "errors" in data:
            raise ValueError(f"Error searching problems: {data['errors']}")

        return data["data"]["problemsetQuestionList"]["questions"]

    async def get_problem_by_id(self, problem_id: int) -> Dict[str, Any]:
        """Get problem by ID number."""
        # First, search for the problem to get its slug
        query = """
        query problemsetQuestionList($filters: QuestionListFilterInput) {
            problemsetQuestionList: questionList(
                categorySlug: ""
                filters: $filters
            ) {
                questions: data {
                    questionFrontendId
                    titleSlug
                }
            }
        }
        """

        response = await self.session.post(
            LEETCODE_API,
            json={
                "query": query,
                "variables": {
                    "filters": {"searchKeywords": str(problem_id)}
                }
            }
        )
        data = response.json()

        questions = data["data"]["problemsetQuestionList"]["questions"]
        for q in questions:
            if str(q["questionFrontendId"]) == str(problem_id):
                return await self.get_problem(q["titleSlug"])

        raise ValueError(f"Problem {problem_id} not found")

    async def close(self):
        """Close the HTTP client."""
        await self.session.aclose()


# Initialize MCP server
app = Server("leetcode-mcp")
leetcode = LeetCodeClient()


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available LeetCode tools."""
    return [
        Tool(
            name="get_leetcode_problem",
            description="Get a LeetCode problem by ID or slug. Returns problem description, examples, constraints, and starter code.",
            inputSchema={
                "type": "object",
                "properties": {
                    "identifier": {
                        "type": "string",
                        "description": "Problem ID (e.g., '1', '42') or slug (e.g., 'two-sum', 'trapping-rain-water')"
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language for starter code (default: python3)",
                        "default": "python3"
                    }
                },
                "required": ["identifier"]
            }
        ),
        Tool(
            name="get_daily_leetcode",
            description="Get today's LeetCode daily challenge problem.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="search_leetcode_problems",
            description="Search LeetCode problems by difficulty and/or topic tags.",
            inputSchema={
                "type": "object",
                "properties": {
                    "difficulty": {
                        "type": "string",
                        "enum": ["easy", "medium", "hard"],
                        "description": "Problem difficulty level"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Topic tags (e.g., ['array', 'hash-table', 'dynamic-programming'])"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 50
                    }
                }
            }
        ),
        Tool(
            name="get_leetcode_hints",
            description="Get hints for a LeetCode problem to help solve it step-by-step.",
            inputSchema={
                "type": "object",
                "properties": {
                    "identifier": {
                        "type": "string",
                        "description": "Problem ID or slug"
                    }
                },
                "required": ["identifier"]
            }
        ),
        Tool(
            name="get_problem_stats",
            description="Get statistics for a LeetCode problem (acceptance rate, submissions, etc.).",
            inputSchema={
                "type": "object",
                "properties": {
                    "identifier": {
                        "type": "string",
                        "description": "Problem ID or slug"
                    }
                },
                "required": ["identifier"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool calls."""
    try:
        if name == "get_leetcode_problem":
            identifier = arguments["identifier"]
            language = arguments.get("language", "python3")

            # Determine if identifier is ID or slug
            if identifier.isdigit():
                problem = await leetcode.get_problem_by_id(int(identifier))
            else:
                problem = await leetcode.get_problem(identifier)

            # Extract code snippet for requested language
            code_snippet = None
            for snippet in problem.get("codeSnippets", []):
                if snippet["langSlug"] == language.lower():
                    code_snippet = snippet["code"]
                    break

            result = {
                "id": problem["questionFrontendId"],
                "title": problem["title"],
                "difficulty": problem["difficulty"],
                "description": problem["content"],
                "topics": [tag["name"] for tag in problem.get("topicTags", [])],
                "likes": problem.get("likes", 0),
                "dislikes": problem.get("dislikes", 0),
                "hints": problem.get("hints", []),
                "starter_code": code_snippet,
                "sample_test_case": problem.get("sampleTestCase", ""),
                "url": f"{LEETCODE_BASE}/problems/{problem['titleSlug']}/"
            }

            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "get_daily_leetcode":
            daily = await leetcode.get_daily_challenge()
            question = daily["question"]

            result = {
                "date": daily["date"],
                "id": question["questionFrontendId"],
                "title": question["title"],
                "difficulty": question["difficulty"],
                "topics": [tag["name"] for tag in question.get("topicTags", [])],
                "url": f"{LEETCODE_BASE}{daily['link']}"
            }

            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "search_leetcode_problems":
            difficulty = arguments.get("difficulty")
            tags = arguments.get("tags")
            limit = arguments.get("limit", 10)

            problems = await leetcode.search_problems(difficulty, tags, limit)

            results = []
            for p in problems:
                results.append({
                    "id": p["questionFrontendId"],
                    "title": p["title"],
                    "slug": p["titleSlug"],
                    "difficulty": p["difficulty"],
                    "topics": [tag["name"] for tag in p.get("topicTags", [])],
                    "acceptance_rate": f"{p.get('acRate', 0):.1f}%",
                    "url": f"{LEETCODE_BASE}/problems/{p['titleSlug']}/"
                })

            return [TextContent(
                type="text",
                text=json.dumps(results, indent=2)
            )]

        elif name == "get_leetcode_hints":
            identifier = arguments["identifier"]

            if identifier.isdigit():
                problem = await leetcode.get_problem_by_id(int(identifier))
            else:
                problem = await leetcode.get_problem(identifier)

            hints = problem.get("hints", [])
            if not hints:
                hints = ["No hints available for this problem."]

            result = {
                "title": problem["title"],
                "hints": hints
            }

            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "get_problem_stats":
            identifier = arguments["identifier"]

            if identifier.isdigit():
                problem = await leetcode.get_problem_by_id(int(identifier))
            else:
                problem = await leetcode.get_problem(identifier)

            stats = json.loads(problem.get("stats", "{}"))

            result = {
                "title": problem["title"],
                "total_accepted": stats.get("totalAcceptedRaw", "N/A"),
                "total_submissions": stats.get("totalSubmissionRaw", "N/A"),
                "acceptance_rate": stats.get("acRate", "N/A"),
                "likes": problem.get("likes", 0),
                "dislikes": problem.get("dislikes", 0)
            }

            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Error in {name}: {e}")
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)})
        )]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
