
import os
from pathlib import Path

import streamlit as st

# Read the API key securely from Streamlit Cloud secrets.
try:
    for key in ("OPENAI_API_KEY", "OPENAI_BASE_URL", "MODEL_NAME"):
        if key in st.secrets:
            os.environ[key] = st.secrets[key]
except Exception:
    # Locally, main.py can load settings from the .env file.
    pass

# Reuse the existing four agents and their tasks.
import main as project
from crewai import Crew, Process

st.set_page_config(
    page_title="Study Group Crew AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Study Group Crew AI")
st.write(
    "Learn any topic with four AI agents: Researcher, "
    "Quiz Maker, Explainer, and Fact-Checker."
)

topic = st.text_input(
    "Enter a topic to study",
    value="Python Object-Oriented Programming",
    max_chars=200
)

if st.button("Generate Study Guide", type="primary"):
    if not topic.strip():
        st.warning("Please enter a study topic.")
    else:
        try:
            with st.spinner(
                "The four AI agents are preparing your study guide. "
                "This may take several minutes."
            ):
                crew = Crew(
                    agents=[
                        project.researcher,
                        project.quiz_maker,
                        project.explainer,
                        project.fact_checker
                    ],
                    tasks=[
                        project.research_task,
                        project.quiz_task,
                        project.explanation_task,
                        project.review_task
                    ],
                    process=Process.sequential,
                    verbose=True
                )

                result = crew.kickoff(
                    inputs={"topic": topic.strip()}
                )

                report = str(result)

                output_dir = Path(__file__).resolve().parent / "output"
                output_dir.mkdir(exist_ok=True)

                report_path = output_dir / "study_report.md"
                report_path.write_text(report, encoding="utf-8")

            st.success("Your study guide is ready!")
            st.markdown(report)

            st.download_button(
                label="Download Study Guide",
                data=report,
                file_name="study_report.md",
                mime="text/markdown"
            )

        except Exception as exc:
            st.error(
                "The study guide could not be generated. "
                "Check your API key, model availability, "
                "and deployment logs."
            )
            st.exception(exc)

st.caption(
    "Powered by Python, CrewAI, LangChain tools, and OpenRouter."
)
