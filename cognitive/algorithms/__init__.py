"""
SOMA Cognitive - Custom Algorithms
====================================

100% UNIQUE. 100% SOMA-NATIVE.

NO external AI. NO borrowed algorithms. These are SOMA-ORIGINAL.

Algorithms:
- SOMARanker: Hybrid relevance scoring (custom formula)
- SOMAPatternMatcher: Relation extraction without ML
- SOMA9Scorer: 9-centric confidence propagation
- SOMAGraphWalker: Custom graph traversal with decay
- SOMASimilarity: Semantic similarity without neural embeddings
- SOMAQueryParser: Natural language to structured query
- SanTEKMetrics: Custom logical metrics for SanTEK improvement
"""

from .SOMA_ranker import somaRanker, RankingResult
from .pattern_matcher import somaPatternMatcher, PatternMatch
from .nine_scorer import soma9Scorer
from .graph_walker import somaGraphWalker, WalkResult, WalkMode, WalkStep
from .semantic_similarity import somaSimilarity, SimilarityResult
from .query_parser import somaQueryParser, ParsedQuery, QueryType
from .santek_metrics import SanTEKMetrics, MetricResult, measure_santek_performance

__all__ = [
    # Ranking
    "SOMARanker",
    "RankingResult",
    
    # Pattern Matching
    "SOMAPatternMatcher",
    "PatternMatch",
    
    # 9-Centric Scoring
    "SOMA9Scorer",
    
    # Graph Walking
    "SOMAGraphWalker",
    "WalkResult",
    "WalkMode",
    "WalkStep",
    
    # Semantic Similarity
    "SOMASimilarity",
    "SimilarityResult",
    
    # Query Parsing
    "SOMAQueryParser",
    "ParsedQuery",
    "QueryType",
    
    # SanTEK Metrics
    "SanTEKMetrics",
    "MetricResult",
    "measure_santek_performance",
]

