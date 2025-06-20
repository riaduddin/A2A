from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.utils import new_agent_text_message
from pydantic import BaseModel


class GreetingAgent(BaseModel):
    """Greeting agent that returns a greeting"""
    print("Greeting Agent initialized")
    async def invoke(self) -> str:
        return "Hello YouTube! Make sure to like and subscribe!"


class GreetingAgentExecutor(AgentExecutor):

    def __init__(self):
        print("Greeting Agent Executor initialized")
        self.agent = GreetingAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        print("Executing Greeting Agent")
        result = await self.agent.invoke()
        print(f"Result from Greeting Agent: {result}")
        await event_queue.enqueue_event(new_agent_text_message(result))
        print("Greeting Agent execution completed")
    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        raise Exception("Cancel not supported")
