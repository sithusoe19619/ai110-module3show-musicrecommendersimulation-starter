# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeSync 1.0**

----------------------------------------------------------------------------

## 2. Intended Use  

VibeSync 1.0 suggests songs from a small catalog based on a user's stated preferences. It is designed for classroom exploration, not a real product.

- It generates a ranked list of up to 5 songs that best match what the user says they like.
- It assumes users can clearly describe their preferences upfront — favorite genre, mood, energy level, and a few yes/no choices. There is no listening history or implicit feedback.
- This is a simulation built to learn how recommender systems work, not to be deployed for real users.

----------------------------------------------------------------------------

## 3. How the Model Works  

Every song gets a score from 0 to 1 based on how closely it matches the user's preferences. The song with the highest score is recommended first.

Seven features are used — genre, energy, valence, mood, acousticness, popularity, and release year. Each one contributes a slice of the total score based on its weight:

- Genre (30%) — exact match scores full points; similar genres get partial credit; unrelated genres score zero.
- Energy (25%) — the closer a song's energy is to the user's target, the higher this part of the score.
- Valence (20%) — the user's mood label maps to a target "positivity" value; songs closer to that value score higher.
- Mood (10%) — exact mood match scores full points; similar moods get partial credit.
- Acousticness, popularity, and release year each contribute 5%.

The user provides: favorite genre, favorite mood, target energy, whether they like acoustic music, whether they prefer mainstream songs, and whether they prefer recent releases. The model turns those inputs into a single number per song and returns the top 5.

----------------------------------------------------------------------------

## 4. Data  

The catalog contains 20 hand-crafted songs. Each song has 12 attributes: id, title, artist, genre, mood, energy, tempo, valence, danceability, acousticness, popularity, and release year.

- 17 genres are represented including pop, rock, hip-hop, lofi, jazz, metal, folk, classical, ambient, electronic, synthwave, indie pop, dream pop, funk, world, acoustic, and emo.
- 16 mood labels are used including happy, chill, intense, relaxed, sad, energetic, peaceful, dark, and aggressive.
- Popularity and release year were added to the starter dataset to support two additional scoring features.
- Several gaps exist: all songs were released between 2017 and 2023, energy values cluster in the mid-to-high range (very calm music is underrepresented), and niche genres like world and classical have only one song each.

----------------------------------------------------------------------------

## 5. Strengths  

- Users with mainstream genre preferences (pop, rock, hip-hop) get the most useful results because those genres have the most songs and similarity connections in the catalog.
- Energy matching works reliably when the user's target falls in the mid range (0.35–0.80), which is where most songs live.
- Chill and lofi profiles consistently returned calm, low-energy songs that matched what a real listener with those preferences would enjoy.
- The score breakdown in the output makes it easy to see exactly why each song ranked where it did — more transparent than most real recommender systems.

----------------------------------------------------------------------------

## 6. Limitations and Bias

**Genre dominates all other signals.**
The genre component carries a weight of 0.30 — three times the weight of mood (0.10) and higher than any other single feature. In our experiments, the top-ranked song never changed even when mood was completely removed from scoring. This means a user's emotional preference is structurarily subordinate to their genre preference, and songs that perfectly match mood but differ in genre will almost always lose to genre-matched songs that miss on mood entirely.

**Low-energy users are structurally penalized by the catalog.**
The energy scoring formula (`1.0 - abs(song_energy - target_energy)`) is mathematically neutral, but the dataset is not. Song energy values range from 0.19 to 0.96, with most songs clustered between 0.35 and 0.93. A user who prefers very calm music (target energy around 0.10) will find that every song in the catalog is far from their target, producing uniformly low energy scores. High-energy users, by contrast, have four or more songs within 0.10 of their target. The formula is fair; the data is not.

**Niche genre users are locked out of meaningful recommendations.**
Genres like `world`, `classical`, `emo`, and `acoustic` have very few or no similarity connections to other genres in the GENRE_SIMILARITY table. A world music fan gets at most one song with a non-zero genre score — the other 19 songs start with a 0.30 deficit that the remaining features cannot overcome. This creates a filter bubble where niche users receive the same narrow pool of results regardless of how their energy, mood, or valence preferences vary.

**The `likes_acoustic` preference is a binary trap that erases nuance.**
The system maps acoustic preference to one of two fixed targets: 0.82 (acoustic) or 0.15 (non-acoustic). A user who enjoys a mix — say, lightly produced songs around 0.50 acousticness — has no way to express that. Both targets will score their preferred range poorly, meaning the system systematically misrepresents users whose taste falls between the two extremes. In a real product, this would push blended-preference users toward recommendations that feel consistently off.

**The mood-to-valence mapping imposes the system's assumptions onto the user.**
When a user picks a mood label like "intense" or "dark," the system silently maps it to a fixed valence target (0.63 and 0.25, respectively). But mood labels mean different things to different people — one user's "intense" is high-energy and euphoric (valence 0.85), while another's is brooding and tense (valence 0.30). The fixed MOOD_TO_VALENCE table treats all users who share a mood label as emotionally identical, which introduces systematic valence scoring errors for anyone whose interpretation diverges from the table's assumption.

**The popularity and release year features cannot reward true outlier preferences.**
The system sets a popularity target of 0.25 for users who dislike mainstream music, but the least popular song in the dataset has a popularity score of 29 (0.29 normalized) — barely below the mainstream threshold. There are no truly underground tracks in the catalog, so anti-mainstream users are never actually rewarded. Similarly, users who prefer older music are assigned a target year of 2018, which is still quite recent; the entire dataset spans only 2017–2023, making it impossible to surface genuinely nostalgic recommendations for listeners who prefer music from earlier decades.

----------------------------------------------------------------------------

## 7. Evaluation

