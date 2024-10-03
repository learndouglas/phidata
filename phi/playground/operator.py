from typing import List, Optional

from phi.agent.agent import Agent, Tool, Toolkit, Function
from phi.agent.session import AgentSession
from phi.utils.log import logger


def format_tools(agent_tools):
    formatted_tools = []
    if agent_tools is not None:
        for tool in agent_tools:
            if isinstance(tool, dict):
                formatted_tools.append(tool)
            elif isinstance(tool, Tool):
                formatted_tools.append(tool.to_dict())
            elif isinstance(tool, Toolkit):
                for f_name, f in tool.functions.items():
                    formatted_tools.append(f.to_dict())
            elif isinstance(tool, Function):
                formatted_tools.append(tool.to_dict())
            elif callable(tool):
                func = Function.from_callable(tool)
                formatted_tools.append(func.to_dict())
            else:
                logger.warning(f"Unknown tool type: {type(tool)}")
    return formatted_tools


def get_agent_by_id(agents: List[Agent], agent_id: str) -> Optional[Agent]:
    for agent in agents:
        if agent.agent_id == agent_id:
            return agent
    return None


def get_session_title(session: AgentSession) -> Optional[str]:
    memory = session.memory
    if memory is not None:
        chat_history = memory.get("chat_history")
        if chat_history is not None:
            for history in chat_history:
                if history.get("role") == "user":
                    return history.get("content")
    return None