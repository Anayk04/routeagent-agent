import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

def summarize_dispatch(dispatch_result: str) -> str:
    """
    Uses Gemini to generate a human-readable executive summary
    of the dispatch decisions made by the RouteAgent.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )

    prompt = f"""
You are a logistics operations analyst.
Below is a raw dispatch report from an autonomous AI dispatch agent.

Convert this into a clean, professional executive summary that a
logistics manager would read. Include:
- Total shipments dispatched vs skipped
- Key matching decisions and why they were optimal
- Any efficiency observations (e.g. smallest vehicle used)
- Overall operational status

Keep it concise, professional, and under 200 words.

RAW DISPATCH REPORT:
{dispatch_result}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content