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


PROFILE_NAME = "Alex"

user_prefs = {
    "genre":        "pop",
    "mood":         "happy",
    "energy":       0.8,
    "valence":      0.78,
    "danceability": 0.75,
    "likes_acoustic": False,
}


def print_header(title: str) -> None:
    width = 60
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_recommendation(rank: int, song: dict, score: float, explanation: str) -> None:
    print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
    print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
    print(f"       Score: {score:.3f}")
    print("       Why:")
    for reason in explanation.replace("Recommended because: ", "").split(" | "):
        print(f"         • {reason}")
    print("  " + "-" * 56)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"\n  Loaded {len(songs)} songs from catalog.")

    print_header(f"User Profile: {PROFILE_NAME}")
    print(f"  Genre     : {user_prefs['genre']}")
    print(f"  Mood      : {user_prefs['mood']}")
    print(f"  Energy    : {user_prefs['energy']}")
    print(f"  Valence   : {user_prefs['valence']}")
    print(f"  Dance     : {user_prefs['danceability']}")
    print(f"  Acoustic  : {user_prefs['likes_acoustic']}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_header("Top 5 Recommendations")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print_recommendation(rank, song, score, explanation)

    print("\n  End of recommendations.\n")


if __name__ == "__main__":
    main()