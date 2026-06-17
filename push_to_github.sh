#!/bin/bash
# Run in Git Bash from inside P2_BMW_Business_Analysis/
# Pre-req: create repo "bmw-business-analysis" on github.com (empty, no README)

set -e
git init
git branch -M main
git config user.name "Shardul Pundir"
git config user.email "shardul.pundir21@gmail.com"

cat > .gitignore << 'IGNORE'
__pycache__/
*.py[cod]
.env
venv/
charts/*.png
.ipynb_checkpoints/
.DS_Store
Thumbs.db
IGNORE

git add .
git commit -m "feat: P2 BMW Business Analysis

Company-level deep-dive into BMW Group.
- Segment P&L: Automotive / Financial Services / Motorcycles (FY2021-2025)
- Geographic revenue mix: China decline from 21% peak to 19.2%
- Powertrain transition: BEV mix 1.9% (2020) to 20.6% (2025)
- Competitive moat radar: BMW vs Mercedes vs VW

Part of BMW Equity Research chain: P1 Industry -> P2 Business -> P3 3-Statement -> P4 DCF -> P5 Report"

git remote add origin https://github.com/SharDXL/bmw-business-analysis.git
git push -u origin main
echo "Done: https://github.com/SharDXL/bmw-business-analysis"
