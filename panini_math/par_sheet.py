"""
Panini Systems | PAR Sheet (Probability Accounting Report) Generator
===================================================================
Generates industry-standard PAR sheets in CSV, JSON, and Markdown formats
ready for studio integration and GLI-11/19 certification submissions.
"""

from typing import Dict, List, Optional
import csv
import io
import json
from .combinatorics import SlotModel, TheoreticalEvaluation


class PARSheetGenerator:
    """
    Generates standardized PAR sheets from mathematical slot specifications.
    """

    def __init__(self, slot_model: SlotModel, evaluation: Optional[TheoreticalEvaluation] = None):
        self.model = slot_model
        self.eval = evaluation if evaluation is not None else slot_model.evaluate_payline_combinatorics()

    def determine_volatility_tier(self, line_hit_freq: float, line_rtp: float) -> str:
        """Classifies game volatility based on hit frequency and RTP dispersion."""
        if line_hit_freq > 0.35:
            return "Low"
        elif line_hit_freq > 0.25:
            return "Medium"
        elif line_hit_freq > 0.18:
            return "High"
        else:
            return "Very High / Extreme"

    def to_dict(self) -> Dict:
        """Exports PAR sheet data structure as dictionary."""
        volatility = self.determine_volatility_tier(self.eval.line_hit_frequency, self.eval.total_rtp)

        details_list = []
        for d in self.eval.details:
            details_list.append({
                "symbol": d.symbol,
                "kind": f"{d.kind}x",
                "combinations": d.combinations,
                "payout": d.payout,
                "total_return": d.total_return,
                "probability": round(d.probability, 8),
                "rtp_contribution_pct": round(d.rtp_contribution * 100.0, 4),
            })

        reel_composition = {}
        for sym, counts in self.model.symbol_counts.items():
            reel_composition[sym] = {f"Reel_{i+1}": counts[i] for i in range(self.model.num_reels)}

        return {
            "metadata": {
                "game_title": self.model.name,
                "provider": "Panini Systems Mathematical Consulting",
                "num_reels": self.model.num_reels,
                "num_paylines": self.model.num_paylines,
                "reel_lengths": self.model.reel_lengths,
                "total_combinations_cycle": self.model.total_cycle,
                "volatility_class": volatility,
            },
            "theoretical_performance": {
                "theoretical_rtp_pct": round(self.eval.total_rtp * 100.0, 4),
                "line_hit_frequency_pct": round(self.eval.line_hit_frequency * 100.0, 4),
                "total_winning_combinations": self.eval.total_combinations_winning,
            },
            "reel_symbol_counts": reel_composition,
            "paytable_analysis": details_list,
        }

    def to_csv(self) -> str:
        """Generates a comma-separated PAR sheet string compatible with Excel."""
        out = io.StringIO()
        writer = csv.writer(out)

        # Header
        writer.writerow(["PANINI SYSTEMS - PROBABILITY ACCOUNTING REPORT (PAR SHEET)"])
        writer.writerow(["Game Title", self.model.name])
        writer.writerow(["Number of Paylines", self.model.num_paylines])
        writer.writerow(["Total Reel Cycle Combinations", self.model.total_cycle])
        writer.writerow(["Theoretical Base RTP", f"{self.eval.total_rtp * 100.0:.4f}%"])
        writer.writerow(["Single Line Hit Frequency", f"{self.eval.line_hit_frequency * 100.0:.4f}%"])
        writer.writerow(["Volatility Tier", self.determine_volatility_tier(self.eval.line_hit_frequency, self.eval.total_rtp)])
        writer.writerow([])

        # Reel Strip Composition
        reel_headers = ["Symbol"] + [f"Reel {i+1}" for i in range(self.model.num_reels)] + ["Total"]
        writer.writerow(reel_headers)
        for sym, counts in self.model.symbol_counts.items():
            row = [sym] + counts + [sum(counts)]
            writer.writerow(row)
        writer.writerow(["Reel Lengths"] + self.model.reel_lengths + [sum(self.model.reel_lengths)])
        writer.writerow([])

        # Paytable & Combinatorial Return
        writer.writerow(["Symbol", "Kind", "Combinations", "Payout (x Line Bet)", "Probability", "Return Contribution %"])
        for d in self.eval.details:
            writer.writerow([
                d.symbol,
                f"{d.kind} of a kind",
                d.combinations,
                d.payout,
                f"{d.probability:.8f}",
                f"{d.rtp_contribution * 100.0:.4f}%",
            ])

        writer.writerow([])
        writer.writerow(["TOTAL COMBINATORIAL RETURN", "", self.eval.total_combinations_winning, "", "", f"{self.eval.total_rtp * 100.0:.4f}%"])

        return out.getvalue()

    def to_markdown(self) -> str:
        """Generates a GitHub-flavored markdown table PAR summary."""
        volatility = self.determine_volatility_tier(self.eval.line_hit_frequency, self.eval.total_rtp)
        md = []
        md.append(f"### PAR Sheet: {self.model.name}\n")
        md.append(f"| Metric | Value |")
        md.append(f"|---|---|")
        md.append(f"| **Active Paylines** | {self.model.num_paylines} |")
        md.append(f"| **Reel Dimensions** | {self.model.num_reels} Reels (Lengths: {self.model.reel_lengths}) |")
        md.append(f"| **Total Combinatorial Cycle** | {self.model.total_cycle:,} |")
        md.append(f"| **Theoretical RTP** | **{self.eval.total_rtp * 100.0:.2f}%** |")
        md.append(f"| **Line Hit Frequency** | {self.eval.line_hit_frequency * 100.0:.2f}% |")
        md.append(f"| **Estimated Volatility** | **{volatility}** |\n")

        md.append("#### Paytable Return Breakdown\n")
        md.append("| Symbol | Match | Combinations | Payout | Probability | Return (RTP %) |")
        md.append("|---|---|---|---|---|---|")
        for d in self.eval.details:
            md.append(
                f"| `{d.symbol}` | {d.kind}x | {d.combinations:,} | {d.payout:,.1f}x | {d.probability:.6f} | {d.rtp_contribution * 100.0:.3f}% |"
            )

        return "\n".join(md)
