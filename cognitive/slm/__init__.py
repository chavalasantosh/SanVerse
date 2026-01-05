"""
SanTOK SLM - Small Language Model

A constrained language generation system that can ONLY emit tokens
sanctioned by SanTOK Cognitive. Hallucination is structurally impossible,
not statistically unlikely.

Architecture:
    SanTOK Cognitive (THINKS) → facts, constraints, reasoning path
    SanTOK SLM (TALKS)        → constrained verbalization ONLY

NumPy is used strictly as a numerical backend.
No pretrained models. No ML frameworks. 100% SanTOK.
"""

from .slm_constraints import (
    TokenConstraint,
    FactConstraint,
    VocabularyScope,
    ConstraintEngine,
)

from .slm_generator import (
    ConstrainedGenerator,
    GenerationConfig,
    GenerationResult,
    SanTOKSLM,
)

from .santok_sequence_optimizer import (
    SanTOKSequenceOptimizer,
    SanTOKSequenceConfig,
    create_santok_sequence_optimizer,
)

from .slm_constrained_decoder import (
    ConstrainedDecoder,
    DecoderConfig,
    SanTOKConstrainedSLM,
    create_santok_constrained_slm,
)

from .training_data import (
    TrainingSequence,
    SanTOKDataGenerator,
    create_training_data,
    create_default_templates,
)

from .slm_trainer import (
    SLMTrainer,
    TrainingConfig,
    create_trainer,
)

__all__ = [
    # Constraints
    'TokenConstraint',
    'FactConstraint',
    'VocabularyScope',
    'ConstraintEngine',
    # Phase 1 Generator
    'ConstrainedGenerator',
    'GenerationConfig',
    'GenerationResult',
    'SanTOKSLM',
    # Phase 2 Sequence Optimizer
    'SanTOKSequenceOptimizer',
    'SanTOKSequenceConfig',
    'create_santok_sequence_optimizer',
    # Phase 2 Decoder
    'ConstrainedDecoder',
    'DecoderConfig',
    'SanTOKConstrainedSLM',
    'create_santok_constrained_slm',
    # Phase 3 Training
    'TrainingSequence',
    'SanTOKDataGenerator',
    'create_training_data',
    'create_default_templates',
    'SLMTrainer',
    'TrainingConfig',
    'create_trainer',
]

