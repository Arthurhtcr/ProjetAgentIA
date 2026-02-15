from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import HumanMessage
from agent import app

config = {"configurable": {"thread_id": "session_finale_M2"}}

def run_agent():
    state = app.get_state(config)
    
    if not state.values:
        print("\n--- LANCEMENT INITIAL ---")
        inputs = {"messages": [HumanMessage(content="Rédige un rapport de stage très développé avec les missions de mon stage chez [Nom Entreprise] jour par jour, en te basant sur les documents que je t'ai fournis. Ne me fais pas une liste de courses, je veux un texte développé.")]}
        for event in app.stream(inputs, config=config, stream_mode="values"):
            pass
    
    while True:
        state = app.get_state(config)
        if state.next:
            print("\n" + "="*50)
            print("SECTION RÉDIGÉE :")
            print(state.values["messages"][-1].content)
            print("="*50)
            
            choice = input("\n[Validation] \n- 'OK' : Valider et passer à la semaine suivante \n- 'Terminer' : Valider et arrêter le rapport ici \n- Ou tape tes corrections : \n> ")
            
            if choice.lower() == "terminer":
                app.update_state(config, {"messages": [HumanMessage(content="Terminer")]})
                for event in app.stream(None, config=config): pass
                print("Rapport finalisé et enregistré !")
                break
            elif choice.lower() == "ok":
                # On enregistre la semaine actuelle dans le fichier avant de passer à la suite
                app.update_state(config, {"messages": [HumanMessage(content="OK, passe à la semaine suivante")]})
                print("Recherche des infos pour la semaine suivante...")
                for event in app.stream(None, config=config): pass
            else:
                app.update_state(config, {"messages": [HumanMessage(content=choice)]})
                for event in app.stream(None, config=config): pass

if __name__ == "__main__":
    run_agent()