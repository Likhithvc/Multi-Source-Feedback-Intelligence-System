"""
Main application entry point.

Orchestrates the feedback intelligence pipeline.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.pipeline import run_pipeline


if __name__ == "__main__":
    run_pipeline()