"""
Example: Using SanTOK with Pretrained Transformer Models

This example demonstrates how to use SanTOK tokenization with pretrained
models (BERT, GPT, T5, etc.) despite vocabulary ID mismatches.

The critical issue: SanTOK's IDs don't match pretrained model vocabularies.
Solution: Use vocabulary adapter to map SanTOK tokens to model vocabulary IDs.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.core_tokenizer import run_once, TextTokenizer
from src.integration.vocabulary_adapter import (
    SanTOKToModelConverter,
    VocabularyAdapter,
    quick_convert_santok_to_model_ids
)

# Check if transformers is available
try:
    from transformers import AutoModel, AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("[WARNING]  transformers library not available.")
    print("   Install with: pip install transformers torch")
    print("   Continuing with vocabulary mapping examples only...\n")


def example_1_basic_mapping():
    """Example 1: Basic SanTOK → Model ID mapping"""
    print("=" * 60)
    print("Example 1: Basic SanTOK → Model ID Mapping")
    print("=" * 60)
    
    text = "Hello world! SanTOK provides superior tokenization."
    
    # Step 1: Tokenize with SanTOK
    print(f"\n1. Tokenizing with SanTOK:")
    print(f"   Text: {text}")
    santok_result = run_once(text, seed=42, embedding_bit=False)
    
    # Extract word tokens
    word_tokens = [rec["text"] for rec in santok_result["word"]["records"]]
    print(f"   SanTOK tokens: {word_tokens}")
    
    # Step 2: Map to model vocabulary IDs
    print(f"\n2. Mapping to BERT vocabulary IDs:")
    model_ids = quick_convert_santok_to_model_ids(word_tokens, model_name="bert-base-uncased")
    print(f"   Model IDs: {model_ids}")
    
    # Decode back to verify
    if TRANSFORMERS_AVAILABLE:
        bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        decoded = bert_tokenizer.decode(model_ids)
        print(f"   Decoded: {decoded}")
    
    print()


def example_2_full_conversion():
    """Example 2: Full conversion with metadata preservation"""
    print("=" * 60)
    print("Example 2: Full Conversion with Metadata Preservation")
    print("=" * 60)
    
    text = "The quick brown fox jumps over the lazy dog."
    
    # Tokenize with SanTOK
    print(f"\n1. SanTOK Tokenization:")
    print(f"   Text: {text}")
    santok_result = run_once(text, seed=42, embedding_bit=False)
    
    word_data = santok_result["word"]
    print(f"   Tokens: {[rec['text'] for rec in word_data['records']]}")
    print(f"   Frontend digits: {word_data['digits']}")
    print(f"   Backend scaled: {word_data['scaled']}")
    
    # Convert to model format
    print(f"\n2. Converting to BERT format:")
    converter = SanTOKToModelConverter(model_name="bert-base-uncased")
    converted = converter.convert_santok_result(santok_result, tokenizer_type="word")
    
    print(f"   Model input IDs: {converted['model_input_ids']}")
    print(f"   Model tokens: {converted['model_tokens']}")
    print(f"   SanTOK tokens preserved: {converted['santok_tokens']}")
    print(f"   SanTOK frontend digits preserved: {converted['santok_frontend_digits']}")
    
    # Show token mapping
    print(f"\n3. Token Mapping (SanTOK index → Model indices):")
    for santok_idx, model_indices in converted['token_mapping'].items():
        santok_token = converted['santok_tokens'][santok_idx]
        model_tokens = [converted['model_tokens'][mid] for mid in model_indices]
        print(f"   SanTOK[{santok_idx}] '{santok_token}' → Model{model_indices} {model_tokens}")
    
    print()


def example_3_model_inference():
    """Example 3: Using with pretrained model for inference"""
    if not TRANSFORMERS_AVAILABLE:
        print("=" * 60)
        print("Example 3: Model Inference (Skipped - transformers not available)")
        print("=" * 60)
        print("   Install transformers and torch to run this example.\n")
        return
    
    print("=" * 60)
    print("Example 3: Using SanTOK with Pretrained Model")
    print("=" * 60)
    
    text = "SanTOK solves the vocabulary compatibility issue."
    
    # Tokenize with SanTOK
    print(f"\n1. Tokenizing with SanTOK:")
    print(f"   Text: {text}")
    santok_result = run_once(text, seed=42, embedding_bit=False)
    
    # Convert to model format
    print(f"\n2. Preparing for model inference:")
    converter = SanTOKToModelConverter(model_name="bert-base-uncased")
    model_inputs = converter.prepare_for_inference(
        santok_result,
        tokenizer_type="word",
        return_tensors="pt"
    )
    
    print(f"   Input IDs shape: {model_inputs['input_ids'].shape}")
    print(f"   Attention mask shape: {model_inputs['attention_mask'].shape}")
    
    # Load model and run inference
    print(f"\n3. Running model inference:")
    model = AutoModel.from_pretrained("bert-base-uncased")
    model.eval()
    
    import torch
    with torch.no_grad():
        outputs = model(**model_inputs)
    
    print(f"   Output shape: {outputs.last_hidden_state.shape}")
    print(f"   [OK] Successfully used SanTOK tokenization with pretrained BERT!")
    
    print()


def example_4_multiple_models():
    """Example 4: Using SanTOK with different models"""
    print("=" * 60)
    print("Example 4: SanTOK with Different Pretrained Models")
    print("=" * 60)
    
    text = "SanTOK works with any HuggingFace model."
    
    # Tokenize with SanTOK
    santok_result = run_once(text, seed=42, embedding_bit=False)
    tokens = [rec["text"] for rec in santok_result["word"]["records"]]
    
    models_to_test = [
        "bert-base-uncased",
        "distilbert-base-uncased",
    ]
    
    if TRANSFORMERS_AVAILABLE:
        models_to_test.extend(["gpt2", "roberta-base"])
    
    print(f"\nText: {text}")
    print(f"SanTOK tokens: {tokens}\n")
    
    for model_name in models_to_test:
        try:
            print(f"Model: {model_name}")
            adapter = VocabularyAdapter(model_name)
            result = adapter.map_santok_tokens_to_model_ids(tokens)
            print(f"  Vocab size: {result['vocab_size']}")
            print(f"  Input IDs: {result['input_ids']}")
            if TRANSFORMERS_AVAILABLE:
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                decoded = tokenizer.decode(result['input_ids'])
                print(f"  Decoded: {decoded}")
            print()
        except Exception as e:
            print(f"  [WARNING]  Error: {e}\n")


def example_5_tokenization_strategies():
    """Example 5: Comparing different SanTOK tokenization strategies"""
    print("=" * 60)
    print("Example 5: Different Tokenization Strategies")
    print("=" * 60)
    
    text = "Subword tokenization splits words."
    
    print(f"\nText: {text}\n")
    
    strategies = ["word", "char", "subword_bpe"]
    
    for strategy in strategies:
        print(f"Strategy: {strategy}")
        santok_result = run_once(text, seed=42, embedding_bit=False)
        
        if strategy in santok_result:
            tokens = [rec["text"] for rec in santok_result[strategy]["records"]]
            print(f"  SanTOK tokens: {tokens}")
            
            # Convert to BERT IDs
            model_ids = quick_convert_santok_to_model_ids(
                tokens, 
                model_name="bert-base-uncased"
            )
            print(f"  BERT IDs: {model_ids}")
            print()
        else:
            print(f"  [WARNING]  Strategy '{strategy}' not available\n")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("SanTOK ↔ Pretrained Models Integration Examples")
    print("=" * 60)
    print("\nThis demonstrates how to use SanTOK tokenization with")
    print("pretrained transformer models despite vocabulary ID mismatches.\n")
    
    try:
        example_1_basic_mapping()
        example_2_full_conversion()
        example_3_model_inference()
        example_4_multiple_models()
        example_5_tokenization_strategies()
        
        print("=" * 60)
        print("[OK] All examples completed!")
        print("=" * 60)
        print("\nKey Takeaways:")
        print("1. SanTOK tokenizes text into token strings")
        print("2. Vocabulary adapter maps token strings to model vocabulary IDs")
        print("3. Model IDs can be used with pretrained models")
        print("4. SanTOK metadata (digits, backend numbers) is preserved")
        print("\nSee docs/VOCABULARY_COMPATIBILITY_ISSUE.md for details.\n")
        
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
