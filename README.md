# Flappy Hell

Un Flappy Bird en Python (pygame) où une IA apprend à jouer grâce à
l'algorithme NEAT (NeuroEvolution of Augmenting Topologies).

## Fonctionnalités

- Jeu Flappy Bird développé avec pygame
- Entraînement d'une IA par neuroévolution (neat-python)
- Visualisation du meilleur oiseau entraîné

## Prérequis

- Python 3.13
- Git

## Installation

```bash
git clone https://github.com/TON_PSEUDO/flappy-hell.git
cd flappy-hell
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

## Utilisation

Lancer le jeu :

```bash
python main.py
```

Entraîner l'IA :

```bash
python train_ai.py
```

Voir jouer le meilleur oiseau entraîné :

```bash
python watch_winner.py
```

## Structure du projet

```
flappy-hell/
├── assets/            # images, sons, polices
├── main.py            # lancement du jeu
├── train_ai.py        # entraînement NEAT
├── watch_winner.py    # démonstration du meilleur génome
├── bird.py            # classe de l'oiseau
├── pipes.py           # classe des tuyaux
├── fire.py            # obstacles de feu
├── game_objects.py    # objets du jeu
├── settings.py        # paramètres
├── neat_config.txt    # configuration NEAT
├── best_genome.pkl    # meilleur génome sauvegardé
└── requirements.txt   # dépendances
```

## Technologies

Python 3.13, pygame 2.6.1, neat-python 2.0.0

## Licence

MIT
