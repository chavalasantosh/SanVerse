"""
SOMA SLM - Neural Transformer-Based Small Language Model

This is a REAL neural network SLM using transformer architecture.
NOT rule-based - uses multi-head attention, feed-forward networks, embeddings.

Usage:
    from soma_slm import somaSLM
    
    slm = SOMASLM()
    slm.load_facts(["Python is a language", "Python is popular"])
    result = slm.generate("What is Python?")
    print(result)
"""

from soma_cognitive.slm import (
    SOMAConstrainedSLM,
    SOMASequenceConfig,
)


class SOMASLM:
    """
    Neural Transformer-Based SOMA Small Language Model.
    
    This uses REAL neural networks:
    - Multi-head attention (transformer)
    - Feed-forward networks
    - Embeddings
    - Positional encoding
    
    NOT rule-based - this is a proper neural language model.
    
    Example:
        slm = SOMASLM()
        slm.load_facts(["Python is a language"])
        print(slm.generate("What is Python?"))
    """
    
    def __init__(self, use_tiny=False):
        """
        Create a new neural SLM.
        
        Args:
            use_tiny: If True, uses smaller model (faster, less memory)
        """
        if use_tiny:
            # Tiny model for low-resource
            config = SOMASequenceConfig(
                vocab_size=5000,
                d_model=64,
                n_layers=2,
                n_heads=2,
                d_ff=256,
            )
        else:
            # Standard model
            config = SOMASequenceConfig(
                vocab_size=10000,
                d_model=128,
                n_layers=2,
                n_heads=4,
                d_ff=512,
            )
        
        self._slm = SOMAConstrainedSLM(config)
        self._facts = []
    
    def load_facts(self, facts):
        """
        Load facts into the SLM and train the neural network.
        
        Args:
            facts: List of fact strings
        """
        self._facts = facts
        self._slm.load_knowledge(facts)
    
    def generate(self, query, max_length=50, temperature=1.0):
        """
        Generate a response using the neural transformer.
        
        Args:
            query: The question or prompt
            max_length: Maximum response length (default: 50)
            temperature: Sampling temperature (default: 1.0)
        
        Returns:
            Generated text string
        """
        # Update decoder config
        self._slm.decoder.config.temperature = temperature
        self._slm.decoder.config.top_k = min(50, max_length)
        
        # Generate using neural transformer
        text, metadata = self._slm.generate(query, max_length=max_length)
        return text
    
    def add_fact(self, fact):
        """
        Add a single fact.
        
        Args:
            fact: Fact string to add
        """
        self._facts.append(fact)
        self._slm.load_knowledge(self._facts)
    
    def clear(self):
        """Clear all facts."""
        self._facts = []
        # Recreate with same config
        config = self._slm.sequence_optimizer.config
        self._slm = SOMAConstrainedSLM(config)
    
    def get_stats(self):
        """Get statistics about the neural model."""
        stats = self._slm.engine.get_stats()
        # Add neural network stats
        optimizer = self._slm.sequence_optimizer
        stats['neural_model'] = {
            'parameters': optimizer.count_parameters(),
            'd_model': optimizer.config.d_model,
            'n_layers': optimizer.config.n_layers,
            'n_heads': optimizer.config.n_heads,
            'vocab_size': optimizer.config.vocab_size,
        }
        return stats
    
    def train(self, epochs=10, learning_rate=0.001):
        """
        Train the neural network on loaded facts.
        
        Args:
            epochs: Number of training epochs
            learning_rate: Learning rate for training
        """
        from soma_cognitive.slm import SLMTrainer, TrainingConfig
        
        trainer = SLMTrainer(
            transformer=self._slm.sequence_optimizer,
            config=TrainingConfig(
                learning_rate=learning_rate,
                batch_size=4,
                epochs=epochs,
            )
        )
        
        # Generate training data from facts
        from soma_cognitive.slm import create_training_data
        training_data = create_training_data(self._facts)
        
        # Train
        trainer.train(training_data, validation_data=training_data[:len(training_data)//5])


# Make it even simpler - just a function
def create_slm():
    """
    Create a new SOMA SLM.
    
    Returns:
        SOMASLM instance
    
    Example:
        slm = create_slm()
        slm.load_facts(["Python is a language"])
        print(slm.generate("What is Python?"))
    """
    return SOMASLM()


# For direct import
__all__ = ['SOMASLM', 'create_slm']
