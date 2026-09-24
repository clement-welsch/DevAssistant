# DevAssistant

Assistant de développement local basé sur un LLM, avec une architecture RAG évolutive et orientée projets.

## 🎯 Objectif

**DevAssistant** est un assistant IA personnel destiné à accompagner le développement logiciel au quotidien.

L'objectif est de disposer d'un assistant capable de :

* comprendre les problématiques techniques rencontrées pendant le développement ;
* rechercher des informations pertinentes dans la documentation des projets ;
* aider à analyser et déboguer du code ;
* expliquer des concepts techniques ;
* accompagner l'apprentissage de nouvelles technologies ;
* conserver un contexte spécifique à chaque projet sans mélanger les connaissances.

Le projet est développé progressivement afin de comprendre et maîtriser les différentes briques techniques plutôt que de dépendre immédiatement d'un framework d'agent ou de RAG.

L'exécution du modèle est prévue **localement**, notamment afin de conserver la maîtrise des données et de limiter les dépendances à des services externes.

---

## 🧠 Principe général

DevAssistant s'appuie sur plusieurs briques complémentaires :

```text
                    ┌──────────────────────┐
                    │       Utilisateur    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    DevAssistant      │
                    │  orchestration/agent│
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌───────────┐    ┌────────────┐   ┌─────────────┐
        │ RAG       │    │ Outils     │   │ Contexte    │
        │ commun    │    │ développeur│   │ projet      │
        └─────┬─────┘    └────────────┘   └──────┬──────┘
              │                                   │
              ▼                                   ▼
       Documentation                     RAG spécifiques
       technique                         NutriScope
       générale                          M2I
                                         CKIN2
              │
              └─────────────────┬─────────────────┘
                                ▼
                       ┌──────────────────┐
                       │      LLM         │
                       │  Gemma / local   │
                       └──────────────────┘
```

### Modèle de langage

Le LLM est exécuté localement via **LM Studio**.

Le modèle actuellement utilisé pour les expérimentations est :

```text
gemma-4-e4b
```

LM Studio fournit une API compatible avec l'API OpenAI permettant à l'application Python de communiquer avec le modèle local.

### Embeddings

Les embeddings permettent de transformer les textes en vecteurs afin de mesurer leur proximité sémantique.

Le modèle actuellement utilisé est :

```text
text-embedding-nomic-embed-text-v1.5
```

### RAG

Le RAG (Retrieval-Augmented Generation) permettra de rechercher les informations pertinentes avant de les transmettre au LLM.

Le principe est :

```text
Question
   │
   ▼
Embedding de la question
   │
   ▼
Recherche de documents similaires
   │
   ▼
Documents pertinents
   │
   ▼
Prompt enrichi avec le contexte
   │
   ▼
LLM
   │
   ▼
Réponse
```

---

# 🏗️ Architecture prévue

L'architecture sera construite progressivement.

```text
DevAssistant/
│
├── devassistant/
│   ├── config.py
│   ├── lmstudio_client.py
│   └── ...
│
├── rag/
│   ├── common/
│   ├── nutriscope/
│   ├── m2i/
│   └── ckin2/
│
├── prompts/
│
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md
```

### `devassistant/`

Contient le cœur de l'application et les composants permettant notamment de communiquer avec le LLM local.

### `rag/`

Contient les connaissances utilisées pour la recherche documentaire.

Les connaissances seront séparées par contexte :

* `common/` → connaissances techniques générales ;
* `nutriscope/` → documentation du projet NutriScope ;
* `m2i/` → supports et exercices de formation ;
* `ckin2/` → documentation du projet CKIN2.

Cette séparation permet d'éviter de mélanger inutilement les contextes.

### `prompts/`

Contient les prompts structurés utilisés par les différents composants de l'assistant.

### `tests/`

Contient les tests et expérimentations permettant de valider progressivement les différentes briques.

---

# 🧪 Étapes de conception

Le projet sera développé par étapes afin de valider chaque concept indépendamment.

## Phase 1 — Environnement et socle Python

Objectifs :

* créer un environnement Python reproductible ;
* définir les dépendances dans `requirements.txt` ;
* mettre en place Git ;
* définir une structure Python propre ;
* mettre en place les premiers tests.

État : **en cours**

---

## Phase 2 — Communication avec le LLM

Objectifs :

* communiquer avec LM Studio ;
* interroger le modèle local ;
* centraliser la configuration ;
* créer une interface Python simple pour envoyer des prompts ;
* vérifier le comportement du modèle.

Premier composant :

```text
lmstudio_client.py
```

État : **expérimental**

---

## Phase 3 — Embeddings

Objectifs :

* générer des embeddings ;
* comprendre la représentation vectorielle des textes ;
* mesurer la similarité entre deux textes ;
* expérimenter la similarité cosinus.

