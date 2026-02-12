from typing import TypedDict, List


class AgentState(TypedDict):
    report_content: str
    current_section: str
    research_data: List[str]
    user_feedback: str
    is_validated: bool