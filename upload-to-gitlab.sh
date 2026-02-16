#!/bin/bash

# GitLab Upload Script for AI Predictive Maintenance System
# This script initializes Git and prepares for GitLab push

set -e

echo "=========================================="
echo "GitLab Upload Setup"
echo "AI Predictive Maintenance System"
echo "=========================================="
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed"
    echo "Please install Git first:"
    echo "  Ubuntu/Debian: sudo apt install git"
    echo "  macOS: brew install git"
    echo "  Windows: Download from https://git-scm.com/"
    exit 1
fi

echo "✓ Git is installed"
echo ""

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already exists"
fi

# Configure git user (if not already configured globally)
echo ""
echo "Configuring Git user..."
echo "Please enter your details:"
read -p "Your name: " git_name
read -p "Your email: " git_email

git config user.name "$git_name"
git config user.email "$git_email"

echo "✓ Git user configured"

# Add all files
echo ""
echo "Adding files to Git..."
git add .

# Create initial commit
echo ""
read -p "Commit message (press Enter for default): " commit_message
if [ -z "$commit_message" ]; then
    commit_message="Initial commit: AI Predictive Maintenance System

Complete implementation with:
- FastAPI backend with ML anomaly detection
- Real-time monitoring dashboard
- WebSocket support
- Complete API documentation
- Docker deployment ready
- Production-ready codebase"
fi

git commit -m "$commit_message" || echo "Files already committed or no changes"

echo ""
echo "✓ Files committed to Git"
echo ""
echo "=========================================="
echo "Next Steps: Upload to GitLab"
echo "=========================================="
echo ""
echo "1. Create a new repository on GitLab:"
echo "   - Go to https://gitlab.com/projects/new"
echo "   - Name: ai-predictive-maintenance"
echo "   - Visibility: Choose Private or Public"
echo "   - DO NOT initialize with README"
echo "   - Click 'Create project'"
echo ""
echo "2. Copy your GitLab repository URL (shown after creation)"
echo "   Example: https://gitlab.com/yourusername/ai-predictive-maintenance.git"
echo ""
echo "3. Run these commands:"
echo ""
read -p "Enter your GitLab repository URL: " gitlab_url

if [ ! -z "$gitlab_url" ]; then
    echo ""
    echo "Adding GitLab remote..."
    git remote remove origin 2>/dev/null || true
    git remote add origin "$gitlab_url"
    
    echo ""
    echo "Setting main branch..."
    git branch -M main
    
    echo ""
    echo "Ready to push! Run this command:"
    echo ""
    echo "    git push -u origin main"
    echo ""
    echo "You may be prompted for your GitLab username and password/token"
    echo ""
    read -p "Push to GitLab now? (y/n): " should_push
    
    if [ "$should_push" = "y" ] || [ "$should_push" = "Y" ]; then
        echo ""
        echo "Pushing to GitLab..."
        git push -u origin main
        echo ""
        echo "✓ Successfully pushed to GitLab!"
        echo ""
        echo "Your repository is now available at:"
        echo "$gitlab_url"
    else
        echo ""
        echo "Skipped push. You can push later with:"
        echo "    git push -u origin main"
    fi
else
    echo ""
    echo "GitLab URL not provided. You can add it later with:"
    echo "    git remote add origin YOUR_GITLAB_URL"
    echo "    git branch -M main"
    echo "    git push -u origin main"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
