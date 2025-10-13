# GitHub Project Management - Setup Guide

این راهنما مراحل setup کامل GitHub Project Management System را شرح می‌دهد.

---

## 📋 Prerequisites

- GitHub repository: `aminak58/freqai-futures-strategy`
- GitHub Personal Access Token با دسترسی‌های:
  - `repo` (full control)
  - `workflow` (update GitHub Actions)
  - `admin:org` (if using GitHub Projects)
- Python 3.11+
- PyGithub installed: `pip install PyGithub`

---

## 🚀 Quick Setup (Day 1)

### Step 1: Install Dependencies

```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Install dev dependencies (includes PyGithub)
pip install -r requirements-dev.txt
```

### Step 2: Set GitHub Token

```powershell
# Set environment variable (current session)
$env:GITHUB_TOKEN="ghp_your_token_here"

# Or set permanently (Windows)
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN', 'ghp_your_token_here', 'User')
```

**To create a token:**
1. GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)
2. Generate new token (classic)
3. Select scopes: `repo`, `workflow`, `admin:org`
4. Copy token (you won't see it again!)

### Step 3: Create Milestones (All 16 Sprints)

```powershell
python scripts/create_milestones.py
```

**Expected output:**
```
✅ Created milestone: Sprint 1 (due 2025-10-27)
✅ Created milestone: Sprint 2 (due 2025-11-10)
...
✅ Created milestone: Sprint 16 (due 2026-08-25)

📊 Summary: Created 16 milestones, Skipped 0
```

### Step 4: Create Sprint 2 Issues

```powershell
python scripts/create_sprint_issues.py --sprint 2
```

**Expected output:**
```
ℹ️  Milestone 'Sprint 2' already exists
✅ Created issue #XX: [US 1.4] Increase Test Coverage to 60%+
✅ Created issue #YY: [US 1.5] Documentation Update

📊 Summary: Created 2/2 issues for Sprint 2
```

### Step 5: Configure GitHub (Manual Steps)

#### 5.1 Create Project Board

1. Go to: https://github.com/aminak58/freqai-futures-strategy/projects
2. Click "New project"
3. Choose "Board" template
4. Name: "FreqAI RL Integration - Sprint Tracking"
5. Add columns:
   - **Backlog** (default)
   - **Sprint Backlog**
   - **In Progress**
   - **In Review**
   - **Testing**
   - **Done**

#### 5.2 Add Issues to Project

1. In Project board, click "+ Add item"
2. Search for Sprint 2 issues
3. Add both US 1.4 and US 1.5
4. Move to "Sprint Backlog" column

#### 5.3 Configure Branch Protection

1. Go to: Settings > Branches
2. Add rule for `master`:
   - Branch name pattern: `master`
   - ✅ Require a pull request before merging
     - ✅ Require approvals: 1
   - ✅ Require status checks to pass before merging
     - ✅ Require branches to be up to date
     - Add required checks:
       - `lint`
       - `security`
       - `test`
       - `coverage-check`
       - `build`
   - ✅ Include administrators
   - Click "Create"

3. Add rule for `sprint-*`:
   - Branch name pattern: `sprint-*`
   - ✅ Require status checks to pass
     - Add: `test`, `lint`
   - Click "Create"

#### 5.4 Enable GitHub Actions

1. Go to: Actions tab
2. If prompted, click "I understand my workflows, go ahead and enable them"
3. Verify CI workflow appears

### Step 6: Test CI Pipeline

```powershell
# Create test branch
git checkout master
git pull origin master
git checkout -b test-ci-setup

# Make a small change
"# CI Test" | Out-File -Append -Encoding utf8 README.md

# Commit and push
git add README.md
git commit -m "test: CI pipeline setup"
git push origin test-ci-setup
```

#### Create Pull Request:
1. Go to GitHub > Pull requests > New pull request
2. Base: `master`, Compare: `test-ci-setup`
3. Create pull request
4. Wait for CI checks to complete

**Expected:** All 5 checks pass ✅
- `lint` ✅
- `security` ✅
- `test` ✅
- `coverage-check` ✅
- `build` ✅

If all pass:
1. Merge PR
2. Delete `test-ci-setup` branch

---

## 🔧 Configuration Files Created

### Issue Templates
- `.github/ISSUE_TEMPLATE/user_story.md` - User story template
- `.github/ISSUE_TEMPLATE/bug_report.md` - Bug report template
- `.github/ISSUE_TEMPLATE/retrospective.md` - Sprint retrospective template

### PR Template
- `.github/PULL_REQUEST_TEMPLATE.md` - Pull request checklist

### GitHub Actions
- `.github/workflows/ci.yml` - CI pipeline (lint, test, coverage, security)

### Scripts
- `scripts/create_milestones.py` - Create all 16 sprint milestones
- `scripts/create_sprint_issues.py` - Create issues for a sprint
- `scripts/sprint_burndown.py` - Generate burndown report
- `scripts/velocity_tracking.py` - Track team velocity

---

## 📊 Daily Usage

### Starting Work on an Issue

```powershell
# 1. Assign yourself to issue in GitHub UI
# 2. Add "in-progress" label
# 3. Create feature branch
git checkout master
git pull origin master
git checkout -b feature/us-1-4-coverage

# 4. Write code + tests
# ... your work ...

# 5. Run tests locally
pytest tests/ -v --cov=src --cov=diagnostics --cov=monitoring

# 6. Commit and push
git add .
git commit -m "[US 1.4] Add strategy tests, coverage 55%"
git push origin feature/us-1-4-coverage

# 7. Create PR in GitHub UI
# - Link to issue: "Closes #XX"
# - Fill in PR template checklist
# - Request review
```

### Checking Sprint Progress

```powershell
# Burndown report
python scripts/sprint_burndown.py --sprint 2

# Velocity tracking
python scripts/velocity_tracking.py
```

---

## 🎯 Sprint 2 Workflow

### Week 1 (Oct 28 - Nov 3)

**Monday:**
- Issues created ✅
- Team assigned ✅
- Sprint planning meeting

**Tuesday-Friday:**
- Work on US 1.4 (Test Coverage)
- Daily commits
- CI checks passing

### Week 2 (Nov 4 - Nov 10)

**Monday-Wednesday:**
- Complete US 1.4
- Start US 1.5 (Documentation)

**Thursday:**
- Finish US 1.5
- Create PR for final review

**Friday:**
- Merge all PRs
- Verify coverage ≥ 60%
- Sprint retrospective
- Create Sprint 3 issues

---

## 📈 Metrics to Track

### Per Sprint:
- **Story Points**: Planned vs Completed
- **Velocity**: Points completed per sprint
- **Coverage**: Test coverage %
- **Cycle Time**: Days from "In Progress" to "Done"
- **Lead Time**: Days from issue creation to done

### Overall Project:
- **Cumulative Flow**: Story points over time
- **Burnup Chart**: Progress toward 159 total points
- **Quality**: Bugs per sprint, test failures

---

## 🔍 Troubleshooting

### PyGithub Import Error

```powershell
pip install --upgrade PyGithub
```

### GitHub Token Expired

1. Generate new token in GitHub settings
2. Update environment variable:
```powershell
$env:GITHUB_TOKEN="ghp_new_token_here"
```

### CI Checks Failing

**Linting errors:**
```powershell
black src/ tests/ diagnostics/ monitoring/
flake8 src/ tests/ diagnostics/ monitoring/ --max-line-length=120
```

**Coverage below target:**
```powershell
# Check current coverage
pytest tests/ --cov=src --cov=diagnostics --cov=monitoring --cov-report=term

# Add more tests until ≥ 60%
```

**Tests failing:**
```powershell
# Run specific test
pytest tests/test_evaluation_protocol.py -v

# Debug with pdb
pytest tests/test_evaluation_protocol.py --pdb
```

---

## 📝 Creating Issues for New Sprints

To add Sprint 3+ issues, edit `scripts/create_sprint_issues.py`:

```python
SPRINT_STORIES = {
    2: [...],  # Sprint 2 (existing)
    3: [       # Add Sprint 3
        {
            "title": "[US 2.1] Contextual Bandit Model",
            "body": """...""",
            "labels": ["user-story", "p0-critical", "sprint-3", "epic-2-bandit"],
            "milestone": "Sprint 3",
            "assignees": ["aminak58"],
        },
        # ... more stories
    ],
}
```

Then run:
```powershell
python scripts/create_sprint_issues.py --sprint 3
```

---

## 🎓 Best Practices

### Commit Messages
```
[US 1.4] Add strategy entry/exit tests
[US 1.5] Update UNIFIED_ARCHITECTURE.md
[Bug] Fix governance halt test
[Refactor] Extract test fixtures
```

### PR Titles
```
[US 1.4] Increase test coverage to 60%+
[US 1.5] Documentation update
[Bug #XX] Fix strategy backtest error
```

### Branch Names
```
feature/us-1-4-coverage
feature/us-1-5-docs
bugfix/governance-halt-issue-XX
hotfix/critical-trading-bug
```

---

## ✅ Setup Complete!

**Verify everything is working:**
- [ ] All 16 milestones created
- [ ] Sprint 2 issues created (2 issues)
- [ ] Issues added to project board
- [ ] Branch protection enabled
- [ ] CI pipeline runs on PR
- [ ] Test PR merged successfully

**You're ready to start Sprint 2!** 🚀

---

## 📚 Next Steps

1. **Start Sprint 2**: Begin work on US 1.4 (Test Coverage)
2. **Daily Updates**: Update issue comments with progress
3. **Weekly Check-ins**: Run burndown/velocity scripts
4. **Sprint End**: Retrospective + prepare Sprint 3

**Full Documentation:**
- `GITHUB_PROJECT_MANAGEMENT.md` - Complete system overview
- `FUTURE_SPRINTS_ROADMAP.md` - 16-sprint roadmap
- `SCRUM_FRAMEWORK.md` - Scrum process details
