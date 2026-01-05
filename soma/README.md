# soma/ - High-Level Wrapper Module

## Overview

High-level wrapper module providing a simplified interface to the SOMA tokenization engine.

## Files

| File        | Description                                                     |
| ----------- | --------------------------------------------------------------- |
| `soma.py` | Main tokenization engine wrapper (TextTokenizationEngine class) |
| `cli.py`    | Command-line interface module                                   |
| `utils/`    | Configuration, logging, validation utilities                    |

## Usage

```python
from soma import TextTokenizationEngine

engine = TextTokenizationEngine()
result = engine.tokenize("Hello world", method="word")
```
