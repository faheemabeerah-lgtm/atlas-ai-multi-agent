
from crewai import Agent
from tools_web_search import duckduckgo_search


def create_research_agent(llm):
    return Agent(
        role="Senior Researcher",
        goal=(
            "Research the given topic thoroughly using web search "
            "and collect reliable evidence from multiple sources."
        ),
        backstory=(
            "You are an experienced research analyst who finds "
            "relevant information, records source URLs, compares "
            "different perspectives, and clearly identifies "
            "gaps in available evidence."
        ),
        llm=llm,
        tools=[duckduckgo_search],
        verbose=True,
        allow_delegation=False,
    )
