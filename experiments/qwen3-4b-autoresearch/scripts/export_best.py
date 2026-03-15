"""
Export Best Configuration
==========================

Export the best configuration found during autoresearch.
"""

import json
import yaml
import argparse
import shutil
from pathlib import Path
from typing import Dict, Any


def load_results(results_file: Path) -> Dict[str, Any]:
    """Load results from JSON file"""
    with open(results_file) as f:
        return json.load(f)


def find_best_experiment(results: Dict[str, Any]) -> Dict[str, Any]:
    """Find the best experiment"""

    all_results = results.get('results', [])

    best = None
    best_loss = float('inf')

    for r in all_results:
        loss = r.get('final_val_loss', float('inf'))
        if loss < best_loss:
            best_loss = loss
            best = r

    return best


def export_config(best_exp: Dict[str, Any], output_dir: Path):
    """Export configuration as YAML"""

    config = best_exp.get('config', {})

    # Create config dict
    export_config = {
        'experiment_id': best_exp.get('experiment_id'),
        'validation_loss': best_exp.get('final_val_loss'),
        'hyperparameters': {
            'learning_rate': config.get('learning_rate'),
            'batch_size': config.get('batch_size'),
            'gradient_accumulation_steps': config.get('gradient_accumulation_steps'),
            'warmup_iters': config.get('warmup_iters'),
            'weight_decay': config.get('weight_decay'),
            'grad_clip': config.get('grad_clip'),
            'beta1': config.get('beta1'),
            'beta2': config.get('beta2'),
        },
        'architecture': {
            'n_layers': config.get('n_layers'),
            'n_heads': config.get('n_heads'),
            'n_kv_heads': config.get('n_kv_heads'),
            'd_model': config.get('d_model'),
            'd_ff': config.get('d_ff'),
            'qk_norm': config.get('qk_norm'),
            'tie_weights': config.get('tie_weights'),
            'gradient_checkpointing': config.get('gradient_checkpointing'),
        },
        'training': {
            'max_iters': config.get('max_iters'),
            'eval_interval': config.get('eval_interval'),
            'seq_length': config.get('seq_length'),
            'compile': config.get('compile'),
        }
    }

    # Save as YAML
    config_file = output_dir / 'best_config.yaml'
    with open(config_file, 'w') as f:
        yaml.dump(export_config, f, default_flow_style=False, indent=2)

    print(f"✅ Exported config: {config_file}")

    # Also save as JSON
    json_file = output_dir / 'best_config.json'
    with open(json_file, 'w') as f:
        json.dump(export_config, f, indent=2)

    print(f"✅ Exported config: {json_file}")

    return export_config


def export_train_script(best_exp: Dict[str, Any], output_dir: Path, experiments_dir: Path):
    """Export the train.py used for best experiment"""

    exp_id = best_exp.get('experiment_id')

    # Try to find the saved train.py for this experiment
    train_file = experiments_dir / f'train_best_exp{exp_id}.py'

    if train_file.exists():
        dest = output_dir / 'best_train.py'
        shutil.copy(train_file, dest)
        print(f"✅ Exported train script: {dest}")
        return True
    else:
        print(f"⚠️  Train script not found for experiment {exp_id}")
        return False


