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












"""
