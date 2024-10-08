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

def retrieve_tasks(priority_level=None):
    """Retrieve tasks filtered by priority level."""
    
    tasks = [
        {"task": "Implement Machine Learning Model", "priority": "High", "effort": 40},
        {"task": "Optimize Database Queries", "priority": "Medium", "effort": 25},
        {"task": "Design User Interface", "priority": "High", "effort": 30},
        {"task": "Set Up CI/CD Pipeline", "priority": "Low", "effort": 20},
        {"task": "Perform Security Audit", "priority": "Medium", "effort": 35}
    ]
    
    if priority_level:
        filtered_tasks = [task for task in tasks if task["priority"].lower() == priority_level.lower()]
        return filtered_tasks

    return tasks

def retrieve_resources(unused_input=None):
    """Simulated external resource retrieval"""
    return [
        {"resource": "Elena", "skill": "Machine Learning", "available_hours": 45},
        {"resource": "Raj", "skill": "Database Optimization", "available_hours": 30},
        {"resource": "Sofia", "skill": "UI/UX Design", "available_hours": 35},
        {"resource": "Liam", "skill": "DevOps", "available_hours": 25},
        {"resource": "Yuki", "skill": "Cybersecurity", "available_hours": 40}
    ]


action_re = re.compile(r'Action:\s*(\w+)(?:\((.*?)\))?')

def query(question, max_turns=10, known_actions={}, LLM_type="gpt-4o"):
    i = 0
    bot = Agent(prompt, LLM_type)
    next_prompt = question

    while i < max_turns:
        i += 1
        result, messages = bot(next_prompt)
        print(result)
        
        # Match the action using the updated regex
        actions = [
            action_re.match(a.strip()) 
            for a in result.split('\n') 
            if action_re.match(a.strip())
        ]
       
        if actions:
            action, action_input = actions[0].groups()
            
            if action_input:
                action_input = action_input.strip("'\"")
                key_value_match = re.match(r'(\w+)=(.+)', action_input)
                if key_value_match:
                    action_input = key_value_match.group(2).strip("'\"")
            else:
                action_input = None

            print(f" -- running {action} with input: {action_input}")

            observation = known_actions[action](action_input)
            
            print("Observation:", observation)
            next_prompt = f"Observation: {observation}"
        else:
            break 

    return messages, result