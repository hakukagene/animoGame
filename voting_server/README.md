# Animo Crowd Battle server

## Local run

```bash
python -m venv .venv
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` on a phone or browser. The Ren'Py host uses the JSON endpoints under `/api`.

## Optional host protection

Set `BATTLE_HOST_TOKEN` in Render and enter the same value in the Ren'Py server settings screen. Do not commit the token to this public repository.

The service intentionally runs with one Gunicorn worker because the live battle state is held in memory. Render PostgreSQL/Redis can be added later when more than one simultaneous room is required.
