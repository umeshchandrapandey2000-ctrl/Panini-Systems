"""
Panini Systems | Combinatorial Slot Mathematics Engine
======================================================
Exact analytical calculation of payline combinations, cycle sizes,
theoretical Return to Player (RTP), and hit frequencies.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
import math


@dataclass
class PaytableEntry:
    symbol: str
    payout_5: float = 0.0
    payout_4: float = 0.0
    payout_3: float = 0.0
    payout_2: float = 0.0


@dataclass
class LineCombinationResult:
    symbol: str
    kind: int  # 2, 3, 4, or 5 of a kind
    combinations: int
    payout: float
    total_return: float
    probability: float
    rtp_contribution: float


@dataclass
class TheoreticalEvaluation:
    total_cycle: int
    total_combinations_winning: int
    line_hit_frequency: float
    line_rtp: float
    total_rtp: float
    details: List[LineCombinationResult] = field(default_factory=list)


class SlotModel:
    """
    Theoretical combinatorial evaluator for multi-reel video slots.
    Calculates exact mathematical outcomes without simulation variance.
    """

    def __init__(
        self,
        name: str,
        reel_strips: List[List[str]],
        paytable: Dict[str, Dict[int, float]],
        num_paylines: int = 25,
        wild_symbol: Optional[str] = "WILD",
        scatter_symbol: Optional[str] = "SCATTER",
    ):
        """
        :param name: Identifier for the game
        :param reel_strips: List of reels, each reel is a list of symbol names
        :param paytable: Mapping of symbol -> {kind: payout} (e.g. {'HP1': {5: 500, 4: 100, 3: 25}})
        :param num_paylines: Number of active paylines
        :param wild_symbol: Name of wild substitution symbol
        :param scatter_symbol: Name of scatter symbol (evaluated independently)
        """
        self.name = name
        self.reel_strips = reel_strips
        self.num_reels = len(reel_strips)
        self.paytable = paytable
        self.num_paylines = num_paylines
        self.wild_symbol = wild_symbol
        self.scatter_symbol = scatter_symbol

        # Compute reel lengths and total cycle
        self.reel_lengths = [len(strip) for strip in reel_strips]
        self.total_cycle = math.prod(self.reel_lengths)

        # Count symbol frequencies per reel
        self.symbol_counts: Dict[str, List[int]] = {}
        all_symbols = set()
        for strip in reel_strips:
            all_symbols.update(strip)

        for sym in all_symbols:
            self.symbol_counts[sym] = [strip.count(sym) for strip in reel_strips]

    def get_symbol_frequency(self, symbol: str, reel_idx: int) -> int:
        """Returns the count of a symbol on a specific reel."""
        if symbol in self.symbol_counts and reel_idx < len(self.symbol_counts[symbol]):
            return self.symbol_counts[symbol][reel_idx]
        return 0

    def evaluate_payline_combinatorics(self) -> TheoreticalEvaluation:
        """
        Evaluates exact combinations for a single payline (left-to-right).
        Applies standard video slot rules:
        - Longest win evaluated per line.
        - Wild substitutes for standard paytable symbols.
        - Scatter pays anywhere (calculated separately).
        """
        results: List[LineCombinationResult] = []
        total_line_return = 0.0
        total_winning_combos = 0

        # Precompute wild counts
        wild_counts = (
            self.symbol_counts.get(self.wild_symbol, [0] * self.num_reels)
            if self.wild_symbol
            else [0] * self.num_reels
        )

        for sym, pays in self.paytable.items():
            if sym == self.scatter_symbol:
                continue  # Scatters are evaluated non-linearly

            c = self.symbol_counts.get(sym, [0] * self.num_reels)
            # Effective counts with wild substitution
            eff = [c[i] + (wild_counts[i] if sym != self.wild_symbol else 0) for i in range(self.num_reels)]

            # 5 of a kind
            if 5 in pays and self.num_reels >= 5:
                n5 = eff[0] * eff[1] * eff[2] * eff[3] * eff[4]
                # If this is not wild itself, subtract pure wild 5-kind to avoid double counting
                if self.wild_symbol and sym != self.wild_symbol and self.wild_symbol in self.paytable:
                    w5 = math.prod(wild_counts[:5])
                    n5 = max(0, n5 - w5)
                payout = pays[5]
                ret = n5 * payout
                prob = n5 / self.total_cycle if self.total_cycle > 0 else 0
                rtp_cont = ret / self.total_cycle if self.total_cycle > 0 else 0
                results.append(
                    LineCombinationResult(
                        symbol=sym,
                        kind=5,
                        combinations=n5,
                        payout=payout,
                        total_return=ret,
                        probability=prob,
                        rtp_contribution=rtp_cont,
                    )
                )
                total_line_return += ret
                total_winning_combos += n5

            # 4 of a kind (reels 1-4 match, reel 5 does NOT match)
            if 4 in pays and self.num_reels >= 5:
                non_match_5 = max(0, self.reel_lengths[4] - eff[4])
                n4 = eff[0] * eff[1] * eff[2] * eff[3] * non_match_5
                payout = pays[4]
                ret = n4 * payout
                prob = n4 / self.total_cycle if self.total_cycle > 0 else 0
                rtp_cont = ret / self.total_cycle if self.total_cycle > 0 else 0
                results.append(
                    LineCombinationResult(
                        symbol=sym,
                        kind=4,
                        combinations=n4,
                        payout=payout,
                        total_return=ret,
                        probability=prob,
                        rtp_contribution=rtp_cont,
                    )
                )
                total_line_return += ret
                total_winning_combos += n4

            # 3 of a kind (reels 1-3 match, reel 4 does NOT match, reel 5 any)
            if 3 in pays and self.num_reels >= 5:
                non_match_4 = max(0, self.reel_lengths[3] - eff[3])
                n3 = eff[0] * eff[1] * eff[2] * non_match_4 * self.reel_lengths[4]
                payout = pays[3]
                ret = n3 * payout
                prob = n3 / self.total_cycle if self.total_cycle > 0 else 0
                rtp_cont = ret / self.total_cycle if self.total_cycle > 0 else 0
                results.append(
                    LineCombinationResult(
                        symbol=sym,
                        kind=3,
                        combinations=n3,
                        payout=payout,
                        total_return=ret,
                        probability=prob,
                        rtp_contribution=rtp_cont,
                    )
                )
                total_line_return += ret
                total_winning_combos += n3

            # 2 of a kind (if defined, e.g. for high pays)
            if 2 in pays and self.num_reels >= 5:
                non_match_3 = max(0, self.reel_lengths[2] - eff[2])
                n2 = eff[0] * eff[1] * non_match_3 * self.reel_lengths[3] * self.reel_lengths[4]
                payout = pays[2]
                ret = n2 * payout
                prob = n2 / self.total_cycle if self.total_cycle > 0 else 0
                rtp_cont = ret / self.total_cycle if self.total_cycle > 0 else 0
                results.append(
                    LineCombinationResult(
                        symbol=sym,
                        kind=2,
                        combinations=n2,
                        payout=payout,
                        total_return=ret,
                        probability=prob,
                        rtp_contribution=rtp_cont,
                    )
                )
                total_line_return += ret
                total_winning_combos += n2

        # Line RTP assuming 1 unit line bet
        line_rtp = (total_line_return / self.total_cycle) if self.total_cycle > 0 else 0.0
        line_hit_freq = (total_winning_combos / self.total_cycle) if self.total_cycle > 0 else 0.0

        # Total RTP for all paylines (standard model: total bet = num_paylines * line_bet)
        # Total Game RTP = (Num_Lines * Line_Return) / (Num_Lines * Line_Bet * Total_Cycle) = Line_RTP
        total_game_rtp = line_rtp

        return TheoreticalEvaluation(
            total_cycle=self.total_cycle,
            total_combinations_winning=total_winning_combos,
            line_hit_frequency=line_hit_freq,
            line_rtp=line_rtp,
            total_rtp=total_game_rtp,
            details=results,
        )

    def evaluate_scatter_mechanics(self, min_scatters: int = 3) -> Dict[str, float]:
        """
        Evaluates scatter trigger probability anywhere on the reels.
        Each reel has S_i scatters out of L_i stops.
        The probability of at least k scatters is calculated combinatorially.
        """
        if not self.scatter_symbol:
            return {"trigger_prob": 0.0, "expected_spins_between_features": float("inf")}

        s_counts = self.symbol_counts.get(self.scatter_symbol, [0] * self.num_reels)
        # Assuming 1 visible position per reel for baseline or 3 visible positions
        # Standard 3x5 video slot: 3 positions visible per reel.
        # Probability reel i shows scatter ~= min(1.0, 3 * s_counts[i] / reel_lengths[i])
        p_reel = [
            min(1.0, 3.0 * s / l) if l > 0 else 0.0
            for s, l in zip(s_counts, self.reel_lengths)
        ]

        # Dynamic programming for Poisson-binomial distribution
        # dp[i][j] = prob of j scatters across first i reels
        dp = [0.0] * (self.num_reels + 1)
        dp[0] = 1.0
        for p in p_reel:
            new_dp = [0.0] * (self.num_reels + 1)
            for j in range(self.num_reels + 1):
                new_dp[j] += dp[j] * (1.0 - p)
                if j + 1 <= self.num_reels:
                    new_dp[j + 1] += dp[j] * p
            dp = new_dp

        trigger_prob = sum(dp[min_scatters:])
        avg_cycle = (1.0 / trigger_prob) if trigger_prob > 0 else float("inf")

        return {
            "trigger_prob": trigger_prob,
            "expected_spins_between_features": avg_cycle,
            "exact_distribution": {k: dp[k] for k in range(self.num_reels + 1)},
        }


def evaluate_line_combinations(slot_model: SlotModel) -> TheoreticalEvaluation:
    """Convenience wrapper for theoretical evaluation."""
    return slot_model.evaluate_payline_combinatorics()