We tested nine user profiles designed to stress-test the scoring logic in different ways. The profiles ranged from straightforward matches (High-Energy Pop, Chill Lofi) to deliberately contradictory combinations (Metal + Peaceful, High-Energy Sad) and edge cases like users with niche genres not well-represented in the catalog (Orphan Genre: World).

For each profile we ran `recommend_songs` against the full 20-song catalog and examined whether the top results matched intuition — meaning: if a real person had those preferences, would they actually enjoy the songs returned?

**What we were looking for:** Whether the top song changed across profiles, whether the score breakdown explained the ranking, and whether the system could surface meaningfully different results when preferences changed.

**What surprised us:**

- *Gym Hero keeps appearing for happy pop users even though it is labeled "intense," not "happy."* The song scores 1.0 on genre (it is pop) and 0.97 on energy, which together outweigh the 0.00 mood score. A real person who wants happy pop would find this jarring — it is a workout hype track, not a feel-good pop song.

- *The Metal + Peaceful profile returned Iron Hymn (aggressive metal) as its #1 result.* The contradiction was completely ignored because genre matched perfectly at 1.0, and that 0.30 weight drowned out the mood mismatch. The system treated "I like metal" as the dominant signal and effectively forgot "I want something peaceful."

- *The Orphan Genre (World) profile produced a surprisingly reasonable top result — Monsoon Season scored 0.95 — but only because it was the one exact world genre match.* The other four spots went to folk and lofi songs with vague acoustic similarity, not because they are musically close to world music, but because everything else scored 0.0 on genre and these happened to win on energy and valence.

- *Removing the mood component entirely in a controlled experiment only caused two songs to swap positions* (Gym Hero and Rooftop Lights at #2 and #3). This confirmed that mood influences the ranking but cannot override genre — it only matters when two songs are already close in score.

----------------------------------------------------------------------------

## 8. Future Work  

- Lower the genre weight and raise the mood weight so emotional preference has a real chance to influence results, not just tiebreak them.
- Replace the binary `likes_acoustic` and `likes_mainstream` flags with a 0–1 slider so users can express nuanced taste instead of being forced into one of two extremes.
- Add a diversity filter so the top 5 results cannot all come from the same genre — this would help surface songs users wouldn't have searched for on their own.

----------------------------------------------------------------------------

## 9. Personal Reflection  

Going into this project, I thought the hard part would be the code. It wasn't. The hard part was deciding what mattered. Every time I assigned a weight, I was making a claim about what music taste actually is — and those claims turned out to be wrong in ways I didn't expect. The moment that stuck with me most was when I removed mood from the scoring entirely and almost nothing changed. I had spent real time designing the mood lookup table, checking similarity values, making sure it felt right. And the algorithm just... didn't care. That was humbling. It made me realize that building a system and understanding a system are two very different things.

AI tools helped me move faster, especially when generating the genre and mood similarity tables. But I learned quickly that I couldn't just trust the output. Some of the suggested valence mappings sounded right on the surface but fell apart when I checked them against actual songs in the catalog. I had to verify everything manually. That back-and-forth — use the tool, then question it — ended up being one of the more useful habits I built during this project.

What surprised me most was how human the results could feel even though the system has no understanding of music at all. When a chill lofi profile got back calm, quiet songs, it felt like the system "got it." But it didn't get anything. It just multiplied some numbers. That gap — between feeling like a recommendation and actually being one — is something I keep thinking about. Real recommenders on Spotify or YouTube probably feel even more intuitive, but they're doing the same thing at a much larger scale. The intelligence is an illusion built from enough data and enough weights.

If I kept going with this, I'd want to break the binary preferences first. Forcing a user to say "yes acoustic" or "no acoustic" throws away too much nuance. A slider would get closer to how people actually feel about music. After that, I'd grow the catalog and see what breaks — because I suspect the niche genre problem, where world and classical users get stuck with the same narrow results, only gets more visible as the catalog expands and the gaps become harder to ignore.

----------------------------------------------------------------------------  

----------------------------------------------------------------------------
## Model Card Sections (Summary)

### Model Name

VibeSync 1.0.
----------------------------------------------------------------------------
### Goal / Task

It suggests songs a user might enjoy. The user tells it their favorite genre, mood, and energy level. It returns the 5 best matches from the catalog.
----------------------------------------------------------------------------
### Data Used

- 20 songs with 12 features each.
- Covers 17 genres and 16 moods.
- All songs are from 2017–2023. No older music. Most songs have mid-to-high energy.
----------------------------------------------------------------------------
### Algorithm Summary

Each song gets a score from 0 to 1. Genre counts the most (30%). Energy is next (25%). Then mood-based valence (20%). Mood label, acousticness, popularity, and release year each add a small amount. The top 5 songs win.
----------------------------------------------------------------------------
### Observed Behavior / Biases

Genre controls the ranking. Changing mood barely moves results. Users who like calm music get poor matches because the catalog skews high-energy. Niche genre users (world, classical) almost always get the same narrow results.
----------------------------------------------------------------------------
### Evaluation Process

We tested 9 user profiles. Some were simple (Chill Lofi). Some were contradictory (Metal + Peaceful). One was a niche edge case (World genre). We checked if the results made sense for a real person with those preferences. We also removed mood entirely in one test to see how much it actually mattered.
----------------------------------------------------------------------------
### Intended Use and Non-Intended Use

**Use it for:**
- Learning how recommender systems work.
- Classroom experiments and exploration.

**Do not use it for:**
- Real music apps or production systems.
- Users who want recommendations based on listening history.
----------------------------------------------------------------------------
### Ideas for Improvement

- Reduce the genre weight so mood has more say.
- Replace yes/no acoustic and mainstream options with a slider.
- Add a rule so the top 5 results come from different genres.
----------------------------------------------------------------------------