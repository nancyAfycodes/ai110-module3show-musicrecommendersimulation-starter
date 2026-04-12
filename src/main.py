"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs

Run from the project root with:
    python -m src.main
"""

from recommender import load_songs, recommend_songs


# --- Experiment modes ---

EXPERIMENTS = [
    {"mode": None,           "label": "Baseline"},
    {"mode": "weight_shift", "label": "Experiment A: Weight Shift (energy x2, genre halved)"},
    {"mode": "no_mood",      "label": "Experiment B: No Mood Matching"},
]


# --- User Profiles ---

PROFILES = [
    {
        "name": "High-Energy Pop",
        "prefs": {
            "genre":          "pop",
            "mood":           "happy",
            "energy":         0.90,
            "valence":        0.85,
            "danceability":   0.88,
            "likes_acoustic": False,
        }
    },
    {
        "name": "Chill Lofi",
        "prefs": {
            "genre":          "lofi",
            "mood":           "chill",
            "energy":         0.38,
            "valence":        0.58,
            "danceability":   0.60,
            "likes_acoustic": True,
        }
    },
    {
        "name": "Deep Intense Rock",
        "prefs": {
            "genre":          "rock",
            "mood":           "intense",
            "energy":         0.92,
            "valence":        0.45,
            "danceability":   0.65,
            "likes_acoustic": False,
        }
    },
    {
        "name": "Edge Case: High Energy + Melancholic Mood",
        "prefs": {
            "genre":          "synthwave",
            "mood":           "melancholic",
            "energy":         0.90,
            "valence":        0.30,
            "danceability":   0.70,
            "likes_acoustic": False,
        }
    },
    {
        "name": "Edge Case: Conflicting Acoustic + Electronic Genre",
        "prefs": {
            "genre":          "electronic",
            "mood":           "focused",
            "energy":         0.95,
            "valence":        0.55,
            "danceability":   0.85,
            "likes_acoustic": True,
        }
    },
    {
        "name": "Edge Case: No Genre or Mood Match in Catalog",
        "prefs": {
            "genre":          "metal",
            "mood":           "angry",
            "energy":         0.99,
            "valence":        0.20,
            "danceability":   0.50,
            "likes_acoustic": False,
        }
    },
]


# --- Output helpers ---

def print_header(title: str) -> None:
    """Prints a formatted section header."""
    width = 60
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_profile(name: str, prefs: dict) -> None:
    """Prints a user profile summary."""
    print_header(f"User Profile: {name}")
    for key, val in prefs.items():
        print(f"  {key:<16}: {val}")


def print_recommendation(rank: int, song: dict, score: float, explanation: str) -> None:
    """Prints a single ranked recommendation with its score and reasons."""
    print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
    print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
    print(f"       Score: {score:.3f}")
    print("       Why:")
    for reason in explanation.replace("Recommended because: ", "").split(" | "):
        print(f"         • {reason}")
    print("  " + "-" * 56)


def run_profile(songs: list, profile: dict, experiment: dict) -> None:
    """Runs the recommender for a single profile under a given experiment mode."""
    name  = profile["name"]
    prefs = profile["prefs"]
    mode  = experiment["mode"]
    label = experiment["label"]

    print_profile(f"{name}  [{label}]", prefs)
    recommendations = recommend_songs(prefs, songs, 5, mode)

    print_header(f"Top 5  |  {name}  |  {label}")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print_recommendation(rank, song, score, explanation)
    print("\n  End of recommendations.\n")


# --- Entry point ---

def main() -> None:
    """Loads songs and runs all profiles under each experiment mode."""
    songs = load_songs("../data/songs.csv")
    print(f"\n  Loaded {len(songs)} songs from catalog.")

    for experiment in EXPERIMENTS:
        for profile in PROFILES[:3]:
            run_profile(songs, profile, experiment)


if __name__ == "__main__":
    main()