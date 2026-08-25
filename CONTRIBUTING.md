# Contributing to SpecuLoop

SpecuLoop is an experimental project reconstructing a lost semantic engine. Contributions are welcome.

## How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python3 wrap/tests/test_core_loop.py`
5. Submit a pull request

## What We Need

- LLM-based decomposition (replace pattern matching in `wrap/translation/decomposer.py`)
- Embedding-based scoring (replace text overlap in `wrap/drag/scorer.py`)
- Graph visualization
- Obsidian vault integration
- Tests for edge cases
- Documentation improvements

## Design Principles

- Every component should be replaceable
- Hypotheses should be labeled with confidence levels
- Prefer simple, inspectable data structures
- Semantic reversibility over character-level reversibility

## Reporting Issues

Open an issue on GitHub. Include:
- What you expected
- What happened
- Steps to reproduce
