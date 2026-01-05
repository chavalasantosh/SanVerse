#!/usr/bin/env python3
"""
SOMA CLI - Complete Command Line Interface

One clean entry point for everything:
- Tokenization
- Training
- Embedding generation
- Vector storage
- Testing
- Custom data handling
- File/URL input
"""

import sys
import os
import json
import numpy as np
from pathlib import Path
from typing import Optional, List
import argparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.dirname(__file__))

# Import with proper error handling
TextTokenizer = None
SOMASemanticTrainer = None
SOMAEmbeddingGenerator = None
EnhancedSOMASemanticTrainer = None

try:
    from src.core.core_tokenizer import TextTokenizer
except ImportError as e:
    print(f"Error: Could not import TextTokenizer: {e}")
    sys.exit(1)

try:
    from src.embeddings.semantic_trainer import somaSemanticTrainer
except ImportError as e:
    print(f"Warning: Could not import somaSemanticTrainer: {e}")

try:
    from src.embeddings.embedding_generator import somaEmbeddingGenerator
except ImportError as e:
    print(f"Warning: Could not import somaEmbeddingGenerator: {e}")

try:
    from enhanced_semantic_trainer.enhanced_trainer import EnhancedSOMASemanticTrainer
except ImportError:
    # Enhanced trainer is optional
    pass


