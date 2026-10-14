
from crewai import Agent


def create_analysis_agent(llm):
    return Agent(
        role="Research Analysis Specialist",
        goal=(
            "Analyze research findings, identify important patterns, "
            "evaluate implications, and distinguish facts from opinions."
        ),
        backstory=(
            "You are an analytical specialist who turns raw research "
            "into structured insights. You examine trends, compare "
            "viewpoints, identify counterarguments, and highlight "
            "uncertainties without inventing evidence."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
