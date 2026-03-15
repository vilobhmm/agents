"""
Analyze AutoResearch Results
=============================

Analyze experiment results, find patterns, and provide insights.
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any

import numpy as np


def load_results(results_file: Path) -> Dict[str, Any]:
    """Load results from JSON file"""
    with open(results_file) as f:
        return json.load(f)


def analyze_hyperparameter_impact(results: List[Dict]) -> Dict[str, Any]:
    """Analyze impact of each hyperparameter"""

    param_values = defaultdict(lambda: defaultdict(list))

    for result in results:
        if 'config' not in result or 'final_val_loss' not in result:
            continue

        config = result['config']
        loss = result['final_val_loss']

        if loss == float('inf') or np.isnan(loss):
            continue

        # Track loss for each parameter value
        for param, value in config.items():
            if isinstance(value, (int, float, bool)):
                param_values[param][str(value)].append(loss)

    # Calculate average loss for each parameter value
    param_analysis = {}
    for param, values_dict in param_values.items():
        analysis = {}
        for value, losses in values_dict.items():
            analysis[value] = {
                'mean_loss': np.mean(losses),
                'std_loss': np.std(losses),
                'count': len(losses)
            }
        param_analysis[param] = analysis

    return param_analysis


def find_best_configs(results: List[Dict], top_k: int = 5) -> List[Dict]:
    """Find top K best configurations"""

    valid_results = [
        r for r in results
        if 'final_val_loss' in r and r['final_val_loss'] != float('inf')
    ]

    sorted_results = sorted(valid_results, key=lambda r: r['final_val_loss'])
    return sorted_results[:top_k]


def calculate_improvement(results: List[Dict]) -> Dict[str, float]:
    """Calculate improvement metrics"""

    valid_losses = [
        r['final_val_loss'] for r in results
        if 'final_val_loss' in r and r['final_val_loss'] != float('inf')
    ]

    if not valid_losses:
        return {}

    return {
        'best_loss': min(valid_losses),
        'worst_loss': max(valid_losses),
        'mean_loss': np.mean(valid_losses),
        'std_loss': np.std(valid_losses),
        'improvement_pct': (max(valid_losses) - min(valid_losses)) / max(valid_losses) * 100,
        'total_experiments': len(valid_losses)
    }


def print_analysis(results_file: Path):
    """Print comprehensive analysis"""

    print("=" * 80)
    print("📊 AutoResearch Results Analysis")
    print("=" * 80)

    # Load results
    data = load_results(results_file)
    results = data.get('results', [])

    if not results:
        print("No results found!")
        return

    # Overall metrics
    print("\n📈 Overall Performance")
    print("-" * 80)
    metrics = calculate_improvement(results)

    print(f"Total Experiments: {metrics['total_experiments']}")
    print(f"Best Loss: {metrics['best_loss']:.4f}")
    print(f"Worst Loss: {metrics['worst_loss']:.4f}")
    print(f"Mean Loss: {metrics['mean_loss']:.4f} ± {metrics['std_loss']:.4f}")
    print(f"Improvement: {metrics['improvement_pct']:.2f}%")

    # Best configurations
    print("\n🏆 Top 5 Configurations")
    print("-" * 80)
    best_configs = find_best_configs(results, top_k=5)

    for i, result in enumerate(best_configs, 1):
        print(f"\n{i}. Experiment #{result['experiment_id']} | Loss: {result['final_val_loss']:.4f}")

        if 'config' in result:
            config = result['config']
            print(f"   Learning Rate: {config.get('learning_rate', 'N/A')}")
            print(f"   Batch Size: {config.get('batch_size', 'N/A')}")
            print(f"   Gradient Accumulation: {config.get('gradient_accumulation_steps', 'N/A')}")
            print(f"   Warmup Steps: {config.get('warmup_iters', 'N/A')}")
            print(f"   Weight Decay: {config.get('weight_decay', 'N/A')}")
            print(f"   Beta1: {config.get('beta1', 'N/A')}, Beta2: {config.get('beta2', 'N/A')}")
            print(f"   QK-Norm: {config.get('qk_norm', 'N/A')}")
            print(f"   Tied Weights: {config.get('tie_weights', 'N/A')}")

    # Hyperparameter analysis
    print("\n🔍 Hyperparameter Impact Analysis")
    print("-" * 80)
    param_analysis = analyze_hyperparameter_impact(results)

    # Learning rate
    if 'learning_rate' in param_analysis:
        print("\n📊 Learning Rate:")
        lr_data = param_analysis['learning_rate']
        for lr, stats in sorted(lr_data.items(), key=lambda x: x[1]['mean_loss']):
            print(f"   {lr}: {stats['mean_loss']:.4f} ± {stats['std_loss']:.4f} (n={stats['count']})")

    # Batch size impact
    if 'gradient_accumulation_steps' in param_analysis:
        print("\n📊 Gradient Accumulation (Effective Batch Size):")
        ga_data = param_analysis['gradient_accumulation_steps']
        for ga, stats in sorted(ga_data.items(), key=lambda x: x[1]['mean_loss']):
            batch_size = int(ga) * 8  # Assuming batch_size=8
            print(f"   {ga} (batch={batch_size}): {stats['mean_loss']:.4f} ± {stats['std_loss']:.4f} (n={stats['count']})")

    # Warmup impact
    if 'warmup_iters' in param_analysis:
        print("\n📊 Warmup Steps:")
        warmup_data = param_analysis['warmup_iters']
        for warmup, stats in sorted(warmup_data.items(), key=lambda x: x[1]['mean_loss']):
            print(f"   {warmup}: {stats['mean_loss']:.4f} ± {stats['std_loss']:.4f} (n={stats['count']})")

    # Weight decay
    if 'weight_decay' in param_analysis:
        print("\n📊 Weight Decay:")
        wd_data = param_analysis['weight_decay']
        for wd, stats in sorted(wd_data.items(), key=lambda x: x[1]['mean_loss']):
            print(f"   {wd}: {stats['mean_loss']:.4f} ± {stats['std_loss']:.4f} (n={stats['count']})")

    # Key insights
    print("\n💡 Key Insights")
    print("-" * 80)

    # Best learning rate
    if 'learning_rate' in param_analysis:
        lr_data = param_analysis['learning_rate']
        best_lr = min(lr_data.items(), key=lambda x: x[1]['mean_loss'])
        print(f"✓ Best Learning Rate: {best_lr[0]} (avg loss: {best_lr[1]['mean_loss']:.4f})")

    # Best effective batch size
    if 'gradient_accumulation_steps' in param_analysis:
        ga_data = param_analysis['gradient_accumulation_steps']
        best_ga = min(ga_data.items(), key=lambda x: x[1]['mean_loss'])
        print(f"✓ Best Effective Batch: {int(best_ga[0]) * 8} (ga={best_ga[0]}, avg loss: {best_ga[1]['mean_loss']:.4f})")

    # Best warmup
    if 'warmup_iters' in param_analysis:
        warmup_data = param_analysis['warmup_iters']
        best_warmup = min(warmup_data.items(), key=lambda x: x[1]['mean_loss'])
        print(f"✓ Best Warmup: {best_warmup[0]} steps (avg loss: {best_warmup[1]['mean_loss']:.4f})")

    # Progress over time
    print("\n📈 Progress Over Time")
    print("-" * 80)
    valid_results = [r for r in results if r.get('final_val_loss', float('inf')) != float('inf')]

    if valid_results:
        # Group by chunks of 20
        chunk_size = 20
        for i in range(0, len(valid_results), chunk_size):
            chunk = valid_results[i:i+chunk_size]
            chunk_losses = [r['final_val_loss'] for r in chunk]
            avg_loss = np.mean(chunk_losses)
            best_loss = min(chunk_losses)

            print(f"Experiments {i+1:3d}-{min(i+chunk_size, len(valid_results)):3d}: "
                  f"Avg={avg_loss:.4f}, Best={best_loss:.4f}")

    print("\n" + "=" * 80)


def main():
    parser = argparse.ArgumentParser(description='Analyze AutoResearch results')
    parser.add_argument(
        '--results',
        type=Path,
        default=Path('logs/all_results.json'),
        help='Path to results JSON file'
    )

    args = parser.parse_args()

    if not args.results.exists():
        print(f"Error: Results file not found: {args.results}")
        return

    print_analysis(args.results)


if __name__ == "__main__":
    main()
