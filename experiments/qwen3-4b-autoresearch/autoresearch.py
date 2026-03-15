"""
AutoResearch Agent for Qwen3-4B
================================

Autonomous ML research agent that runs experiments overnight.
Based on Karpathy's AutoResearch framework (630 lines of autonomous research magic).

How it works:
1. Read the research program (program.md)
2. Modify train.py based on the program
3. Run training for exactly 5 minutes
4. Check if validation loss improved
5. Record results and repeat

Expected: ~12 experiments/hour, ~100 experiments overnight (8 hours)

The agent can rediscover ML innovations like RMSNorm, tied embeddings,
learning rate schedules, and more - autonomously!
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import anthropic


# =============================================================================
# Configuration
# =============================================================================

class AutoResearchConfig:
    """AutoResearch configuration"""

    # API
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    model: str = "claude-sonnet-4-5"  # Latest Claude model

    # Experiment settings
    experiment_duration: int = 300  # 5 minutes per experiment
    max_experiments: int = 100      # Run up to 100 experiments
    experiments_dir: Path = Path("experiments")
    logs_dir: Path = Path("logs")

    # Files
    train_script: Path = Path("train.py")
    program_file: Path = Path("program.md")
    results_file: Path = Path("logs/all_results.json")

    # Optimization
    metric: str = "val_loss"        # Metric to optimize
    direction: str = "minimize"     # Lower is better


# =============================================================================
# Experiment Runner
# =============================================================================

class ExperimentRunner:
    """Runs a single 5-minute training experiment"""

    def __init__(self, config: AutoResearchConfig):
        self.config = config

    def run_experiment(self, experiment_id: int) -> Dict[str, Any]:
        """Run a single training experiment"""

        print(f"\n{'='*80}")
        print(f"🧪 Experiment #{experiment_id}")
        print(f"{'='*80}")

        start_time = time.time()

        # Run train.py
        try:
            result = subprocess.run(
                [sys.executable, str(self.config.train_script)],
                capture_output=True,
                text=True,
                timeout=self.config.experiment_duration + 60  # Extra 60s buffer
            )

            # Parse results
            results_path = self.config.logs_dir / "latest_result.json"
            if results_path.exists():
                with open(results_path) as f:
                    results = json.load(f)
            else:
                results = {
                    'final_val_loss': float('inf'),
                    'error': 'No results file generated'
                }

            # Add stdout/stderr for debugging
            results['stdout'] = result.stdout
            results['stderr'] = result.stderr
            results['returncode'] = result.returncode

        except subprocess.TimeoutExpired:
            results = {
                'final_val_loss': float('inf'),
                'error': 'Experiment timed out'
            }
        except Exception as e:
            results = {
                'final_val_loss': float('inf'),
                'error': str(e)
            }

        elapsed = time.time() - start_time
        results['experiment_id'] = experiment_id
        results['timestamp'] = datetime.now().isoformat()
        results['elapsed_time'] = elapsed

        print(f"\n⏱️  Experiment completed in {elapsed:.1f}s")
        print(f"📊 Validation Loss: {results.get('final_val_loss', 'N/A')}")

        return results


# =============================================================================
# AutoResearch Agent
# =============================================================================

class AutoResearchAgent:
    """AI Agent that modifies train.py to discover optimal hyperparameters"""

    def __init__(self, config: AutoResearchConfig):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.anthropic_api_key)
        self.runner = ExperimentRunner(config)

        # Track best result
        self.best_loss = float('inf')
        self.best_experiment = None
        self.all_results: List[Dict] = []

        # Load program
        self.program = self._load_program()

    def _load_program(self) -> str:
        """Load research program from program.md"""
        if self.config.program_file.exists():
            return self.config.program_file.read_text()
        else:
            # Default program
            return """
# Research Program: Qwen3-4B on TinyStories

## Objective
Optimize the Qwen3-4B model training on TinyStories dataset.
Minimize validation loss through hyperparameter search.

## Areas to Explore

### 1. Learning Rate
- Try different learning rates: 3e-4, 6e-4, 1e-3, 2e-3
- Adjust warmup steps: 1000, 2000, 4000
- Experiment with min_lr ratio: 0.1, 0.05, 0.01

### 2. Batch Size & Gradient Accumulation
- Try effective batch sizes: 32, 64, 128, 256
- Adjust gradient_accumulation_steps accordingly

### 3. Optimizer
- Experiment with Adam beta values
- Try different weight decay: 0.0, 0.01, 0.1

### 4. Architecture
- Test QK-Normalization on/off
- Test tied weights on/off
- Test gradient checkpointing on/off

### 5. Learning Rate Schedule
- Cosine annealing variations
- Different warmup strategies

## Strategy
1. Start with baseline configuration
2. Vary one hyperparameter at a time initially
3. Once promising directions found, combine best settings
4. Focus on biggest improvements first
5. Be systematic but exploratory

