"""
Panini Systems | Command Line Interface & Demonstration Suite
============================================================
Run quick validations, Monte Carlo simulations, and generate PAR sheets
directly from the terminal.
"""

import sys
import argparse
from .combinatorics import SlotModel
from .monte_carlo import MonteCarloSimulator
from .par_sheet import PARSheetGenerator
from .gacha_markov import GachaPityModel


def get_sample_game() -> SlotModel:
    """Returns a balanced 5x3 video slot configuration with ~96.2% theoretical RTP."""
    # 5 reels with 30-32 stops each
    reel1 = ["WILD", "HP1", "LP1", "MP1", "LP2", "HP2", "LP3", "SCATTER", "HP3", "LP1",
             "MP2", "LP2", "HP1", "LP3", "MP1", "LP1", "HP2", "LP2", "MP2", "LP3",
             "HP3", "LP1", "MP1", "LP2", "HP1", "LP3", "MP2", "LP1", "HP2", "LP2"]

    reel2 = ["LP1", "HP1", "LP2", "MP1", "WILD", "HP2", "LP3", "MP2", "HP3", "SCATTER",
             "LP1", "HP1", "LP2", "MP1", "LP3", "HP2", "MP2", "LP1", "HP3", "LP2",
             "MP1", "LP3", "HP1", "LP1", "MP2", "LP2", "HP2", "LP3", "HP3", "LP1"]

    reel3 = ["HP1", "LP1", "MP1", "LP2", "HP2", "WILD", "LP3", "HP3", "LP1", "MP2",
             "SCATTER", "HP1", "LP2", "MP1", "LP3", "HP2", "LP1", "MP2", "HP3", "LP2",
             "HP1", "LP3", "MP1", "LP1", "HP2", "LP2", "MP2", "LP3", "HP3", "LP1"]

    reel4 = ["LP2", "HP1", "LP1", "MP1", "HP2", "LP3", "WILD", "HP3", "LP2", "MP2",
             "LP1", "HP1", "SCATTER", "MP1", "LP2", "HP2", "LP3", "MP2", "HP3", "LP1",
             "LP2", "HP1", "MP1", "LP3", "HP2", "LP1", "MP2", "LP2", "HP3", "LP3"]

    reel5 = ["MP1", "LP3", "HP1", "LP1", "HP2", "LP2", "HP3", "MP2", "WILD", "LP1",
             "HP1", "LP2", "MP1", "LP3", "HP2", "SCATTER", "MP2", "LP1", "HP3", "LP2",
             "MP1", "LP3", "HP1", "LP1", "HP2", "LP2", "MP2", "LP3", "HP3", "LP1"]

    paytable = {
        "WILD": {5: 1000.0, 4: 250.0, 3: 50.0},
        "HP1":  {5: 500.0,  4: 150.0, 3: 30.0, 2: 5.0},
        "HP2":  {5: 350.0,  4: 100.0, 3: 20.0},
        "HP3":  {5: 250.0,  4: 75.0,  3: 15.0},
        "MP1":  {5: 150.0,  4: 50.0,  3: 10.0},
        "MP2":  {5: 100.0,  4: 35.0,  3: 8.0},
        "LP1":  {5: 50.0,   4: 20.0,  3: 5.0},
        "LP2":  {5: 35.0,   4: 15.0,  3: 4.0},
        "LP3":  {5: 25.0,   4: 10.0,  3: 3.0},
    }

    return SlotModel(
        name="Babylonian Fortunes 5x3",
        reel_strips=[reel1, reel2, reel3, reel4, reel5],
        paytable=paytable,
        num_paylines=25,
        wild_symbol="WILD",
        scatter_symbol="SCATTER",
    )


def run_cli():
    parser = argparse.ArgumentParser(description="Panini Systems Game Math Engine")
    parser.add_argument("--mode", choices=["eval", "sim", "gacha", "par"], default="eval",
                        help="Action to perform: eval (combinatorics), sim (Monte Carlo), gacha, or par (export)")
    parser.add_argument("--spins", type=int, default=100000, help="Number of Monte Carlo spins")
    args = parser.parse_args()

    print("=================================================================")
    print("        PANINI SYSTEMS | APPLIED MATHEMATICS CONSULTING         ")
    print("             Game Mathematics Computational Engine              ")
    print("=================================================================\n")

    slot = get_sample_game()

    if args.mode == "eval":
        print(f"[*] Calculating theoretical combinatorics for: {slot.name}")
        evaluation = slot.evaluate_payline_combinatorics()
        print(f" -> Total Reel Cycle: {evaluation.total_cycle:,} combinations")
        print(f" -> Theoretical Line RTP: {evaluation.line_rtp * 100.0:.4f}%")
        print(f" -> Total Game Theoretical RTP: {evaluation.total_rtp * 100.0:.4f}%")
        print(f" -> Line Hit Frequency: {evaluation.line_hit_frequency * 100.0:.4f}%")
        print(f" -> Winning Combinations per Line: {evaluation.total_combinations_winning:,}")

    elif args.mode == "sim":
        print(f"[*] Running Monte Carlo simulation ({args.spins:,} spins)...")
        simulator = MonteCarloSimulator(slot)
        res = simulator.run_simulation(num_spins=args.spins)
        print(f" -> Completed {res.total_spins:,} spins.")
        print(f" -> Empirical RTP: {res.empirical_rtp * 100.0:.4f}%")
        print(f" -> Hit Frequency: {res.hit_frequency * 100.0:.2f}%")
        print(f" -> Standard Deviation (σ): {res.standard_deviation:.4f}")
        print(f" -> Volatility Index (90%): {res.volatility_index_90:.4f}")
        print(f" -> Volatility Index (95%): {res.volatility_index_95:.4f}")
        print(f" -> 95% Confidence Interval: [{res.ci_95[0]*100:.2f}%, {res.ci_95[1]*100:.2f}%]")
        print(f" -> Max Single Win: {res.max_single_win:.1f}x Total Bet")
        print("\n[*] Win Tier Distribution:")
        for tier, pct in res.win_distribution_pct.items():
            print(f"    {tier:<15}: {pct:>6.2f}%")

    elif args.mode == "par":
        print(f"[*] Generating PAR Sheet for: {slot.name}")
        par_gen = PARSheetGenerator(slot)
        print(par_gen.to_markdown())

    elif args.mode == "gacha":
        print("[*] Modeling Gacha Pity Distribution (Standard Genshin-style: Base 0.6%, Soft 74, Hard 90)...")
        gacha = GachaPityModel()
        metrics = gacha.calculate_distribution()
        print(f" -> Base Probability: {metrics.base_rate * 100.0:.2f}%")
        print(f" -> Expected Pulls (Single 5-Star): {metrics.expected_pulls_single:.2f} pulls")
        print(f" -> Consolidated Rate: {metrics.consolidated_rate * 100.0:.2f}%")
        print(f" -> Expected Pulls (Featured with 50/50): {metrics.expected_pulls_featured_5050:.2f} pulls")
        print(f" -> Median Pulls (50% of players): {metrics.median_pulls} pulls")
        print(f" -> 90th Percentile: {metrics.percentile_90} pulls")
        print(f" -> 99th Percentile: {metrics.percentile_99} pulls")


if __name__ == "__main__":
    run_cli()
