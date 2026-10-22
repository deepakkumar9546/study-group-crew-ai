
import os
from pathlib import Path
from typing import Type

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import BaseTool

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


# Load API settings from .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv(
    "OPENAI_BASE_URL",
    "https://openrouter.ai/api/v1"
)
model_name = os.getenv("MODEL_NAME", "openrouter/free")

if not api_key or api_key == "your_openrouter_api_key_here":
    raise ValueError(
        "Add your OpenRouter API key to the .env file first."
    )

# Connect CrewAI to the OpenRouter-compatible API.
llm = LLM(
    model=model_name,
    api_key=api_key,
    base_url=base_url,
    custom_openai=True,
    temperature=0.2
)


# -----------------------------
# LANGCHAIN TOOLS
# -----------------------------

class SearchInput(BaseModel):
    query: str = Field(description="Topic or question to search for")


class DuckDuckGoAdapter(BaseTool):
    name: str = "DuckDuckGo Web Search"
    description: str = (
        "Search the web for information about a topic."
    )
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        tool = DuckDuckGoSearchRun()
        return str(tool.invoke({"query": query}))


class WikipediaAdapter(BaseTool):
    name: str = "Wikipedia Search"
    description: str = (
        "Find background information about a topic on Wikipedia."
    )
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        wrapper = WikipediaAPIWrapper(
            top_k_results=3,
            doc_content_chars_max=4000
        )
        tool = WikipediaQueryRun(api_wrapper=wrapper)
        return str(tool.invoke({"query": query}))


web_search = DuckDuckGoAdapter()
wikipedia_search = WikipediaAdapter()


# -----------------------------
# FOUR SPECIALIZED AGENTS
# -----------------------------

researcher = Agent(
    role="Topic Researcher",
    goal="Collect useful and accurate information about {topic}",
    backstory=(
        "You are a careful educational researcher who uses "
        "web search and reference material to gather relevant facts."
    ),
    tools=[web_search, wikipedia_search],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

quiz_maker = Agent(
    role="Quiz Maker",
    goal="Create a useful quiz based on the research about {topic}",
    backstory=(
        "You are an experienced teacher who creates clear "
        "multiple-choice questions with correct answers and explanations."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)

explainer = Agent(
    role="Explainer",
    goal="Explain {topic} in simple language with examples",
    backstory=(
        "You are a patient teacher who explains difficult concepts "
        "in a beginner-friendly way."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)

fact_checker = Agent(
    role="Fact-Checker",
    goal="Review the study material and flag unsupported claims",
    backstory=(
        "You are a careful academic reviewer who checks factual "
        "claims, identifies uncertainty, and improves learning material."
    ),
    tools=[wikipedia_search],
    llm=llm,
    verbose=True,
    allow_delegation=False
)


# -----------------------------
# TASKS AND CONTEXT FLOW
# -----------------------------

research_task = Task(
    description=(
        "Research the topic '{topic}'. Explain the main concepts, "
        "important facts, practical uses, and common misconceptions. "
        "Use the available search tools. Include source names or "
        "URLs when available. Do not invent facts."
    ),
    expected_output=(
        "Organized research notes containing key concepts, facts, "
        "examples, and available source references."
    ),
    agent=researcher
)

quiz_task = Task(
    description=(
        "Using the research notes, create 5 multiple-choice questions "
        "about '{topic}'. Provide four options per question, the "
        "correct answer, and a short explanation. Keep the questions "
        "relevant to the supplied research."
    ),
    expected_output=(
        "Five numbered MCQs with four options, correct answers, "
        "and brief explanations."
    ),
    agent=quiz_maker,
    context=[research_task]
)

explanation_task = Task(
    description=(
        "Explain '{topic}' for a beginner using the research notes "
        "and quiz. Include a simple definition, key points, at least "
        "one practical example, and a short revision summary."
    ),
    expected_output=(
        "A beginner-friendly explanation with examples and a revision "
        "summary, consistent with the research notes."
    ),
    agent=explainer,
    context=[research_task, quiz_task]
)

review_task = Task(
    description=(
        "Review all research, quiz questions, and explanations about "
        "'{topic}'. Check important factual claims against reliable "
        "reference information where possible. Correct clear errors, "
        "flag claims that cannot be verified, and produce one final "
        "Markdown study guide with sections for Research, Explanation, "
        "Quiz with Answers, Fact-Checking Notes, and Key Takeaways. "
        "Never claim that an unsupported fact has been verified."
    ),
    expected_output=(
        "A complete Markdown study guide with all five sections, "
        "including corrections and explicit uncertainty notes."
    ),
    agent=fact_checker,
    context=[research_task, quiz_task, explanation_task]
)


# -----------------------------
# RUN THE CREW AND SAVE OUTPUT
# -----------------------------

def main():
    topic = input(
        "Enter a study topic (default: Python OOP): "
    ).strip()

    if not topic:
        topic = "Python Object-Oriented Programming"

    print(f"\nStarting Study Group Crew for: {topic}\n")

    crew = Crew(
        agents=[
            researcher,
            quiz_maker,
            explainer,
            fact_checker
        ],
        tasks=[
            research_task,
            quiz_task,
            explanation_task,
            review_task
        ],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff(inputs={"topic": topic})

    report_path = OUTPUT_DIR / "study_report.md"
    report_path.write_text(str(result), encoding="utf-8")

    print("\nStudy Group Crew completed.")
    print(f"Report saved to: {report_path}")
    print("\nPreview:\n")
    print(str(result)[:1500])


if __name__ == "__main__":
    main()
