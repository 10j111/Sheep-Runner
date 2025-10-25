
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

You may include screenshots, GIFs, or short demo videos here for presentation. To add a screenshot, place the image under `assets/` (for example `assets/screenshots/demo1.png`) and reference it in the README with Markdown:

```markdown
![Gameplay demo](assets/screenshots/demo1.png)
```

## Prepare a public GitHub repository (submission instructions)

When you're ready to submit, create a public GitHub repository and push the project. Example commands (run from the `sheep-runner` folder):

```powershell
# Initialize the repo (if not already a git repo)
git init
git add .
git commit -m "Initial commit - Sheep Runner"
# Create a repo on GitHub (replace <your-repo-url> with the remote URL from GitHub)
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

Make sure the repository is set to Public on GitHub so your instructor can access it.

## Submitting the link on Blackboard

After you create the public GitHub repository, copy the repository URL and submit it on Blackboard as requested by your course instructions. You can update the repo contents later and Blackboard will reference the same URL.

## Troubleshooting

- If you get an error `ModuleNotFoundError: No module named 'pygame'` or `No module named 'numpy'`, confirm you're running the Python executable from the activated virtual environment and that `pip install -r requirements.txt` completed successfully.
- If the Pygame window doesn't show or crashes, check the terminal for error messages and ensure your system has SDL support (most Windows installations are fine with the pygame wheel).

## License & Credits

This project is provided for coursework. Feel free to use and adapt it for the assignment. Include proper attribution if you reuse code or assets from elsewhere.

---

提交说明（中文简要）：

1. 使用上面的步骤创建并激活虚拟环境，安装依赖。
2. 在 GitHub 上创建公开仓库并将本项目推送（参考上面的 git 命令）。
3. 在 Blackboard 提交 GitHub 仓库链接。

如果要我代为创建仓库并推送（你需要给我 GitHub repo 的 URL 或授权令牌），告诉我，我可以把当前项目打包并生成推送步骤说明。
