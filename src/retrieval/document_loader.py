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

1. **genre** (string)L Primary musical genre
   - Examples: pop















"""
