# Git Flow Workflow Guide

## Overview

This project follows the **Git Flow** branching model, a robust workflow designed for projects with scheduled releases. This workflow provides a clear separation between development work and production-ready code.

## Branch Structure

### Main Branches

- **`main`** - Production-ready code, stable releases only
- **`develop`** - Integration branch for ongoing development

### Branch Purposes

| Branch | Purpose | Merge Target | Lifetime |
|--------|---------|--------------|----------|
| `main` | Production releases | - | Permanent |
| `develop` | Development integration | `main` | Permanent |
| `feature/*` | New features | `develop` | Temporary |
| `hotfix/*` | Production bug fixes | `main` & `develop` | Temporary |

## Daily Development Workflow

### 1. Working on Features

All development happens on the `develop` branch or feature branches:

```bash
# Start working (ensure you're on develop)
git checkout develop
git pull origin develop

# Make your changes
# Edit files...

# Commit your work
git add .
git commit -m "feat: add user authentication system"
git push origin develop
```

### 2. Feature Branch Workflow (Recommended for larger features)

```bash
# Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/user-dashboard

# Work on your feature
git add .
git commit -m "feat: implement user dashboard layout"
git push -u origin feature/user-dashboard

# When feature is complete, merge back to develop
git checkout develop
git pull origin develop
git merge feature/user-dashboard
git push origin develop

# Clean up
git branch -d feature/user-dashboard
git push origin --delete feature/user-dashboard
```

## Release Workflow

### Creating a Release

When `develop` is stable and ready for production:

```bash
# 1. Switch to main and ensure it's up to date
git checkout main
git pull origin main

# 2. Merge develop into main
git merge develop

# 3. Push to production
git push origin main

# 4. Tag the release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 5. Return to develop for continued development
git checkout develop
```

## Hotfix Workflow

For critical production bugs that need immediate fixes:

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug-fix

# 2. Fix the issue
git add .
git commit -m "hotfix: resolve critical authentication bug"

# 3. Merge into main
git checkout main
git merge hotfix/critical-bug-fix
git push origin main

# 4. Tag the hotfix
git tag -a v1.0.1 -m "Hotfix version 1.0.1"
git push origin v1.0.1

# 5. Merge into develop to keep it up to date
git checkout develop
git merge hotfix/critical-bug-fix
git push origin develop

# 6. Clean up
git branch -d hotfix/critical-bug-fix
```

## Commit Message Standards

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples:
```bash
git commit -m "feat: add user registration endpoint"
git commit -m "fix: resolve login validation issue"
git commit -m "docs: update API documentation"
git commit -m "refactor: optimize database queries"
```

## Branch Protection Rules

### Main Branch
- Requires pull request reviews
- Requires status checks to pass
- No direct pushes (except for hotfixes)
- Requires up-to-date branches before merging

### Develop Branch
- Direct pushes allowed for team members
- Requires status checks to pass

## Best Practices

### Do's ✅
- Keep commits atomic and focused
- Write clear, descriptive commit messages
- Regularly sync with `origin/develop`
- Test your code before committing
- Use feature branches for complex features
- Tag all releases with semantic versioning

### Don'ts ❌
- Don't commit directly to `main`
- Don't force push to shared branches
- Don't commit broken code to `develop`
- Don't use generic commit messages like "fix"
- Don't leave feature branches open indefinitely

## Quick Reference Commands

### Daily Commands
```bash
# Check current status
git status

# See all branches
git branch -a

# Switch branches
git checkout develop
git checkout main

# Sync with remote
git pull origin develop

# Push changes
git push origin develop
```

### Release Commands
```bash
# Create release
git checkout main
git pull origin main
git merge develop
git push origin main
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
git checkout develop
```

## Troubleshooting

### Common Issues

**Merge Conflicts:**
```bash
# When conflicts occur during merge
git status  # See conflicted files
# Edit files to resolve conflicts
git add .
git commit -m "resolve merge conflicts"
```

**Accidentally committed to wrong branch:**
```bash
# Move last commit to correct branch
git log --oneline -n 5  # Find commit hash
git checkout correct-branch
git cherry-pick <commit-hash>
git checkout wrong-branch
git reset --hard HEAD~1
```

## Getting Help

- Review this document for workflow questions
- Use `git help <command>` for Git command help
- Check Git status frequently with `git status`
- When in doubt, create a feature branch

---

**Remember:** This workflow keeps our codebase stable while allowing continuous development. The `main` branch should always be deployable, and `develop` should be our integration point for new features.
