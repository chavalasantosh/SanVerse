"""
COMPLETE SanTOK Model Trainer - Single File
============================================

ONE complete file that does everything:
- Validates training data quality
- Builds vocabulary
- Trains semantic embeddings (with quality monitoring)
- Generates feature-based embeddings
- Combines vectors (semantic + feature)
- Trains language model (with quality checks)


Usage:
    python train_src.py --data training_data.txt

All quality checks included:
- Rejects datasets < 0.5 MB
- Stops if semantic loss diverges
- Rejects LM training if loss = 0.0
- All validation and monitoring built-in
"""

import argparse
import bz2
import pickle
import random
import re
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple, Union

import numpy as np
from tqdm import tqdm

# Add src to path for SanTOK imports
sys.path.insert(0, str(Path(__file__).parent))

# Import SanTOK components (these exist in your codebase)
from src.training.vocabulary_builder import SanTOKVocabularyBuilder
from src.training.language_model_trainer import (
    SanTOKLanguageModel,
    SanTOKLanguageModelTrainer
)
from src.embeddings.embedding_generator import SanTOKEmbeddingGenerator
from src.embeddings.semantic_trainer import SanTOKSemanticTrainer
from src.core.core_tokenizer import TextTokenizer


class CompleteSanTOKTrainer:
    """
    Complete unified trainer - everything in one class.
    """
    def __init__(
        self,
        vocab_size: int = 60000,
        embedding_dim: int = 768,
        num_layers: int = 12,
        num_heads: int = 12,
        max_seq_length: int = 1024,
        learning_rate: float = 1e-4,
        batch_size: int = 32,
        use_semantic: bool = True,
        use_feature_based: bool = True,
        vector_combination: str = "weighted_average"
    ) -> None:
        """
        Initialize complete trainer.
        
        Args:
            vocab_size: Size of vocabulary
            embedding_dim: Dimension of embeddings
            num_layers: Number of transformer layers
            num_heads: Number of attention heads
            max_seq_length: Maximum sequence length
            learning_rate: Learning rate for training
            batch_size: Batch size for training
            use_semantic: Whether to use semantic embeddings
            use_feature_based: Whether to use feature-based embeddings
            vector_combination: Method to combine vectors
        
        Raises:
            ValueError: If parameters are invalid
        """
        if vocab_size < 1:
            raise ValueError(f"vocab_size must be positive, got {vocab_size}")
        if embedding_dim < 1:
            raise ValueError(f"embedding_dim must be positive, got {embedding_dim}")
        if num_layers < 1:
            raise ValueError(f"num_layers must be positive, got {num_layers}")
        if num_heads < 1:
            raise ValueError(f"num_heads must be positive, got {num_heads}")
        if max_seq_length < 1:
            raise ValueError(f"max_seq_length must be positive, got {max_seq_length}")
        if learning_rate <= 0:
            raise ValueError(f"learning_rate must be positive, got {learning_rate}")
        if batch_size < 1:
            raise ValueError(f"batch_size must be positive, got {batch_size}")
        if vector_combination not in ["weighted_average", "concatenate", "sum"]:
            raise ValueError(
                f"vector_combination must be one of ['weighted_average', 'concatenate', 'sum'], "
                f"got {vector_combination}"
            )
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.max_seq_length = max_seq_length
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.use_semantic = use_semantic
        self.use_feature_based = use_feature_based
        self.vector_combination = vector_combination

        # Components
        self.vocab_builder = None
        self.model = None
        self.tokenizer = TextTokenizer(seed=42, embedding_bit=False)
        self.semantic_trainer = None
        self.feature_embedder = None
        self.semantic_embedder = None
        self.vector_embeddings = {}

    def validate_dataset(self, text_file: Union[str, Path]) -> bool:
        """Validate training data with strict requirements."""
        print("\n" + "="*70)
        print("Dataset Quality Validation")
        print("="*70)

        # Handle compressed files
        if text_file.suffix == '.bz2':
            print(f"  Detected compressed file: {text_file}")
            print("  Will extract text during processing...")
            # For validation, we'll check the compressed size
            file_size = text_file.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            print(f"  Compressed size: {file_size_mb:.2f} MB")
            if file_size_mb < 1.0:
                print(f"\n❌ ERROR: Compressed file too small ({file_size_mb:.2f} MB)")
                print(f"   Need at least 1 MB compressed (expands to ~5-10 MB text)")
                return False
            # For .bz2 files, we'll validate after extraction
            return True

        with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()

        text_size = len(text)
        text_size_mb = text_size / (1024 * 1024)
        min_size_mb = 0.5
        min_chars = int(min_size_mb * 1024 * 1024)

        print("\n[1] Size Check:")
        print(f"   Current: {text_size:,} chars ({text_size_mb:.2f} MB)")
        print(f"   Required: {min_chars:,} chars ({min_size_mb:.2f} MB minimum)")

        if text_size < min_chars:
            print("\n❌ CRITICAL ERROR: Dataset too small!")
            print(f"   You have: {text_size:,} chars ({text_size_mb:.2f} MB)")
            print(f"   Minimum required: {min_chars:,} chars ({min_size_mb:.2f} MB)")
            print("   For semantic embeddings: Need at least 1-5 MB")
            print("   For language model: Need at least 10-50 MB")
            return False

        print("\n[2] Sentence Structure Check:")
        sentences = [s.strip() for s in text.split('.') if s.strip() and len(s.strip()) > 10]
        sentence_count = len(sentences)
        print(f"   Sentences found: {sentence_count:,}")
        print("   Required: 500+ sentences")

        if sentence_count < 500:
            print("\n❌ ERROR: Insufficient sentence structure!")
            print(f"   Found: {sentence_count} sentences")
            print("   Required: 500+ sentences")
            return False

        avg_sentence_len = sum(len(s) for s in sentences) / len(sentences) if sentences else 0
        print(f"   Avg sentence length: {avg_sentence_len:.1f} chars")

        if avg_sentence_len < 30:
            print("\n❌ ERROR: Sentences too short!")
            print(f"   Average: {avg_sentence_len:.1f} chars")
            print("   Required: 30+ chars per sentence")
            return False

        print("\n[3] Vocabulary Diversity Check:")
        words = text.split()
        unique_words = set(words)
        unique_ratio = len(unique_words) / len(words) if words else 0
        print(f"   Total words: {len(words):,}")
        print(f"   Unique words: {len(unique_words):,}")
        print(f"   Unique ratio: {unique_ratio*100:.1f}%")

        # Wikipedia and large corpora naturally have lower unique ratios
        # Adjust threshold based on dataset size
        min_unique_ratio = 0.15 if text_size < 10 * 1024 * 1024 else 0.05

        if len(words) > 0 and unique_ratio < min_unique_ratio:
            print("\n❌ ERROR: Too many repeated words!")
            print(f"   Unique ratio: {unique_ratio*100:.1f}%")
            print(f"   Required: {min_unique_ratio*100:.1f}%+ unique words")
            print("   (Large datasets like Wikipedia naturally have lower ratios)")
            return False

        print(f"\n[4] Token Metadata Detection:")
        lines = text.split('\n')[:100]
        metadata_patterns = 0
        for line in lines:
            if 'word' in line.lower() and any(c.isdigit() for c in line) and len(line.split()) > 5:
                metadata_patterns += 1

        if metadata_patterns > len(lines) * 0.3:
            print("   ⚠️  WARNING: Detected token metadata patterns!")
            print("   This file appears to be SanTOK token output, not source text.")
            print("   Token metadata cannot train semantic embeddings.")
            return False

        print("\n" + "="*70)
        print("✓ Dataset Validation PASSED")
        print("="*70)
        return True

    def train(
        self,
        text_file: Path,
        epochs: int = 10,
        semantic_epochs: int = 10,
        output_dir: Path = Path("models"),
        vocab_path: Optional[Path] = None
    ):
        """Complete training pipeline - everything in one method."""
        output_dir.mkdir(parents=True, exist_ok=True)

        print("\n" + "="*70)
        print("COMPLETE SanTOK Model Training")
        print("="*70)
        print(f"Data: {text_file}")
        print(f"Output: {output_dir}")
        print()

        # Step 1: Handle compressed files and validate dataset
        if text_file.suffix == '.bz2':
            print(f"\n[Step 1a] Processing compressed file: {text_file}")
            # Extract to text file
            extracted_path = output_dir.parent / "training_data" / "combined_training_data.txt"
            extracted_path.parent.mkdir(parents=True, exist_ok=True)

            if not extracted_path.exists() or extracted_path.stat().st_size < 1000000:
                extracted_path = extract_text_from_wikipedia_bz2(
                    text_file, extracted_path, max_size_mb=50.0
                )
            else:
                print(f"  Using existing extracted file: {extracted_path}")
                size_mb = extracted_path.stat().st_size / (1024*1024)
                print(f"  Size: {size_mb:.2f} MB")

            text_file = extracted_path

        # Validate dataset
        if not self.validate_dataset(text_file):
            print("\n❌ TRAINING ABORTED: Dataset quality insufficient")
            return False

        # Step 2: Build/load vocabulary
        if vocab_path and vocab_path.exists():
            print(f"\n[Step 2] Loading vocabulary from {vocab_path}...")
            self.vocab_builder = SanTOKVocabularyBuilder()
            self.vocab_builder.load(vocab_path)
        else:
            print("\n[Step 2] Building vocabulary...")
            self.vocab_builder = SanTOKVocabularyBuilder(vocab_size=self.vocab_size, min_frequency=2)
            self.vocab_builder.build_vocabulary(text_file)
            vocab_save_path = output_dir / "santok_60k_vocab.pkl"
            self.vocab_builder.save(vocab_save_path)
            print(f"✓ Vocabulary saved: {vocab_save_path}")

        print(f"✓ Vocabulary: {len(self.vocab_builder.token_to_id):,} tokens")

        # Step 3: Train semantic embeddings (if enabled)
        if self.use_semantic:
            print("\n[Step 3] Training semantic embeddings...")
            success = self._train_semantic(text_file, semantic_epochs, output_dir)
            if not success:
                print("\n❌ Semantic training failed - aborting")
                return False

        # Step 4: Generate vector embeddings
        print("\n[Step 4] Generating vector embeddings...")
        self._generate_vectors(text_file, output_dir)

        # Step 5: Train language model
        print("\n[Step 5] Training language model...")
        self._train_language_model(text_file, epochs, output_dir)

        print("\n" + "="*70)
        print("✓ Training Complete!")
        print("="*70)
        print(f"  Model: {output_dir / f'santok_lm_epoch_{epochs}.pkl'}")
        if self.use_semantic:
            print(f"  Semantic: {output_dir / 'santok_semantic_model.pkl'}")
        print(f"  Vectors: {output_dir / 'santok_vector_embeddings.pkl'}")

        return True

    def _train_semantic(self, text_file: Path, epochs: int, output_dir: Path) -> bool:
        """Train semantic embeddings with quality monitoring."""
        self.semantic_trainer = SanTOKSemanticTrainer(embedding_dim=self.embedding_dim)

        with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()

        streams = self.tokenizer.build(text)
        all_tokens = []
        for stream in streams.values():
            if hasattr(stream, 'tokens'):
                all_tokens.extend(stream.tokens)

        print(f"  Tokenized {len(all_tokens):,} tokens")

        # Build vocab and co-occurrence
        self.semantic_trainer.build_vocab(all_tokens)
        self.semantic_trainer.build_cooccurrence(all_tokens)

        # Train with monitoring
        print(f"  Training semantic embeddings (epochs={epochs})...")
        loss_history = []
        best_loss = float('inf')
        epochs_without_improvement = 0

        vocab_size = len(self.semantic_trainer.vocab)
        use_sparse = self.semantic_trainer.cooccurrence_dict is not None

        for epoch in range(epochs):
            total_loss = 0.0
            num_updates = 0

            if use_sparse:
                cooccurrence_pairs = list(
                    self.semantic_trainer.cooccurrence_dict.items()
                )
                max_pairs = min(100000, len(cooccurrence_pairs))
                if len(cooccurrence_pairs) > max_pairs:
                    cooccurrence_pairs = random.sample(cooccurrence_pairs, max_pairs)

                for (i, j), _weight in cooccurrence_pairs:
                    loss = self.semantic_trainer._update_embeddings(
                        i, j, positive=True
                    )
                    total_loss += loss
                    num_updates += 1

                    for _ in range(5):
                        neg_j = np.random.randint(0, vocab_size)
                        if (i, neg_j) not in self.semantic_trainer.cooccurrence_dict:
                            self.semantic_trainer._update_embeddings(
                                i, neg_j, positive=False
                            )
            else:
                max_iterations = min(100000, vocab_size * vocab_size)
                iterations = 0
                for i in range(vocab_size):
                    for j in range(vocab_size):
                        if iterations >= max_iterations:
                            break
                        if self.semantic_trainer.cooccurrence_matrix[i, j] > 0:
                            loss = self.semantic_trainer._update_embeddings(
                                i, j, positive=True
                            )
                            total_loss += loss
                            num_updates += 1
                            iterations += 1

                            for _ in range(5):
                                neg_j = np.random.randint(0, vocab_size)
                                if self.semantic_trainer.cooccurrence_matrix[i, neg_j] == 0:
                                    self.semantic_trainer._update_embeddings(
                                        i, neg_j, positive=False
                                    )
                    if iterations >= max_iterations:
                        break

            avg_loss = total_loss / max(num_updates, 1)
            loss_history.append(avg_loss)

            # Quality checks
            is_improving = avg_loss < best_loss - 0.01
            is_diverging = (
                len(loss_history) >= 2 and
                loss_history[-1] > loss_history[-2] * 1.1
            )

            if is_improving:
                best_loss = avg_loss
                epochs_without_improvement = 0
            else:
                epochs_without_improvement += 1

            status = f"  Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}"
            if is_improving:
                status += " ✓"
            elif is_diverging:
                status += " ⚠️ DIVERGING"
            print(status)

            # Stop if diverging
            if is_diverging and epoch >= 2:
                print(f"\n❌ TRAINING STOPPED: Loss diverging (epoch {epoch + 1})")
                print(f"   Loss increased: {loss_history[-2]:.4f} → {avg_loss:.4f}")
                return False

            if epochs_without_improvement >= 3 and epoch >= 3:
                print("\n⚠️ EARLY STOPPING: No improvement for 3 epochs")
                break

            if (epoch + 1) % 2 == 0:
                self.semantic_trainer.token_embeddings = (
                    self.semantic_trainer._normalize(
                        self.semantic_trainer.token_embeddings
                    )
                )
                self.semantic_trainer.context_embeddings = (
                    self.semantic_trainer._normalize(
                        self.semantic_trainer.context_embeddings
                    )
                )

        # Save semantic model
        semantic_path = output_dir / "santok_semantic_model.pkl"
        self.semantic_trainer.save(str(semantic_path))
        print(f"✓ Semantic model saved: {semantic_path}")

        return True

    def _generate_vectors(self, text_file: Path, output_dir: Path):
        """Generate combined vector embeddings."""
        if self.use_feature_based:
            self.feature_embedder = SanTOKEmbeddingGenerator(
                strategy="feature_based",
                embedding_dim=self.embedding_dim
            )

        if self.use_semantic:
            self.semantic_embedder = SanTOKEmbeddingGenerator(
                strategy="semantic",
                embedding_dim=self.embedding_dim,
                semantic_model_path=str(output_dir / "santok_semantic_model.pkl")
            )
            self.semantic_embedder.semantic_trainer = self.semantic_trainer

        with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()

        streams = self.tokenizer.build(text)
        token_to_id_map = {}
        for stream in streams.values():
            if hasattr(stream, 'tokens'):
                for token in stream.tokens:
                    token_text = token.text
                    if token_text in self.vocab_builder.token_to_id:
                        vocab_id = self.vocab_builder.token_to_id[token_text]
                        if vocab_id not in token_to_id_map:
                            token_to_id_map[vocab_id] = token

        print(f"  Generating embeddings for {len(token_to_id_map):,} tokens...")

        for vocab_id, token in tqdm(token_to_id_map.items(), desc="  Generating vectors"):
            semantic_emb = None
            feature_emb = None

            if self.use_semantic:
                semantic_emb = self.semantic_embedder.generate(token)

            if self.use_feature_based:
                feature_emb = self.feature_embedder.generate(token)

            # Combine
            if self.vector_combination == "weighted_average":
                if semantic_emb is not None and feature_emb is not None:
                    combined = 0.6 * semantic_emb + 0.4 * feature_emb
                    combined = combined / np.linalg.norm(combined)
                elif semantic_emb is not None:
                    combined = semantic_emb
                elif feature_emb is not None:
                    combined = feature_emb
                else:
                    continue
            elif self.vector_combination == "semantic_only":
                combined = semantic_emb if semantic_emb is not None else feature_emb
            elif self.vector_combination == "feature_only":
                combined = feature_emb if feature_emb is not None else semantic_emb
            else:
                combined = semantic_emb if semantic_emb is not None else feature_emb

            self.vector_embeddings[vocab_id] = combined.astype(np.float32)

        # Save vectors
        vector_path = output_dir / "santok_vector_embeddings.pkl"
        with open(vector_path, 'wb') as f:
            pickle.dump(self.vector_embeddings, f)
        print(f"✓ Vector embeddings saved: {vector_path}")

    def _train_language_model(self, text_file: Path, epochs: int, output_dir: Path):
        """Train language model with quality checks."""
        # Create model
        self.model = SanTOKLanguageModel(
            vocab_size=len(self.vocab_builder.token_to_id),
            embedding_dim=self.embedding_dim,
            num_layers=self.num_layers,
            num_heads=self.num_heads,
            max_seq_length=self.max_seq_length
        )

        # Update model embeddings with vectors
        if self.vector_embeddings:
            for vocab_id, embedding in self.vector_embeddings.items():
                if vocab_id < self.model.vocab_size:
                    self.model.token_embeddings[vocab_id] = embedding

        # Create trainer
        trainer = SanTOKLanguageModelTrainer(
            model=self.model,
            vocab_builder=self.vocab_builder,
            learning_rate=self.learning_rate,
            batch_size=self.batch_size,
            seq_length=self.max_seq_length
        )

        # Train (with built-in validation)
        trainer.train(
            text_file=text_file,
            epochs=epochs,
            save_every=2,
            output_dir=output_dir
        )


