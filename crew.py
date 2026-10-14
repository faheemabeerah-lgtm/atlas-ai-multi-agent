from crewai import Crew, Process, Task
from llm_config import get_llm
from agents.research_agent import create_research_agent
from agents.analysis_agent import create_analysis_agent
from agents.fact_checker_agent import create_fact_checker_agent
from agents.report_writer_agent import create_report_writer_agent

def run_research(topic, focus, depth, on_agent_start=None, on_agent_done=None):
    """Run four sequential agents and return (final_report, extracted_source_links)."""
    llm = get_llm()

    researcher = create_research_agent(llm)
    analyst = create_analysis_agent(llm)
    fact_checker = create_fact_checker_agent(llm)
    writer = create_report_writer_agent(llm)

    def notify_start(name, detail):
        if on_agent_start:
            on_agent_start(name, detail)

    def notify_done(name):
        if on_agent_done:
            on_agent_done(name)

    research_task = Task(
        description=(
            "Research this topic using your DuckDuckGo Web Search tool: {topic}\n"
            "Research angle: {focus}\n"
            "Find useful, reasonably recent evidence from multiple sources. Include exact source URLs, "
            "publication dates when visible, short descriptions of what each source supports, and differing views. "
            "Do not write the final report yet. If search fails, say so clearly."
        ),
        expected_output="Research notes with key facts, source titles, URLs, dates where available, and open questions.",
        agent=researcher,
        callback=lambda output: notify_done("Research Agent"),
    )

    analysis_task = Task(
        description=(
            "Analyze the research notes provided by the preceding task for topic: {topic}.\n"
            "Angle: {focus}. Identify 5–8 important findings, patterns, practical implications, counterarguments, "
            "and evidence gaps. Clearly distinguish sourced facts from interpretation."
        ),
        expected_output="A structured analysis of findings, implications, caveats, and claims needing verification.",
        agent=analyst,
        context=[research_task],
        callback=lambda output: notify_done("Analysis Agent"),
    )

    fact_check_task = Task(
        description=(
            "Fact-check the most important factual claims in the research and analysis for: {topic}.\n"
            "Use DuckDuckGo Web Search to independently look for confirmation or contradiction. "
            "Provide claim-by-claim status (supported, mixed, not verified), evidence URLs, date/context caveats, "
            "and corrections. Do not treat search snippets alone as definitive proof."
        ),
        expected_output="A concise verification ledger with claim, status, supporting or conflicting URLs, and caveats.",
        agent=fact_checker,
        context=[research_task, analysis_task],
        callback=lambda output: notify_done("Fact-Checker Agent"),
    )

    writer_task = Task(
        description=(
            "Write the final research report on: {topic}\n"
            "Research angle: {focus}. Desired depth: {depth}.\n"
            "Use the research notes, analysis, and fact-checking ledger. Include: title, date/context note, "
            "executive summary, key findings, detailed analysis, what is uncertain or disputed, conclusion, "
            "and 3 follow-up questions. Include source URLs inline or in a References section. "
            "Do not fabricate URLs or citations. If evidence is weak or unavailable, disclose that."
        ),
        expected_output="A polished Markdown research report with source URLs and explicit uncertainty notes.",
        agent=writer,
        context=[research_task, analysis_task, fact_check_task],
        callback=lambda output: notify_done("Report Writer Agent"),
    )

    notify_start("Research Agent", "Searching the web and collecting evidence.")
    crew = Crew(
        agents=[researcher, analyst, fact_checker, writer],
        tasks=[research_task, analysis_task, fact_check_task, writer_task],
        process=Process.sequential,
        verbose=True,
    )

    # CrewAI runs tasks sequentially. Notify UI of the next stage from task callbacks.
    # These callbacks fire when a task completes; start labels are updated from a lightweight
    # task callback wrapper below when supported by the installed CrewAI release.
    result = crew.kickoff(inputs={"topic": topic, "focus": focus, "depth": depth})

    report = str(result)
    sources = []
    import re
    seen = set()
    for url in re.findall(r'https?://[^\s\]\)>,]+', report):
        clean_url = url.rstrip(".,;:")
        if clean_url not in seen:
            seen.add(clean_url)
            sources.append({"title": clean_url, "url": clean_url, "snippet": ""})
    return report, sources
