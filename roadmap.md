# Roadmap : Agent IA - Workflow d'écriture de rapport de stage

## Objectif
Développer un agent autonome capable de rédiger un rapport de stage structuré en utilisant un graphe d'états, avec une validation humaine quotidienne et une gestion de mémoire long terme.

## Phases de Développement

### Phase 1 : Initialisation
- [x] Initialiser le dépôt Github.
- [ ] Créer l'environnement virtuel et installer les dépendances.
- [x] Envoyer le mail d'initialisation avec l'URL du repo.
- [x] Configurer le fichier `roadmap.md` (ce fichier).

### Phase 2 : Architecture du Graphe (LangGraph)
- [ ] Définir l'état du graphe pour suivre l'avancement du rapport.
- [ ] Implémenter les nœuds :
    - `researcher` : Cherche des infos (ChromaDB d'abord, Tavily en secours).
    - `writer` : Rédige ou met à jour une section en Markdown.
    - `human_review` : Point d'arrêt pour la validation journalière.
- [ ] Configurer les arêtes avec la logique de boucle pour la reformulation.

### Phase 3 : Intelligence & RAG
- [ ] Configurer **ChromaDB** pour stocker les données de l'entreprise et les notes de stage.
- [ ] Intégrer l'outil de recherche **Tavily**.
- [ ] Développer les prompts système pour garantir le ton et la structure du rapport.

### Phase 4 : Persistance & Interaction
- [ ] Implémenter un `Checkpointer` pour permettre d'arrêter et reprendre le workflow.
- [ ] Créer l'interface d'interaction pour la validation humaine.
- [ ] Gérer l'export automatique vers le fichier final `rapport_final.md`.

### Phase 5 : Bonus & Finalisation
- [ ] Implémenter une couche de détection de Prompt Injection.
- [ ] Générer une version PDF du rapport final.

---
