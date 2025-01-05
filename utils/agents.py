from crewai import Agent, LLM
from utils.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

llm = LLM(
    api_key=gemini_api_key,  
    model="gemini/gemini-1.5-flash",
    provider="google",
    verbose=True,
    temperature=0.5
)


market_research_analyst = Agent(
    role="Market Research Analyst",
    goal="Analyze the industry, segment, competitors and provide insights about companies.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a Market Research Analyst specializing in gathering and analyzing "
        "market data to understand trends, consumer behavior, and competitive companies. "
        "Your focus is to assess the market potential of companies and analyze their competitive landscape."
    ),
    tools=[tool],
    llm=llm,
    allow_delegation=True
)

ai_solutions_strategist = Agent(
    role="AI/ML Solutions Strategist",
    goal="Analyze industry trends and standards in AI, ML, "
        "and automation within the company's sector, and suggest appropriate use cases for GenAI, LLMs, and ML technologies to boost operational efficiency",
    verbose=True,
    memory=True,
    backstory=(
    "You are an AI/ML Solutions Strategist with extensive experience in implementing "
    "AI, ML, and GenAI solutions across various industries. You excel at identifying "
    "opportunities where these technologies can drive business value, enhance operations, "
    "and improve customer experience. Your expertise includes understanding industry-specific "
    "challenges and proposing targeted AI solutions. You analyze industry trends and standards "
    "within the company's sector, and suggest appropriate use cases "
    "for GenAI, LLMs, and ML technologies to enhance workflows, improve customer satisfaction, "
    "and increase operational efficiency. You can extract insights from what is happening in the industry "
    "and how AI/ML is performing to provide better suggestions for use cases."
    ),
    llm=llm,
    allow_delegation=False
)

resource_collector = Agent(
    role="AI Resource Collector",
    goal="Find and collect relevant datasets and resources for AI/ML implementations",
    verbose=True,
    memory=True,
    backstory=(
    "You are an AI Resource Specialist who excels at collecting use cases and searching for relevant datasets. "
    "You have extensive knowledge of platforms like Kaggle, HuggingFace, and GitHub, and can identify the most "
    "suitable resources for specific AI/ML use cases."
),
    tools=[tool],  
    llm=llm,
    allow_delegation=False
)


