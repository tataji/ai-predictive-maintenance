# How to Upload to GitLab - Step by Step Guide

This guide will walk you through uploading the AI Predictive Maintenance System to GitLab.

## Prerequisites

- GitLab account (free at https://gitlab.com)
- Git installed on your computer
- The project files downloaded

## Method 1: Automated Script (Easiest)

### Step 1: Run the Upload Script
```bash
cd ai-predictive-maintenance
chmod +x upload-to-gitlab.sh
./upload-to-gitlab.sh
```

The script will:
1. Initialize Git repository
2. Configure your Git user
3. Add all files
4. Create initial commit
5. Guide you through adding GitLab remote
6. Optionally push to GitLab

### Step 2: Create GitLab Repository
When prompted by the script:
1. Go to https://gitlab.com/projects/new
2. Fill in:
   - **Project name**: ai-predictive-maintenance
   - **Visibility**: Private (or Public if you want)
   - **Initialize with README**: ❌ UNCHECK THIS
3. Click "Create project"
4. Copy the repository URL shown (e.g., `https://gitlab.com/yourusername/ai-predictive-maintenance.git`)
5. Paste it into the script when prompted

### Step 3: Push to GitLab
The script will offer to push. Choose 'y' and enter your GitLab credentials when prompted.

---

## Method 2: Manual Upload (Full Control)

### Step 1: Create GitLab Repository

1. **Go to GitLab**: https://gitlab.com
2. **Sign in** or create account
3. **Click** the "+" icon → "New project/repository"
4. **Select** "Create blank project"
5. **Fill in**:
   ```
   Project name: ai-predictive-maintenance
   Project URL: [your-username]/ai-predictive-maintenance
   Visibility: Private (recommended) or Public
   
   IMPORTANT: Uncheck "Initialize repository with a README"
   ```
6. **Click** "Create project"

### Step 2: Initialize Git Locally

Open terminal in the project folder:

```bash
cd ai-predictive-maintenance

# Initialize Git repository
git init

# Configure your identity (if not done globally)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: AI Predictive Maintenance System

Complete implementation with:
- FastAPI backend with ML anomaly detection
- Real-time monitoring dashboard
- WebSocket support
- Complete API documentation
- Docker deployment ready
- Production-ready codebase"
```

### Step 3: Connect to GitLab

Replace `YOUR_USERNAME` with your GitLab username:

```bash
# Add GitLab as remote origin
git remote add origin https://gitlab.com/YOUR_USERNAME/ai-predictive-maintenance.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitLab
git push -u origin main
```

### Step 4: Enter Credentials

When prompted:
- **Username**: Your GitLab username
- **Password**: Your GitLab password OR Personal Access Token (recommended)

---

## Method 3: Using GitLab Personal Access Token (Most Secure)

### Why Use a Token?
- More secure than password
- Can be revoked anytime
- Required if you have 2FA enabled

### Create Personal Access Token

1. **Go to** GitLab → Avatar → Settings
2. **Click** "Access Tokens" (left sidebar)
3. **Fill in**:
   ```
   Token name: ai-maintenance-upload
   Expiration date: [choose or leave blank]
   Scopes: ✓ api, ✓ write_repository
   ```
4. **Click** "Create personal access token"
5. **Copy** the token (you won't see it again!)

### Use Token to Push

```bash
# When prompted for password, use your token instead
git push -u origin main

# Username: your-gitlab-username
# Password: [paste your token here]
```

### Store Credentials (Optional)

To avoid entering credentials every time:

```bash
# Linux/Mac - store credentials
git config --global credential.helper store

# Windows - use credential manager
git config --global credential.helper manager

# After first successful push, credentials are saved
```

---

## Method 4: Using SSH Keys (Advanced)

### Step 1: Generate SSH Key (if you don't have one)

```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Press Enter to accept default location
# Enter passphrase (optional but recommended)

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519
```

### Step 2: Add SSH Key to GitLab

```bash
# Copy your public key
cat ~/.ssh/id_ed25519.pub
```

1. Go to GitLab → Avatar → Settings → SSH Keys
2. Paste the key
3. Give it a title (e.g., "My Laptop")
4. Click "Add key"

### Step 3: Use SSH URL

```bash
# Remove HTTPS remote if already added
git remote remove origin

# Add SSH remote
git remote add origin git@gitlab.com:YOUR_USERNAME/ai-predictive-maintenance.git

# Push
git push -u origin main
```

---

## Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://gitlab.com/YOUR_USERNAME/ai-predictive-maintenance.git
```

### Error: "failed to push some refs"
```bash
# If GitLab repo was initialized with README
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Error: "Authentication failed"
- Check username spelling
- Use Personal Access Token instead of password
- Verify token has correct permissions

### Error: "Permission denied (publickey)"
- SSH key not added to GitLab
- SSH key not loaded in agent: `ssh-add ~/.ssh/id_ed25519`

### Large files warning
```bash
# If you get warnings about large files (>100MB)
# Use Git LFS or remove from tracking:
git rm --cached path/to/large/file
echo "path/to/large/file" >> .gitignore
git commit -m "Remove large file"
```

---

## Verify Upload

After successful push:

1. **Visit** your GitLab repository
2. **Check** all files are present:
   - backend/
   - frontend/
   - Documentation files (.md)
   - Configuration files

3. **Verify** README displays properly

---

## Make Repository Public (Optional)

To share your project:

1. Go to repository → Settings → General
2. Expand "Visibility, project features, permissions"
3. Change "Project visibility" to Public
4. Click "Save changes"

---

## Add GitLab CI/CD (Optional)

Create `.gitlab-ci.yml` for automated testing:

```yaml
image: python:3.9

stages:
  - test
  - build

test:
  stage: test
  script:
    - cd backend
    - pip install -r requirements.txt
    - python -m pytest

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t maintenance-system .
```

---

## Clone Repository Later

To clone on another machine:

```bash
# HTTPS
git clone https://gitlab.com/YOUR_USERNAME/ai-predictive-maintenance.git

# SSH
git clone git@gitlab.com:YOUR_USERNAME/ai-predictive-maintenance.git
```

---

## Update Repository Later

After making changes:

```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Description of changes"

# Push
git push origin main
```

---

## Summary Commands

**Quick upload (after creating empty GitLab repo):**
```bash
cd ai-predictive-maintenance
git init
git add .
git commit -m "Initial commit"
git remote add origin https://gitlab.com/YOUR_USERNAME/ai-predictive-maintenance.git
git branch -M main
git push -u origin main
```

**Using the automated script:**
```bash
./upload-to-gitlab.sh
```

---

## Need Help?

- GitLab Documentation: https://docs.gitlab.com/ee/user/project/repository/
- Git Basics: https://git-scm.com/book/en/v2/Getting-Started-Git-Basics
- SSH Keys: https://docs.gitlab.com/ee/user/ssh.html

---

**Your repository will be available at:**
`https://gitlab.com/YOUR_USERNAME/ai-predictive-maintenance`
