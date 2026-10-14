
from crewai import Agent


def create_report_writer_agent(llm):
    return Agent(
        role="Professional Research Report Writer",
        goal=(
            "Produce a clear, comprehensive Markdown research report "
            "using the research, analysis, and fact-checking results."
        ),
        backstory=(
            "You are a professional report writer who transforms "
            "research evidence into well-organized reports. You include "
            "an executive summary, key findings, detailed analysis, "
            "uncertainties, conclusions, follow-up questions, and "
            "references supported by the supplied evidence."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