def extract_text_from_wikipedia_bz2(
    bz2_path: Path, output_path: Path, max_size_mb: float = 50.0
) -> Path:
    """Extract text from Wikipedia .bz2 XML dump."""
    print(f"\nExtracting text from Wikipedia dump: {bz2_path}")
    print("  This may take a few minutes...")

    max_size_bytes = int(max_size_mb * 1024 * 1024)
    extracted_size = 0

    # Pattern to extract text from XML
    text_pattern = re.compile(r'<text[^>]*>(.*?)</text>', re.DOTALL)

    with bz2.open(bz2_path, 'rt', encoding='utf-8', errors='ignore') as bz2_file:
        with open(output_path, 'w', encoding='utf-8') as out_file:
            buffer = ""
            for line in bz2_file:
                buffer += line

                # Extract text when we find </text> tag
                if '</text>' in buffer:
                    matches = text_pattern.findall(buffer)
                    for match in matches:
                        # Clean XML tags and get plain text
                        text = re.sub(r'<[^>]+>', '', match)
                        text = re.sub(r'\[\[[^\]]+\]\]', '', text)  # Remove wiki links
                        text = re.sub(r'\{[^}]+\}', '', text)  # Remove templates
                        text = text.strip()

                        if len(text) > 50:  # Only sentences with substantial content
                            out_file.write(text + '\n')
                            extracted_size += len(text)

                            if extracted_size >= max_size_bytes:
                                size_mb = extracted_size/1024/1024
                                print(f"  Extracted {size_mb:.2f} MB (limit: {max_size_mb} MB)")
                                return output_path

                    buffer = ""

                # Progress update
                if extracted_size > 0 and extracted_size % (10 * 1024 * 1024) == 0:
                    size_mb = extracted_size/1024/1024
                    print(f"  Extracted: {size_mb:.2f} MB...")

    size_mb = extracted_size/1024/1024
    print(f"✓ Extracted {size_mb:.2f} MB to {output_path}")
    return output_path


