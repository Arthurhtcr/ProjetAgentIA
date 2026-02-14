from langchain_core.tools import tool
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.tools.tavily_search import TavilySearchResults
import os

embeddings = HuggingFaceEmbeddings(
    model_name="jinaai/jina-embeddings-v3", 
    model_kwargs={"trust_remote_code": True}
)

persist_dir = os.path.join(os.path.dirname(__file__), "../chroma_db")
vector_db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
tavily = TavilySearchResults(k=2)

@tool
def recherche_rapport(query: str):
    """
    Recherche des informations pour le rapport de stage. 
    Cherche d'abord dans les documents internes (notes de stage) 
    puis sur le web si l'information est manquante ou incomplète.
    """
    print(f"--- TOOL: Recherche pour '{query}' ---")
    
    docs_with_scores = vector_db.similarity_search_with_score(query, k=2)
    
    info_interne = ""
    needs_web = True
    
    if docs_with_scores:
        score = docs_with_scores[0][1]
        if score < 0.8: 
            needs_web = False
            print(f"Tool : Info trouvée en interne (score: {score:.2f})")
        info_interne = "\n".join([d[0].page_content for d in docs_with_scores])

    info_web = ""
    if needs_web:
        print("Tool : Info interne insuffisante, appel à Tavily...")
        web_results = tavily.invoke({"query": query})
        info_web = f"\n\nRésultats Web : {web_results}"

    return f"SOURCES TROUVÉES :\n{info_interne}{info_web}"