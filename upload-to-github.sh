#!/bin/bash

# GitHub Upload Script for AI Predictive Maintenance System
# This script will help you push the project to GitHub

echo "=========================================="
echo "GitHub Upload Helper"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed"
    echo "Please install git first: https://git-scm.com/downloads"
    exit 1
fi

echo "Before running this script, make sure you have:"
echo "1. Created a new repository on GitHub.com"
echo "2. Named it something like 'ai-predictive-maintenance'"
echo "3. Do NOT initialize it with README, .gitignore, or license"
echo ""
read -p "Have you created the GitHub repository? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Please create a repository first at:"
    echo "https://github.com/new"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo ""
read -p "Enter your GitHub username: " github_username
read -p "Enter your repository name (e.g., ai-predictive-maintenance): " repo_name

echo ""
echo "Initializing git repository..."
cd /mnt/user-data/outputs/ai-predictive-maintenance

# Initialize git if not already initialized
if [ ! -d .git ]; then
    git init
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already exists"
fi

# Add all files
echo ""
echo "Adding files to git..."
git add .
echo "✓ Files added"

# Create initial commit
echo ""
echo "Creating initial commit..."
git commit -m "Initial commit: AI Predictive Maintenance System

Complete production-ready implementation with:
- FastAPI backend with ML anomaly detection
- Real-time monitoring dashboard
- WebSocket support
- Complete documentation
- Docker deployment ready
- Test suite included"

echo "✓ Commit created"

# Add remote
echo ""
echo "Adding GitHub remote..."
git branch -M main
git remote remove origin 2>/dev/null  # Remove if exists
git remote add origin "https://github.com/${github_username}/${repo_name}.git"
echo "✓ Remote added"

# Push to GitHub
echo ""
echo "=========================================="
echo "Ready to push to GitHub!"
echo "=========================================="
echo ""
echo "Repository: https://github.com/${github_username}/${repo_name}"
echo ""
echo "IMPORTANT: You will need to authenticate with GitHub."
echo "Choose one of these methods:"
echo ""
echo "Method 1 - Personal Access Token (Recommended):"
echo "  1. Go to: https://github.com/settings/tokens"
echo "  2. Click 'Generate new token (classic)'"
echo "  3. Give it 'repo' permissions"
echo "  4. Copy the token"
echo "  5. Use it as your password when prompted"
echo ""
echo "Method 2 - GitHub CLI:"
echo "  Run: gh auth login"
echo ""
read -p "Ready to push? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Pushing to GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "✓ SUCCESS! Project uploaded to GitHub"
        echo "=========================================="
        echo ""
        echo "Your repository is now live at:"
        echo "https://github.com/${github_username}/${repo_name}"
        echo ""
        echo "Next steps:"
        echo "1. Visit your repository"
        echo "2. Add a description and topics"
        echo "3. Star your own repo ⭐"
        echo "4. Share with others!"
        echo ""
    else
        echo ""
        echo "Push failed. Common solutions:"
        echo "1. Make sure you created the repository on GitHub"
        echo "2. Check your authentication (use personal access token)"
        echo "3. Verify the repository name is correct"
        echo ""
        echo "To try again manually:"
        echo "cd /mnt/user-data/outputs/ai-predictive-maintenance"
        echo "git push -u origin main"
    fi
else
    echo ""
    echo "No problem! When you're ready, run:"
    echo "cd /mnt/user-data/outputs/ai-predictive-maintenance"
    echo "git push -u origin main"
fi

echo ""
echo "=========================================="