def find_training_data() -> Optional[Path]:
    """Auto-detect training data file."""
    # First check for already extracted text files
    possible_locations = [
        Path("training_data/combined_training_data.txt"),
        Path("training_data/custom/training.txt"),
        Path("user_datasets/training.txt"),
    ]

    # Check for existing extracted text files (must be > 1MB to be valid)
    for path in possible_locations:
        if path.exists() and path.stat().st_size > 1000000:  # At least 1MB
            return path

    # Check for Wikipedia dump (BEST option - 122 MB!)
    wikipedia_bz2 = Path(
        "training_data/wikipedia/enwiki-latest-pages-articles.xml.bz2"
    )
    if wikipedia_bz2.exists():
        print(f"\n✓ Found Wikipedia dump: {wikipedia_bz2}")
        size_mb = wikipedia_bz2.stat().st_size / (1024*1024)
        print(f"  Size: {size_mb:.2f} MB")
        print("  This is perfect for training!")

        # Extract to text file
        output_path = Path("training_data/combined_training_data.txt")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if not output_path.exists() or output_path.stat().st_size < 1000000:
            print("\n  Extracting text from Wikipedia dump...")
            # Extract text from Wikipedia dump (extract 50 MB of text)
            extract_text_from_wikipedia_bz2(
                wikipedia_bz2, output_path, max_size_mb=50.0
            )
        else:
            print(f"  Using existing extracted file: {output_path}")
            size_mb = output_path.stat().st_size / (1024*1024)
            print(f"  Size: {size_mb:.2f} MB")

        if output_path.exists() and output_path.stat().st_size > 1000000:
            return output_path

    # Fallback to small files (will fail validation but user will see error)
    for path in possible_locations:
        if path.exists():
            return path

    return None


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Complete SanTOK Model Trainer - Single File",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python train_src.py --data training_data.txt
  python train_src.py  (auto-detects training data)
  python train_src.py --data data.txt --epochs 20
        """
    )
    parser.add_argument(
        "--data",
        type=str,
        help="Training data file path (optional - will auto-detect)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="models",
        help="Output directory (default: models)"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=10,
        help="Language model epochs (default: 10)"
    )
    parser.add_argument(
        "--semantic-epochs",
        type=int,
        default=10,
        help="Semantic embedding epochs (default: 10)"
    )
    parser.add_argument("--vocab", type=str, help="Path to existing vocabulary (optional)")

    args = parser.parse_args()

    # Find training data
    if args.data:
        data_path = Path(args.data)
    else:
        print("No --data specified, auto-detecting training data...")
        data_path = find_training_data()
        if data_path:
            print(f"✓ Found training data: {data_path}")
        else:
            print("❌ Error: No training data found!")
            print("\nPlease provide training data:")
            cmd = "python train_src.py --data your_data.txt"
            print(f"  1. Use --data flag: {cmd}")
            print("  2. Or place data in one of these locations:")
            print("     - training_data/combined_training_data.txt")
            print("     - training_data/custom/training.txt")
            print("     - user_datasets/training.txt")
            return

    if not data_path.exists():
        print(f"❌ Error: Training data not found: {data_path}")
        return

    output_dir = Path(args.output)

    # Create trainer
    trainer = CompleteSanTOKTrainer(
        vocab_size=60000,
        embedding_dim=768,
        num_layers=12,
        num_heads=12,
        use_semantic=True,
        use_feature_based=True,
        vector_combination="weighted_average"
    )

    # Train
    vocab_path = Path(args.vocab) if args.vocab else None
    success = trainer.train(
        text_file=data_path,
        epochs=args.epochs,
        semantic_epochs=args.semantic_epochs,
        output_dir=output_dir,
        vocab_path=vocab_path
    )

    if success:
        print("\n✓ All training completed successfully!")
    else:
        print("\n❌ Training failed - check errors above")


if __name__ == "__main__":
    main()
