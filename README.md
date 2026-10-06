# Flappy Hell

Un jeu de type **Flappy Bird** développé en Python avec **pygame**, dans lequel une intelligence artificielle apprend à jouer grâce à l'algorithme **NEAT (NeuroEvolution of Augmenting Topologies)**.

Le projet combine développement de jeu, simulation, apprentissage par neuroévolution et sauvegarde du meilleur génome entraîné.

## Fonctionnalités

- Jeu Flappy Bird développé avec pygame
- Entraînement automatique d'une IA avec NEAT
- Évolution d'une population de réseaux de neurones
- Sauvegarde du meilleur génome entraîné
- Visualisation du meilleur oiseau après entraînement

## Prérequis

- Python 3.13
- Git

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/louchenilounes/flappy_hell.git
cd flappy_hell
```

Créer l'environnement virtuel :

```bash
python -m venv .venv
```

Activer l'environnement virtuel dans Git Bash :

```bash
source .venv/Scripts/activate
```

Installer les dépendances :

```bash
python -m pip install -r requirements.txt
```

## Utilisation

### Lancer le jeu

```bash
python main.py
```

### Entraîner l'IA

```bash
python train_ai.py
```

L'entraînement utilise NEAT pour faire évoluer progressivement les réseaux de neurones afin d'améliorer les performances des oiseaux.

Le meilleur génome est sauvegardé dans :

```text
best_genome.pkl
```

### Visualiser le meilleur oiseau

Après l'entraînement :

```bash
python watch_winner.py
```

## Structure du projet

```text
flappy_hell/
├── assets/            # Images, sons et polices
├── main.py            # Lancement du jeu
├── train_ai.py        # Entraînement de l'IA avec NEAT
├── watch_winner.py    # Démonstration du meilleur génome
├── bird.py            # Gestion de l'oiseau
├── pipes.py           # Gestion des tuyaux
├── fire.py            # Gestion des obstacles de feu
├── game_objects.py    # Objets du jeu
├── settings.py        # Paramètres du jeu
├── neat_config.txt    # Configuration de NEAT
├── best_genome.pkl    # Meilleur génome entraîné
└── requirements.txt   # Dépendances Python
```

## Technologies

- Python 3.13
- pygame 2.6.1
- neat-python 2.0.0
- NEAT (NeuroEvolution of Augmenting Topologies)

## Licence

MIT
