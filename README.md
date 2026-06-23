# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
   + To guess a random number from 1 to 25/50/100 depending on the difficulty. Just a simple fidget game.
- [x] Detail which bugs you found.
   + Quite a few: The code containing logic wasn't in the right file; The logic of the hints were switched up; the difficulty were not even correct (1-100 for Normal, 1-50 for Hard); Guessing out of bounds showed a bug where the number got cast into a string if the attempt was even; The score calculator did not compensate justifiably to the number of guesses; Case sensitivity when typing out in the difficulty selector.
- [x] Explain what fixes you applied.
   + All of them was really straightforward. I just need to go to the code where the logic breaks, put a right fix to it (which usually just requires switching up existing code or just a few line of simple code), then it is done. After that, ran pytest and run the app again myself to test it manually.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Select Hard (1-100) and guesses 50
2. Game returns "Too Low", if get hint is checked: "Go HIGHER!"
3. Guesses 60, game returns " Too High", "Go LOWER!"
4. Guesses 57, Correct number, game won
5. Score updates according to each guess and whether game is won or lost. Press new game to play again


## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= 32 passed in 0.11s =========================
```

## 🚀 Stretch Features

- Did not implement
