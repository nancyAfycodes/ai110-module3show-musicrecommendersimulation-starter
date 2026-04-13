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


def score_song(
    user_prefs: Dict,
    song: Dict,
    experiment: Optional[str] = None,
) -> Tuple[float, List[str]]:
    """
    Scores a single song against a user preference dictionary.

    Scoring rules (Algorithm Recipe):
      +2.0  — genre match
      +1.0  — mood match
      +0.4  — energy closeness  (weighted: 1 - |song - target|)
      +0.6  — valence closeness (weighted: 1 - |song - target|)
      +0.2  — danceability closeness
      +0.5  — acousticness preference match

    Args:
        user_prefs: user preference dictionary
        song:       song dictionary to score
        experiment: optional experiment mode —
                    "weight_shift"   doubles energy weight, halves genre weight
                    "no_mood"        disables mood matching entirely

    Returns:
        (total_score, reasons) where reasons is a list of human-readable strings
    """
    score = 0.0
    reasons = []

    genre_weight  = 1.0 if experiment == "weight_shift" else 2.0
    energy_weight = 0.8 if experiment == "weight_shift" else 0.4

    # --- Genre match ---
    if song["genre"] == user_prefs.get("genre"):
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight}): song is {song['genre']}")

    # --- Mood match (skipped in no_mood experiment) ---
    if experiment != "no_mood" and song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"mood match (+1.0): song is {song['mood']}")

    # --- Energy closeness ---
    target_energy = user_prefs.get("energy", 0.5)
    energy_contrib = round(energy_weight * (1.0 - abs(song["energy"] - target_energy)), 3)
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


def apply_diversity_penalty(
    scored: List[Tuple[Dict, float, str]],
    artist_penalty: float = 0.5,
    genre_penalty: float = 0.3,
    max_per_artist: int = 1,
    max_per_genre: int = 2,
) -> List[Tuple[Dict, float, str]]:
    """
    Re-ranks a scored song list to enforce artist and genre diversity.

    Rules:
      - If an artist already appears max_per_artist times in selected results,
        deduct artist_penalty from that song's score.
      - If a genre already appears max_per_genre times in selected results,
        deduct genre_penalty from that song's score.

    Args:
        scored:          pre-sorted list of (song, score, explanation) tuples
        artist_penalty:  score deduction per duplicate artist (default 0.5)
        genre_penalty:   score deduction per duplicate genre (default 0.3)
        max_per_artist:  allowed appearances per artist before penalty (default 1)
        max_per_genre:   allowed appearances per genre before penalty (default 2)

    Returns:
        re-ranked list with diversity penalties applied and noted in explanation
    """
    selected = []
    artist_counts: Dict[str, int] = {}
    genre_counts: Dict[str, int] = {}

    for song, score, explanation in scored:
        artist = song["artist"]
        genre  = song["genre"]
        penalty = 0.0
        penalty_notes = []

        if artist_counts.get(artist, 0) >= max_per_artist:
            penalty += artist_penalty
            penalty_notes.append(f"artist diversity penalty (-{artist_penalty}): {artist} already recommended")

        if genre_counts.get(genre, 0) >= max_per_genre:
            penalty += genre_penalty
            penalty_notes.append(f"genre diversity penalty (-{genre_penalty}): {genre} already at limit")

        adjusted_score = round(score - penalty, 3)
        if penalty_notes:
            explanation = explanation + " | " + " | ".join(penalty_notes)

        selected.append((song, adjusted_score, explanation))
        artist_counts[artist] = artist_counts.get(artist, 0) + 1
        genre_counts[genre]   = genre_counts.get(genre, 0) + 1

    selected.sort(key=lambda x: x[1], reverse=True)
    return selected


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    experiment: Optional[str] = None,
    diversity: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Args:
        user_prefs: user preference dictionary
        songs:      full song catalog as list of dicts
        k:          number of top results to return
        experiment: optional experiment mode passed through to score_song
        diversity:  if True, applies diversity penalty to avoid artist/genre repetition

    Returns top k as: (song_dict, score, explanation)
    """
    scored = []
    for song in songs:
        total, reasons = score_song(user_prefs, song, experiment)
        explanation = (
            "Recommended because: " + " | ".join(reasons)
            if reasons else
            "Recommended as a general match to your taste profile."
        )
        scored.append((song, total, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)

    if diversity:
        scored = apply_diversity_penalty(scored)

    return scored[:k]


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


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Scores every song against the user profile and returns the top k."""
        user_prefs = {
            "genre":          user.favorite_genre,
            "mood":           user.favorite_mood,
            "energy":         user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

        scored = []
        for song in self.songs:
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
            total, _ = score_song(user_prefs, song_dict)
            scored.append((song, total))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation for why a song was recommended."""
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