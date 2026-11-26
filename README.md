# Callout

**Say it. Score it.** A free, voice-activated score counter for 1 to 5 players or teams.

Say "point for Mark" and Callout adds the point and reads the score aloud.

**Play now:** https://callout-gamma.vercel.app

## Features

- **Voice control** for adding, removing and undoing points
- **Score read aloud** after each score change (on by default)
- **1 to 5 counters**, side by side, each with its own name and color
- **Custom rules:** starting score, winning score, points per tap, win by 2, and scores below zero
- **Count up or down:** set "Until" lower than "Starting at" to count down
- **Spoken setup:** tap "Speak the rules" and say "until 20, starting at 5"
- **Liquid Glass-style buttons**, in a contrasting color on each side
- **Next Match:** after a win, return to the rules page with the same names and rules
- **Extras:** game timer, tap sounds, vibration, keep screen on, and swap sides (where your device supports them)
- Saves your rules and unfinished game on your device

## How to play

1. Tap **New Game**.
2. Choose how many counters you want and enter names.
3. Set **Starting at** and **Until**.
4. Tap **Start Game** and allow the microphone.
5. Call out points, or tap **+** and **−**.

## Voice commands

Replace "Mark" with any name you entered, or a counter color such as "blue".

| Say | What happens |
|---|---|
| "Point for Mark" | Adds your "points per tap" amount |
| "Add 3 to Mark" | Adds 3 points |
| "Minus point Mark" | Removes your "points per tap" amount |
| "Undo" | Reverses the last score change during a match |
| "What's the score" | Reads the score |
| "Reset game" | Returns all scores to the starting number |
| "Next match" | After a win, opens the rules page |
| "Stop listening" | Turns the microphone off |

Wait for the score to finish being read before saying the next command.

## Run it on your computer

You need Python 3. There are no extra packages to install.

```bash
python app.py
```

Callout opens in your browser, usually at `http://localhost:8765`.

## Publishing

This repository is connected to Vercel. Each push to the `main` branch publishes the new version automatically.

To get the latest code on your computer:

```bash
git pull
```

## Voice support

- Use Chrome or Safari and allow microphone access.
- On iPhone, turn on Siri and Dictation. If listening stops, tap **Mic**.
- Voice recognition is provided by your browser. It may need an internet connection and may send audio to the browser maker's service.
- Noisy rooms and unusual names can cause missed commands.

## Project files

| File | Purpose |
|---|---|
| `app.py` | The whole app |
| `pyproject.toml` | Python and Vercel settings |
| `README.md` | This guide |