def create_readme(best_exp: Dict[str, Any], export_config: Dict, output_dir: Path):
    """Create README for the exported configuration"""

    readme_content = f"""# Best AutoResearch Configuration

## Experiment Information

- **Experiment ID**: {best_exp.get('experiment_id')}
- **Validation Loss**: {best_exp.get('final_val_loss'):.4f}
- **Best Loss**: {best_exp.get('best_val_loss', 'N/A')}
- **Iterations**: {best_exp.get('iterations', 'N/A')}
- **Training Time**: {best_exp.get('time_seconds', 'N/A'):.1f}s

## Hyperparameters

### Optimizer
- **Learning Rate**: {export_config['hyperparameters']['learning_rate']}
- **Warmup Steps**: {export_config['hyperparameters']['warmup_iters']}
- **Weight Decay**: {export_config['hyperparameters']['weight_decay']}
- **Betas**: ({export_config['hyperparameters']['beta1']}, {export_config['hyperparameters']['beta2']})
- **Gradient Clip**: {export_config['hyperparameters']['grad_clip']}

### Batch Configuration
- **Batch Size**: {export_config['hyperparameters']['batch_size']}
- **Gradient Accumulation**: {export_config['hyperparameters']['gradient_accumulation_steps']}
- **Effective Batch Size**: {export_config['hyperparameters']['batch_size'] * export_config['hyperparameters']['gradient_accumulation_steps']}

### Architecture Features
- **QK-Normalization**: {export_config['architecture']['qk_norm']}
- **Tied Weights**: {export_config['architecture']['tie_weights']}
- **Gradient Checkpointing**: {export_config['architecture']['gradient_checkpointing']}

## Model Architecture

- **Layers**: {export_config['architecture']['n_layers']}
- **Dimensions**: {export_config['architecture']['d_model']}
- **Feed-Forward**: {export_config['architecture']['d_ff']}
- **Attention Heads**: {export_config['architecture']['n_heads']} (Q) / {export_config['architecture']['n_kv_heads']} (KV)

## Usage

### Training with Best Config

```bash
# Use the exported train.py
python best_train.py
```

### Apply Config to New Training

```python
from pathlib import Path
import yaml

# Load config
with open('best_config.yaml') as f:
    config = yaml.safe_load(f)

# Use hyperparameters
learning_rate = config['hyperparameters']['learning_rate']
batch_size = config['hyperparameters']['batch_size']
# ... etc
```

### Configuration File

The complete configuration is available in:
- `best_config.yaml` - YAML format
- `best_config.json` - JSON format
- `best_train.py` - Full training script

## Reproducing Results

To reproduce these results:

1. Use the exact hyperparameters listed above
2. Use the same random seed (42)
3. Train on TinyStories dataset
4. Run for the same number of iterations

Expected validation loss: ~{best_exp.get('final_val_loss'):.4f}

## Notes

This configuration was discovered through autonomous hyperparameter search using the AutoResearch framework.

**Key Insights:**
- This configuration represents the optimal settings found across {best_exp.get('experiment_id')} experiments
- It may be specific to the TinyStories dataset and Qwen3-4B architecture
- Transfer to other datasets/models may require adaptation

---

**Generated by AutoResearch Export Tool**
"""

    readme_file = output_dir / 'README.md'
    readme_file.write_text(readme_content)
    print(f"✅ Created README: {readme_file}")


def main():
    parser = argparse.ArgumentParser(description='Export best AutoResearch configuration')
    parser.add_argument(
        '--results',
        type=Path,
        default=Path('logs/all_results.json'),
        help='Path to results JSON file'
    )
    parser.add_argument(
        '--experiments',
        type=Path,
        default=Path('experiments'),
        help='Directory with saved experiment scripts'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('best_config'),
        help='Output directory for exported files'
    )

    args = parser.parse_args()

    if not args.results.exists():
        print(f"❌ Error: Results file not found: {args.results}")
        return

    print("=" * 80)
    print("📦 Exporting Best Configuration")
    print("=" * 80)

    # Load results
    results = load_results(args.results)

    # Find best experiment
    best_exp = find_best_experiment(results)

    if not best_exp:
        print("❌ No valid experiments found!")
        return

    print(f"\n🏆 Best Experiment: #{best_exp.get('experiment_id')}")
    print(f"📊 Validation Loss: {best_exp.get('final_val_loss'):.4f}")

    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)

    # Export configuration
    print("\n📝 Exporting configuration...")
    export_config_dict = export_config(best_exp, args.output)

    # Export train script
    print("\n📄 Exporting train script...")
    export_train_script(best_exp, args.output, args.experiments)

    # Create README
    print("\n📋 Creating README...")
    create_readme(best_exp, export_config_dict, args.output)

    print(f"\n✅ Export complete! Files saved to: {args.output}")
    print("\n📂 Exported files:")
    print(f"   - best_config.yaml")
    print(f"   - best_config.json")
    print(f"   - best_train.py")
    print(f"   - README.md")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
