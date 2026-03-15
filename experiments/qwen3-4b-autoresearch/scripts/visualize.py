"""
Visualize AutoResearch Results
===============================

Create plots and visualizations of experiment results.
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def load_results(results_file: Path) -> List[Dict]:
    """Load results from JSON file"""
    with open(results_file) as f:
        data = json.load(f)
        return data.get('results', [])


def plot_loss_over_time(results: List[Dict], output_dir: Path):
    """Plot validation loss over experiments"""

    valid_results = [
        r for r in results
        if 'final_val_loss' in r and r['final_val_loss'] != float('inf')
    ]

    if not valid_results:
        print("No valid results to plot!")
        return

    exp_ids = [r['experiment_id'] for r in valid_results]
    losses = [r['final_val_loss'] for r in valid_results]

    # Calculate running best
    running_best = []
    best_so_far = float('inf')
    for loss in losses:
        best_so_far = min(best_so_far, loss)
        running_best.append(best_so_far)

    plt.figure(figsize=(12, 6))
    plt.plot(exp_ids, losses, 'o-', alpha=0.6, label='Validation Loss', markersize=4)
    plt.plot(exp_ids, running_best, 'r-', linewidth=2, label='Best So Far')
    plt.xlabel('Experiment Number')
    plt.ylabel('Validation Loss')
    plt.title('AutoResearch: Loss Over Time')
    plt.legend()
    plt.grid(True, alpha=0.3)

    output_file = output_dir / 'loss_over_time.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    plt.close()


def plot_hyperparameter_heatmaps(results: List[Dict], output_dir: Path):
    """Plot heatmaps for hyperparameter combinations"""

    valid_results = [
        r for r in results
        if 'config' in r and 'final_val_loss' in r and r['final_val_loss'] != float('inf')
    ]

    if len(valid_results) < 10:
        print("Not enough results for heatmaps!")
        return

    # LR vs Batch Size
    lr_batch_data = {}
    for r in valid_results:
        config = r['config']
        lr = config.get('learning_rate')
        ga = config.get('gradient_accumulation_steps')

        if lr and ga:
            batch_size = ga * config.get('batch_size', 8)
            key = (lr, batch_size)
            if key not in lr_batch_data:
                lr_batch_data[key] = []
            lr_batch_data[key].append(r['final_val_loss'])

    if lr_batch_data:
        # Create heatmap data
        unique_lrs = sorted(set(k[0] for k in lr_batch_data.keys()))
        unique_batches = sorted(set(k[1] for k in lr_batch_data.keys()))

        heatmap_data = np.full((len(unique_lrs), len(unique_batches)), np.nan)

        for i, lr in enumerate(unique_lrs):
            for j, batch in enumerate(unique_batches):
                key = (lr, batch)
                if key in lr_batch_data:
                    heatmap_data[i, j] = np.mean(lr_batch_data[key])

        plt.figure(figsize=(10, 8))
        sns.heatmap(
            heatmap_data,
            xticklabels=[str(b) for b in unique_batches],
            yticklabels=[f"{lr:.0e}" for lr in unique_lrs],
            annot=True,
            fmt='.3f',
            cmap='RdYlGn_r',
            cbar_kws={'label': 'Validation Loss'}
        )
        plt.xlabel('Effective Batch Size')
        plt.ylabel('Learning Rate')
        plt.title('Learning Rate vs Batch Size')

        output_file = output_dir / 'lr_batch_heatmap.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_file}")
        plt.close()


def plot_hyperparameter_distributions(results: List[Dict], output_dir: Path):
    """Plot distributions of each hyperparameter's performance"""

    valid_results = [
        r for r in results
        if 'config' in r and 'final_val_loss' in r and r['final_val_loss'] != float('inf')
    ]

    if not valid_results:
        return

    # Collect hyperparameter data
    hyperparams = ['learning_rate', 'gradient_accumulation_steps', 'warmup_iters', 'weight_decay']

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for idx, param in enumerate(hyperparams):
        param_data = {}
        for r in valid_results:
            value = r['config'].get(param)
            if value is not None:
                if value not in param_data:
                    param_data[value] = []
                param_data[value].append(r['final_val_loss'])

        if param_data:
            values = sorted(param_data.keys())
            means = [np.mean(param_data[v]) for v in values]
            stds = [np.std(param_data[v]) for v in values]

            axes[idx].errorbar(
                range(len(values)),
                means,
                yerr=stds,
                marker='o',
                capsize=5,
                linewidth=2,
                markersize=8
            )
            axes[idx].set_xticks(range(len(values)))
            axes[idx].set_xticklabels([str(v) for v in values], rotation=45)
            axes[idx].set_ylabel('Validation Loss')
            axes[idx].set_title(param.replace('_', ' ').title())
            axes[idx].grid(True, alpha=0.3)

    plt.tight_layout()
    output_file = output_dir / 'hyperparameter_distributions.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    plt.close()


def plot_improvement_timeline(results: List[Dict], output_dir: Path):
    """Plot timeline showing when improvements occurred"""

    valid_results = [
        r for r in results
        if 'final_val_loss' in r and r['final_val_loss'] != float('inf')
    ]

    if not valid_results:
        return

    # Find improvements
    improvements = []
    best_so_far = float('inf')

    for r in valid_results:
        loss = r['final_val_loss']
        if loss < best_so_far:
            improvements.append({
                'exp_id': r['experiment_id'],
                'loss': loss,
                'improvement': (best_so_far - loss) / best_so_far * 100 if best_so_far != float('inf') else 0
            })
            best_so_far = loss

    if improvements:
        plt.figure(figsize=(12, 6))

        exp_ids = [imp['exp_id'] for imp in improvements]
        losses = [imp['loss'] for imp in improvements]

        plt.subplot(2, 1, 1)
        plt.plot(exp_ids, losses, 'go-', markersize=8, linewidth=2)
        plt.ylabel('Validation Loss')
        plt.title('Improvements Over Time')
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 1, 2)
        improvements_pct = [imp['improvement'] for imp in improvements]
        plt.bar(exp_ids, improvements_pct, color='green', alpha=0.7)
        plt.xlabel('Experiment Number')
        plt.ylabel('Improvement (%)')
        plt.title('Relative Improvement at Each Milestone')
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        output_file = output_dir / 'improvement_timeline.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_file}")
        plt.close()


def main():
    parser = argparse.ArgumentParser(description='Visualize AutoResearch results')
    parser.add_argument(
        '--results',
        type=Path,
        default=Path('logs/all_results.json'),
        help='Path to results JSON file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('logs/plots'),
        help='Output directory for plots'
    )

    args = parser.parse_args()

    if not args.results.exists():
        print(f"Error: Results file not found: {args.results}")
        return

    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("📊 Creating Visualizations")
    print("=" * 80)

    # Load results
    results = load_results(args.results)

    if not results:
        print("No results to visualize!")
        return

    print(f"\nLoaded {len(results)} experiments")

    # Create plots
    print("\nGenerating plots...")
    plot_loss_over_time(results, args.output)
    plot_hyperparameter_heatmaps(results, args.output)
    plot_hyperparameter_distributions(results, args.output)
    plot_improvement_timeline(results, args.output)

    print(f"\n✅ Visualizations saved to: {args.output}")
    print("=" * 80)


if __name__ == "__main__":
    main()
