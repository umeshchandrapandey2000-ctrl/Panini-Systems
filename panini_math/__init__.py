"""
Panini Systems | Applied Mathematics & Game Math Computational Engine
=====================================================================

A high-precision mathematical suite for slot game mathematics,
combinatorial RTP analysis, Monte Carlo simulation, volatility profiling,
and probabilistic economy modeling.
"""

from .combinatorics import SlotModel, evaluate_line_combinations
from .monte_carlo import MonteCarloSimulator, SimulationResult
from .par_sheet import PARSheetGenerator
from .gacha_markov import GachaPityModel

__version__ = "1.0.0"
__author__ = "Panini Systems"
__all__ = [
    "SlotModel",
    "evaluate_line_combinations",
    "MonteCarloSimulator",
    "SimulationResult",
    "PARSheetGenerator",
    "GachaPityModel",
]
