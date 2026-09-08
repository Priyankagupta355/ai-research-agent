import os
import json
import time

from dotenv import load_dotenv
from groq import Groq, RateLimitError

from app.tools.calculator import calculate
from app.tools.search_tool import search_web
from app.tools.web_reader import read_webpage

from app.tools.tool_schemas import (
    calculate_tool,
    search_web_tool,
    read_webpage_tool,
)


# ============================================================
# GROQ CONFIGURATION
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set in the environment."
    )

client = Groq(
    api_key=GROQ_API_KEY
)

MODEL_NAME = "openai/gpt-oss-120b"


# ============================================================
# AGENT CONFIGURATION
# ============================================================

# Maximum characters from one tool result sent back to Groq
MAX_TOOL_RESULT_CHARS = 3000

# Maximum total research information used for report generation
MAX_RESEARCH_CONTENT_CHARS = 12000

# Maximum output tokens for agent decisions
MAX_AGENT_OUTPUT_TOKENS = 700

# Maximum output tokens for final report
MAX_REPORT_OUTPUT_TOKENS = 1200

# Maximum number of tool calls in one research task
MAX_TOOL_CALLS = 6

# Maximum number of Groq decision rounds
MAX_AGENT_TURNS = 4


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _limit_text(text: str, max_chars: int) -> str:
    """
    Limit text size before sending it to the model.
    """

    text = str(text)

    if len(text) <= max_chars:
        return text

    return (
        f"{text[:max_chars]}\n"
        "[Content truncated]"
    )


def _create_completion(**kwargs):
    """
    Create Groq completion with simple rate-limit retry.
    """

    try:

        return client.chat.completions.create(
            **kwargs
        )

    except RateLimitError:

        print(
            "[Groq] Rate limit reached. "
            "Retrying after 2 seconds..."
        )

        time.sleep(2)

        return client.chat.completions.create(
            **kwargs
        )


def _research_content(
    research_data: list[dict]
) -> str:
    """
    Convert collected tool results into compact
    research information for the report writer.
    """

    if not research_data:
        return ""

    content_parts = []

    for index, item in enumerate(
        research_data,
        start=1
    ):

        content_parts.append(
            f"""
Research Result #{index}

Tool:
{item["tool"]}

Arguments:
{item["arguments"]}

Result:
{_limit_text(
    item["result"],
    MAX_TOOL_RESULT_CHARS
)}
"""
        )

    content = "\n".join(
        content_parts
    )

    return _limit_text(
        content,
        MAX_RESEARCH_CONTENT_CHARS
    )


# ============================================================
# AVAILABLE PYTHON FUNCTIONS
# ============================================================

available_functions = {

    "calculate": calculate,

    "search_web": search_web,

    "read_webpage": read_webpage,
}


# ============================================================
# AVAILABLE GROQ TOOLS
# ============================================================

tools = [

    calculate_tool,

    search_web_tool,

    read_webpage_tool,
]


# ============================================================
# FINAL REPORT GENERATOR
# ============================================================

