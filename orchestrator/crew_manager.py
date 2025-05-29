from typing import List, Optional, Union, Dict, Any
from crewai import Agent, Task, Crew, Process
from agents.market_data_agent import MarketDataAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FinancialCrew:
    def __init__(self):
        self.market_data = MarketDataAgent()
        
    def create_agents(self) -> List[Agent]:
        """Create specialized agents for different tasks"""
        
        market_analyst = Agent(
            role='Market Analyst',
            goal='Analyze market data and provide insights',
            backstory='Expert in Asian tech markets with years of experience in portfolio analysis',
            tools=[
                self.market_data.get_portfolio_exposure,
                self.market_data.get_earnings_surprises,
                self.market_data.get_market_sentiment
            ],
            verbose=True,
            allow_delegation=False
        )
        
        report_writer = Agent(
            role='Report Writer',
            goal='Create clear and concise market briefs',
            backstory='Experienced financial writer who specializes in converting complex data into clear narratives',
            verbose=True,
            allow_delegation=False
        )
        
        return [market_analyst, report_writer]
    
    def create_tasks(self, agents: List[Agent]) -> List[Task]:
        """Create tasks for the agents"""
        
        analyze_market = Task(
            description='Analyze Asian tech stocks exposure and earnings',
            agent=agents[0]
        )
        
        write_brief = Task(
            description='Create a market brief based on the analysis',
            agent=agents[1]
        )
        
        return [analyze_market, write_brief]
    
    def run_crew(self) -> str:
        """Execute the crew's tasks"""
        
        if not os.getenv("OPENAI_API_KEY"):
            return "Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
        
        agents = self.create_agents()
        tasks = self.create_tasks(agents)
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return result 