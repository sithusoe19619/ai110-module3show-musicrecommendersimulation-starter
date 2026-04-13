"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import sys
from recommender import load_songs, recommend_songs, list_modes

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False
    print("Warning: tabulate not installed. Falling back to plain output. Run: pip install tabulate")


def main() -> None:
    available = list_modes()

    if len(sys.argv) > 1:
        mode_arg = sys.argv[1]
        if mode_arg not in available:
            print(f"Unknown mode '{mode_arg}'.")
            print(f"Available modes: {', '.join(available)}")
            sys.exit(1)
        modes = [mode_arg]
    else:
        modes = available

    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    high_energy_pop = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.75,
        "likes_acoustic": False,
        "likes_mainstream": True,
        "prefers_recent": True,
        "allow_explicit": True,
        "preferred_language": "English",
        "preferred_instruments": ["synth", "drums"],
        "listening_context": "workout",
        "user_age": 22,
        "favorite_subgenre": "dance pop",
    }

    chill_lofi = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.30,
        "likes_acoustic": True,
        "likes_mainstream": False,
        "prefers_recent": False,
        "allow_explicit": False,
        "preferred_language": "English",
        "preferred_instruments": ["piano", "guitar"],
        "listening_context": "study",
        "user_age": 24,
        "favorite_subgenre": "lo-fi hip hop",
    }

    deep_intense_rock = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "likes_acoustic": False,
        "likes_mainstream": False,
        "prefers_recent": False,
        "allow_explicit": True,
        "preferred_language": "English",
        "preferred_instruments": ["guitar", "drums"],
        "listening_context": "workout",
        "user_age": 26,
        "favorite_subgenre": "hard rock",
    }

    high_energy_sad = {
        "favorite_genre": "pop",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "likes_acoustic": False,
        "likes_mainstream": True,
        "prefers_recent": True,
        "allow_explicit": True,
        "preferred_language": "English",
        "preferred_instruments": ["synth", "vocals"],
        "listening_context": "commute",
        "user_age": 21,
        "favorite_subgenre": "electropop",
    }

    metal_peaceful = {
        "favorite_genre": "metal",
        "favorite_mood": "peaceful",
        "target_energy": 0.85,
        "likes_acoustic": False,
        "likes_mainstream": False,
        "prefers_recent": False,
        "allow_explicit": True,
        "preferred_language": "English",
        "preferred_instruments": ["guitar", "bass"],
        "listening_context": "workout",
        "user_age": 28,
        "favorite_subgenre": "death metal",
    }

    acoustic_electronic = {
        "favorite_genre": "electronic",
        "favorite_mood": "focused",
        "target_energy": 0.60,
        "likes_acoustic": True,
        "likes_mainstream": False,
        "prefers_recent": True,
        "allow_explicit": False,
        "preferred_language": "English",
        "preferred_instruments": ["synth", "bass"],
        "listening_context": "study",
        "user_age": 25,
        "favorite_subgenre": "tech house",
    }

    orphan_genre_world = {
        "favorite_genre": "world",
        "favorite_mood": "spiritual",
        "target_energy": 0.40,
        "likes_acoustic": True,
        "likes_mainstream": False,
        "prefers_recent": False,
        "allow_explicit": False,
        "preferred_language": "Hindi",
        "preferred_instruments": ["sitar", "tabla"],
        "listening_context": "study",
        "user_age": 32,
        "favorite_subgenre": "Indian classical fusion",
    }

    anti_mainstream_recent = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.30,
        "likes_acoustic": True,
        "likes_mainstream": False,
        "prefers_recent": True,
        "allow_explicit": False,
        "preferred_language": "English",
        "preferred_instruments": ["piano", "guitar"],
        "listening_context": "study",
        "user_age": 23,
        "favorite_subgenre": "lo-fi hip hop",
    }

    maximal_indifference = {
        "favorite_genre": "jazz",
        "favorite_mood": "nostalgic",
        "target_energy": 0.50,
        "likes_acoustic": True,
        "likes_mainstream": False,
        "prefers_recent": False,
        "allow_explicit": False,
        "preferred_language": "English",
        "preferred_instruments": ["piano", "bass"],
        "listening_context": "study",
        "user_age": 34,
        "favorite_subgenre": "smooth jazz",
    }

    profiles = [
        ("High-Energy Pop", high_energy_pop),
        ("Chill Lofi", chill_lofi),
        ("Deep Intense Rock", deep_intense_rock),
        ("High-Energy + Sad", high_energy_sad),
        ("Metal + Peaceful", metal_peaceful),
        ("Acoustic Electronic", acoustic_electronic),
        ("Orphan Genre (World)", orphan_genre_world),
        ("Anti-Mainstream + Recent", anti_mainstream_recent),
        ("Maximal Indifference", maximal_indifference),
    ]

    for mode in modes:
        print("\n" + "█" * 50)
        print(f"  SCORING MODE: {mode.upper()}")
        print("█" * 50)
        for label, prefs in profiles:
            recommendations = recommend_songs(prefs, songs, k=5, mode=mode)

            print("\n" + "=" * 50)
            print(f"  Top Recommendations — {label}")
            print("=" * 50)

            # maps reason feature name → song dict key → display value
            FEATURE_VALUE = {
                "genre":            lambda s: s["genre"],
                "energy":           lambda s: str(s["energy"]),
                "valence":          lambda s: str(s["valence"]),
                "mood":             lambda s: s["mood"],
                "acousticness":     lambda s: str(s["acousticness"]),
                "popularity":       lambda s: str(s["popularity"]),
                "release year":     lambda s: str(s["release_year"]),
                "explicit":         lambda s: "yes" if s["explicit"] else "no",
                "language":         lambda s: s["language"],
                "instruments":      lambda s: s["instruments"].replace("|", ", "),
                "listening context":lambda s: s["listening_context"],
                "listener age":     lambda s: str(s["avg_listener_age"]),
                "subgenre":         lambda s: s["subgenre"],
            }

            def fmt_reason(reason_str, song):
                # reason_str looks like "genre match: 0.85"
                feature = reason_str.split(" match:")[0].strip()
                score_val = reason_str.split(": ")[-1]
                value = FEATURE_VALUE.get(feature, lambda s: "?")(song)
                return f"{feature}: {value}({score_val})"

            if HAS_TABULATE:
                headers = ["#", "Title", "Artist", "Score",
                           "Top Reasons [feature: value(score)]",
                           "Weak Spots [feature: value(score)]"]
                rows = []
                for i, (song, score, explanation) in enumerate(recommendations, start=1):
                    all_reasons = explanation.split(" | ")
                    sorted_reasons = sorted(all_reasons, key=lambda r: float(r.split(": ")[-1]), reverse=True)
                    top3 = "\n".join(fmt_reason(r, song) for r in sorted_reasons[:3])
                    weak3 = "\n".join(fmt_reason(r, song) for r in sorted_reasons[-3:])
                    rows.append([i, song["title"], song["artist"], f"{score:.2f}", top3, weak3])
                print(tabulate(rows, headers=headers, tablefmt="grid"))
            else:
                for i, (song, score, explanation) in enumerate(recommendations, start=1):
                    all_reasons = explanation.split(" | ")
                    sorted_reasons = sorted(all_reasons, key=lambda r: float(r.split(": ")[-1]), reverse=True)
                    top3 = " · ".join(fmt_reason(r, song) for r in sorted_reasons[:3])
                    weak3 = " · ".join(fmt_reason(r, song) for r in sorted_reasons[-3:])
                    print(f"  #{i}  {song['title']} by {song['artist']}  [{score:.2f}]")
                    print(f"       ↑ {top3}")
                    print(f"       ↓ {weak3}")


if __name__ == "__main__":
    main()
