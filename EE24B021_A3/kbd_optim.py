#!/usr/bin/env python3
"""
Keyboard Layout Optimization via Simulated Annealing

This script optimizes the placement of characters on a keyboard
(for single-finger typing) using simulated annealing.
The objective is to minimize the total Euclidean distance the finger must travel
to type a given text corpus.
"""

import argparse
import math
import os
import random
import string
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt

# --- Type Aliases for Clarity ---
Point = Tuple[float, float]
Layout = Dict[str, Point]

# --- Keyboard layout utility functions ---

def qwerty_coordinates(chars: str) -> Layout:
    """
    Return QWERTY grid coordinates for the provided character set.
    Unmapped characters default to the location of space.
    """
    row0 = "qwertyuiop"
    row1 = "asdfghjkl"
    row2 = "zxcvbnm"
    coords = {}
    # Top row
    for i, c in enumerate(row0):
        coords[c] = (float(i), 0.0)
    # Home row
    for i, c in enumerate(row1):
        coords[c] = (0.5 + float(i), 1.0)
    # Bottom row
    for i, c in enumerate(row2):
        coords[c] = (1.0 + float(i), 2.0)
    # Space bar location for unmapped characters
    space_xy = (4.5, 3.0)
    coords[" "] = space_xy
    for ch in chars:
        if ch not in coords:
            coords[ch] = space_xy
    return coords

def initial_layout(chars: str = string.ascii_lowercase) -> Layout:
    """
    Return the initial QWERTY layout for the provided character set.
    """
    return qwerty_coordinates(chars)

def preprocess_text(text: str, chars: str) -> str:
    """
    Lowercase and filter the text to the allowed character set,
    mapping all other characters to space.
    """
    out = ""
    for i in text.lower():
        out += i if i in chars else " "
    return out

def path_length_cost(text: str, layout: Layout) -> float:
    """
    Calculate total Euclidean distance traveled to type the given text using the layout.
    """
    cost = 0.0
    if not text:
        return 0.0
    prev = layout[text[0]]
    for ch in text[1:]:
        curr = layout[ch]
        dx = curr[0] - prev[0]
        dy = curr[1] - prev[1]
        cost += (dx ** 2 + dy ** 2) ** 0.5
        prev = curr
    return cost

def swap_chars(layout: Layout) -> Layout:
    """
    Randomly swap the positions of two characters in the keyboard layout.
    """
    keys = list(layout.keys())
    a, b = random.sample(keys, 2)
    new_layout = layout.copy()
    new_layout[a], new_layout[b] = new_layout[b], new_layout[a]
    return new_layout

# --- Annealing Parameters as a dataclass ---

@dataclass
class SAParams:
    iters: int = 5000    # Total iterations (outer loop)
    t0: float = 1.0      # Initial temperature
    alpha: float = 0.995 # Annealing (cooling) rate per epoch
    epoch: int = 50      # Steps per epoch (temp updated after each)

# --- Simulated Annealing Main Function ---

def simulated_annealing(
    text: str,
    layout: Layout,
    params: SAParams,
    rng: random.Random
) -> Tuple[Layout, float, List[float], List[float]]:
    """
    Simulated annealing to optimize keyboard layout.
    Returns (best layout, best cost, best cost trace, current cost trace)
    """
    current_layout = layout.copy()
    best_layout = layout.copy()
    current_cost = path_length_cost(text, current_layout)
    best_cost = current_cost
    best_costs = [best_cost]
    current_costs = [current_cost]

    temp = params.t0

    for it in range(params.iters):
        for e in range(params.epoch):
            candidate = swap_chars(current_layout)
            candidate_cost = path_length_cost(text, candidate)
            delta_cost = candidate_cost - current_cost

            # Accept if better OR probabilistically worse
            if delta_cost < 0 or rng.random() < math.exp(-delta_cost / temp):
                current_layout = candidate
                current_cost = candidate_cost

            # Track global best
            if current_cost < best_cost:
                best_layout = current_layout.copy()
                best_cost = current_cost

            current_costs.append(current_cost)
            best_costs.append(best_cost)
        temp *= params.alpha # Cool down after each epoch

    return best_layout, best_cost, best_costs, current_costs

# --- Plotting Utilities ---

def plot_costs(
    layout: Layout, best_trace: List[float], current_trace: List[float]
) -> None:

    # Plot cost trace
    out_dir = "."
    plt.figure(figsize=(6, 3))
    plt.plot(best_trace, lw=1.5, label="Best so far")
    plt.plot(current_trace, lw=1.5, label="Current")
    plt.xlabel("Iteration")
    plt.ylabel("Best Cost")
    plt.title("Best Cost vs Iteration")
    plt.legend(loc="best", fontsize="small", framealpha=0.9)
    plt.tight_layout()
    path = os.path.join(out_dir, f"cost_trace.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")

    # Plot layout scatter
    xs, ys, labels = [], [], []
    for ch, (x, y) in layout.items():
        xs.append(x)
        ys.append(y)
        labels.append(ch)

    plt.figure(figsize=(6, 3))
    plt.scatter(xs, ys, s=250, c="#1f77b4")
    for x, y, ch in zip(xs, ys, labels):
        plt.text(
            x,
            y,
            ch,
            ha="center",
            va="center",
            color="white",
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.15", fc="#1f77b4", ec="none", alpha=0.9),
        )
    plt.gca().invert_yaxis()
    plt.title("Optimized Layout")
    plt.axis("equal")
    plt.tight_layout()
    path = os.path.join(out_dir, f"layout.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def main():
    # You can add argparse for CLI usage as needed
    chars = string.ascii_lowercase + " "
    rng = random.Random(0)  # Fix seed for reproducibility

    # Fallback demo text
    text = "the quick brown fox jumps over the lazy dog apl is the best course ever"
    layout0 = initial_layout(chars)
    cleaned_text = preprocess_text(text, chars)
    baseline_cost = path_length_cost(cleaned_text, layout0)
    print(f"Baseline QWERTY cost: {baseline_cost:.4f}")

    # Annealing parameters
    params = SAParams(iters=2000, t0=10.0, alpha=0.995, epoch=1)

    # Run simulated annealing
    start = time.time()
    best_layout, best_cost, best_trace, current_trace = simulated_annealing(
        cleaned_text, layout0, params, rng)
    elapsed = time.time() - start

    print(f"Optimized cost: {best_cost:.4f} (improvement: {baseline_cost - best_cost:.4f})")
    print(f"Runtime: {elapsed:.2f}s")

    # Plot results
    plot_costs(best_layout,best_trace, current_trace)

if __name__ == "__main__":
    main()
