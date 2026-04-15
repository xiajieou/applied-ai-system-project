# Profile Comparison Reflection

Profiles compared:
- High-Energy Pop
- Chill Lofi
- Deep Intense Rock

Pairwise comments:

1. High-Energy Pop vs Chill Lofi
High-Energy Pop prioritizes songs with strong energy and lower acousticness, so songs like `Gym Hero` rank high. Chill Lofi shifts toward lower energy and high acousticness, which moves tracks like `Library Rain` and `Midnight Coding` to the top. This makes sense because the two profiles disagree on both energy target and acoustic preference.

2. High-Energy Pop vs Deep Intense Rock
Both profiles want high energy, so they overlap on songs like `Gym Hero` and `Sunrise City`. The difference is genre and mood: Deep Intense Rock strongly rewards `rock` + `intense`, so `Storm Runner` becomes the clear top result. This confirms genre and mood features are decisive when energy is similar.

3. Chill Lofi vs Deep Intense Rock
These profiles diverge the most. Chill Lofi rewards low-energy, acoustic songs and ranks relaxed tracks first, while Deep Intense Rock surfaces high-energy tracks with lower acousticness. The output change is expected because nearly every core preference flips between these two profiles.

Experiment note:
When genre weight was reduced and energy importance was increased, the strongest high-energy songs kept the same top-3 order, but score differences tightened. This shows the current dataset has dominant matches that remain stable under moderate weight changes.
