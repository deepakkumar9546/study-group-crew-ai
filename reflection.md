# Project Reflection — Study Group Crew AI

During this project, I built a multi-agent system using Python and CrewAI to help students learn a topic. The system contains four agents: Topic Researcher, Quiz Maker, Explainer, and Fact-Checker. Each agent has a specific role, goal, and backstory.

The project ran successfully. The agents executed their tasks sequentially, passed information through task context, and generated a study guide containing research notes, explanations, quiz questions, answers, and fact-checking notes. I integrated two LangChain tools for web search and Wikipedia search using CrewAI-compatible adapters. The final output was saved to a Markdown file.

One limitation was that live web verification was unavailable during the run. Therefore, the fact-checking agent could not freshly verify every claim against online sources. The quality of the output also depends on the language model and the information returned by the tools.

In the future, I would improve the project by adding stronger source verification, better error handling, automated tests, and a simple user interface. I would also test the system on different study topics to evaluate the accuracy and usefulness of the generated material.

This project helped me understand how multiple AI agents can work together, how tools extend their capabilities, and how task context passes information between agents.