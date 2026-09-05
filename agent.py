
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from tools import TOOLS
from summarizer import summarize_dispatch


load_dotenv()

console = Console()


def build_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )

    agent = create_react_agent(
    llm,
    TOOLS,
)

    return agent


def main() -> None:
    console.print()
    console.print(
        Panel(
            "[bold cyan]🚚 ROUTEAGENT[/bold cyan]\n"
            "[dim]Autonomous Logistics Dispatch System[/dim]",
            border_style="cyan",
            expand=False,
        )
    )

    console.print("\n[bold yellow]Starting dispatch process...[/bold yellow]\n")

    agent = build_agent()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": """
You are RouteAgent, an autonomous logistics dispatch agent.

Your job is to dispatch every pending shipment using the best
available driver and idle vehicle.

DISPATCH WORKFLOW:
1. Call get_pending_shipments
2. Call get_available_drivers
3. Call get_idle_vehicles
4. Match every pending shipment to the best available driver and vehicle
5. Call dispatch_shipment for every valid match
6. Provide a final dispatch summary

MATCHING RULES:
- Shipment weight must not exceed vehicle capacity
- Prefer the smallest vehicle that can safely carry the shipment weight
- Do not assign the same driver or vehicle to multiple shipments
- If no suitable driver or vehicle exists, skip that shipment and explain why
- Never invent IDs, capacities, weights or any data
- Use only information returned by the tools
- Process shipments in FIFO order based on created_at

REASONING for every dispatch must include:
- Shipment weight
- Selected vehicle and its capacity and why it fits
- Selected driver and why they were chosen

Now dispatch all pending shipments.
"""
                }
            ]
        }
    )

    # ---------------------------------------------------------
    # Extract final Gemini response
    # ---------------------------------------------------------

    raw_output = result["messages"][-1].content

    if isinstance(raw_output, list):
        raw_text = " ".join(
            block["text"]
            for block in raw_output
            if isinstance(block, dict)
            and block.get("type") == "text"
        )
    else:
        raw_text = str(raw_output)

    # ---------------------------------------------------------
    # Gemini dispatch log
    # ---------------------------------------------------------

    console.print(
        Panel(
            "[bold blue]GEMINI DISPATCH LOG[/bold blue]\n"
            "[dim]AI dispatch execution and reasoning[/dim]",
            border_style="blue",
            expand=False,
        )
    )

    console.print(Markdown(raw_text))

    # ---------------------------------------------------------
    # Claude executive summary
    # ---------------------------------------------------------

    console.print()

    console.print(
        Panel(
            "[bold magenta]CLAUDE EXECUTIVE SUMMARY[/bold magenta]\n"
            "[dim]Management-level dispatch analysis[/dim]",
            border_style="magenta",
            expand=False,
        )
    )

    claude_summary = summarize_dispatch(raw_text)

    console.print(Markdown(claude_summary))

    # ---------------------------------------------------------
    # Completion
    # ---------------------------------------------------------

    console.print()

    console.print(
        Panel(
            "[bold green]✓ ROUTEAGENT DISPATCH COMPLETED[/bold green]",
            border_style="green",
            expand=False,
        )
    )

    console.print()


if __name__ == "__main__":
    main()
