# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**Content-based Music Recommender**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

- The intended use for this recommender system is for educational purposes only. It is meant to mimic real recommender systems such as Spotify. The user can modify the songs used in the project to reflect his/her personal taste. 
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

- Some of the features in this recommender system include genre, energy, danceability and mood, with each having scores that helps group songs that are similar together. For example, a high-energy pop song, which has high energy score and danceability, is ranked higher than a song that isn't. Therefore, if a users selects a song, the recommender will generate a score based on the song's similarity to a song the user has previously listened to. However, if it is the user's first time listening to the song, it will be used as a baseline for other songs in same genre that have the same and/or similar characteristics

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

- The total number of songs in songs.csv file is 20. I added additional 10 songs to the songs already present in the file. The genre represented in the data set include high-energy pop, and deep intense rock, which is what is represented in the song choice used in the project. 
---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

- The recommender was great in recommending songs based on the user preference. For instance, high-energy pop songs, seems to be popular with the user. Since the songs used in the project are small, it means that the same can be applied to real-world situations. Consequently, expanding the genre explored in the project can assist in creating a more accurate user profile that can be tailored to each user. 
---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

- In general, I noticed that the recommender seems to favor, high-energy pop songs. Every iteration seems to give high-energy pop preference over other genre of music. The recommender assumes that the user always wants to listen to high-energy pop first. all experiments and iterations gave preference to high-energy pop over others. Since the number of songs is small, results produced favors high-energy pop. I think if the number of genre and songs was increased, the result obtained may become evenly spread out amongst each genre of music in the songs file.
---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

- In experimenting, I changed the genre score and mood to note any difference in each user profile. However, the changes did not produce any significant difference, for it favored one genre, high-energy pop, over others. This means that this recommender is heavily skewed to one form of genre, high-energy pop. 
---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

- In the future, I'd like to use real songs to test how it would perform as compared to auto-generated songs. In addition, I will increase the number and variety of songs used in the project. This allows testing to note if there's any significant difference from the original classification of a song to the result obtained when the recommender is used. 
---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

- One of the most important lesson learned from this project is that recommender systems, such as Spotify, YouTube, and Pandora, are very complicated. Such platforms analyze lots of datapoints to be able to recommend potential songs/ videos that may be of interest as well as suggest songs/videos the user maybe interested in. In addition, I think the human factor is still important to allow the recommender system to function properly. If a users seems to be interested in a particular kind of song and/or topic doesn't mean that the user(human) can't listen to or watch videos that the user may not have previously considered. I think recommender systems in general still needs 'human element' to function effectively.

* The answer below is AI-generated. It provides a much detailed assessment of the over project
# Model Card — Music Recommender System

## Model Overview

A content-based music recommender that scores songs against a user preference
profile using weighted audio features (energy, valence, danceability,
acousticness) and categorical matches (genre, mood). Built as a CLI simulation
using a 20-song catalog loaded from `data/songs.csv`.

---

## Limitations and Bias

### 1. Genre Over-Prioritization (Filter Bubble)
The genre match carries the single highest weight in the scoring formula
(+2.0 points), which is more than double any other individual signal. This
creates a strong filter bubble — a user who lists "pop" as their preferred
genre will almost always receive pop songs in their top 5, even if a jazz or
indie track is a near-perfect match on every audio feature. During Experiment
A (genre weight halved to +1.0), non-genre songs surfaced immediately,
confirming that genre dominance is a design choice with real consequences for
diversity of recommendations.

### 2. Cold-Start Weakness
Users with no listening history, no liked artists, and only a single preferred
genre receive recommendations based entirely on static preference values.
There is no behavioral signal to refine or personalize results beyond the
initial profile. This means two users with identical profiles will always
receive identical recommendations regardless of how differently they actually
listen, which reduces the system's ability to adapt to real individual taste.

### 3. Score Collapse on Unknown Preferences
When a user's preferred genre and mood have no match in the catalog (as
demonstrated by the "metal / angry" edge case profile), the total scores for
all songs collapse into a narrow band of roughly 1.0–1.5 points. The system
has no mechanism to signal low confidence or warn the user that it is
essentially guessing. A score of 1.2 looks similar in the output to a score
of 4.6, even though one represents a near-perfect match and the other
represents a complete absence of relevant signal.

### 4. Mood Matching is Binary
The mood score is awarded as a flat +1.0 for an exact string match or +0.0
for anything else. This means "chill" and "relaxed" are treated as completely
unrelated moods despite being semantically very close, while "intense" and
"focused" are similarly penalized for not being identical strings. A
similarity-aware mood scoring approach — such as grouping moods into clusters
or using a numeric mood embedding — would produce more nuanced results.

### 5. Small Catalog Amplifies All Biases
With only 20 songs across 7 genres, some genres have only one or two
representatives. This means any bias in the scoring weights is amplified —
there are simply not enough songs in underrepresented genres to compete with
pop or lofi tracks even when the audio features are a better match. A
production system would require a catalog of thousands of songs before these
scoring weights could be properly calibrated and evaluated.

---

## Intended Use

This system is intended as an educational simulation of content-based
recommendation logic. It is not suitable for production use and should not
be used as the sole basis for music discovery in a real application without
significant expansion of the catalog, user profiling, and scoring calibration.

---

## Evaluation

### Profiles Tested

**High-Energy Pop** — This profile produced the most intuitive results.
Sunrise City ranked first in every experiment mode because it matched on
genre, mood, and all audio features simultaneously. Gym Hero consistently
appeared in the top 3 despite having an "intense" mood rather than "happy."
This was the biggest surprise — Gym Hero scores so well on energy, valence,
and danceability that it outranks many happy songs. In plain terms, the system
sees Gym Hero as a happy-sounding song because its numbers say so, even if the
word "intense" is attached to it. The lesson here is that mood labels are just
words — the actual audio features tell a different story.

**Chill Lofi** — Results felt accurate and predictable. Library Rain and
Midnight Coding consistently ranked at the top because they match on both
genre and mood. Focus Flow occasionally outranked Library Rain in Experiment B
(no mood matching) because its audio features are marginally closer to the
target. This confirmed that mood matching is doing real work in the baseline —
removing it visibly shuffled the rankings.

**Deep Intense Rock** — Storm Runner dominated every experiment, which makes
sense since it is the only rock song with an "intense" mood. The more
interesting observation was that Bass Drop Zero (electronic, intense) crept
into the top 3 under Experiment A because its energy profile nearly matches
the rock target. This shows the system can surface cross-genre songs when
audio features align — which is either a feature or a bug depending on the
user's expectations.

### What Surprised Us
The biggest surprise across all profiles was how much genre weight shapes the
top results. Removing it (Experiment A) immediately diversified the
recommendations in ways that sometimes felt more musically accurate. A user
who loves high-energy music might genuinely enjoy Bass Drop Zero even if they
said their favorite genre is rock — and Experiment A surfaces that possibility
while the baseline does not.

## Experimental Findings

| Experiment | Change | Observed Effect |
|---|---|---|
| Baseline | Default weights | Genre + mood dominate; intuitive results for well-matched profiles |
| Weight Shift | Energy x2, genre halved | Non-genre songs enter top 5; recommendations feel more audio-driven |
| No Mood | Mood check disabled | Mood-mismatched songs rise; rankings feel less emotionally coherent |