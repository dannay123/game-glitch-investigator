import pytest

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    reset_game_state,
)


# --- get_range_for_difficulty: Normal/Hard swap fixed ---

def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_range_normal_is_1_to_50():
    # Normal was wrongly 1-100; fixed to 1-50
    assert get_range_for_difficulty("Normal") == (1, 50)


def test_range_hard_is_1_to_100():
    # Hard was wrongly 1-50; fixed to 1-100 (hard = bigger range)
    assert get_range_for_difficulty("Hard") == (1, 100)


def test_range_unknown_defaults_to_1_to_100():
    assert get_range_for_difficulty("Whatever") == (1, 100)


def test_range_case_insensitive():
    # difficulty selector should be case insensitive (and whitespace-tolerant)
    assert get_range_for_difficulty("easy") == (1, 20)
    assert get_range_for_difficulty("NORMAL") == (1, 50)
    assert get_range_for_difficulty("  hArD  ") == (1, 100)


# --- parse_guess: floats truncate, scientific notation skipped ---

def test_parse_valid_int():
    assert parse_guess("42") == (True, 42, None)


def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_empty():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_float_truncates_down():
    # Floats should truncate, not round
    assert parse_guess("5.9") == (True, 5, None)


def test_parse_float_whole():
    assert parse_guess("7.0") == (True, 7, None)


def test_parse_negative_int():
    assert parse_guess("-3") == (True, -3, None)


# --- check_guess: hint swap fixed (returns tuple) ---

def test_check_win():
    assert check_guess(50, 50) == ("Win", "🎉 Correct!")


def test_check_too_high_says_go_lower():
    # Guessed too high -> hint must tell user to go LOWER
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_check_too_low_says_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


def test_check_large_overshoot_says_go_lower():
    # Guessed 200 vs secret 29: numeric compare must say too high -> go LOWER.
    # (Old str() cast made "200" < "29" wrongly read as too low.)
    outcome, message = check_guess(200, 29)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_check_large_negative_undershoot_says_go_higher():
    # Guessed -200 vs secret 29: numeric compare must say too low -> go HIGHER.
    outcome, message = check_guess(-200, 29)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


def test_check_type_mismatch_path_too_high():
    # int guess vs str secret triggers TypeError fallback path
    outcome, message = check_guess(60, "50")
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_check_type_mismatch_path_too_low():
    outcome, message = check_guess(4, "50")
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


# --- update_score: no negatives, consistent penalties, win off-by-one fixed ---

def test_win_first_attempt_full_100():
    # attempt_number 1 = first guess -> full 100 points
    assert update_score(0, "Win", 1) == 100


def test_win_later_attempt_decrements_by_10():
    assert update_score(0, "Win", 2) == 90
    assert update_score(0, "Win", 3) == 80


def test_win_points_floor_at_10():
    # Many attempts can't drop win reward below 10
    assert update_score(0, "Win", 20) == 10


def test_too_high_penalizes_5():
    assert update_score(50, "Too High", 4) == 45


def test_too_low_penalizes_5():
    assert update_score(50, "Too Low", 4) == 45


def test_too_high_no_bonus_on_even_attempt():
    # Old bug gave +5 on even attempts; now always -5
    assert update_score(50, "Too High", 2) == 45


def test_score_never_goes_negative():
    assert update_score(0, "Too Low", 1) == 0
    assert update_score(3, "Too High", 1) == 0


def test_unknown_outcome_unchanged():
    assert update_score(42, "Whatever", 1) == 42


# --- reset_game_state: New Game must fully reset so finished games replay ---

def test_reset_returns_playing_status():
    # Core bug: status stayed "won"/"lost", so st.stop() blocked new guesses.
    assert reset_game_state(7)["status"] == "playing"


def test_reset_clears_attempts_and_history():
    state = reset_game_state(7)
    assert state["attempts"] == 0
    assert state["history"] == []


def test_reset_sets_new_secret():
    assert reset_game_state(42)["secret"] == 42


def test_reset_from_won_lets_player_guess_again():
    # Simulate a finished, WON game then New Game.
    won = {"secret": 13, "attempts": 3, "status": "won", "history": [10, 20, 13]}
    fresh = reset_game_state(55)
    won.update(fresh)
    # status no longer "won" -> app.py won't st.stop()
    assert won["status"] == "playing"
    assert won["attempts"] == 0
    assert won["history"] == []
    assert won["secret"] == 55


def test_reset_from_lost_lets_player_guess_again():
    # Simulate a finished, LOST (out of attempts) game then New Game.
    lost = {"secret": 99, "attempts": 8, "status": "lost", "history": [1, 2, 3]}
    fresh = reset_game_state(4)
    lost.update(fresh)
    assert lost["status"] == "playing"
    assert lost["attempts"] == 0
    assert lost["history"] == []
    assert lost["secret"] == 4
