# Fishing Minigame for Ren'Py

This is a fishing minigame integrated into the Ren'Py visual novel engine. The minigame was originally developed as a standalone Pygame application and has been refactored to work within Ren'Py.

## How It Works

The minigame is implemented in `game/fishing_minigame.rpy` and uses Ren'Py's screen language and Python functionality to create an interactive fishing experience.

### Gameplay

- **Objective**: Catch the fish by keeping the bobber (fishing hook) in contact with the fish for a certain amount of time.
- **Controls**: Press and hold the SPACE key to move the bobber upward. Release to let it fall.
- **Timer**: You have 10 seconds to catch the fish before it swims away.
- **Progress Bar**: The vertical bar on the right shows your progress toward catching the fish.

### Integration

The minigame is integrated into the main story at the fishing date scene. The result of the minigame (whether you caught a fish or not) affects the dialogue that follows.

### Files

- `fishing_minigame.rpy`: The main Ren'Py implementation of the minigame
- `fishing-minigame/water.png`: Background image
- `fishing-minigame/bobber.png`: The fishing bobber image
- `fishing-minigame/fish.png`: The fish image
- `fishing-minigame/catch-text.png`: Success screen overlay
- `fishing-minigame/away-text.png`: Failure screen overlay

## Technical Details

The minigame uses:
- Ren'Py's screen language for UI
- Python classes for game logic
- Timer-based updates for animation
- Collision detection for gameplay mechanics

To call the minigame from any point in the script, use:
```renpy
$ caught_fish = renpy.call_in_new_context("fishing_minigame")
```

The variable `caught_fish` will be `True` if the player caught the fish, or `False` if they didn't.
