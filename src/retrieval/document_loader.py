"""  
Rag Retrieval System - Document Loader Module

This module loads and manages domain knowledge documents that serve as 
context for the recommendation system. It implements retrieval-agumented
generation by injecting relevant domain rules and metadata into the scoring process. 

"""

# ============================================================================
# DOMAIN KNOWLEDGE DOCUMENTS
# ============================================================================
# These are the knowledge documents that will be retrieved and injected
# as context into the recommendation engine.

SONG_METADATA_GUIDE = """
SONG METADATA GUIDE
==================

Each song in the system has the following attributes:

1. **genre** (string): Primary musical genre
   - Examples: pop, lofi, rock, ambient, jazz, synthwave, indie_pop
   - Usage: Matches against user's favorite_genre preference
   - Weight in scoring: 2.0 (high importance)

2. **mood** (string): Emotional tone of the song
   - Examples: upbeat, chill, energetic, intense, melancholic, peaceful
   - Usage: Matches against user's favorite_mood preference
   - Weight in scoring 1.0 (medium importance)

3. **energy** (float, 0.0-1.0): Overall energetic intensity 
   - 0.0 = Very low (ambient, lo-fi, sleep music)
   - 1.0 = Very high (intense rock, dance, metal)
   - Usage: Matched against user's target_energy with bonus for proximity
   - Max points: 1.5 (peaks at user's target, decreases with distance)

4. **acousticness** (float, 0.0-1.0): Acoustic vs electronic
   - 0.0 = Pure electronic synthesis
   - 1.0 = Pure acoustic instruments
   - Usage: Conditional bonus if user like_acoustic
   - Max points: 1.5 (peak at user's target, decreases with distance)

5. **tempo_bpm** (integer): Beats per minute
   - Range: 60-180 BPM typical
   - Usage: Context only (not scored, but explains pacing)

6. **valence** (float, 0.0-1.0): Musical positivity/happiness
   - 0.0 = Sad, dark, negative mood
   - 1.0 = Happy, upbeat, positive mood
   - Usage: Context only (supports genre interpretation)   

7. **danceability** (float, 0,0-1.0): Rhythmic groove/beat clarity
   - 0.0 = Not danceable (spoken word, free form)
   - 1.0 = Highly danceable (electronic dance, funk, pop)
   - Usage: Context only (supports genre interpretation)
"""

USER_PREFERENCE_RULES  = """ 
USER PREFERENCE RULES
=====================

The recommendation system learns from four core user preference signals:

1. **favorite_genre** (string): Primary music taste
   - Definition: The genre the user most enjoys listening to
   - Scoring rule: Exact genre match = +2.0 points (highest weight)
   - Interpretation: Users strongly prefer songs in their favorite genre

2. **favorite_mood** (string): Preferred emotional tone
   - Definition: The emotional atmosphere the user seeks
   - Scoring rule: Exact mood match = +1.0 points
   - Interpretation: Users want songs that match their current emotional state

3. **target_energy** (float, 0.0-1.0): Desired intensity level
   - Definition: The energetic level (calm vs. intense) user prefers
   - Scoring rule:
     * Peak points (1.5) at exact target energy
     * Decreases with distance: max(0, 1.5 - 2.5 * abs(song_energy - target_energy))
     * Penalty factor of 2.5 ensures steep falloff
   - Interpretation: Users have a sweet spot for activity level

4. **likes_acoustic** (boolean): Acoustic vs. electronic preference
   - Definition: Whether user prefers acoustic instruments over electronics
   - Scoring rule (if True):
     * If acousticness > 0.5: +0.5 bonus points
     * If acousticness <= 0.5: +0.2 bonus points
   - Interpretation: Enables differentiation between similar genres

COMBINING PREFERENCES:
- All scores are additive and normalized
- A song can score at most: 2.0 (genre) + 1.0 (mood) + 1.5 (energy) + 0.5 (acoustic) = 5.0 points
- Top-k recommendations selected by highest total score
"""