## Success Criteria
- Minimize validation loss
- Keep training stable (no NaN losses)
- Complete within 5 minutes per experiment
"""

    def _load_train_script(self) -> str:
        """Load current train.py content"""
        return self.config.train_script.read_text()

    def _save_train_script(self, content: str):
        """Save modified train.py"""
        self.config.train_script.write_text(content)

    def _create_modification_prompt(self, results_history: List[Dict]) -> str:
        """Create prompt for Claude to modify train.py"""

        prompt = f"""You are an ML research agent optimizing Qwen3-4B training.

# Research Program
{self.program}

# Current train.py
```python
{self._load_train_script()}
```

# Previous Experiments
"""

        # Add last 5 experiments
        for result in results_history[-5:]:
            exp_id = result['experiment_id']
            val_loss = result.get('final_val_loss', 'N/A')
            config = result.get('config', {})

            prompt += f"\nExperiment #{exp_id}: val_loss = {val_loss}"
            if config:
                prompt += f"\n  - learning_rate: {config.get('learning_rate')}"
                prompt += f"\n  - batch_size: {config.get('batch_size')}"
                prompt += f"\n  - gradient_accumulation: {config.get('gradient_accumulation_steps')}"
                prompt += f"\n  - warmup_iters: {config.get('warmup_iters')}"

        prompt += f"\n\n# Best So Far\nValidation Loss: {self.best_loss:.4f}"

        prompt += """

# Your Task
Modify train.py to improve validation loss. Focus on the TrainConfig class.

**Rules:**
1. Only modify hyperparameters in TrainConfig
2. Keep experiment_time_limit = 300 (5 minutes)
3. Make systematic changes based on previous results
4. Ensure changes are valid Python
5. Return ONLY the complete modified train.py file

**Output:**
Return the full train.py file with your modifications.
No explanations, just the code.
"""

        return prompt

    def get_modification(self, results_history: List[Dict]) -> str:
        """Ask Claude to modify train.py"""

        print("\n🤖 Asking AI agent for modifications...")

        prompt = self._create_modification_prompt(results_history)

        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=16000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Extract code from response
        content = response.content[0].text

        # Remove markdown code blocks if present
        if "```python" in content:
            content = content.split("```python")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        return content.strip()

    def run_research(self):
        """Main research loop"""

        print("=" * 80)
        print("🚀 AutoResearch: Qwen3-4B Optimization")
        print("=" * 80)
        print(f"Model: {self.config.model}")
        print(f"Max Experiments: {self.config.max_experiments}")
        print(f"Experiment Duration: {self.config.experiment_duration}s (5 min)")
        print("=" * 80)

        # Ensure directories exist
        self.config.logs_dir.mkdir(exist_ok=True)
        self.config.experiments_dir.mkdir(exist_ok=True)

        # Run experiments
        for exp_id in range(1, self.config.max_experiments + 1):

            # Run experiment with current train.py
            results = self.runner.run_experiment(exp_id)
            self.all_results.append(results)

            # Check if best
            val_loss = results.get('final_val_loss', float('inf'))
            if val_loss < self.best_loss:
                self.best_loss = val_loss
                self.best_experiment = exp_id
                print(f"\n✨ New best! Loss: {self.best_loss:.4f}")

                # Save best train.py
                best_script = self.config.experiments_dir / f"train_best_exp{exp_id}.py"
                best_script.write_text(self._load_train_script())

            # Save all results
            with open(self.config.results_file, 'w') as f:
                json.dump({
                    'best_loss': self.best_loss,
                    'best_experiment': self.best_experiment,
                    'total_experiments': len(self.all_results),
                    'results': self.all_results
                }, f, indent=2)

            # Get AI modification for next experiment
            if exp_id < self.config.max_experiments:
                try:
                    modified_script = self.get_modification(self.all_results)
                    self._save_train_script(modified_script)

                    # Save this version
                    version_file = self.config.experiments_dir / f"train_exp{exp_id+1}.py"
                    version_file.write_text(modified_script)

                    print(f"✅ Modified train.py for experiment #{exp_id+1}")

                except Exception as e:
                    print(f"❌ Error getting modification: {e}")
                    print("Continuing with current train.py")

            # Brief pause
            time.sleep(2)

        # Final summary
        print("\n" + "=" * 80)
        print("🎉 Research Complete!")
        print("=" * 80)
        print(f"Total Experiments: {len(self.all_results)}")
        print(f"Best Validation Loss: {self.best_loss:.4f}")
        print(f"Best Experiment: #{self.best_experiment}")
        print(f"Results saved to: {self.config.results_file}")
        print("=" * 80)


# =============================================================================
# Main
# =============================================================================

def main():
    """Run autoresearch"""

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please set it with: export ANTHROPIC_API_KEY='your-key'")
        sys.exit(1)

    # Create config
    config = AutoResearchConfig()

    # Create and run agent
    agent = AutoResearchAgent(config)
    agent.run_research()


if __name__ == "__main__":
    main()
