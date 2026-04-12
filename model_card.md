# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

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

---

## 7. Evaluation

We tested nine user profiles designed to stress-test the scoring logic in different ways. The profiles ranged from straightforward matches (High-Energy Pop, Chill Lofi) to deliberately contradictory combinations (Metal + Peaceful, High-Energy Sad) and edge cases like users with niche genres not well-represented in the catalog (Orphan Genre: World).

For each profile we ran `recommend_songs` against the full 20-song catalog and examined whether the top results matched intuition — meaning: if a real person had those preferences, would they actually enjoy the songs returned?

**What we were looking for:** Whether the top song changed across profiles, whether the score breakdown explained the ranking, and whether the system could surface meaningfully different results when preferences changed.

**What surprised us:**

- *Gym Hero keeps appearing for happy pop users even though it is labeled "intense," not "happy."* The song scores 1.0 on genre (it is pop) and 0.97 on energy, which together outweigh the 0.00 mood score. A real person who wants happy pop would find this jarring — it is a workout hype track, not a feel-good pop song.

- *The Metal + Peaceful profile returned Iron Hymn (aggressive metal) as its #1 result.* The contradiction was completely ignored because genre matched perfectly at 1.0, and that 0.30 weight drowned out the mood mismatch. The system treated "I like metal" as the dominant signal and effectively forgot "I want something peaceful."

- *The Orphan Genre (World) profile produced a surprisingly reasonable top result — Monsoon Season scored 0.95 — but only because it was the one exact world genre match.* The other four spots went to folk and lofi songs with vague acoustic similarity, not because they are musically close to world music, but because everything else scored 0.0 on genre and these happened to win on energy and valence.

- *Removing the mood component entirely in a controlled experiment only caused two songs to swap positions* (Gym Hero and Rooftop Lights at #2 and #3). This confirmed that mood influences the ranking but cannot override genre — it only matters when two songs are already close in score.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
