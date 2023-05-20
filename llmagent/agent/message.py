"""
Structured messages to an agent, typically from an LLM, to be handled by
an agent. The messages could represent, for example:
- information or data given to the agent
- request for information or data from the agent
- request to run a method of the agent
"""

from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List
from random import choice


INSTRUCTION = """
    When one of these tools is applicable, you must express your request in 
    JSON format. The fields will be based on the tool description, which will be of 
    the form:
    
    <tool_name>: description involving <arg1> maybe some other <arg2> and so on.
    
    The JSON format will be:
    {
        "request": "<tool_name>",
        "<arg1>": <value1>,
        "<arg2>": <value2>
    } 
    where it is important to note that <arg1> is the NAME of the argument, 
    and <value1> is teh VALUE of the argument.
    
    For example if a tool has this description is available:
    
    country_capital: check if <city> is the capital of <country>,
    
    and you want to check whether the capital of France is Paris, you must the 
    ask in the following JSON format: 
    
    The JSON format will be:
    {
        "request": "country_capital",
        "country": "France",
        "city": "Paris"
    }
    
    But if you want to find out the population of France, you must ask in natural
    nautral language: "What is the population of France?"
    
    Whenever possible, AND ONLY IF APPLICABLE, use these tools, with the JSON syntax 
    specified above. When a tool is applicable, simply use this syntax, do not write 
    anything else. Only if no tool is exactly applicable, ask in natural language. 
    """


class AgentMessage(ABC, BaseModel):
    """
    A (structured) message to an agent, typically from an LLM, to be handled by
    the agent. The message could represent
    - information or data given to the agent
    - request for information or data from the agent
    Attributes:
        request (str): name of agent method to map to.
        purpose (str): purpose of agent method, expressed in general terms.
        result (str): result of agent method.
    """

    request: str
    purpose: str
    result: str

    class Config:
        arbitrary_types_allowed = True
        validate_all = True
        validate_assignment = True

    @classmethod
    @abstractmethod
    def examples(cls) -> List["AgentMessage"]:
        """
        Examples to use in few-shot demos with JSON formatting instructions.
        Returns:
        """
        pass

    def usage_example(self) -> str:
        """
        Instruction to the LLM showing an example of how to use the message.
        Returns:
            str: example of how to use the message
        """
        # pick a random example of the fields
        ex = choice(self.examples())
        return ex.json_example()

    def json_example(self):
        return self.json(indent=4, exclude={"result", "purpose"})

    def dict_example(self):
        return self.dict(exclude={"result", "purpose"})