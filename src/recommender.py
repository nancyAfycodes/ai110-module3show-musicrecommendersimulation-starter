import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Scores every song against the user profile and returns the top k.
        """
        scored = []
        for song in self.songs:
            score = self._score(user, song)
            scored.append((song, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def _score(self, user: UserProfile, song: Song) -> float:
        """
        Computes a similarity score between a song and a user profile.
        """
        score = 0.0

        # Genre match
        if song.genre == user.favorite_genre:
            score += 2.0

        # Mood match
        if song.mood == user.favorite_mood:
            score += 1.0

        # Energy closeness (rewards proximity to target)
        energy_score = 1.0 - abs(song.energy - user.target_energy)
        score += 0.4 * energy_score

        # Acousticness preference
        acoustic_match = (user.likes_acoustic and song.acousticness >= 0.6) or \
                         (not user.likes_acoustic and song.acousticness < 0.4)
        if acoustic_match:
            score += 0.5

        return score

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Returns a human-readable explanation for why a song was recommended.
        """
        reasons = []

        if song.genre == user.favorite_genre:
            reasons.append(f"matches your favorite genre ({song.genre})")

        if song.mood == user.favorite_mood:
            reasons.append(f"matches your preferred mood ({song.mood})")

        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff <= 0.1:
            reasons.append("energy level is very close to your target")
        elif energy_diff <= 0.2:
            reasons.append("energy level is close to your target")

        if user.likes_acoustic and song.acousticness >= 0.6:
            reasons.append("has a strong acoustic feel you tend to enjoy")
        elif not user.likes_acoustic and song.acousticness < 0.4:
            reasons.append("has the electronic/produced sound you prefer")

        if reasons:
            return "Recommended because it " + ", and ".join(reasons) + "."
        return "Recommended as a general match to your taste profile."


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    int(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })

    return songs


def _score_song(song: Dict, user_prefs: Dict) -> Tuple[float, List[str]]:
    """
    Computes a score and reasons list for a single song against user_prefs.
    Extracted to keep recommend_songs complexity within allowed limits.
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"matches your favorite genre ({song['genre']})")

    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"matches your preferred mood ({song['mood']})")

    target_energy = user_prefs.get("energy", 0.5)
    score += 0.4 * (1.0 - abs(song["energy"] - target_energy))
    energy_diff = abs(song["energy"] - target_energy)
    if energy_diff <= 0.1:
        reasons.append("energy level is very close to your target")
    elif energy_diff <= 0.2:
        reasons.append("energy level is close to your target")

    if "valence" in user_prefs:
        score += 0.6 * (1.0 - abs(song["valence"] - user_prefs["valence"]))
        if abs(song["valence"] - user_prefs["valence"]) <= 0.15:
            reasons.append("emotional tone aligns with your preference")

    if "danceability" in user_prefs:
        score += 0.2 * (1.0 - abs(song["danceability"] - user_prefs["danceability"]))

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Scores every song against user_prefs and returns the top k as:
        (song_dict, score, explanation)
    """
    scored = []

    for song in songs:
        score, reasons = _score_song(song, user_prefs)
        explanation = (
            "Recommended because it " + ", and ".join(reasons) + "."
            if reasons else
            "Recommended as a general match to your taste profile."
        )
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]