def generate_report(
    user_query: str,
    research_content: str
):
    """
    Generate final structured research report
    using only collected research information.
    """

    response = _create_completion(

        model=MODEL_NAME,

        messages=[

            {
                "role": "system",

                "content": (
                    "You are a professional research report writer.\n\n"

                    "Create a factual, concise and useful "
                    "research report using ONLY the provided "
                    "research information.\n\n"

                    "Do not invent facts.\n"
                    "Do not invent sources.\n"
                    "Do not invent URLs.\n"
                    "Do not claim that research was performed "
                    "if no research information was provided.\n\n"

                    "If the research information contains "
                    "sources, include them in the sources array.\n\n"

                    "If no sources are available, return an "
                    "empty sources array.\n\n"

                    "If the research information is insufficient "
                    "to answer the question, clearly say so."
                )
            },

            {
                "role": "user",

                "content": f"""
Research Question:

{user_query}


Research Information:

{research_content}


Create the final structured research report.
"""
            },
        ],

        response_format={

            "type": "json_schema",

            "json_schema": {

                "name": "research_report",

                "strict": True,

                "schema": {

                    "type": "object",

                    "properties": {

                        "title": {

                            "type": "string"
                        },

                        "summary": {

                            "type": "string"
                        },

                        "key_findings": {

                            "type": "array",

                            "items": {

                                "type": "string"
                            }
                        },

                        "sources": {

                            "type": "array",

                            "items": {

                                "type": "object",

                                "properties": {

                                    "title": {

                                        "type": "string"
                                    },

                                    "url": {

                                        "type": "string"
                                    },
                                },

                                "required": [
                                    "title",
                                    "url"
                                ],

                                "additionalProperties": False,
                            },
                        },

                        "conclusion": {

                            "type": "string"
                        },
                    },

                    "required": [

                        "title",

                        "summary",

                        "key_findings",

                        "sources",

                        "conclusion",
                    ],

                    "additionalProperties": False,
                },
            },
        },

        max_tokens=MAX_REPORT_OUTPUT_TOKENS,
    )

    content = response.choices[0].message.content

    if not content:

        raise ValueError(
            "Groq returned an empty report."
        )

    try:

        return json.loads(content)

    except json.JSONDecodeError as e:

        print(
            "[Report] Invalid JSON returned by Groq:"
        )

        print(content)

        raise ValueError(
            "Failed to parse final research report JSON."
        ) from e


# ============================================================
# MAIN RESEARCH AGENT
# ============================================================

