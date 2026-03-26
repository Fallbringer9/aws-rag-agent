

# AWS RAG Agent – Du prototype local à une architecture cloud

## Overview

Ce projet est une implémentation complète d’un système de **Retrieval-Augmented Generation (RAG) avec un agent IA**, conçu pour fonctionner à la fois **en local et dans le cloud (AWS)**.

L’objectif principal de ce projet est d’explorer et de comprendre en profondeur :

- Le fonctionnement concret des systèmes RAG
- L’intégration d’un **agent IA** au-dessus d’un pipeline de retrieval
- La transformation d’un **projet local en architecture cloud scalable**

Ce projet n’est pas une simple démo, mais un **backend complet** avec ingestion, recherche et exposition via API.

---

## Objectif du projet

L’objectif de ce projet est simple :

Construire et comprendre un système IA basé sur le RAG et les agents, en local puis en cloud.

Cela inclut :

- Comprendre la recherche vectorielle (FAISS)
- Travailler avec des LLM via AWS Bedrock
- Mettre en place une architecture avec agent
- Apprendre à cloudifier un projet Python réel

---

## Du local au cloud

### Version locale

Au départ, le projet fonctionnait entièrement en local :

- Lecture de documents depuis le disque
- Découpage (chunking)
- Génération d’embeddings
- Stockage dans FAISS
- Requête via un agent

Tout était exécuté via un script (`main.py`) avec un état local.

---

### Version cloud (AWS)

Le projet a ensuite été entièrement cloudifié avec :

- AWS Lambda (exécution)
- Amazon S3 (stockage)
- API Gateway (exposition HTTP)
- AWS Bedrock (LLM + embeddings)

#### Architecture finale

User → API Gateway → Lambda (Query) → Agent → Retrieval (FAISS) → S3 → Bedrock → Réponse

Ingestion :

Upload S3 → Lambda (Ingestion) → Chunking → Embeddings → FAISS → S3 (artifacts)

---

## Fonctionnalités principales

- Pipeline RAG avec FAISS
- Agent IA basé sur Strands
- Ingestion automatique via trigger S3
- Architecture serverless (AWS Lambda)
- Séparation ingestion / query
- Support multi-documents
- Persistance de l’index vectoriel dans S3

---

## Stack technique

### Backend
- Python

### IA
- FAISS
- AWS Bedrock (Claude + Titan)
- Strands (agent)

### Cloud
- AWS Lambda
- S3
- API Gateway
- IAM

---

## Architecture

Le projet est structuré en plusieurs couches :

- Handlers (interfaces) → point d’entrée AWS
- Services (app) → orchestration
- Logique métier → RAG, retrieval, agent

Cela permet :

- Test local
- Réutilisation du code
- Bonne séparation des responsabilités

---

## Cloudification : ce qui a changé

Le projet a été transformé de :

- fichiers locaux → stockage S3
- script unique → Lambdas séparées
- état mémoire → persistance via S3
- exécution manuelle → architecture événementielle

La logique métier (chunking, embedding, retrieval, agent) n’a pas été réécrite, mais adaptée pour fonctionner dans un environnement stateless.

---

## Ce qui est présent dans Lambda

Chaque Lambda contient :

- Le code métier (ingestion, retrieval, RAG, agent)
- Les handlers (points d’entrée)
- Les services applicatifs

Les dépendances lourdes sont séparées en layers :

- Layer FAISS → faiss + numpy
- Layer Strands → agent

---

## Challenges rencontrés

### FAISS dans Lambda
- Problème : dépendance native
- Solution : layer construit via Docker

### Limite de taille Lambda
- Problème : dépassement 250MB
- Solution : séparation code / layers

### Permissions Bedrock
- Problème : AccessDenied
- Solution : ajout des permissions nécessaires (InvokeModel, Converse, streaming)

### Stateless
- Problème : pas d’état persistant
- Solution : stockage des artefacts dans S3

---

## Pourquoi Lambda

Lambda est adapté car :

- Les requêtes sont courtes (quelques secondes)
- Le système est stateless
- Scalabilité automatique
- Coût optimisé

---

## Apprentissage

Ce projet a été réalisé avec l’aide :

- De la documentation officielle (AWS, FAISS, etc.)
- D’outils d’IA pour comprendre, debugger et structurer l’architecture

L’objectif n’était pas seulement de faire fonctionner le projet, mais de comprendre chaque couche en profondeur.

---

## Améliorations possibles

- Optimisation du chargement FAISS
- Ajout d’authentification API
- Monitoring (CloudWatch)
- Passage à une architecture containerisée
- Indexation incrémentale

---

## Conclusion

Ce projet montre le passage de :

Un prototype local

à

Un backend IA serverless, scalable et prêt pour la production.

Il met en évidence la compréhension de :

- RAG
- Agents IA
- Architecture cloud
- Contraintes réelles de production