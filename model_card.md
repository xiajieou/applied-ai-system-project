# Model Card - Music Recommender Simulation

## 1. Model Name

VibeMap Classroom Recommender v2

## 2. Goal and Intended Use

This project started as the Module 3 music recommender and was extended into a fuller applied AI system for the final project. It suggests top songs from a small catalog based on a user's stated preferences, but now it also demonstrates retrieval-augmented guidance, a visible workflow trace, a specialized mode, and a repeatable evaluation script.

Intended use:

- Demonstrate how user inputs are transformed into ranked outputs
- Show how retrieved guidance can influence scoring behavior
- Support discussion of bias, filter bubbles, and evaluation

Non-intended use:

- Real production recommendations for diverse users
- High-stakes decisions
- Personalized discovery across large, multilingual catalogs

## 3. Algorithm Summary (Plain Language)

The model checks each song one-by-one and gives points for matching the user's favorite genre and mood. It then adds similarity points when a song's energy is close to the user's target energy level. A small acoustic bonus is added when the user's acoustic preference aligns with the song.

After each song receives a total score, the list is sorted from highest to lowest. The top `k` songs are returned with human-readable reasons, such as "genre matches" or "energy is close." Retrieval-guided notes can slightly shift the weights before scoring, and specialized mode can rebalance the profile further for a more tailored demo.

## 4. Data Used

The dataset contains 10 songs in `data/songs.csv`.

Features used:

- Categorical: `genre`, `mood`
- Numeric: `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`

Catalog coverage includes pop, lofi, rock, ambient, jazz, synthwave, and indie pop. The dataset is intentionally small and not representative of broad global music tastes. No additional songs were added in this version.

The retrieval layer also uses small hand-written guidance documents that describe the scoring rules and specialization behavior.

## 5. Observed Strengths

- Gives intuitive results for clearly defined profiles.
- Produces explainable output with reason strings for each recommendation.
- Distinguishes high-energy and low-energy profiles reliably.
- The retrieval layer makes the scoring process easier to explain.
- The workflow trace makes it easier to show what the system is doing step by step.

## 6. Limitations and Biases

- Small dataset size limits diversity and can repeat similar songs.
- Genre and energy can dominate the score, reducing exploration.
- Features like lyrics, language, era, and artist novelty are ignored.
- Users with mixed preferences (for example, high energy but sad mood) may receive less satisfying recommendations.
- The retrieval documents are handcrafted, so they can reflect the author's assumptions.
- Specialized mode is still rule-based, not a trained fine-tune, so it is only a lightweight specialization demo.

## 7. Evaluation Process

Profiles tested:

- High-Energy Pop
- Chill Lofi
- Deep Intense Rock

What was checked:

- Whether top-3 and top-5 results matched expected vibe and style
- Whether reasons were consistent with the scoring logic
- Whether rank order changed under RAG and specialized mode
- Whether the workflow emitted a visible plan/retrieve/verify/reflect trace

Experiment:

- Compared baseline scoring against RAG-enhanced scoring
- Compared baseline against specialized mode
- Measured how often the top recommendation or score changed

Interpretation:

The system is stable for strong matches in this small catalog, but the retrieval and specialization layers can nudge scores and explanations in a controlled way. That makes the project better for showing how AI systems can be grounded and evaluated without becoming opaque.

## 8. Ideas for Improvement

- Expand the catalog with more genres, moods, and edge-case songs.
- Add diversity logic so top results are not all near-duplicates.
- Add more user preference fields (tempo range, danceability preference, artist familiarity).
- Replace the rule-based specialization with a learned profile adapter if a larger dataset becomes available.
- Track offline evaluation metrics across multiple profiles and retrieval settings.

## 9. Personal Reflection

The biggest learning moment was seeing how a very small amount of math can create recommendations that feel believable. I learned that scoring and ranking are separate jobs: scoring gives each song a number, while ranking decides which numbers matter most to the user.

AI tools helped speed up implementation and wording, especially for generating structured explanations and testing ideas quickly. One helpful suggestion was to organize the project around separate baseline, RAG, and specialized modes because that made the evaluation story clearer. One flawed suggestion was to over-emphasize genre weight everywhere, which would have made the system less balanced and more repetitive.

What surprised me most is how quickly simple rules can feel "smart" even when they ignore many real-world factors. If I extend this project next, I would focus on diversity-aware ranking and a larger dataset so recommendations can stay relevant without becoming repetitive.
