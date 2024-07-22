import importlib
import src.config as config
importlib.reload(config)
from src.config import system_prompt as prompt
from openai import OpenAI
import re
from dotenv import load_dotenv

_ = load_dotenv()

client = OpenAI()

class Agent:
    def __init__(self, system="", LLM_type="gpt-4o-mini"):
        self.system = system
        self.messages = []
        self.LLM_type = LLM_type
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result, self.messages

    def execute(self):
        completion = client.chat.completions.create(
                        model=self.LLM_type, 
                        temperature=0,
                        messages=self.messages)
        return completion.choices[0].message.content

def calculate(what):
    return eval(what)

def retrieve_tasks(unused_input=None):
    """Simulated external data retrieval"""
    return [
        {"task": "Implement Machine Learning Model", "priority": "High", "effort": 40},
        {"task": "Optimize Database Queries", "priority": "Medium", "effort": 25},
        {"task": "Design User Interface", "priority": "High", "effort": 30},
        {"task": "Set Up CI/CD Pipeline", "priority": "Low", "effort": 20},
        {"task": "Perform Security Audit", "priority": "Medium", "effort": 35}
    ]

def retrieve_resources(unused_input=None):
    """Simulated external resource retrieval"""
    return [
        {"resource": "Elena", "skill": "Machine Learning", "available_hours": 45},
        {"resource": "Raj", "skill": "Database Optimization", "available_hours": 30},
        {"resource": "Sofia", "skill": "UI/UX Design", "available_hours": 35},
        {"resource": "Liam", "skill": "DevOps", "available_hours": 25},
        {"resource": "Yuki", "skill": "Cybersecurity", "available_hours": 40}
    ]

def allocate_resources(allocation_input=None):
    """Parse the allocation_input and return a list of allocations
    For simplicity, let's assume it's already in the correct format"""
    if allocation_input is None:
        return "Error: No allocation input provided. Please provide allocation details."
    return eval(allocation_input)

def estimate_budget(hours, hourly_rate):
    """Estimate the budget based on the number of hours and hourly rate"""
    return hours * hourly_rate

action_re = re.compile(r'Action: (\w+)(?:\s*:\s*(.+))?')

def query(question, max_turns=10, known_actions={} ,LLM_type="gpt-4o-mini"):
    i = 0
    bot = Agent(prompt, LLM_type)
    next_prompt = question

    while i < max_turns:
        i += 1
        result, messages = bot(next_prompt)
        print(result)
        
        actions = [
            action_re.match(a) 
            for a in result.split('\n') 
            if action_re.match(a)
        ]
       
        if actions:
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            
            # Always pass action_input, even if it's None
            observation = known_actions[action](action_input)
            
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            break 

    return messages