"""
Panini Systems | Gacha Probability & Markov Chain Economy Engine
================================================================
Mathematical modeling of gacha drop rates, soft/hard pity distributions,
absorbing Markov chains, and player spend percentiles.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import math


@dataclass
class GachaDistributionMetrics:
    base_rate: float
    soft_pity_start: int
    hard_pity: int
    expected_pulls_single: float
    consolidated_rate: float
    expected_pulls_featured_5050: float
    median_pulls: int
    percentile_75: int
    percentile_90: int
    percentile_95: int
    percentile_99: int
    pull_probabilities: List[float]  # PMF: P(X = k)
    cumulative_probabilities: List[float]  # CDF: P(X <= k)


class GachaPityModel:
    """
    Exact analytical model for gacha drop rates with pity systems.
    """

    def __init__(
        self,
        base_rate: float = 0.006,  # 0.6% standard base rate
        soft_pity_start: int = 74,
        hard_pity: int = 90,
        soft_pity_increment: float = 0.06,  # +6% per pull after soft pity start
        featured_probability: float = 0.50,  # 50% chance of featured on 5-star
    ):
        self.base_rate = base_rate
        self.soft_pity_start = soft_pity_start
        self.hard_pity = hard_pity
        self.soft_pity_increment = soft_pity_increment
        self.featured_probability = featured_probability

    def get_pull_rate(self, pull_number: int) -> float:
        """Returns conditional probability P(Win on pull k | Failed pulls 1..k-1)."""
        if pull_number < self.soft_pity_start:
            return self.base_rate
        elif pull_number >= self.hard_pity:
            return 1.0
        else:
            steps_into_soft = pull_number - self.soft_pity_start + 1
            rate = self.base_rate + (steps_into_soft * self.soft_pity_increment)
            return min(1.0, rate)

    def calculate_distribution(self) -> GachaDistributionMetrics:
        """
        Calculates exact Probability Mass Function (PMF) and Cumulative
        Distribution Function (CDF) for acquiring a top-tier item.
        """
        pmf: List[float] = [0.0] * (self.hard_pity + 1)
        cdf: List[float] = [0.0] * (self.hard_pity + 1)

        prob_survival = 1.0  # P(No hit up to step k-1)
        expected_pulls = 0.0

        for k in range(1, self.hard_pity + 1):
            p_k = self.get_pull_rate(k)
            # P(X = k) = P(Fail 1..k-1) * p_k
            prob_exact_hit = prob_survival * p_k
            pmf[k] = prob_exact_hit
            cdf[k] = cdf[k - 1] + prob_exact_hit
            expected_pulls += k * prob_exact_hit
            prob_survival *= (1.0 - p_k)

        # Force normalization at hard pity if floating precision leaves minute residual
        if cdf[self.hard_pity] < 1.0:
            pmf[self.hard_pity] += (1.0 - cdf[self.hard_pity])
            cdf[self.hard_pity] = 1.0

        # Consolidated rate = 1 / E[pulls]
        consolidated_rate = 1.0 / expected_pulls if expected_pulls > 0 else 0.0

        # With 50/50 mechanics (guaranteed next if first is lost):
        # E[Pulls to Featured] = E[X] * (0.5 * 1 + 0.5 * 2) = 1.5 * E[X]
        expected_featured = expected_pulls * (1.0 + (1.0 - self.featured_probability))

        # Calculate percentiles from CDF
        def find_percentile(target: float) -> int:
            for k in range(1, self.hard_pity + 1):
                if cdf[k] >= target:
                    return k
            return self.hard_pity

        median = find_percentile(0.50)
        p75 = find_percentile(0.75)
        p90 = find_percentile(0.90)
        p95 = find_percentile(0.95)
        p99 = find_percentile(0.99)

        return GachaDistributionMetrics(
            base_rate=self.base_rate,
            soft_pity_start=self.soft_pity_start,
            hard_pity=self.hard_pity,
            expected_pulls_single=expected_pulls,
            consolidated_rate=consolidated_rate,
            expected_pulls_featured_5050=expected_featured,
            median_pulls=median,
            percentile_75=p75,
            percentile_90=p90,
            percentile_95=p95,
            percentile_99=p99,
            pull_probabilities=pmf,
            cumulative_probabilities=cdf,
        )
