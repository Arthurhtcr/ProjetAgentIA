from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
load_dotenv()

from agent import app

config = {"configurable": {"thread_id": "test_1"}}


inputs = {"messages": [HumanMessage(content="Rédige un rapport de stage très développé avec les missions de mon stage chez [Nom Entreprise] jour par jour, en te basant sur les documents que je t'ai fournis. Ne me fais pas une liste de courses, je veux un texte développé.")]}

print("--- DÉBUT DU TEST ---")
for event in app.stream(inputs, config=config):
    for node_name, value in event.items():
        print(f"Fin du nœud : {node_name}")
        if "messages" in value:
            last_msg = value["messages"][-1]
            content = last_msg.content if hasattr(last_msg, 'content') else last_msg
            print(f"Contenu : {content}")