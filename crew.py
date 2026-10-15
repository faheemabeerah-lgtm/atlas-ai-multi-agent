
# Fix the known CrewAI + Groq cache_breakpoint bug.
import crewai.llms.cache as _crewai_cache

_crewai_cache.mark_cache_breakpoint = lambda msg: msg

from crewai import Crew, Process, Task

from llm_config import get_llm
from tools_web_search import get_search_tool

from agents.research_agent import create_research_agent
from agents.analysis_agent import create_analysis_agent
from agents.fact_checker_agent import create_fact_checker_agent
from agents.report_writer_agent import create_report_writer_agent


def run_research(topic):
    topic = topic.strip()

    if not topic:
        raise ValueError("Please enter a research topic.")

    llm = get_llm()
    search_tool = get_search_tool()

    researcher = create_research_agent(llm, search_tool)
    analyst = create_analysis_agent(llm)
    fact_checker = create_fact_checker_agent(llm)
    writer = create_report_writer_agent(llm)

    research_task = Task(
        description=(
            "Research the topic: {topic}. "
            "Use web search to collect relevant facts, evidence, "
            "and useful sources. Clearly distinguish facts from "
            "uncertain claims."
        ),
        expected_output=(
            "A detailed research summary with key facts, "
            "evidence, and source links."
        ),
        agent=researcher,
    )

    analysis_task = Task(
        description=(
            "Analyze the research findings about {topic}. "
            "Identify the main themes, insights, benefits, risks, "
            "and important implications. Use the research task output."
        ),
        expected_output=(
            "A structured analysis with key insights, benefits, "
            "risks, and implications."
        ),
        agent=analyst,
        context=[research_task],
    )

    fact_check_task = Task(
        description=(
            "Check the research and analysis about {topic}. "
            "Identify unsupported claims, contradictions, and "
            "uncertainties. Do not invent evidence or sources."
        ),
        expected_output=(
            "A fact-check report identifying supported findings, "
            "uncertain claims, and corrections needed."
        ),
        agent=fact_checker,
        context=[research_task, analysis_task],
    )

    report_task = Task(
        description=(
            "Write a polished final research report about {topic}. "
            "Include an executive summary, key findings, analysis, "
            "fact-check notes, conclusion, and source links. "
            "Do not invent citations."
        ),
        expected_output=(
            "A clear, well-organized research report with headings "
            "and source links."
        ),
        agent=writer,
        context=[research_task, analysis_task, fact_check_task],
    )

    crew = Crew(
        agents=[
            researcher,
            analyst,
            fact_checker,
            writer,
        ],
        tasks=[
            research_task,
            analysis_task,
            fact_check_task,
            report_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(inputs={"topic": topic})
    return str(result)
