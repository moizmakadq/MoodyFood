# 🚀 GitHub Setup Guide for Moodyfood

This guide will help you push your Moodyfood project to GitHub.

---

## 📋 Prerequisites

- [x] Git installed (version 2.52.0.windows.1 ✓)
- [ ] GitHub account created
- [ ] GitHub repository created (optional - can be done via CLI)

---

## 🔧 Step-by-Step Instructions

### Step 1: Initialize Git Repository (if not already done)

```bash
cd "d:\Mtech Nirma University\AML\AML Project\Moodyfood"
git init
```

### Step 2: Configure Git (First Time Only)

```bash
# Set your name and email (use your GitHub email)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --global --list
```

### Step 3: Add Files to Git

```bash
# Add all files (respecting .gitignore)
git add .

# Check what will be committed
git status
```

### Step 4: Create Initial Commit

```bash
git commit -m "Initial commit: Moodyfood AI-powered food recommendation system"
```

### Step 5: Create GitHub Repository

**Option A: Via GitHub Website (Recommended for beginners)**
1. Go to https://github.com
2. Click the "+" icon in top-right corner
3. Select "New repository"
4. Repository name: `moodyfood` (or `Moodyfood`)
5. Description: "AI-powered food recommendation system using emotion detection"
6. Choose: Public or Private
7. **DO NOT** initialize with README, .gitignore, or license (we already have these)
8. Click "Create repository"

**Option B: Via GitHub CLI (if installed)**
```bash
gh repo create moodyfood --public --source=. --remote=origin
```

### Step 6: Connect Local Repository to GitHub

After creating the repository on GitHub, you'll see instructions. Use these commands:

```bash
# Add remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/moodyfood.git

# Verify remote
git remote -v
```

### Step 7: Push to GitHub

```bash
# Push to main branch (or master, depending on your default)
git branch -M main
git push -u origin main
```

If you get an authentication error, you'll need to authenticate using one of these methods:
- **Personal Access Token (PAT)** - Recommended
- **SSH Key**
- **GitHub CLI**

---

## 🔐 Authentication Methods

### Method 1: Personal Access Token (PAT)

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "Moodyfood Project"
4. Select scopes: `repo` (full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)
7. When pushing, use the token as your password:
   ```bash
   Username: your_github_username
   Password: ghp_xxxxxxxxxxxxxxxxxxxx (your token)
   ```

### Method 2: SSH Key (More Secure)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
# Then change remote URL:
git remote set-url origin git@github.com:YOUR_USERNAME/moodyfood.git
```

### Method 3: GitHub CLI

```bash
# Install GitHub CLI from https://cli.github.com/
# Then authenticate:
gh auth login
```

---

## 📝 Common Git Commands

### Check Status
```bash
git status
```

### Add Changes
```bash
# Add specific file
git add filename.py

# Add all changes
git add .
```

### Commit Changes
```bash
git commit -m "Your commit message"
```

### Push Changes
```bash
git push
```

### Pull Latest Changes
```bash
git pull
```

### View Commit History
```bash
git log --oneline
```

### Create New Branch
```bash
git checkout -b feature/new-feature
```

### Switch Branches
```bash
git checkout main
```

---

## 🎯 Quick Command Sequence

Here's the complete sequence to push your code:

```bash
# 1. Navigate to project directory
cd "d:\Mtech Nirma University\AML\AML Project\Moodyfood"

# 2. Initialize git (if needed)
git init

# 3. Add all files
git add .

# 4. Commit
git commit -m "Initial commit: Moodyfood AI-powered food recommendation system"

# 5. Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/moodyfood.git

# 6. Push to GitHub
git branch -M main
git push -u origin main
```

---

## ⚠️ Important Notes

### Files That Won't Be Pushed (in .gitignore)
- `venv/` - Virtual environment
- `__pycache__/` - Python cache files
- `*.db` - Database files (if uncommented in .gitignore)
- `logs/*.log` - Log files
- `models/*.h5` - Large model files
- `.vscode/`, `.idea/` - IDE settings

### Database Consideration
Currently, `database/*.db` is **NOT** ignored, so your database will be pushed. If you want to exclude it:

```bash
# Edit .gitignore and uncomment this line:
database/*.db

# Then remove from git if already tracked:
git rm --cached database/food_recommendation.db
git commit -m "Remove database from version control"
```

### Large Files Warning
If you have files larger than 100MB, GitHub will reject them. Use Git LFS:

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.h5"
git lfs track "*.pb"

# Add .gitattributes
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

---

## 🔄 Updating Your Repository

After making changes:

```bash
# 1. Check what changed
git status

# 2. Add changes
git add .

# 3. Commit with descriptive message
git commit -m "Add new feature: XYZ"

# 4. Push to GitHub
git push
```

---

## 🆘 Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/moodyfood.git
```

### Error: "failed to push some refs"
```bash
# Pull first, then push
git pull origin main --rebase
git push
```

### Error: "Authentication failed"
- Use Personal Access Token instead of password
- Or set up SSH authentication

### Error: "large files detected"
```bash
# Use Git LFS for files > 100MB
git lfs install
git lfs track "*.h5"
```

---

## ✅ Verification

After pushing, verify your repository:

1. Go to `https://github.com/YOUR_USERNAME/moodyfood`
2. Check that all files are present
3. Verify README.md displays correctly
4. Check that .gitignore is working (venv/ should not be there)

---

## 🎉 Next Steps

After successfully pushing to GitHub:

1. **Update README.md** with your actual GitHub username
2. **Add Topics** to your repository (Python, AI, Machine Learning, Streamlit, etc.)
3. **Create a LICENSE file** (MIT License recommended)
4. **Add repository description** on GitHub
5. **Enable GitHub Pages** (optional, for documentation)
6. **Set up GitHub Actions** (optional, for CI/CD)
7. **Add collaborators** if working in a team

---

## 📚 Additional Resources

- [GitHub Docs](https://docs.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [GitHub Desktop](https://desktop.github.com/) - GUI alternative
- [Git LFS](https://git-lfs.github.com/) - For large files

---

**Good luck with your GitHub push! 🚀**
