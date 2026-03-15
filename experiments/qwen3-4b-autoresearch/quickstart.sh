#!/bin/bash
# Qwen3-4B AutoResearch Quickstart Script

set -e  # Exit on error

echo "================================================================================================"
echo "🚀 Qwen3-4B AutoResearch Quickstart"
echo "================================================================================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo -e "\n${YELLOW}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"

# Check CUDA
echo -e "\n${YELLOW}Checking CUDA availability...${NC}"
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    echo -e "${GREEN}✓ CUDA available${NC}"
else
    echo -e "${YELLOW}⚠ CUDA not found - will use CPU (slower)${NC}"
fi

# Check API key
echo -e "\n${YELLOW}Checking Anthropic API key...${NC}"
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}✗ ANTHROPIC_API_KEY not set${NC}"
    echo ""
    echo "To use AutoResearch, you need an Anthropic API key:"
    echo "  1. Get your key from: https://console.anthropic.com/"
    echo "  2. Set it: export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    echo -e "${YELLOW}You can still run single experiments without the API key.${NC}"
else
    echo -e "${GREEN}✓ API key found${NC}"
fi

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create directories
echo -e "\n${YELLOW}Creating directories...${NC}"
mkdir -p data logs experiments best_config
echo -e "${GREEN}✓ Directories created${NC}"

# Test model
echo -e "\n${YELLOW}Testing Qwen3-4B model...${NC}"
python -c "
from models.qwen3 import create_qwen3_4b
import torch

model = create_qwen3_4b()
print(f'Model parameters: {model.count_parameters()}')

# Quick forward pass
x = torch.randint(0, 50304, (2, 64))
logits, loss, _ = model(x, targets=x)
print(f'Forward pass: ✓ (output shape: {logits.shape})')
" && echo -e "${GREEN}✓ Model test passed${NC}"

# Menu
echo ""
echo "================================================================================================"
echo "What would you like to do?"
echo "================================================================================================"
echo ""
echo "  1) Run a single 5-minute training experiment"
echo "  2) Start AutoResearch (overnight optimization)"
echo "  3) Analyze existing results"
echo "  4) Visualize results"
echo "  5) Export best configuration"
echo "  6) Exit"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo -e "\n${YELLOW}Running single experiment...${NC}"
        python train.py
        echo -e "\n${GREEN}✓ Experiment complete!${NC}"
        echo "Results saved to: logs/latest_result.json"
        ;;

    2)
        if [ -z "$ANTHROPIC_API_KEY" ]; then
            echo -e "\n${RED}Error: ANTHROPIC_API_KEY required for AutoResearch${NC}"
            echo "Set it with: export ANTHROPIC_API_KEY='your-key'"
            exit 1
        fi

        echo -e "\n${YELLOW}Starting AutoResearch...${NC}"
        echo "This will run up to 100 experiments (5 minutes each)."
        echo "Estimated time: ~8 hours for 100 experiments"
        echo ""
        read -p "Continue? (y/n): " confirm

        if [ "$confirm" = "y" ]; then
            echo -e "\n${GREEN}🚀 Starting AutoResearch...${NC}"
            echo "You can safely close this terminal. Results will be saved to logs/"
            python autoresearch.py
        else
            echo "Cancelled."
        fi
        ;;

    3)
        if [ ! -f "logs/all_results.json" ]; then
            echo -e "\n${RED}No results found. Run some experiments first.${NC}"
            exit 1
        fi

        echo -e "\n${YELLOW}Analyzing results...${NC}"
        python scripts/analyze_results.py
        ;;

    4)
        if [ ! -f "logs/all_results.json" ]; then
            echo -e "\n${RED}No results found. Run some experiments first.${NC}"
            exit 1
        fi

        echo -e "\n${YELLOW}Creating visualizations...${NC}"
        python scripts/visualize.py
        echo -e "\n${GREEN}✓ Plots saved to: logs/plots/${NC}"
        ;;

    5)
        if [ ! -f "logs/all_results.json" ]; then
            echo -e "\n${RED}No results found. Run some experiments first.${NC}"
            exit 1
        fi

        echo -e "\n${YELLOW}Exporting best configuration...${NC}"
        python scripts/export_best.py
        echo -e "\n${GREEN}✓ Best config saved to: best_config/${NC}"
        ;;

    6)
        echo "Goodbye!"
        exit 0
        ;;

    *)
        echo -e "\n${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo "================================================================================================"
echo "✨ Done!"
echo "================================================================================================"
