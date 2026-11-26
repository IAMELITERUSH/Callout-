# Callout

**Say it. Score it.** A free, voice-activated score counter for 1 to 5 players or teams.

Say "point for Mark" and Callout adds the point and reads the score aloud.

**Play now:** https://callout-gamma.vercel.app

## Features

- **Smart voice control** that understands everyday phrasing, corrections and questions
- **Score read aloud** after each score change (on by default)
- **1 to 5 counters**, side by side, each with its own name and color
- **Custom rules:** starting score, winning score, points per tap, win by 2, and scores below zero
- **Count up or down:** set "Until" lower than "Starting at" to count down
- **Spoken setup:** set names and rules by voice
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

## Smart voice

You don't need exact commands. Callout works out who you mean and what you want, so you can talk naturally. It runs inside your browser with built-in language rules, with no AI account, key or fee.

Use the names you entered, a counter color ("red team"), a position ("player two", or "left side" with two counters).

| You want to | For example |
|---|---|
| Add points | "Give Sara two" · "Mark scores" · "Another one for Mark" |
| Score several at once | "2 for Mark and 1 for Sara" · "Everyone gets a point" |
| Take points away | "Take one from Mark" · "Sara loses 2" |
| Set a score | "Set Mark to 10" · "Sara should have 8" |
| Fix a mistake | "No, that was Sara" · "Scratch that" |
| Repeat | "Same again" · "One more" |
| Ask | "Who's winning?" · "How many does Mark need?" · "What are we playing to?" |
| Control the game | "Swap sides" · "Start over" · "Be quiet" · "Start talking" · "Go home" · "Stop listening" |
| After a win | "Next match" · "Play again" |

To avoid scoring from background chatter, Callout ignores sentences it isn't sure about. The top of the screen shows what it heard. Wait for the score to finish being read before speaking again.

### Spoken rules

On the rules page, tap **Speak the rules** and say, for example, "names are Mark and Sara, first to 21, win by 2".

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
