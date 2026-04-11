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


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against a user preference dictionary.

    Scoring rules (Algorithm Recipe):
      +2.0  — genre match
      +1.0  — mood match
      +0.4  — energy closeness  (weighted: 1 - |song - target|)
      +0.6  — valence closeness (weighted: 1 - |song - target|)
      +0.2  — danceability closeness
      +0.5  — acousticness preference match

    Returns:
        (total_score, reasons)  where reasons is a list of human-readable strings
    """
    score = 0.0
    reasons = []

    # --- Genre match (+2.0) ---
    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"genre match (+2.0): song is {song['genre']}")

    # --- Mood match (+1.0) ---
    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"mood match (+1.0): song is {song['mood']}")

    # --- Energy closeness (up to +0.4) ---
    target_energy = user_prefs.get("energy", 0.5)
    energy_contrib = round(0.4 * (1.0 - abs(song["energy"] - target_energy)), 3)
    score += energy_contrib
    reasons.append(f"energy score (+{energy_contrib}): song={song['energy']}, target={target_energy}")

    # --- Valence closeness (up to +0.6) ---
    if "valence" in user_prefs:
        valence_contrib = round(0.6 * (1.0 - abs(song["valence"] - user_prefs["valence"])), 3)
        score += valence_contrib
        reasons.append(f"valence score (+{valence_contrib}): song={song['valence']}, target={user_prefs['valence']}")

    # --- Danceability closeness (up to +0.2) ---
    if "danceability" in user_prefs:
        dance_contrib = round(0.2 * (1.0 - abs(song["danceability"] - user_prefs["danceability"])), 3)
        score += dance_contrib
        reasons.append(f"danceability score (+{dance_contrib}): song={song['danceability']}, target={user_prefs['danceability']}")

    # --- Acousticness preference (+0.5) ---
    if "likes_acoustic" in user_prefs:
        acoustic_match = (
            user_prefs["likes_acoustic"] and song["acousticness"] >= 0.6
        ) or (
            not user_prefs["likes_acoustic"] and song["acousticness"] < 0.4
        )
        if acoustic_match:
            score += 0.5
            reasons.append(f"acousticness match (+0.5): song={song['acousticness']}")

    return round(score, 3), reasons


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
        # Convert UserProfile to dict so we can reuse score_song()
        user_prefs = {
            "genre":        user.favorite_genre,
            "mood":         user.favorite_mood,
            "energy":       user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

        def to_dict(song: Song) -> Dict:
            return {
                "id":           song.id,
                "title":        song.title,
                "artist":       song.artist,
                "genre":        song.genre,
                "mood":         song.mood,
                "energy":       song.energy,
                "tempo_bpm":    song.tempo_bpm,
                "valence":      song.valence,
                "danceability": song.danceability,
                "acousticness": song.acousticness,
            }

        scored = sorted(
            ((song, score_song(user_prefs, to_dict(song))[0]) for song in self.songs),
            key=lambda x: x[1],
            reverse=True
        )
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Returns a human-readable explanation for why a song was recommended.
        """
        user_prefs = {
            "genre":          user.favorite_genre,
            "mood":           user.favorite_mood,
            "energy":         user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dict = {
            "id":           song.id,
            "title":        song.title,
            "artist":       song.artist,
            "genre":        song.genre,
            "mood":         song.mood,
            "energy":       song.energy,
            "tempo_bpm":    song.tempo_bpm,
            "valence":      song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }
        total, reasons = score_song(user_prefs, song_dict)
        lines = [f"Score: {total}"] + [f"  - {r}" for r in reasons]
        return "\n".join(lines)


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


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Scores every song against user_prefs and returns the top k as:
        (song_dict, score, explanation)
    """
    def build_entry(song: Dict) -> Tuple[Dict, float, str]:
        total, reasons = score_song(user_prefs, song)
        explanation = (
            "Recommended because: " + " | ".join(reasons)
            if reasons else
            "Recommended as a general match to your taste profile."
        )
        return song, total, explanation

    scored = sorted(
        (build_entry(song) for song in songs),
        key=lambda x: x[1],
        reverse=True
    )
    return scored[:k]