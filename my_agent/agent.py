from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import tools_condition
from utils.nodes import researcher, writer, human_review, tool_node



def decide_to_continue(state: MessagesState):
    last_message = state["messages"][-1].content.lower()
    if "ok" in last_message in last_message:
        return END
    return "writer"

workflow = StateGraph(MessagesState)

workflow.add_node("researcher", researcher)
workflow.add_node("tools", tool_node)
workflow.add_node("writer", writer)
workflow.add_node("human_review", human_review)

workflow.add_edge(START, "researcher")
workflow.add_conditional_edges(
    "researcher",
    tools_condition, 
    {
        "tools": "tools",
        "__end__": "writer"
    }
)
workflow.add_edge("tools", "researcher")
workflow.add_edge("writer", "human_review")

# Logique de décision : validation ou retour au writer
workflow.add_conditional_edges("human_review",decide_to_continue,
    {
        "end": END,
        "writer": "writer"
    }
)

app = workflow.compile(interrupt_before=["human_review"])


try:
    # Utilise Mermaid pour générer un PNG via une API web (plus simple)
    image_data = app.get_graph().draw_mermaid_png()
    with open("graph_workflow.png", "wb") as f:
        f.write(image_data)
    print("Graphe généré avec succès : graph_workflow.png")
except Exception as e:
    print(f"Erreur lors de la génération du graphe : {e}")