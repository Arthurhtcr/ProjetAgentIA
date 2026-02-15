from langgraph.prebuilt import ToolNode
from langchain.chat_models import init_chat_model
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from .state import AgentState
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.tools.tavily_search import TavilySearchResults
from .tools import recherche_rapport


embeddings = HuggingFaceEmbeddings(model_name="jinaai/jina-embeddings-v3", model_kwargs={"trust_remote_code": True})
vector_db = Chroma(persist_directory="../chroma_db", embedding_function=embeddings)

tavily = TavilySearchResults(k=2)


llm = init_chat_model(
    model="mistral-small-latest",
    temperature=0.1,  
    max_tokens=1000
)

tools = [recherche_rapport]
tool_node = ToolNode(tools)

llm_with_tools = llm.bind_tools([recherche_rapport])

def researcher(state: AgentState):
    print("--- NOEUD RESEARCHER ---")
    sys_msg = SystemMessage(content="""Tu es un assistant de recherche. 
    Ta mission est d'extraire les informations pour UNE SEULE SEMAINE de stage à la fois.
    Regarde l'historique : si aucune semaine n'est rédigée, cherche la Semaine 1. 
    Si la Semaine 1 existe, cherche la Semaine 2. 
    NE CHERCHE PAS TOUT LE STAGE D'UN COUP.""")
    
    response = llm_with_tools.invoke([sys_msg] + state["messages"])
    return {"messages": [response]}
    
# --- NOEUD WRITER ---
def writer(state: MessagesState):
    print("--- RÉDACTION ---")
    messages = state.get("messages", [])
    context = messages[-1].content

    system_prompt = """Tu es un expert en rédaction de rapports de stage de Master 2. 
    Ta mission est de rédiger ou mettre à jour une section du rapport en utilisant UNIQUEMENT les sources fournies.
    Rédige un rapport de stage très développé avec les missions de mon stage chez [Nom Entreprise] jour par jour, en te basant sur les documents que je t'ai fournis. Ne me fais pas une liste de courses, je veux un texte développé.
    RÈGLES STRICTES :
    1. STYLE : Ton académique, professionnel.
    2. FORMAT : Utilise exclusivement le Markdown (titres, listes à puces, gras).
    3. FIDÉLITÉ : Si une information n'est pas dans les sources, ne l'invente pas. 
    4. STRUCTURE : Commence par un titre de niveau ## ou ###.
    5. LANGUE : Français impeccable.

    Si les sources mentionnent des éléments de l'entreprise, intègre-les avec précision.
    Ajoutes les sources utilisées à la fin de la section, sous une rubrique "Sources" formatée en Markdown.

    RÈGLE CRUCIALE : Ne rédige qu'UNE SEULE SEMAINE à la fois. 
    Si tu reçois des informations sur plusieurs semaines, choisis la suivante dans l'ordre chronologique.
    Arrête-toi après avoir rédigé une semaine.
    """
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Rédige une section basée sur ces recherches :\n{context}")
    ])
    
    return {"messages": [response]}

# --- NOEUD HUMAN REVIEW ---
def human_review(state: MessagesState):
    print("--- ATTENTE DE VALIDATION HUMAINE ---")
    return {}


def saver(state: MessagesState):
    print("--- EXPORT DANS LE FICHIER ---")
    
    report_text = ""
    for m in reversed(state["messages"]):
        if m.type == "ai" and not m.tool_calls:
            report_text = m.content
            break

    with open("rapport_final.md", "a", encoding="utf-8") as f:
        f.write("\n\n") 
        f.write(report_text)
        f.write("\n\n---")
        
    return {"messages": [SystemMessage(content="Semaine ajoutée au fichier.")]}