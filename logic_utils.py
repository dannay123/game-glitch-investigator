def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    d = (difficulty or "").strip().lower()  #FIX: difficulty selector case insensitive
    if d == "easy":
        return 1, 20
    if d == "normal":          #FIX: number ranges accordingly to difficulty
        return 1, 50
    if d == "hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"          #FIX: Hint switchup fixed
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def reset_game_state(secret):
    """
    Return a fresh game state for a new game.

    Resets attempts, status, and history so a finished game (won/lost)
    becomes playable again. `secret` is the new randomly drawn number
    (drawn by the caller within the difficulty range).
    """
    return {
        "secret": secret,
        "attempts": 0,
        "status": "playing",
        "history": [],
    }


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)        #FIX: win score calculator
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High" or outcome == "Too Low":  #FIX: scores cant be negative and too high deducts points
        new_score = current_score - 5
        if new_score < 0:
            new_score = 0
        return new_score

    return current_score
