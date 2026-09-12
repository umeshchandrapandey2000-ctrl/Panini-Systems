"""
Panini Systems | Monte Carlo Slot Simulation Engine
===================================================
High-throughput statistical simulation, empirical RTP validation,
standard deviation, confidence intervals, and regulatory Volatility Index (VI).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import random
import math
from .combinatorics import SlotModel


# Standard 25-line definition for 3x5 reel matrix (row indices 0, 1, 2)
DEFAULT_25_PAYLINES = [
    [1, 1, 1, 1, 1],  # Line 1: Center
    [0, 0, 0, 0, 0],  # Line 2: Top
    [2, 2, 2, 2, 2],  # Line 3: Bottom
    [0, 1, 2, 1, 0],  # Line 4: V-shape down
    [2, 1, 0, 1, 2],  # Line 5: V-shape up
    [0, 0, 1, 2, 2],  # Line 6
    [2, 2, 1, 0, 0],  # Line 7
    [1, 2, 2, 2, 1],  # Line 8
    [1, 0, 0, 0, 1],  # Line 9
    [0, 1, 0, 1, 0],  # Line 10
    [2, 1, 2, 1, 2],  # Line 11
    [1, 0, 1, 0, 1],  # Line 12
    [1, 2, 1, 2, 1],  # Line 13
    [0, 1, 1, 1, 0],  # Line 14
    [2, 1, 1, 1, 2],  # Line 15
    [0, 2, 0, 2, 0],  # Line 16
    [2, 0, 2, 0, 2],  # Line 17
    [0, 0, 2, 0, 0],  # Line 18
    [2, 2, 0, 2, 2],  # Line 19
    [0, 2, 2, 2, 0],  # Line 20
    [2, 0, 0, 0, 2],  # Line 21
    [1, 1, 0, 1, 1],  # Line 22
    [1, 1, 2, 1, 1],  # Line 23
    [0, 1, 2, 2, 2],  # Line 24
    [2, 1, 0, 0, 0],  # Line 25
]


@dataclass
class SimulationResult:
    total_spins: int
    total_bet: float
    total_won: float
    empirical_rtp: float
    hit_frequency: float
    mean_payout_per_spin: float
    variance: float
    standard_deviation: float
    volatility_index_90: float
    volatility_index_95: float
    ci_90: Tuple[float, float]
    ci_95: Tuple[float, float]
    max_single_win: float
    win_distribution: Dict[str, int] = field(default_factory=dict)
    win_distribution_pct: Dict[str, float] = field(default_factory=dict)


class MonteCarloSimulator:
    """
    Simulates millions of game rounds to verify theoretical combinatorics
    and compute empirical volatility metrics conforming to GLI-11 standards.
    """

    def __init__(
        self,
        slot_model: SlotModel,
        paylines: Optional[List[List[int]]] = None,
        rows_visible: int = 3,
        random_seed: Optional[int] = None,
    ):
        self.model = slot_model
        self.rows_visible = rows_visible
        self.paylines = (
            paylines
            if paylines is not None
            else DEFAULT_25_PAYLINES[: slot_model.num_paylines]
        )
        if random_seed is not None:
            random.seed(random_seed)

    def evaluate_line_win(self, window: List[List[str]], line: List[int]) -> float:
        """
        Evaluates payout for a single payline across the visible window.
        window is indexed as window[reel_idx][row_idx].
        """
        symbols_on_line = [window[reel_idx][line[reel_idx]] for reel_idx in range(self.model.num_reels)]
        first_sym = symbols_on_line[0]

        # Determine winning symbol candidate
        candidate_sym = None
        wild = self.model.wild_symbol

        # Find first non-wild symbol
        for s in symbols_on_line:
            if s != wild:
                candidate_sym = s
                break

        if candidate_sym is None:
            # Entire line is wild!
            candidate_sym = wild

        # Count consecutive matching symbols from left
        match_count = 0
        for s in symbols_on_line:
            if s == candidate_sym or s == wild:
                match_count += 1
            else:
                break

        # Lookup in paytable
        payout = 0.0
        if candidate_sym in self.model.paytable:
            pays = self.model.paytable[candidate_sym]
            payout = pays.get(match_count, 0.0)

        # Check if pure wild pays higher
        if wild and wild in self.model.paytable:
            pure_wild_count = 0
            for s in symbols_on_line:
                if s == wild:
                    pure_wild_count += 1
                else:
                    break
            wild_pays = self.model.paytable[wild].get(pure_wild_count, 0.0)
            if wild_pays > payout:
                payout = wild_pays

        return payout

    def run_simulation(
        self, num_spins: int = 100_000, line_bet: float = 1.0
    ) -> SimulationResult:
        """
        Runs Monte Carlo simulation of `num_spins`.
        Tracks sum of payouts, sum of squares, and win tiers.
        """
        total_bet_per_spin = len(self.paylines) * line_bet
        total_bet = total_bet_per_spin * num_spins
        total_won = 0.0
        sum_sq = 0.0
        winning_spins = 0
        max_win = 0.0

        distribution_buckets = {
            "0x (Loss)": 0,
            "(0x, 1x]": 0,
            "(1x, 2x]": 0,
            "(2x, 5x]": 0,
            "(5x, 20x]": 0,
            "(20x, 50x]": 0,
            "(50x, 100x]": 0,
            "100x+": 0,
        }

        reels = self.model.reel_strips
        lengths = self.model.reel_lengths
        num_reels = self.model.num_reels
        rows = self.rows_visible

        for _ in range(num_spins):
            # Spin reels: pick random stop index for each reel
            window = []
            for r in range(num_reels):
                l = lengths[r]
                stop = random.randint(0, l - 1)
                # Extract visible window of size `rows`
                col = [reels[r][(stop + row) % l] for row in range(rows)]
                window.append(col)

            # Evaluate paylines
            spin_payout = 0.0
            for line in self.paylines:
                payout_units = self.evaluate_line_win(window, line)
                spin_payout += payout_units * line_bet

            total_won += spin_payout
            sum_sq += spin_payout * spin_payout

            if spin_payout > 0:
                winning_spins += 1
                if spin_payout > max_win:
                    max_win = spin_payout

            # Bucket win multiple relative to total bet
            multiple = spin_payout / total_bet_per_spin if total_bet_per_spin > 0 else 0
            if multiple == 0:
                distribution_buckets["0x (Loss)"] += 1
            elif multiple <= 1.0:
                distribution_buckets["(0x, 1x]"] += 1
            elif multiple <= 2.0:
                distribution_buckets["(1x, 2x]"] += 1
            elif multiple <= 5.0:
                distribution_buckets["(2x, 5x]"] += 1
            elif multiple <= 20.0:
                distribution_buckets["(5x, 20x]"] += 1
            elif multiple <= 50.0:
                distribution_buckets["(20x, 50x]"] += 1
            elif multiple <= 100.0:
                distribution_buckets["(50x, 100x]"] += 1
            else:
                distribution_buckets["100x+"] += 1

        empirical_rtp = (total_won / total_bet) if total_bet > 0 else 0.0
        hit_freq = (winning_spins / num_spins) if num_spins > 0 else 0.0
        mean_payout = total_won / num_spins
        variance = (sum_sq / num_spins) - (mean_payout * mean_payout)
        variance = max(0.0, variance)
        std_dev = math.sqrt(variance)

        # Standard deviation normalized by total bet per spin
        normalized_std_dev = (std_dev / total_bet_per_spin) if total_bet_per_spin > 0 else 0.0
        std_err_rtp = (normalized_std_dev / math.sqrt(num_spins)) if num_spins > 0 else 0.0

        # Confidence intervals for RTP
        ci_90 = (empirical_rtp - 1.6449 * std_err_rtp, empirical_rtp + 1.6449 * std_err_rtp)
        ci_95 = (empirical_rtp - 1.9599 * std_err_rtp, empirical_rtp + 1.9599 * std_err_rtp)

        # Volatility Index (Standard gaming metric)
        vi_90 = 1.6449 * normalized_std_dev
        vi_95 = 1.9599 * normalized_std_dev

        pct_buckets = {
            k: (v / num_spins) * 100.0 for k, v in distribution_buckets.items()
        }

        return SimulationResult(
            total_spins=num_spins,
            total_bet=total_bet,
            total_won=total_won,
            empirical_rtp=empirical_rtp,
            hit_frequency=hit_freq,
            mean_payout_per_spin=mean_payout,
            variance=variance,
            standard_deviation=normalized_std_dev,
            volatility_index_90=vi_90,
            volatility_index_95=vi_95,
            ci_90=ci_90,
            ci_95=ci_95,
            max_single_win=max_win / total_bet_per_spin if total_bet_per_spin > 0 else 0,
            win_distribution=distribution_buckets,
            win_distribution_pct=pct_buckets,
        )
