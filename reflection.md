# Reflection: Profile Comparisons

This file compares pairs of user profiles we tested. For each pair, we explain what changed between their results and why it makes sense — written so anyone can follow along, no coding knowledge needed.

---

## Pair 1: High-Energy Pop vs. Chill Lofi

Think of these two listeners as opposites. The High-Energy Pop person wants feel-good, popular, recent pop music they can dance to. The Chill Lofi person wants something quiet and mellow to study or relax to — soft background music, not something you would hear at a party.

The results were completely different, which is exactly what we would hope for. Pop got Sunrise City and Gym Hero — upbeat, well-known songs. Lofi got Library Rain and Midnight Coding — quiet, calm tracks with a low-key vibe.

Not a single song appeared in both lists. That is a good sign. It means our system actually understood the difference between these two types of listeners, not just their genre preference but also their energy and mood.

---

## Pair 2: High-Energy Pop vs. High-Energy Sad

Here is where things get interesting — and a little broken.

These two listeners want almost the same thing: popular, recent pop music with high energy. The only difference is that one wants "happy" songs and the other wants "sad" ones.

You would expect different results. But Gym Hero and Sunrise City showed up at the top of both lists.

Why? Because our catalog simply does not have any sad pop songs. So when the system looked for a sad pop match, it came up empty on mood — and just kept recommending whatever scored highest on genre and energy instead.

This is exactly why Gym Hero keeps showing up for people who want "Happy Pop" too. Gym Hero is a pop song with high energy, so it always scores near the top — even though it is clearly a workout hype track, not a feel-good sing-along. The system cannot tell the difference because it is just matching labels and numbers, not actually listening to the music.

---

## Pair 3: Deep Intense Rock vs. Metal + Peaceful

Both of these listeners want loud, high-energy, underground music. The difference is genre (rock vs. metal) and mood (intense vs. peaceful).

The Rock + Intense profile worked perfectly. Storm Runner — a hard-driving rock song with an intense feel — came out on top. Genre matched, mood matched, energy matched. This is the system working the way it should.

The Metal + Peaceful profile did not work at all. Iron Hymn, which is a heavy and aggressive metal track, scored number one. But the listener said they want something peaceful. The problem is that Iron Hymn is the only metal song in our entire catalog, so it automatically wins on genre — and that advantage was so large it buried the mood mismatch completely.

It is like asking a librarian for "a quiet metal album" and they hand you the loudest one in the store because it is the only metal album they have. Technically they found your genre. But they completely ignored what you were actually in the mood for.

---

## Pair 4: Acoustic Electronic vs. Anti-Mainstream + Recent

The Acoustic Electronic profile is a contradiction — this person wants electronic music but also likes acoustic, organic sounds. Those two things rarely go together.

The system returned Velvet Pulse, an electronic track, at the top. The genre is right, but the song is very produced and synthetic — nothing acoustic about it. The system picked the closest genre match and could not resolve the contradiction. The result is half-right, which in practice means half-wrong.

The Anti-Mainstream + Recent profile ran into a different problem. This person wants underground music that is also new. But our catalog does not actually have any truly underground songs — even the least popular ones are still moderately well-known. So the system returned the most underground-ish songs available, even though they are not really underground by most people's standards. The system did its best, but the data just was not there to support this kind of listener.

---

## Pair 5: Orphan Genre (World) vs. Maximal Indifference

The World Music profile is the toughest test. There is only one world music song in the entire catalog — Monsoon Season. So that song lands at the top by a wide margin, and the rest of the list is filled with folk and acoustic songs that vaguely share a calm feel — not because they sound like world music, but because there is nothing better to offer.

Imagine walking into a music store and asking for world music. They have one world music album. They give you that first, then hand you five folk albums to fill the rest of the bag. That is exactly what our system did.

The Maximal Indifference profile — a jazz listener with moderate, middle-of-the-road preferences — got the most balanced results. Coffee Shop Stories came first, but several other songs scored close behind it. Jazz connects loosely to a few other genres, so more songs got a fair shot at the ranking. No single song dominated by a landslide.

The big takeaway from this pair: a niche listener gets one great match and then filler. A listener with broader, more common tastes gets a real ranking where the order actually means something.