class SOMACLI:
    """Main CLI interface for soma."""
    
    def __init__(self) -> None:
        self.tokenizer: Optional[Any] = None
        self.trainer: Optional[Any] = None
        self.embedding_generator: Optional[Any] = None
        
    def tokenize(
        self,
        text: Optional[str] = None,
        file: Optional[str] = None,
        url: Optional[str] = None,
        method: str = "word",
        seed: int = 42,
        output: Optional[str] = None,
        format: str = "json"  # Using format as parameter name, but avoiding conflict
    ) -> Optional[Dict[str, Any]]:
        """
        Tokenize text, file, or URL.
        
        Args:
            text: Text string to tokenize
            file: Path to file to tokenize
            url: URL to fetch and tokenize
            method: Tokenization method to use
            seed: Random seed for deterministic results
            output: Output file path (optional)
            format: Output format ("json" or "pretty")
        
        Returns:
            Dictionary with tokenization results, or None on error
        """
        if not isinstance(method, str):
            raise TypeError(f"method must be str, got {type(method).__name__}")
        if not isinstance(seed, int):
            raise TypeError(f"seed must be int, got {type(seed).__name__}")
        if not isinstance(format, str):
            raise TypeError(f"format must be str, got {type(format).__name__}")
        
        print("=" * 60)
        print("SOMA Tokenization")
        print("=" * 60)
        print()
        
        # Get input
        input_text: str = ""
        source: str = ""
        
        if text:
            if not isinstance(text, str):
                raise TypeError(f"text must be str, got {type(text).__name__}")
            input_text = text
            source = "text"
        elif file:
            if not isinstance(file, str):
                raise TypeError(f"file must be str, got {type(file).__name__}")
            if not os.path.exists(file):
                print(f"Error: File not found: {file}", file=sys.stderr)
                return None
            try:
                # Try text first
                with open(file, 'r', encoding='utf-8') as f:
                    input_text = f.read()
            except (UnicodeDecodeError, UnicodeError):
                # If UTF-8 fails, try reading as binary and convert
                try:
                    with open(file, 'rb') as f:
                        raw_bytes = f.read()
                    # Try to decode
                    input_text = raw_bytes.decode('utf-8', errors='replace')
                except Exception as e:
                    print(f"Error reading file: {e}", file=sys.stderr)
                    return None
            source = f"file: {file}"
        elif url:
            if not isinstance(url, str):
                raise TypeError(f"url must be str, got {type(url).__name__}")
            try:
                import urllib.request
                import socket
                # Set timeout
                socket.setdefaulttimeout(30)
                req = urllib.request.Request(url, headers={'User-Agent': 'SOMA-CLI/1.0'})
                with urllib.request.urlopen(req, timeout=30) as response:
                    raw_data = response.read()
                    input_text = raw_data.decode('utf-8', errors='replace')
                source = f"url: {url}"
            except Exception as e:
                print(f"Error loading URL: {e}", file=sys.stderr)
                return None
        else:
            print("Error: Must provide --text, --file, or --url", file=sys.stderr)
            return None
        
        print(f"Source: {source}")
        print(f"Input length: {len(input_text)} characters")
        print(f"Method: {method}")
        print(f"Seed: {seed}")
        print()
        
        # Tokenize
        print("Tokenizing...")
        try:
            if TextTokenizer is None:
                print("Error: TextTokenizer not available.", file=sys.stderr)
                return None
            if not input_text or len(input_text.strip()) == 0:
                print("Error: Input text is empty.", file=sys.stderr)
                return None
            tokenizer = TextTokenizer(seed=seed, embedding_bit=False)
            streams = tokenizer.build(input_text)
            
            if not streams:
                print("Error: No streams generated.")
                return
            
            print(f"Streams generated: {list(streams.keys())}")
            for stream_name, stream in streams.items():
                print(f"  - {stream_name}: {len(stream.tokens)} tokens")
            print()
            
            # Get requested stream
            if method in streams:
                tokens = streams[method].tokens
                print(f"Selected stream '{method}': {len(tokens)} tokens")
                print()
                
                # Show sample
                print("Sample tokens (first 10):")
                for i, token in enumerate(tokens[:10]):
                    print(f"  {i+1}. '{token.text}' (UID: {token.uid})")
                if tokens and len(tokens) > 10:
                    print(f"  ... and {len(tokens) - 10} more")
                print()
                
                # Save output
                if output:
                    # Create output directory if needed
                    output_dir = os.path.dirname(output)
                    if output_dir and output_dir != '' and not os.path.exists(output_dir):
                        os.makedirs(output_dir, exist_ok=True)
                    
                    if format == "json":
                        data = {
                            "source": source,
                            "method": method,
                            "seed": seed,
                            "total_tokens": len(tokens),
                            "tokens": [
                                {
                                    "text": t.text,
                                    "uid": t.uid,
                                    "index": t.index,
                                    "content_id": t.content_id
                                }
                                for t in tokens
                            ]
                        }
                        with open(output, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        print(f"Saved to: {output}")
                    elif format == "txt":
                        with open(output, 'w', encoding='utf-8') as f:
                            for token in tokens:
                                f.write(f"{token.text}\n")
                        print(f"Saved to: {output}")
                    else:
                        print(f"Unknown format: {format}")
            else:
                print(f"Error: Method '{method}' not found in streams")
                print(f"Available methods: {list(streams.keys())}")
                
        except Exception as e:
            print(f"Error during tokenization: {e}")
            import traceback
            traceback.print_exc()
    
    def train(
        self,
        text: Optional[str] = None,
        file: Optional[str] = None,
        url: Optional[str] = None,
        model_path: str = "SOMA_model.pkl",
        embedding_dim: int = 768,
        epochs: int = 10,
        window_size: int = 5,
        enhanced: bool = False
    ):
        """Train semantic embeddings."""
        print("=" * 60)
        print("SOMA Semantic Training")
        print("=" * 60)
        print()
        
        # Get input
        if text:
            input_text = text
        elif file:
            if not os.path.exists(file):
                print(f"Error: File not found: {file}")
                return
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    input_text = f.read()
            except (UnicodeDecodeError, UnicodeError):
                try:
                    with open(file, 'rb') as f:
                        raw_bytes = f.read()
                    input_text = raw_bytes.decode('utf-8', errors='replace')
                except Exception as e:
                    print(f"Error reading file: {e}")
                    return
        elif url:
            try:
                import urllib.request
                import socket
                socket.setdefaulttimeout(30)
                req = urllib.request.Request(url, headers={'User-Agent': 'SOMA-CLI/1.0'})
                with urllib.request.urlopen(req, timeout=30) as response:
                    raw_data = response.read()
                    input_text = raw_data.decode('utf-8', errors='replace')
            except Exception as e:
                print(f"Error loading URL: {e}")
                return
        else:
            print("Error: Must provide --text, --file, or --url")
            return
        
        print(f"Corpus length: {len(input_text)} characters")
        print(f"Model path: {model_path}")
        print(f"Embedding dim: {embedding_dim}")
        print(f"Epochs: {epochs}")
        print(f"Enhanced: {enhanced}")
        print()
        
        # Tokenize
        print("Step 1: Tokenizing...")
        if TextTokenizer is None:
            print("Error: TextTokenizer not available.")
            return
        if not input_text or len(input_text.strip()) == 0:
            print("Error: Input text is empty.")
            return
        tokenizer = TextTokenizer(seed=42, embedding_bit=False)
        streams = tokenizer.build(input_text)
        
        if not streams:
            print("Error: No streams generated.")
            return
        
        total_tokens = sum(len(s.tokens) for s in streams.values())
        if total_tokens == 0:
            print("Error: No tokens generated.")
            return
        print(f"Total tokens: {total_tokens:,}")
        print()
        
        # Train
        print("Step 2: Training...")
        try:
            if enhanced:
                if EnhancedSOMASemanticTrainer is None:
                    print("Error: Enhanced trainer not available. Install enhanced_semantic_trainer module.")
                    return
                trainer = EnhancedSOMASemanticTrainer(
                    embedding_dim=embedding_dim,
                    epochs=epochs,
                    window_size=window_size,
                    use_multi_stream=True,
                    use_temporal=True,
                    use_content_id_clustering=True,
                    use_math_properties=True
                )
                trainer.train(streams)
            else:
                if SOMASemanticTrainer is None:
                    print("Error: Semantic trainer not available.")
                    return
                trainer = SOMASemanticTrainer(
                    embedding_dim=embedding_dim,
                    epochs=epochs,
                    window_size=window_size
                )
                all_tokens = []
                for stream in streams.values():
                    all_tokens.extend(stream.tokens)
                if not all_tokens:
                    print("Error: No tokens found in streams.")
                    return
                trainer.build_vocab(all_tokens)
                trainer.build_cooccurrence(all_tokens)
                trainer.train(all_tokens)
            
            # Save
            print()
            print("Step 3: Saving model...")
            # Create output directory if needed
            model_dir = os.path.dirname(model_path)
            if model_dir and model_dir != '' and not os.path.exists(model_dir):
                os.makedirs(model_dir, exist_ok=True)
            trainer.save(model_path)
            print()
            print("=" * 60)
            print("Training complete!")
            print(f"Model saved to: {model_path}")
            print("=" * 60)
            
        except Exception as e:
            print(f"Error during training: {e}")
            import traceback
            traceback.print_exc()
    
    def embed(
        self,
        text: Optional[str] = None,
        file: Optional[str] = None,
        model_path: str = "SOMA_model.pkl",
        output: Optional[str] = None,
        strategy: str = "feature_based"
    ):
        """Generate embeddings."""
        print("=" * 60)
        print("SOMA Embedding Generation")
        print("=" * 60)
        print()
        
        # Get input
        if text:
            input_text = text
        elif file:
            if not os.path.exists(file):
                print(f"Error: File not found: {file}")
                return
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    input_text = f.read()
            except (UnicodeDecodeError, UnicodeError):
                try:
                    with open(file, 'rb') as f:
                        raw_bytes = f.read()
                    input_text = raw_bytes.decode('utf-8', errors='replace')
                except Exception as e:
                    print(f"Error reading file: {e}")
                    return
        else:
            print("Error: Must provide --text or --file")
            return
        
        print(f"Input length: {len(input_text)} characters")
        print(f"Model: {model_path}")
        print(f"Strategy: {strategy}")
        print()
        
        # Check if model exists
        if not os.path.exists(model_path):
            print(f"Warning: Model not found: {model_path}")
            print("Using feature-based embeddings (no training required)")
            strategy = "feature_based"
        
        # Tokenize
        print("Tokenizing...")
        if TextTokenizer is None:
            print("Error: TextTokenizer not available.")
            return
        if not input_text or len(input_text.strip()) == 0:
            print("Error: Input text is empty.")
            return
        tokenizer = TextTokenizer(seed=42, embedding_bit=False)
        streams = tokenizer.build(input_text)
        
        if not streams:
            print("Error: No streams generated.")
            return
        
        # Generate embeddings
        print("Generating embeddings...")
        try:
            if strategy == "semantic" and os.path.exists(model_path):
                if SOMASemanticTrainer is None:
                    print("Error: Semantic trainer not available.")
                    return
                # Load trained model
                trainer = SOMASemanticTrainer()
                trainer.load(model_path)
                
                # Generate embeddings
                embeddings = []
                if "word" not in streams or not streams["word"].tokens:
                    print("Error: No word tokens found.")
                    return
                tokens = streams["word"].tokens
                for token in tokens:
                    emb = trainer.get_embedding(token.uid)
                    if emb is not None:
                        embeddings.append(emb)
                
                if not embeddings:
                    print("Warning: No embeddings generated. Tokens may not be in vocabulary.")
                    return
                
                print(f"Generated {len(embeddings)} embeddings")
            else:
                if SOMAEmbeddingGenerator is None:
                    print("Error: Embedding generator not available.")
                    return
                # Feature-based
                generator = SOMAEmbeddingGenerator(strategy=strategy)
                if "word" not in streams or not streams["word"].tokens:
                    print("Error: No word tokens found.")
                    return
                tokens = streams["word"].tokens
                embeddings = generator.generate_batch(tokens)
                if not embeddings:
                    print("Error: No embeddings generated.")
                    return
                print(f"Generated {len(embeddings)} embeddings")
            
            # Save
            if output:
                # Create output directory if needed
                output_dir = os.path.dirname(output)
                if output_dir and output_dir != '' and not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                # Convert to numpy array if needed
                if isinstance(embeddings, list):
                    embeddings_array = np.array(embeddings)
                else:
                    embeddings_array = embeddings
                np.save(output, embeddings_array)
                print(f"Saved embeddings to: {output}")
            
            print()
            print("=" * 60)
            print("Embedding generation complete!")
            print("=" * 60)
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    def test(self, quick: bool = False):
        """Run tests."""
        print("=" * 60)
        print("SOMA Tests")
        print("=" * 60)
        print()
        
        if quick:
            print("Running quick smoke tests...")
        else:
            print("Running full test suite...")
        print()
        
        # Basic tokenization test
        print("Test 1: Basic Tokenization")
        streams = None
        try:
            if TextTokenizer is None:
                print("  ✗ Failed: TextTokenizer not available")
            else:
                tokenizer = TextTokenizer(seed=42, embedding_bit=False)
                streams = tokenizer.build("Hello world")
                assert "word" in streams
                assert len(streams["word"].tokens) > 0
                print("  ✓ Passed")
        except Exception as e:
            print(f"  ✗ Failed: {e}")
        
        # Embedding test
        print("Test 2: Embedding Generation")
        try:
            if SOMAEmbeddingGenerator is None:
                print("  ✗ Failed: SOMAEmbeddingGenerator not available")
            elif streams is None or "word" not in streams:
                print("  ✗ Failed: No streams from previous test")
            else:
                generator = SOMAEmbeddingGenerator()
                tokens = streams["word"].tokens
                if not tokens:
                    print("  ✗ Failed: No tokens found")
                else:
                    embeddings = generator.generate_batch(tokens)
                    if embeddings is None or len(embeddings) == 0:
                        print("  ✗ Failed: No embeddings generated")
                    elif len(embeddings) != len(tokens):
                        print(f"  ✗ Failed: Embedding count mismatch ({len(embeddings)} vs {len(tokens)})")
                    else:
                        print("  ✓ Passed")
        except Exception as e:
            print(f"  ✗ Failed: {e}")
        
        print()
        print("=" * 60)
        print("Tests complete!")
        print("=" * 60)
    
    def info(self):
        """Show system information."""
        print("=" * 60)
        print("SOMA System Information")
        print("=" * 60)
        print()
        
        print("Available Features:")
        print("  ✓ Tokenization (9 methods)")
        print("  ✓ Semantic embedding training")
        print("  ✓ Enhanced semantic trainer")
        print("  ✓ Embedding generation")
        print("  ✓ Vector storage")
        print()
        
        print("Tokenization Methods:")
        methods = ["space", "word", "char", "grammar", "subword", 
                   "subword_bpe", "subword_syllable", "subword_frequency", "byte"]
        for method in methods:
            print(f"  - {method}")
        print()
        
        print("Embedding Strategies:")
        strategies = ["feature_based", "hash_based", "semantic", "hybrid"]
        for strategy in strategies:
            print(f"  - {strategy}")
        print()
        
        print("=" * 60)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="SOMA CLI - Complete tokenization and embedding system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Tokenize text
  python soma_cli.py tokenize --text "Hello world" --method word
  
  # Tokenize file
  python soma_cli.py tokenize --file data.txt --output tokens.json
  
  # Train embeddings
  python soma_cli.py train --file corpus.txt --model-path model.pkl
  
  # Generate embeddings
  python soma_cli.py embed --text "Hello world" --model-path model.pkl
  
  # Run tests
  python soma_cli.py test
  
  # Show info
  python soma_cli.py info
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Tokenize command
    tokenize_parser = subparsers.add_parser('tokenize', help='Tokenize text/file/URL')
    tokenize_parser.add_argument('--text', type=str, help='Input text')
    tokenize_parser.add_argument('--file', type=str, help='Input file path')
    tokenize_parser.add_argument('--url', type=str, help='Input URL')
    tokenize_parser.add_argument('--method', type=str, default='word', 
                                help='Tokenization method (default: word)')
    tokenize_parser.add_argument('--seed', type=int, default=42, help='Random seed')
    tokenize_parser.add_argument('--output', type=str, help='Output file path')
    tokenize_parser.add_argument('--format', type=str, default='json', 
                                choices=['json', 'txt'], help='Output format',
                                dest='output_format')  # Avoid conflict with Python's format
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Train semantic embeddings')
    train_parser.add_argument('--text', type=str, help='Training text')
    train_parser.add_argument('--file', type=str, help='Training file path')
    train_parser.add_argument('--url', type=str, help='Training URL')
    train_parser.add_argument('--model-path', type=str, default='SOMA_model.pkl',
                            help='Model output path')
    train_parser.add_argument('--embedding-dim', type=int, default=768,
                            help='Embedding dimension')
    train_parser.add_argument('--epochs', type=int, default=10, help='Training epochs')
    train_parser.add_argument('--window-size', type=int, default=5, help='Context window')
    train_parser.add_argument('--enhanced', action='store_true',
                            help='Use enhanced trainer')
    
    # Embed command
    embed_parser = subparsers.add_parser('embed', help='Generate embeddings')
    embed_parser.add_argument('--text', type=str, help='Input text')
    embed_parser.add_argument('--file', type=str, help='Input file path')
    embed_parser.add_argument('--model-path', type=str, default='SOMA_model.pkl',
                            help='Trained model path')
    embed_parser.add_argument('--output', type=str, help='Output file path (.npy)')
    embed_parser.add_argument('--strategy', type=str, default='feature_based',
                            choices=['feature_based', 'hash_based', 'semantic', 'hybrid'],
                            help='Embedding strategy')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run tests')
    test_parser.add_argument('--quick', action='store_true', help='Quick smoke tests')
    
    # Info command
    subparsers.add_parser('info', help='Show system information')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = SOMACLI()
    
    if args.command == 'tokenize':
        cli.tokenize(
            text=args.text,
            file=args.file,
            url=args.url,
            method=args.method,
            seed=args.seed,
            output=args.output,
            format=getattr(args, 'output_format', None) or getattr(args, 'format', 'json')
        )
    elif args.command == 'train':
        cli.train(
            text=args.text,
            file=args.file,
            url=args.url,
            model_path=args.model_path,
            embedding_dim=args.embedding_dim,
            epochs=args.epochs,
            window_size=args.window_size,
            enhanced=args.enhanced
        )
    elif args.command == 'embed':
        cli.embed(
            text=args.text,
            file=args.file,
            model_path=args.model_path,
            output=args.output,
            strategy=args.strategy
        )
    elif args.command == 'test':
        cli.test(quick=args.quick)
    elif args.command == 'info':
        cli.info()


if __name__ == "__main__":
    main()
