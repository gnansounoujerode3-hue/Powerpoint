"""Moteur du Pack 1500 : catalogue, scènes vectorielles et rendus PowerPoint/SVG."""
import sys
from pathlib import Path

# Les modules internes s'importent entre eux par leur nom court.
sys.path.insert(0, str(Path(__file__).resolve().parent))

__version__ = "1.0.0"
