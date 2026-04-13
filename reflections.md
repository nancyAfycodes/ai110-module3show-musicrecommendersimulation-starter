## Reflection
- One of the most important lesson learned from this project is that recommender systems, such as Spotify, YouTube, and Pandora, are very complicated. Such platforms analyze lots of datapoints to be able to recommend potential songs/ videos that may be of interest as well as suggest songs/videos the user maybe interested in. In addition, I think the human factor is still important to allow the recommender system to function properly. If a users seems to be interested in a particular kind of song and/or topic doesn't mean that the user(human) can't listen to or watch videos that the user may not have previously considered. I think recommender systems in general still needs 'human element' to function effectively.



* Answer below is AI-generated
# Reflection — Music Recommender Simulation

## High-Energy Pop vs Chill Lofi

These two profiles sit at opposite ends of the energy spectrum and the
recommender handled them very differently. The High-Energy Pop profile
gravitated toward fast, upbeat songs with high danceability, while the Chill
Lofi profile pulled toward slow, acoustic, low-energy tracks. What was
interesting is that no song appeared in both top 5 lists — the energy gap
between the two profiles (0.90 vs 0.38) was large enough to completely
separate their results. This makes intuitive sense: someone who wants music
for the gym and someone who wants music for studying are not looking for the
same thing, and the system correctly understood that without being explicitly
told.

## High-Energy Pop vs Deep Intense Rock

Both profiles want high-energy music, but they diverge on valence — Pop wants
positivity (0.85) while Rock wants darkness (0.45). This difference pushed
their results in noticeably different directions. Pop recommendations stayed
bright and danceable (Sunrise City, Gym Hero), while Rock recommendations
leaned darker and more aggressive (Storm Runner, Neon Samurai). The overlap
was minimal, which shows that valence is doing meaningful work as a feature
even when energy levels are similar. In plain language: two people can both
want loud music but still want completely different feelings from it.

## Chill Lofi vs Deep Intense Rock

This was the most dramatic contrast of all three profile pairs. These profiles
disagree on almost every feature — energy, valence, danceability, and
acousticness all point in opposite directions. Not a single song appeared in
both top 5 lists. The Lofi profile surfaced quiet, acoustic, introspective
tracks while the Rock profile surfaced aggressive, electric, high-tempo songs.
This comparison was the clearest demonstration that the scoring formula is
working as intended — when two users have genuinely different tastes, the
system gives them genuinely different results.

## Why Does Gym Hero Keep Showing Up for Happy Pop?

Imagine you told a friend: "I want happy music." Your friend doesn't just
look at whether a song is labeled happy — they think about how it sounds.
Does it have a fast beat? Does it feel uplifting? Is it easy to dance to?
Gym Hero scores very high on all of those things. Even though it is tagged
as "intense," its musical numbers — its tempo, its brightness, its energy —
all say "this is a feel-good song." The recommender listens to the numbers,
not just the label. So when it hears that you want happy pop, it sees Gym Hero
and thinks: "this sounds exactly like what they want." It is only when you
look at the mood tag that you realize there is a mismatch — and that is
precisely the kind of limitation this project was designed to surface.

## What I Would Change

After running all three profiles and both experiments, the clearest takeaway
is that genre weight is too high relative to the audio features. A user who
genuinely enjoys high-energy, high-valence music should be able to receive
recommendations across genres — not just from their single stated preference.
Reducing the genre weight and increasing the valence and energy weights
(as Experiment A demonstrated) produced recommendations that felt more
musically accurate even if they were less genre-consistent. In a real system,
genre should probably act as a soft filter or a tiebreaker rather than the
dominant scoring factor.