
from crewai import Agent
from tools_web_search import duckduckgo_search


def create_fact_checker_agent(llm):
    return Agent(
        role="Fact-Checking Specialist",
        goal=(
            "Independently verify important research claims, "
            "identify contradictions, and report evidence and caveats."
        ),
        backstory=(
            "You are a careful fact-checker who verifies claims "
            "against independent sources. You classify claims as "
            "supported, mixed, or not verified, and never fabricate "
            "citations or treat search snippets as conclusive proof."
        ),
        llm=llm,
        tools=[duckduckgo_search],
        verbose=True,
        allow_delegation=False,
    )
