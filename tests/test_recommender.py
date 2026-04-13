from src.recommender import Song, UserProfile, Recommender, recommend_songs, score_song, SCORING_MODES, load_songs


def make_song(id=1, genre="pop", mood="happy", energy=0.8, valence=0.9,
              acousticness=0.2, popularity=72, release_year=2022,
              explicit=0, language="English", instruments="synth|drums|bass",
              listening_context="workout", avg_listener_age=22, subgenre="dance pop"):
    return {
        "id": id, "title": f"Song {id}", "artist": "Test",
        "genre": genre, "mood": mood, "energy": energy,
        "tempo_bpm": 120, "valence": valence, "danceability": 0.8,
        "acousticness": acousticness, "popularity": popularity,
        "release_year": release_year, "explicit": explicit,
        "language": language, "instruments": instruments,
        "listening_context": listening_context,
        "avg_listener_age": avg_listener_age, "subgenre": subgenre,
    }


def make_prefs(genre="pop", mood="happy", energy=0.8, acoustic=False,
               mainstream=True, recent=True, allow_explicit=True,
               language="English", instruments=None, context="workout",
               age=22, subgenre="dance pop"):
    return {
        "favorite_genre": genre, "favorite_mood": mood,
        "target_energy": energy, "likes_acoustic": acoustic,
        "likes_mainstream": mainstream, "prefers_recent": recent,
        "allow_explicit": allow_explicit,
        "preferred_language": language,
        "preferred_instruments": instruments or [],
        "listening_context": context,
        "user_age": age,
        "favorite_subgenre": subgenre,
    }


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1, title="Test Pop Track", artist="Test Artist",
            genre="pop", mood="happy", energy=0.8, tempo_bpm=120,
            valence=0.9, danceability=0.8, acousticness=0.2,
            popularity=72, release_year=2022, explicit=0,
            language="English", instruments="synth|drums|bass",
            listening_context="workout", avg_listener_age=22,
            subgenre="dance pop",
        ),
        Song(
            id=2, title="Chill Lofi Loop", artist="Test Artist",
            genre="lofi", mood="chill", energy=0.4, tempo_bpm=80,
            valence=0.6, danceability=0.5, acousticness=0.9,
            popularity=45, release_year=2021, explicit=0,
            language="English", instruments="piano|guitar|bass",
            listening_context="study", avg_listener_age=24,
            subgenre="lo-fi hip hop",
        ),
    ]
    return Recommender(songs)


# --- existing tests ---

def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop", favorite_mood="happy",
        target_energy=0.8, likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)
    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop", favorite_mood="happy",
        target_energy=0.8, likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]
    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# --- scoring mode tests ---

def test_all_scoring_modes_sum_to_one():
    for name, weights in SCORING_MODES.items():
        total = round(sum(weights.values()), 10)
        assert total == 1.0, f"{name} weights sum to {total}, not 1.0"


def test_invalid_mode_falls_back_to_balanced():
    songs = [make_song(id=1), make_song(id=2, genre="lofi")]
    prefs = make_prefs()
    results_invalid = recommend_songs(prefs, songs, k=2, mode="nonexistent_mode")
    results_balanced = recommend_songs(prefs, songs, k=2, mode="balanced")
    assert [s["id"] for s, _, _ in results_invalid] == [s["id"] for s, _, _ in results_balanced]


def test_genre_first_mode_ranks_genre_match_higher():
    # song1: exact genre match, poor energy; song2: wrong genre, perfect energy
    song1 = make_song(id=1, genre="pop", energy=0.3)
    song2 = make_song(id=2, genre="lofi", energy=0.8)
    prefs = make_prefs(genre="pop", energy=0.8)
    results = recommend_songs(prefs, [song1, song2], k=2, mode="genre_first")
    assert results[0][0]["id"] == 1  # genre match wins in genre_first


def test_energy_focused_mode_ranks_energy_match_higher():
    # song1: exact energy match, wrong genre; song2: right genre, poor energy
    song1 = make_song(id=1, genre="lofi", energy=0.8, listening_context="workout")
    song2 = make_song(id=2, genre="pop", energy=0.2, listening_context="study")
    prefs = make_prefs(genre="pop", energy=0.8, context="workout")
    results = recommend_songs(prefs, [song1, song2], k=2, mode="energy_focused")
    assert results[0][0]["id"] == 1  # energy match wins in energy_focused


# --- new feature tests ---

def test_explicit_filter_penalizes_explicit_songs():
    song_clean = make_song(id=1, explicit=0)
    song_explicit = make_song(id=2, explicit=1)
    prefs = make_prefs(allow_explicit=False)
    results = recommend_songs(prefs, [song_clean, song_explicit], k=2)
    assert results[0][0]["id"] == 1  # clean song ranks higher


def test_explicit_allowed_does_not_penalize():
    song_clean = make_song(id=1, explicit=0, energy=0.5)
    song_explicit = make_song(id=2, explicit=1, energy=0.8)
    prefs = make_prefs(allow_explicit=True, energy=0.8)
    results = recommend_songs(prefs, [song_clean, song_explicit], k=2)
    # both score on explicit, energy decides
    assert results[0][0]["id"] == 2


