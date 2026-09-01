# Animo Crowd Monster Battle

Ren'Py audience battle connected to a Flask service on Render. Players open the public service URL on their phones and answer each live question. Every correct answer damages the monster; every wrong answer damages the audience team.

## Project layout

- `game/crowd_battle_client.rpy` — Ren'Py HTTP client and shared battle state
- `game/crowd_battle_questions.rpy` — question bank and damage values
- `game/crowd_battle_screens.rpy` — battle HUD, timer, results and settings UI
- `game/script.rpy` — complete playable battle flow
- `voting_server/` — Flask API and mobile voting page
- `render.yaml` — Render Blueprint configuration
- `server.py` — compatibility entry point for an existing root-level Render service

## Run locally

```bash
cd voting_server
python -m venv .venv
pip install -r requirements.txt
python app.py
```

Start the Ren'Py project and keep the default server URL `http://127.0.0.1:5000`.

For another phone on the same Wi-Fi, use the computer's LAN URL, such as `http://192.168.1.20:5000`, in both the phone browser and the Ren'Py server settings.

## Deploy to Render

Create a new Render Blueprint from this repository. Render reads `render.yaml` and starts `voting_server/app.py`. When deployment completes, enter the resulting `https://...onrender.com` URL in the Ren'Py server settings screen.

An existing Render Web Service can keep the previous start command:

```text
gunicorn --workers 1 server:app
```

Optional: add a Render environment variable named `BATTLE_HOST_TOKEN`. Enter the same token in the Ren'Py settings screen. Never commit a real token to this public repository.

## Damage balance

The demo starts with team HP `200` and monster HP `250`.

- Correct answer: `25` monster damage
- Wrong answer: `20` team damage
- No answer: no damage

Change per-question values in `game/crowd_battle_questions.rpy`.
