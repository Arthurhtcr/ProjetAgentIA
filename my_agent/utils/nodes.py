from langgraph.prebuilt import ToolNode
from langchain.chat_models import init_chat_model
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from .state import AgentState



llm = init_chat_model(
    model="mistral-small-latest",
    temperature=0.1,  
    max_tokens=1000
)

# --- NOEUD RESEARCHER ---
def researcher(state: AgentState):
    print("--- RECHERCHE D'INFOS ---")
    last_message = state['messages'][-1].content
    
    # Chercher dans ChromaDB
    # results = vector_db.similarity_search(last_message)
    
    # Si résultats insuffisants -> Tavily
    # if not results:
    #     results = tavily.search(last_message)
    research_results = "infos trouvées"
    
    return {"messages": [SystemMessage(content=f"Voici les recherches : {research_results}")]}

# --- NOEUD WRITER ---
def writer(state: AgentState):
    print("--- RÉDACTION ---")
    new_content = state['report_content'] + "\n## Nouvelle Section\nContenu généré..."
    return {"report_content": new_content}

# --- NOEUD HUMAN REVIEW ---
def human_review(state: AgentState):
    print("--- ATTENTE DE VALIDATION HUMAINE ---")
    pass