
# Sheep Runner — Pixel-style Endless Runner

This is a small pixel-style endless runner implemented in Python using Pygame. The player controls a sheep that runs to the right, eats collectibles, avoids obstacles and wolves, and can shoot projectiles.

This README prepares the project for submission to a public GitHub repository and explains how to run and interact with the game.

## Features

- Player sheep with movement and double-jump
- Collectibles: grass and mushrooms with timed effects (grow, pink theme, fly)
- Obstacles and moving wolves (enemies)
- Shooting mechanic (Space or Left Mouse) to destroy wolves
- Procedural short sound effects and optional background music (requires numpy)
- Simple menu and rules screen

## Requirements

- Python 3.11+ (the project was tested with Python 3.13)
- The project uses these Python packages:

  - pygame==2.6.1
  - numpy==2.3.4

## Installation (Windows - PowerShell)

Open a PowerShell terminal in the project folder (`sheep-runner`) and run the commands below.

1) Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3) Run the game:

```powershell
python main.py
```

Notes:
- If you already have a project-wide `.venv` created (for example the one included in the workspace), you can run the game with that Python executable directly:

```powershell
C:\path\to\your\.venv\Scripts\python.exe main.py
```

## Controls

- A / Left Arrow: Move left
- D / Right Arrow: Move right
- W / Up Arrow / Space: Jump (double jump supported)
- Space or Left Mouse: Shoot a projectile (space does NOT make the sheep jump in the current build — it's reserved for shooting)
- R: Restart after game over
- Mouse click: Select menu buttons

## Files in this repo

- `main.py` — game entry point
- `game.py` — main game loop, rendering, input handling, sound
- `sheep.py` — `Sheep` player class
- `grass.py` — collectibles, obstacles, wolves, spawner logic
- `config.py` — tuning constants (screen size, speeds, spawn rates)
- `assets/` — placeholder folders for sprites and fonts (currently contains `.gitkeep` placeholders)
- `requirements.txt` — Python dependencies
- `README.md` — this file

## Screenshots / Demo






https://github.com/user-attachments/assets/93501418-d0a7-4105-ac65-d799d94638f0



