"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    # Starter example profile
    user_prefs = {
        "genre":        "pop",
        "mood":         "happy",
        "energy":       0.8,
        "valence":      0.78,
        "danceability": 0.75,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("Top recommendations:\n")
    for rec in recommendations:
        song, score, explanation = rec
        print(f"  {song['title']} by {song['artist']} [{song['genre']} · {song['mood']}]")
        print(f"  Score: {score:.2f}")
        print(f"  Because: {explanation}")
        print()


if __name__ == "__main__":
    main()