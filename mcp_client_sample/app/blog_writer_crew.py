from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama  # or use OpenAI

# Define the LLM
llm = Ollama(model="llama3.1:8b")  # You can also use OpenAI(model="gpt-4") if you prefer

# Define Agents
researcher = Agent(
    role="Researcher",
    goal="Find accurate information on the latest AI trends",
    backstory="You're a tech-savvy research analyst with a knack for finding reliable and up-to-date info.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

writer = Agent(
    role="Writer",
    goal="Write a clear and engaging summary from the research",
    backstory="You're a professional writer skilled at converting data into easy-to-read reports.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Define Tasks
research_task = Task(
    description="Research the latest trends in AI for 2025, including new models, frameworks, and use cases.",
    expected_output="A bullet-point list of at least 5 current AI trends with 1-2 sentence explanations.",
    agent=researcher
)

writing_task = Task(
    description="Take the AI trends research and write a blog-style summary for a general audience.",
    expected_output="A 4-5 paragraph blog post titled 'Top AI Trends in 2025'.",
    agent=writer
)

# Create Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,  # or Process.parallel
    verbose=True
)

# Kick off the crew
result = crew.kickoff()
print("\nFinal Output:\n")
print(result)
