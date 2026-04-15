# Model Card - Music Recommender Simulation

## 1. Model Name

VibeMap Classroom Recommender v1.

## 2. Goal and Intended Use

This model suggests top songs from a small catalog based on a single user's stated preferences. It is designed for classroom exploration of recommendation concepts and explainable scoring.

Intended use:

- Demonstrate how user inputs are transformed into ranked outputs
- Show how simple weighting choices affect behavior
- Support discussion of bias and filter bubbles

Non-intended use:

- Real production recommendations for diverse users
- High-stakes decisions
- Personalized discovery across large, multilingual catalogs

## 3. Algorithm Summary (Plain Language)

The model checks each song one-by-one and gives points for matching the user's favorite genre and mood. It then adds similarity points when a song's energy is close to the user's target energy level. A small acoustic bonus is added when the user's acoustic preference aligns with the song.

After each song receives a total score, the list is sorted from highest to lowest. The top `k` songs are returned with human-readable reasons, such as "genre matches" or "energy is close." This keeps the recommendation process transparent.

## 4. Data Used

The dataset contains 10 songs in `data/songs.csv`.

Features used:

- Categorical: `genre`, `mood`
- Numeric: `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`

Catalog coverage includes pop, lofi, rock, ambient, jazz, synthwave, and indie pop. The dataset is intentionally small and not representative of broad global music tastes. No additional songs were added in this version.

## 5. Observed Strengths

- Gives intuitive results for clearly defined profiles.
- Produces explainable output with reason strings for each recommendation.
- Distinguishes high-energy and low-energy profiles reliably.
- Works well as a teaching tool because weights are easy to inspect and tune.

## 6. Limitations and Biases

- Small dataset size limits diversity and can repeat similar songs.
- Genre and energy can dominate the score, reducing exploration.
- Features like lyrics, language, era, and artist novelty are ignored.
- Users with mixed preferences (for example, high energy but sad mood) may receive less satisfying recommendations.
- The model can reinforce a narrow taste lane (filter bubble) instead of balancing relevance with novelty.

## 7. Evaluation Process

Profiles tested:

- High-Energy Pop
- Chill Lofi
- Deep Intense Rock

What was checked:

- Whether top-5 results matched expected vibe and style
- Whether reasons were consistent with the scoring logic
- Whether rank order changed under a weight experiment

Experiment:

- Halved genre weight and doubled maximum energy contribution
- For High-Energy Pop, top-3 ordering stayed the same, but score margins changed

Interpretation:

The model is stable for strong matches in this small catalog. Weight changes impact confidence more than ranking when there are clear feature winners.

## 8. Ideas for Improvement

- Expand the catalog with more genres, moods, and edge-case songs.
- Add diversity logic so top results are not all near-duplicates.
- Include more user preference fields (tempo range, danceability preference, artist familiarity).
- Add a profile conflict handler for contradictory preferences.
- Track offline evaluation metrics across multiple profiles.

## 9. Personal Reflection

The biggest learning moment was seeing how a very small amount of math can create recommendations that feel believable. I learned that scoring and ranking are separate jobs: scoring gives each song a number, while ranking decides which numbers matter most to the user.

AI tools helped speed up implementation and wording, especially for generating structured explanations and testing ideas quickly. I still had to double-check suggested logic and outputs, because small weighting changes can create unintended behavior. What surprised me most is how quickly simple rules can feel "smart" even when they ignore many real-world factors.

If I extend this project next, I would focus on diversity-aware ranking and a larger dataset so recommendations can stay relevant without becoming repetitive.