def run_agent(user_query: str):
    """
    Run the AI Research Agent.

    Flow:

    User Query
        ↓
    Groq
        ↓
    Search Web
        ↓
    Read Webpage if needed
        ↓
    Additional research if needed
        ↓
    Final Report
    """

    # --------------------------------------------------------
    # Validate query
    # --------------------------------------------------------

    if not user_query or not user_query.strip():

        return {

            "title": "Invalid Research Query",

            "summary": (
                "No research question was provided."
            ),

            "key_findings": [],

            "sources": [],

            "conclusion": (
                "Please provide a research question."
            ),
        }


    user_query = user_query.strip()


    # --------------------------------------------------------
    # Store research results
    # --------------------------------------------------------

    research_data = []


    # --------------------------------------------------------
    # Initial messages
    # --------------------------------------------------------

    messages = [

        {
            "role": "system",

            "content": (
                "You are an AI Research Assistant.\n\n"

                "Your job is to research questions and "
                "provide accurate, useful and source-based "
                "answers.\n\n"

                "IMPORTANT RULES:\n\n"

                "1. For research questions, ALWAYS use "
                "the search_web tool first.\n\n"

                "2. Do not answer a research question "
                "only from your internal knowledge.\n\n"

                "3. After receiving search results, inspect "
                "important webpages using read_webpage when "
                "more detailed information is required.\n\n"

                "4. You may use multiple tools when necessary.\n\n"

                "5. For calculations, use calculate.\n\n"

                "6. Do not invent facts.\n\n"

                "7. Do not invent URLs.\n\n"

                "8. For read_webpage, always provide the "
                "complete URL in the url argument.\n\n"

                "9. Do not use cursor or loc arguments.\n\n"

                "10. Prefer authoritative and relevant "
                "sources.\n\n"

                "11. When search results contain useful "
                "sources, continue researching instead of "
                "immediately answering.\n\n"

                "12. Before finishing, make sure you have "
                "enough research information to answer "
                "the user's question."
            ),
        },

        {
            "role": "user",

            "content": user_query,
        },
    ]


    # ========================================================
    # AGENT LOOP
    # ========================================================

    agent_turn = 0

    while (

        len(research_data) < MAX_TOOL_CALLS

        and agent_turn < MAX_AGENT_TURNS

    ):

        agent_turn += 1

        print(
            f"\n========== AGENT TURN {agent_turn} =========="
        )


        # ----------------------------------------------------
        # Ask Groq what to do
        # ----------------------------------------------------

        response = _create_completion(

            model=MODEL_NAME,

            messages=messages,

            tools=tools,

            tool_choice="auto",

            max_tokens=MAX_AGENT_OUTPUT_TOKENS,
        )


        response_message = (
            response.choices[0].message
        )


        # ----------------------------------------------------
        # Add assistant message to conversation
        # ----------------------------------------------------

        messages.append(
            response_message
        )


        # ====================================================
        # NO TOOL CALL
        # ====================================================

        if not response_message.tool_calls:

            print(
                "[Agent] No more tools requested."
            )


            # ------------------------------------------------
            # No research was performed
            # ------------------------------------------------

            if not research_data:

                content = (
                    response_message.content
                    or
                    "The agent did not perform web research."
                )

                return {

                    "title": "Research Result",

                    "summary": content,

                    "key_findings": [],

                    "sources": [],

                    "conclusion": content,
                }


            # ------------------------------------------------
            # Research completed
            # ------------------------------------------------

            print(
                "\n[Agent] Research completed."
            )

            print(
                "[Agent] Generating final report..."
            )


            return generate_report(

                user_query=user_query,

                research_content=_research_content(
                    research_data
                ),
            )


        # ====================================================
        # TOOL CALLS
        # ====================================================

        remaining_tool_calls = (
            MAX_TOOL_CALLS
            -
            len(research_data)
        )


        tool_calls = response_message.tool_calls[
            :remaining_tool_calls
        ]


        for tool_call in tool_calls:

            function_name = (
                tool_call.function.name
            )


            # ------------------------------------------------
            # Parse arguments
            # ------------------------------------------------

            try:

                function_args = json.loads(
                    tool_call.function.arguments
                )

            except json.JSONDecodeError:

                print(
                    "[Agent] Invalid tool arguments."
                )

                function_args = {}


            # ------------------------------------------------
            # Limit search results
            # ------------------------------------------------

            if function_name == "search_web":

                function_args["max_results"] = min(

                    int(
                        function_args.get(
                            "max_results",
                            5
                        )
                    ),

                    5,
                )


            # ------------------------------------------------
            # Log tool call
            # ------------------------------------------------

            print(
                f"\n[Agent] Using tool: "
                f"{function_name}"
            )

            print(
                f"[Agent] Arguments: "
                f"{function_args}"
            )


            # ------------------------------------------------
            # Find Python function
            # ------------------------------------------------

            function_to_call = (
                available_functions.get(
                    function_name
                )
            )


            # ------------------------------------------------
            # Tool not found
            # ------------------------------------------------

            if function_to_call is None:

                function_response = (
                    f"Error: Tool "
                    f"'{function_name}' not found."
                )


            # ------------------------------------------------
            # Execute tool
            # ------------------------------------------------

            else:

                try:

                    function_response = (
                        function_to_call(
                            **function_args
                        )
                    )

                except Exception as e:

                    print(
                        f"[Tool Error] "
                        f"{function_name}: {e}"
                    )

                    function_response = (
                        f"Tool error: {str(e)}"
                    )


            # ------------------------------------------------
            # Convert result to string
            # ------------------------------------------------

            function_response = str(
                function_response
            )


            # ------------------------------------------------
            # Store research result
            # ------------------------------------------------

            research_data.append(

                {

                    "tool": function_name,

                    "arguments": function_args,

                    "result": function_response,
                }
            )


            # ------------------------------------------------
            # Log result
            # ------------------------------------------------

            print(
                f"[Agent] Tool result length: "
                f"{len(function_response)} characters"
            )


            # ------------------------------------------------
            # Send tool result back to Groq
            # ------------------------------------------------

            messages.append(

                {

                    "role": "tool",

                    "tool_call_id": (
                        tool_call.id
                    ),

                    "name": function_name,

                    "content": _limit_text(

                        function_response,

                        MAX_TOOL_RESULT_CHARS,
                    ),
                }
            )


    # ========================================================
    # LOOP ENDED
    # ========================================================

    print(
        "\n[Agent] Maximum research loop reached."
    )


    # --------------------------------------------------------
    # If we have research, generate report
    # --------------------------------------------------------

    if research_data:

        print(
            "[Agent] Generating report from collected data..."
        )

        return generate_report(

            user_query=user_query,

            research_content=_research_content(
                research_data
            ),
        )


    # --------------------------------------------------------
    # No research
    # --------------------------------------------------------

    return {

        "title": "Research Failed",

        "summary": (
            "The research request could not be completed."
        ),

        "key_findings": [],

        "sources": [],

        "conclusion": (
            "No usable research information was obtained."
        ),
    }