def test_language_match_scores_1_on_match():
    prefs = make_prefs(language="English")
    song = make_song(language="English")
    score, reasons = score_song(prefs, song, SCORING_MODES["balanced"])
    lang_reason = next(r for r in reasons if "language" in r)
    assert "1.00" in lang_reason


def test_language_mismatch_scores_0():
    prefs = make_prefs(language="English")
    song = make_song(language="Hindi")
    score, reasons = score_song(prefs, song, SCORING_MODES["balanced"])
    lang_reason = next(r for r in reasons if "language" in r)
    assert "0.00" in lang_reason


def test_instruments_full_overlap_scores_1():
    prefs = make_prefs(instruments=["guitar", "drums"])
    song = make_song(instruments="guitar|drums|bass")
    score, reasons = score_song(prefs, song, SCORING_MODES["balanced"])
    inst_reason = next(r for r in reasons if "instruments" in r)
    assert "1.00" in inst_reason


def test_instruments_no_overlap_scores_0():
    prefs = make_prefs(instruments=["piano", "violin"])
    song = make_song(instruments="synth|drums|bass")
    score, reasons = score_song(prefs, song, SCORING_MODES["balanced"])
    inst_reason = next(r for r in reasons if "instruments" in r)
    assert "0.00" in inst_reason


def test_instruments_empty_preference_scores_half():
    prefs = make_prefs(instruments=[])
    song = make_song(instruments="guitar|drums")
    score, reasons = score_song(prefs, song, SCORING_MODES["balanced"])
    inst_reason = next(r for r in reasons if "instruments" in r)
    assert "0.50" in inst_reason


def test_listening_context_match_scores_1():
    prefs = make_prefs(context="workout")
    song = make_song(listening_context="workout")
    score, reasons = score_song(prefs, song, SCORING_MODES["balanced"])
    ctx_reason = next(r for r in reasons if "listening context" in r)
    assert "1.00" in ctx_reason


def test_listening_context_mismatch_scores_0():
    prefs = make_prefs(context="workout")
    song = make_song(listening_context="sleep")
    score, reasons = score_song(prefs, song, SCORING_MODES["balanced"])
    ctx_reason = next(r for r in reasons if "listening context" in r)
    assert "0.00" in ctx_reason


def test_age_exact_match_scores_1():
    prefs = make_prefs(age=25)
    song = make_song(avg_listener_age=25)
    score, reasons = score_song(prefs, song, SCORING_MODES["balanced"])
    age_reason = next(r for r in reasons if "listener age" in r)
    assert "1.00" in age_reason


def test_age_large_gap_scores_0():
    prefs = make_prefs(age=20)
    song = make_song(avg_listener_age=50)  # gap of 30 → score = 0.0
    score, reasons = score_song(prefs, song, SCORING_MODES["balanced"])
    age_reason = next(r for r in reasons if "listener age" in r)
    assert "0.00" in age_reason


def test_subgenre_exact_match_scores_1():
    prefs = make_prefs(genre="pop", subgenre="dance pop")
    song = make_song(genre="pop", subgenre="dance pop")
    score, reasons = score_song(prefs, song, SCORING_MODES["balanced"])
    sub_reason = next(r for r in reasons if "subgenre" in r)
    assert "1.00" in sub_reason


def test_subgenre_partial_match_scores_half():
    prefs = make_prefs(genre="pop", subgenre="dance pop")
    song = make_song(genre="pop", subgenre="electropop")  # "pop" in "electropop"
    score, reasons = score_song(prefs, song, SCORING_MODES["balanced"])
    sub_reason = next(r for r in reasons if "subgenre" in r)
    assert "0.50" in sub_reason


def test_subgenre_no_match_scores_0():
    prefs = make_prefs(genre="pop", subgenre="dance pop")
    song = make_song(genre="rock", subgenre="hard rock")
    score, reasons = score_song(prefs, song, SCORING_MODES["balanced"])
    sub_reason = next(r for r in reasons if "subgenre" in r)
    assert "0.00" in sub_reason


def test_load_songs_parses_new_fields():
    songs = load_songs("data/songs.csv")
    assert len(songs) == 20
    s = songs[0]
    assert isinstance(s["explicit"], int)
    assert isinstance(s["avg_listener_age"], int)
    assert isinstance(s["language"], str)
    assert isinstance(s["instruments"], str)
    assert isinstance(s["listening_context"], str)
    assert isinstance(s["subgenre"], str)


def test_recommend_songs_returns_correct_count():
    songs = load_songs("data/songs.csv")
    prefs = make_prefs()
    results = recommend_songs(prefs, songs, k=5)
    assert len(results) == 5


def test_scores_always_between_0_and_1():
    songs = load_songs("data/songs.csv")
    prefs = make_prefs()
    for mode in SCORING_MODES:
        results = recommend_songs(prefs, songs, k=20, mode=mode)
        for _, score, _ in results:
            assert 0.0 <= score <= 1.0, f"Score {score} out of range in mode {mode}"