Cette phase constitue la base du système de recherche sémantique.

État : **prototype fonctionnel**

---

## Phase 4 — Premier RAG minimal

Construire un RAG complet sans framework afin de comprendre précisément son fonctionnement.

Pipeline :

```text
Question
    ↓
Embedding
    ↓
Similarité
    ↓
Sélection des documents
    ↓
Construction du contexte
    ↓
Prompt
    ↓
LLM
    ↓
Réponse
```

Objectif : disposer d'un RAG minimal fonctionnel avant d'introduire des abstractions supplémentaires.

État : **à venir**

---

## Phase 5 — Gestion des connaissances

Objectifs :

* organiser les documents ;
* découper les documents en morceaux pertinents (*chunking*) ;
* générer et conserver leurs embeddings ;
* mettre en place une recherche plus efficace ;
* séparer les connaissances communes des connaissances propres aux projets.

État : **à venir**

---

## Phase 6 — RAG spécialisés

Mise en place de plusieurs bases de connaissances indépendantes :

```text
RAG commun
├── Python
├── C++
├── Git
├── SQL
├── PostgreSQL
├── pandas
├── NumPy
├── pytest
└── ...

RAG NutriScope
RAG M2I
RAG CKIN2
```

L'objectif est de pouvoir fournir au système uniquement le contexte nécessaire à la demande.

État : **à venir**

---

## Phase 7 — Outils développeur

L'assistant pourra progressivement accéder à des outils permettant notamment de :

* analyser des fichiers ;
* rechercher dans le code ;
* interpréter des erreurs ;
* exécuter certaines opérations contrôlées ;
* exploiter les résultats de tests ;
* interagir avec Git.

Les outils seront ajoutés progressivement et avec des limites explicites.

État : **à venir**

---

## Phase 8 — Agent / orchestration

Une couche d'orchestration sera introduite lorsque les briques précédentes seront suffisamment maîtrisées.

Son rôle sera notamment de déterminer :

```text
Question utilisateur
       │
       ▼
Quel contexte ?
       │
       ├── connaissances générales
       ├── NutriScope
       ├── M2I
       └── CKIN2
       │
       ▼
Quels outils ?
       │
       ▼
Recherche / analyse
       │
       ▼
LLM
       │
       ▼
Réponse
```

L'agent ne constituera donc pas le point de départ du projet : il sera construit **au-dessus des briques déjà validées**.

État : **à venir**

---

# 🔬 Philosophie de développement

DevAssistant est développé selon une approche incrémentale :

1. comprendre une technologie ;
2. réaliser une expérimentation minimale ;
3. vérifier son fonctionnement ;
4. l'intégrer au projet ;
5. écrire les tests nécessaires ;
6. documenter le fonctionnement ;
7. passer à la brique suivante.

Le projet privilégie donc la compréhension de l'architecture et des mécanismes sous-jacents avant l'utilisation de frameworks complexes.

---

# 🌿 Organisation Git

Le développement utilise un modèle basé sur deux branches principales :

```text
main
  │
  └── develop
        │
        ├── feat/...
        ├── fix/...
        └── refactor/...
```

* `main` : version stable ;
* `develop` : branche d'intégration ;
* `feat/...` : nouvelles fonctionnalités ;
* `fix/...` : corrections ;
* `refactor/...` : évolutions structurelles.

Chaque fonctionnalité doit partir de `develop` et être intégrée à `develop` après validation.

Exemple :

```bash
git checkout develop
git checkout -b feat/rag-v2
```

---

# 🔒 Données et confidentialité

Le projet est conçu pour fonctionner localement.

Les éléments suivants ne doivent pas être versionnés :

* environnement virtuel Python ;
* fichiers contenant des secrets ;
* données personnelles ;
* documents privés ;
* modèles LLM ;
* bases vectorielles ou données générées volumineuses.

Le dépôt contient le **code et la configuration nécessaires à la reconstruction du projet**, mais pas les ressources locales qui peuvent être lourdes ou sensibles.

---

# 🚧 État actuel

Le projet se trouve actuellement dans sa phase expérimentale initiale.

Les premières briques validées sont :

* environnement Python dédié ;
* communication avec LM Studio ;
* génération d'embeddings ;
* calcul de similarité cosinus ;
* premiers tests de communication avec le LLM.

La prochaine étape consiste à mettre en place une structure Python propre puis à construire un **premier RAG minimal de bout en bout**, sans framework spécialisé.

---

## 📌 Technologies envisagées

* Python 3.12
* LM Studio
* Gemma
* text-embedding-nomic-embed-text-v1.5
* NumPy
* OpenAI Python SDK
* Git
* pytest

Des technologies supplémentaires pourront être introduites lorsque leur nécessité sera démontrée par l'évolution du projet.
