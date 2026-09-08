calculate_tool = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Calculate a mathematical expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A mathematical expression such as 25 * 4"
                }
            },
            "required": ["expression"]
        }
    }
}


search_web_tool = {
    "type": "function",
    "function": {
        "name": "search_web",
        "description": "Search the web for current or factual information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of search results"
                }
            },
            "required": ["query"]
        }
    }
}

read_webpage_tool = {
    "type": "function",
    "function": {
        "name": "read_webpage",
        "description": (
            "Read and extract the text content from a webpage URL."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The complete URL of the webpage to read"
                },
                "cursor": {
                    "type": "integer",
                    "description": "Ignored compatibility parameter"
                },
                "loc": {
                    "type": "integer",
                    "description": "Ignored compatibility parameter"
                }
            }
        }
    }
}