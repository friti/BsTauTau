#!/bin/bash

echo "=== Combining datacards ==="
combineCards.py datacards/*.txt > combined_datacard.txt
echo "✓ Combined datacard created: combined_datacard.txt"

echo ""
echo "=== Creating workspace ==="
text2workspace.py combined_datacard.txt -o workspace.root
echo "✓ Workspace created: workspace.root"

echo ""
echo "=== Running asymptotic limits (blind) ==="
combine -M AsymptoticLimits workspace.root -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

#combine -M AsymptoticLimits workspace.root -t -1 --freezeParameters all --setParameters lumiscale=400.0/59.7
