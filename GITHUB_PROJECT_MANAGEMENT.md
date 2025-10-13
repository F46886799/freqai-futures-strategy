# GitHub Project Management System

**تاریخ:** 13 اکتبر 2025  
**پروژه:** FreqAI Futures Strategy - RL Integration  
**هدف:** تبدیل roadmap به یک سیستم trackable و enforceable

---

## 🎯 چالش

**مشکل:** Roadmap فعلی فقط یک سند است. هیچ enforcement یا tracking واقعی ندارد.

**راه‌حل:** استفاده از قابلیت‌های GitHub برای ایجاد یک سیستم کامل:
- ✅ **Trackability**: هر task قابل پیگیری
- ✅ **Accountability**: مشخص است چه کسی مسئول چیست
- ✅ **Automation**: CI/CD و GitHub Actions خودکارسازی
- ✅ **Enforcement**: Branch protection + required checks
- ✅ **Visibility**: Dashboards, reports, metrics

---

## 🏗️ معماری سیستم

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Project Board                      │
│                  (Kanban for Sprint Tracking)                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Milestones                         │
│           (Sprint 1, Sprint 2, ..., Sprint 16)              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Issues                            │
│      (User Stories with labels, assignees, checklists)      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Pull Requests + Review                      │
│           (Code changes linked to issues)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    CI/CD Pipeline                            │
│   (Tests, Coverage, Linting, Security Scans)                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Branch Protection Rules                     │
│   (Enforce: Tests pass, Coverage ≥ target, Review approved) │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Merge to Master                          │
│                  (Automated deployment)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Component 1: GitHub Issues (User Stories)

### Issue Template: User Story

**فایل:** `.github/ISSUE_TEMPLATE/user_story.md`

```markdown
---
name: User Story
about: Template for a user story in the sprint
title: '[US X.Y] '
labels: user-story
assignees: ''
---

## User Story

**As a** [role]  
**I want** [feature]  
**So that** [benefit]

## Details

**Sprint:** Sprint X  
**Epic:** Epic X - [Name]  
**Story Points:** X  
**Priority:** P0/P1/P2/P3

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Tasks

- [ ] Task 1: Description
- [ ] Task 2: Description
- [ ] Task 3: Description

## Testing Requirements

- [ ] Unit tests written (coverage ≥ X%)
- [ ] Integration tests written
- [ ] Manual testing completed
- [ ] Edge cases covered

## Documentation

- [ ] Code comments added
- [ ] API documentation updated
- [ ] User guide updated
- [ ] Architecture diagrams updated (if applicable)

## Definition of Done

- [ ] All acceptance criteria met
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Coverage target met
- [ ] Documentation complete
- [ ] No regressions introduced
- [ ] Deployed to staging (if applicable)

## Related Issues

- Depends on: #XXX
- Blocks: #XXX
- Related to: #XXX

## Notes

[Additional notes, design decisions, etc.]
```

### Labels System

```yaml
# Epic Labels
epic-1-foundation: "#0052CC"
epic-2-bandit: "#00875A"
epic-3-actor-critic: "#FF5630"
epic-4-production: "#6554C0"

# Type Labels
user-story: "#FFC400"
bug: "#DE350B"
enhancement: "#36B37E"
documentation: "#0747A6"
technical-debt: "#FF8B00"

# Priority Labels
p0-critical: "#DE350B"
p1-high: "#FF8B00"
p2-medium: "#FFC400"
p3-low: "#36B37E"

# Status Labels
in-progress: "#0052CC"
blocked: "#FF5630"
needs-review: "#FFAB00"
ready-to-merge: "#00875A"

# Sprint Labels
sprint-1: "#E3FCEF"
sprint-2: "#E3FCEF"
# ... sprint-16

# Component Labels
component-strategy: "#DFE1E6"
component-governance: "#DFE1E6"
component-rl: "#DFE1E6"
component-evaluation: "#DFE1E6"
component-monitoring: "#DFE1E6"
component-ci-cd: "#DFE1E6"
```

### Issue Creation Script

**فایل:** `scripts/create_sprint_issues.py`

```python
#!/usr/bin/env python3
"""
Create GitHub Issues for all User Stories in a Sprint
"""

import os
import yaml
from github import Github

# Load sprint data
SPRINT_2_STORIES = [
    {
        "title": "[US 1.4] Increase Test Coverage to 60%+",
        "body": """
## User Story

**As a** developer  
**I want** test coverage increased to 60%+  
**So that** code quality is high before RL integration

## Details

**Sprint:** Sprint 2  
**Epic:** Epic 1 - Foundation  
**Story Points:** 13  
**Priority:** P1

## Acceptance Criteria

- [ ] Overall coverage ≥ 60%
- [ ] Strategy coverage ≥ 60%
- [ ] Governance coverage ≥ 80%
- [ ] All critical paths tested

## Technical Tasks

- [ ] Test strategy entry/exit logic
- [ ] Test gating funnel
- [ ] Test governance integration
- [ ] Test regime detection
- [ ] Test edge cases (empty dataframes)
- [ ] Test governance halt scenarios
- [ ] Test extreme market conditions
- [ ] Integration test: full backtest workflow
- [ ] Integration test: FreqAI pipeline

## Testing Requirements

- [ ] Unit tests for all strategy methods
- [ ] Edge case tests
- [ ] Integration tests
- [ ] Coverage report generated

## Documentation

- [ ] Test documentation updated
- [ ] Coverage report in docs/

## Definition of Done

- [ ] Coverage ≥ 60% overall
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Coverage report committed
""",
        "labels": ["user-story", "p1-high", "sprint-2", "epic-1-foundation", "component-strategy"],
        "milestone": "Sprint 2",
        "assignees": ["aminak58"],
    },
    {
        "title": "[US 1.5] Documentation Update",
        "body": """
## User Story

**As a** team member  
**I want** all documentation up-to-date  
**So that** new contributors can understand the project

## Details

**Sprint:** Sprint 2  
**Epic:** Epic 1 - Foundation  
**Story Points:** 5  
**Priority:** P2

## Acceptance Criteria

- [ ] All docs in docs/guides/ updated
- [ ] All docs in docs/architecture/ updated
- [ ] RL_INTEGRATION_PLAN.md created
- [ ] No broken links

## Technical Tasks

- [ ] Update CI_CD_GUIDE.md
- [ ] Update DEVELOPMENT_GUIDE.md
- [ ] Update CURRENT_STATUS.md
- [ ] Update UNIFIED_ARCHITECTURE.md
- [ ] Review LSTM/MVP docs
- [ ] Create RL_INTEGRATION_PLAN.md
- [ ] Fix broken links
- [ ] Update README.md

## Documentation

- [ ] All guides up-to-date
- [ ] Architecture diagrams current
- [ ] RL roadmap documented

## Definition of Done

- [ ] All docs updated
- [ ] No broken links
- [ ] RL plan documented
- [ ] Code reviewed
""",
        "labels": ["user-story", "p2-medium", "sprint-2", "epic-1-foundation", "documentation"],
        "milestone": "Sprint 2",
        "assignees": ["aminak58"],
    },
]


def create_issues(repo_name: str, token: str):
    """Create GitHub Issues from sprint data"""
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    # Create milestone if doesn't exist
    try:
        milestone = repo.create_milestone("Sprint 2", due_on="2025-11-10")
        print(f"✅ Created milestone: Sprint 2")
    except:
        milestones = repo.get_milestones(state="open")
        milestone = next((m for m in milestones if m.title == "Sprint 2"), None)
        print(f"ℹ️  Milestone 'Sprint 2' already exists")
    
    # Create issues
    for story in SPRINT_2_STORIES:
        issue = repo.create_issue(
            title=story["title"],
            body=story["body"],
            labels=story["labels"],
            milestone=milestone,
            assignees=story.get("assignees", []),
        )
        print(f"✅ Created issue #{issue.number}: {story['title']}")


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN not set")
        exit(1)
    
    create_issues("aminak58/freqai-futures-strategy", token)
```

**استفاده:**
```bash
# Set token (یکبار)
$env:GITHUB_TOKEN="ghp_your_token_here"

# Create issues for Sprint 2
python scripts/create_sprint_issues.py
```

---

## 📊 Component 2: GitHub Projects (Kanban Board)

### Project Structure

**نام Project:** FreqAI RL Integration - 16 Sprint Roadmap

**Columns:**
1. **Backlog** - User stories not yet started
2. **Sprint Backlog** - Current sprint stories
3. **In Progress** - Actively being worked on
4. **In Review** - PR open, awaiting review
5. **Testing** - Tests being written/run
6. **Done** - Merged to master

### Automation Rules

**GitHub Actions:** `.github/workflows/project_automation.yml`

```yaml
name: Project Automation

on:
  issues:
    types: [opened, closed, labeled, unlabeled]
  pull_request:
    types: [opened, closed, ready_for_review]

jobs:
  automate-project:
    runs-on: ubuntu-latest
    steps:
      - name: Move issue to Sprint Backlog
        if: github.event.action == 'labeled' && contains(github.event.label.name, 'sprint-')
        uses: alex-page/github-project-automation-plus@v0.8.3
        with:
          project: FreqAI RL Integration
          column: Sprint Backlog
          repo-token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Move issue to In Progress
        if: github.event.action == 'labeled' && github.event.label.name == 'in-progress'
        uses: alex-page/github-project-automation-plus@v0.8.3
        with:
          project: FreqAI RL Integration
          column: In Progress
          repo-token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Move PR to In Review
        if: github.event.action == 'ready_for_review'
        uses: alex-page/github-project-automation-plus@v0.8.3
        with:
          project: FreqAI RL Integration
          column: In Review
          repo-token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Move to Done on merge
        if: github.event.action == 'closed' && github.event.pull_request.merged == true
        uses: alex-page/github-project-automation-plus@v0.8.3
        with:
          project: FreqAI RL Integration
          column: Done
          repo-token: ${{ secrets.GITHUB_TOKEN }}
```

---

## 🎯 Component 3: GitHub Milestones (Sprint Tracking)

### Milestone Creation Script

**فایل:** `scripts/create_milestones.py`

```python
#!/usr/bin/env python3
"""Create GitHub Milestones for all 16 sprints"""

import os
from datetime import datetime
from github import Github

SPRINTS = [
    {"title": "Sprint 1", "due_date": "2025-10-27", "description": "Foundation: Evaluation + Signal Audit + Baseline"},
    {"title": "Sprint 2", "due_date": "2025-11-10", "description": "Foundation: Test Coverage 60%+ + Documentation"},
    {"title": "Sprint 3", "due_date": "2026-01-19", "description": "Contextual Bandit: Model Foundation"},
    {"title": "Sprint 4", "due_date": "2026-02-02", "description": "Contextual Bandit: Replay Buffer"},
    {"title": "Sprint 5", "due_date": "2026-02-16", "description": "Contextual Bandit: Offline Training"},
    {"title": "Sprint 6", "due_date": "2026-03-02", "description": "Contextual Bandit: FreqAI Integration + A/B Testing"},
    {"title": "Sprint 7", "due_date": "2026-03-16", "description": "Contextual Bandit: Validation"},
    {"title": "Sprint 8", "due_date": "2026-04-20", "description": "Actor-Critic: Architecture (Part 1)"},
    {"title": "Sprint 9", "due_date": "2026-05-03", "description": "Actor-Critic: Architecture (Part 2)"},
    {"title": "Sprint 10", "due_date": "2026-05-17", "description": "Actor-Critic: PPO Training"},
    {"title": "Sprint 11", "due_date": "2026-05-31", "description": "Actor-Critic: Online Fine-tuning"},
    {"title": "Sprint 12", "due_date": "2026-06-14", "description": "Actor-Critic: Validation"},
    {"title": "Sprint 13", "due_date": "2026-07-12", "description": "Production: Gradual Rollout (Part 1)"},
    {"title": "Sprint 14", "due_date": "2026-07-28", "description": "Production: Gradual Rollout (Part 2)"},
    {"title": "Sprint 15", "due_date": "2026-08-11", "description": "Production: Monitoring & Alerting"},
    {"title": "Sprint 16", "due_date": "2026-08-25", "description": "Production: Documentation"},
]


def create_milestones(repo_name: str, token: str):
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    for sprint in SPRINTS:
        try:
            due_date = datetime.strptime(sprint["due_date"], "%Y-%m-%d")
            milestone = repo.create_milestone(
                title=sprint["title"],
                description=sprint["description"],
                due_on=due_date,
            )
            print(f"✅ Created milestone: {sprint['title']} (due {sprint['due_date']})")
        except Exception as e:
            print(f"⚠️  Milestone {sprint['title']} may already exist: {e}")


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN not set")
        exit(1)
    
    create_milestones("aminak58/freqai-futures-strategy", token)
```

---

## 🔒 Component 4: Branch Protection Rules

### Protection for `master` branch

**Settings > Branches > Branch protection rules**

```yaml
Branch: master

Rules:
  ✅ Require a pull request before merging
    ✅ Require approvals: 1
    ✅ Dismiss stale pull request approvals when new commits are pushed
    ✅ Require review from Code Owners
  
  ✅ Require status checks to pass before merging
    ✅ Require branches to be up to date before merging
    Required checks:
      - test-suite (pytest)
      - coverage-check (≥ target %)
      - linting (flake8, black, mypy)
      - security-scan (bandit)
  
  ✅ Require conversation resolution before merging
  
  ✅ Require signed commits (optional but recommended)
  
  ✅ Include administrators (even admins must follow rules)
  
  ✅ Restrict pushes
    - Only allow pull requests
  
  ✅ Do not allow bypassing the above settings
```

### Protection for sprint branches (`sprint-*`)

```yaml
Branch pattern: sprint-*

Rules:
  ✅ Require status checks to pass before merging
    Required checks:
      - test-suite (pytest)
      - linting (flake8, black)
  
  ⬜ Require pull request (optional for sprint branches)
```

---

## 🤖 Component 5: CI/CD Pipeline

### Main CI Workflow

**فایل:** `.github/workflows/ci.yml`

```yaml
name: CI Pipeline

on:
  push:
    branches: ['master', 'sprint-*', 'feature/*']
  pull_request:
    branches: ['master']

jobs:
  # Job 1: Linting
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
      
      - name: Lint with flake8
        run: |
          flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 src/ tests/ --count --max-complexity=10 --max-line-length=120 --statistics
      
      - name: Format check with black
        run: black --check src/ tests/
      
      - name: Type check with mypy
        run: mypy src/
  
  # Job 2: Security Scan
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install bandit
      
      - name: Security scan with bandit
        run: bandit -r src/ -ll
  
  # Job 3: Test Suite
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run tests with pytest
        run: |
          pytest tests/ -v --cov=src --cov-report=xml --cov-report=html --cov-report=term
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
  
  # Job 4: Coverage Check (Enforcement)
  coverage-check:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Check coverage threshold
        run: |
          # Get current sprint target
          CURRENT_COVERAGE=$(pytest tests/ --cov=src --cov-report=term | grep TOTAL | awk '{print $4}' | sed 's/%//')
          TARGET_COVERAGE=60  # Sprint 2 target
          
          echo "Current coverage: ${CURRENT_COVERAGE}%"
          echo "Target coverage: ${TARGET_COVERAGE}%"
          
          if (( $(echo "$CURRENT_COVERAGE < $TARGET_COVERAGE" | bc -l) )); then
            echo "❌ Coverage ${CURRENT_COVERAGE}% is below target ${TARGET_COVERAGE}%"
            exit 1
          else
            echo "✅ Coverage ${CURRENT_COVERAGE}% meets target ${TARGET_COVERAGE}%"
          fi
  
  # Job 5: Build validation (if applicable)
  build:
    runs-on: ubuntu-latest
    needs: [lint, security, test]
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Validate imports
        run: |
          python -c "from src.main import main; print('✅ Imports valid')"
      
      - name: Validate strategy
        run: |
          python -c "from user_data.strategies.FreqAIHybridStrategy import FreqAIHybridStrategy; print('✅ Strategy valid')"
```

### Coverage Enforcement Script

**فایل:** `scripts/check_coverage.sh`

```bash
#!/bin/bash
# Check if coverage meets sprint target

set -e

# Determine sprint target based on branch
if [[ "$GITHUB_REF" == *"sprint-2"* ]] || [[ "$GITHUB_BASE_REF" == "master" ]]; then
    TARGET=60
elif [[ "$GITHUB_REF" == *"sprint-3"* ]]; then
    TARGET=65
else
    TARGET=60  # Default
fi

echo "🎯 Coverage target for this sprint: ${TARGET}%"

# Run coverage
COVERAGE=$(pytest tests/ --cov=src --cov-report=term | grep TOTAL | awk '{print $4}' | sed 's/%//')

echo "📊 Current coverage: ${COVERAGE}%"

# Compare
if (( $(echo "$COVERAGE < $TARGET" | bc -l) )); then
    echo "❌ FAIL: Coverage ${COVERAGE}% is below target ${TARGET}%"
    echo "📝 Add more tests to meet the target"
    exit 1
else
    echo "✅ PASS: Coverage ${COVERAGE}% meets target ${TARGET}%"
fi
```

---

## 📝 Component 6: Pull Request Template

**فایل:** `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
## Description

<!-- Brief description of changes -->

## Related Issue

Closes #XXX

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Sprint

**Sprint:** Sprint X  
**Epic:** Epic X - [Name]  
**Story Points:** X

## Checklist

### Code Quality
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] No unnecessary code or files

### Testing
- [ ] Unit tests added/updated
- [ ] All tests passing locally
- [ ] Coverage meets sprint target (≥ X%)
- [ ] Edge cases covered
- [ ] Integration tests added (if applicable)

### Documentation
- [ ] Code docstrings updated
- [ ] README updated (if needed)
- [ ] Architecture docs updated (if needed)
- [ ] CHANGELOG updated

### CI/CD
- [ ] All CI checks passing
- [ ] No merge conflicts
- [ ] Branch up-to-date with base

### Security
- [ ] No sensitive data exposed
- [ ] No security vulnerabilities introduced
- [ ] Dependencies updated (if needed)

### Review
- [ ] Ready for review
- [ ] Assigned reviewers
- [ ] Linked to issue/milestone

## Screenshots (if applicable)

<!-- Add screenshots for UI changes -->

## Additional Notes

<!-- Any additional context -->
```

---

## 📈 Component 7: Progress Tracking & Reporting

### Sprint Burndown Script

**فایل:** `scripts/sprint_burndown.py`

```python
#!/usr/bin/env python3
"""Generate sprint burndown chart"""

import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from github import Github


def get_sprint_burndown(repo_name: str, token: str, sprint_number: int):
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    # Get milestone
    milestones = repo.get_milestones(state="open")
    milestone = next((m for m in milestones if m.title == f"Sprint {sprint_number}"), None)
    
    if not milestone:
        print(f"❌ Sprint {sprint_number} milestone not found")
        return
    
    # Get issues
    issues = repo.get_issues(milestone=milestone, state="all")
    
    # Calculate story points
    total_points = 0
    completed_points = 0
    
    for issue in issues:
        # Extract story points from labels or title
        points = 0
        for label in issue.labels:
            if label.name.startswith("points-"):
                points = int(label.name.split("-")[1])
                break
        
        total_points += points
        if issue.state == "closed":
            completed_points += points
    
    # Print summary
    print(f"\n📊 Sprint {sprint_number} Burndown")
    print(f"Total Story Points: {total_points}")
    print(f"Completed: {completed_points}")
    print(f"Remaining: {total_points - completed_points}")
    print(f"Progress: {completed_points/total_points*100:.1f}%")
    
    # Due date
    due_date = milestone.due_on
    if due_date:
        days_remaining = (due_date.date() - datetime.now().date()).days
        print(f"Days Remaining: {days_remaining}")


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN not set")
        exit(1)
    
    get_sprint_burndown("aminak58/freqai-futures-strategy", token, sprint_number=2)
```

### Velocity Tracking

**فایل:** `scripts/velocity_tracking.py`

```python
#!/usr/bin/env python3
"""Track team velocity across sprints"""

import os
from github import Github
import matplotlib.pyplot as plt


def calculate_velocity(repo_name: str, token: str):
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    # Get all milestones
    milestones = repo.get_milestones(state="all")
    
    velocity_data = []
    
    for milestone in milestones:
        if not milestone.title.startswith("Sprint"):
            continue
        
        # Get issues
        issues = repo.get_issues(milestone=milestone, state="closed")
        
        # Sum story points
        sprint_points = 0
        for issue in issues:
            for label in issue.labels:
                if label.name.startswith("points-"):
                    sprint_points += int(label.name.split("-")[1])
                    break
        
        velocity_data.append({
            "sprint": milestone.title,
            "points": sprint_points,
        })
    
    # Print velocity
    print("\n📈 Team Velocity")
    print("=" * 40)
    for sprint in velocity_data:
        print(f"{sprint['sprint']}: {sprint['points']} points")
    
    if velocity_data:
        avg_velocity = sum(s["points"] for s in velocity_data) / len(velocity_data)
        print(f"\nAverage Velocity: {avg_velocity:.1f} points/sprint")
    
    # Plot (optional)
    # plt.bar([s["sprint"] for s in velocity_data], [s["points"] for s in velocity_data])
    # plt.xlabel("Sprint")
    # plt.ylabel("Story Points")
    # plt.title("Team Velocity")
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # plt.savefig("velocity.png")
    # print("\n✅ Chart saved: velocity.png")


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN not set")
        exit(1)
    
    calculate_velocity("aminak58/freqai-futures-strategy", token)
```

---

## 🎯 Component 8: Sprint Retrospective Template

**فایل:** `.github/ISSUE_TEMPLATE/sprint_retrospective.md`

```markdown
---
name: Sprint Retrospective
about: Template for sprint retrospective meeting
title: '[Retro] Sprint X'
labels: retrospective
assignees: ''
---

## Sprint X Retrospective

**Date:** [Date]  
**Sprint Duration:** [Start] - [End]  
**Attendees:** [Names]

---

## 📊 Sprint Metrics

| Metric | Planned | Actual | Variance |
|--------|---------|--------|----------|
| Story Points | X | Y | Z |
| Issues Completed | X | Y | Z |
| Velocity | X | Y | Z |
| Test Coverage | X% | Y% | Z% |

---

## ✅ What Went Well

- Item 1
- Item 2
- Item 3

---

## ⚠️ What Could Be Improved

- Item 1
- Item 2
- Item 3

---

## 🚀 Action Items

- [ ] Action 1 (Owner: @username)
- [ ] Action 2 (Owner: @username)
- [ ] Action 3 (Owner: @username)

---

## 📝 Notes

[Additional notes from the retrospective]

---

## 🎯 Next Sprint Focus

- Priority 1
- Priority 2
- Priority 3
```

---

## 🚀 Implementation Plan

### Phase 1: Setup (Day 1)

```bash
# 1. Create issue templates
mkdir -p .github/ISSUE_TEMPLATE
# Create user_story.md, bug_report.md, retrospective.md

# 2. Create PR template
# Create .github/PULL_REQUEST_TEMPLATE.md

# 3. Create workflow files
mkdir -p .github/workflows
# Create ci.yml, project_automation.yml

# 4. Create scripts
mkdir -p scripts
# Create create_sprint_issues.py, create_milestones.py, sprint_burndown.py, velocity_tracking.py

# 5. Commit and push
git add .github/ scripts/
git commit -m "[Setup] GitHub Project Management System"
git push origin master
```

### Phase 2: Configure GitHub (Day 1)

**In GitHub UI:**

1. **Create Project Board**
   - Settings > Projects > New Project
   - Name: "FreqAI RL Integration"
   - Template: Kanban
   - Columns: Backlog, Sprint Backlog, In Progress, In Review, Testing, Done

2. **Create Milestones**
   - Run: `python scripts/create_milestones.py`
   - Verify all 16 sprints created

3. **Configure Branch Protection**
   - Settings > Branches > Add rule
   - Apply rules for `master` and `sprint-*`

4. **Enable Actions**
   - Actions > Enable workflows
   - Verify CI pipeline runs

### Phase 3: Create Sprint 2 Issues (Day 1)

```bash
# Set GitHub token
$env:GITHUB_TOKEN="ghp_your_token_here"

# Create Sprint 2 issues
python scripts/create_sprint_issues.py

# Verify:
# - 2 issues created (US 1.4, US 1.5)
# - Labels applied
# - Milestone assigned
# - Added to project board
```

### Phase 4: Test CI/CD (Day 1)

```bash
# Create test branch
git checkout -b test-ci
echo "# test" >> README.md
git add README.md
git commit -m "test: CI pipeline"
git push origin test-ci

# Create PR in GitHub UI
# Verify:
# - Linting runs
# - Tests run
# - Coverage check runs
# - Security scan runs
# - All checks pass

# Merge PR
# Delete test branch
```

---

## 📊 Dashboard & Metrics

### GitHub Insights

**Pulse (Weekly Summary):**
- Issues opened/closed
- PRs opened/merged
- Commits
- Contributors

**Path:** Insights > Pulse

---

### Codecov Dashboard

**Integration:**
```yaml
# .codecov.yml
coverage:
  status:
    project:
      default:
        target: 60%  # Sprint 2 target
        threshold: 1%
    patch:
      default:
        target: 60%
```

**Dashboard:** https://codecov.io/gh/aminak58/freqai-futures-strategy

---

### Custom Dashboard (Optional)

**فایل:** `dashboard/sprint_dashboard.py`

```python
#!/usr/bin/env python3
"""Generate HTML dashboard for sprint progress"""

import os
from github import Github
from jinja2 import Template

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>FreqAI RL Integration - Sprint Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .metric { display: inline-block; margin: 10px; padding: 20px; background: #f0f0f0; border-radius: 8px; }
        .metric h3 { margin: 0 0 10px 0; }
        .metric .value { font-size: 32px; font-weight: bold; }
        .progress-bar { width: 300px; height: 30px; background: #ddd; border-radius: 15px; overflow: hidden; }
        .progress-fill { height: 100%; background: #4CAF50; }
    </style>
</head>
<body>
    <h1>Sprint {{ sprint_number }} Dashboard</h1>
    <div class="metric">
        <h3>Story Points</h3>
        <div class="value">{{ completed_points }} / {{ total_points }}</div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {{ progress }}%;"></div>
        </div>
    </div>
    <div class="metric">
        <h3>Test Coverage</h3>
        <div class="value">{{ coverage }}%</div>
    </div>
    <div class="metric">
        <h3>Days Remaining</h3>
        <div class="value">{{ days_remaining }}</div>
    </div>
</body>
</html>
"""


def generate_dashboard(repo_name: str, token: str, sprint_number: int):
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    # Get milestone data (same as sprint_burndown.py)
    # ...
    
    # Render HTML
    template = Template(TEMPLATE)
    html = template.render(
        sprint_number=sprint_number,
        completed_points=13,
        total_points=18,
        progress=72.2,
        coverage=52,
        days_remaining=5,
    )
    
    with open("sprint_dashboard.html", "w") as f:
        f.write(html)
    
    print("✅ Dashboard generated: sprint_dashboard.html")


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    generate_dashboard("aminak58/freqai-futures-strategy", token, 2)
```

---

## 🎯 Success Criteria

### Sprint 2 (Example)

**Before Sprint Starts:**
- ✅ Sprint 2 milestone created (due Nov 10)
- ✅ 2 issues created (US 1.4, US 1.5)
- ✅ Issues added to project board (Sprint Backlog column)
- ✅ Branch protection enabled
- ✅ CI/CD pipeline running

**During Sprint:**
- ✅ Issues moved to "In Progress" when work starts
- ✅ PRs linked to issues
- ✅ CI checks passing on all PRs
- ✅ Coverage increasing toward 60%
- ✅ Daily standup notes in issue comments

**Sprint End:**
- ✅ All issues closed
- ✅ All PRs merged
- ✅ Coverage ≥ 60%
- ✅ Retrospective issue created
- ✅ Sprint 3 issues created

---

## 🔄 Weekly Workflow

### Monday (Sprint Planning if new sprint)
1. Create sprint issues: `python scripts/create_sprint_issues.py`
2. Review and refine issues with team
3. Move issues to Sprint Backlog column
4. Assign issues to team members

### Tuesday-Thursday (Development)
1. Move issue to "In Progress"
2. Create feature branch: `git checkout -b feature/us-X-Y`
3. Develop + write tests
4. Commit regularly with descriptive messages
5. Push and create PR when ready
6. PR moves to "In Review" automatically

### Friday (Review & Retrospective)
1. Review PRs and merge
2. Check sprint burndown: `python scripts/sprint_burndown.py`
3. Update velocity: `python scripts/velocity_tracking.py`
4. If sprint ends: Create retrospective issue

---

## 🎓 Training & Documentation

### For Team Members

**چک‌لیست شروع کار:**
- [ ] Read GITHUB_PROJECT_MANAGEMENT.md (این فایل)
- [ ] Install GitHub CLI: `gh`
- [ ] Set GITHUB_TOKEN in environment
- [ ] Clone repo and install dependencies
- [ ] Run tests locally: `pytest tests/`
- [ ] Review current sprint issues
- [ ] Self-assign an issue
- [ ] Create feature branch and start coding!

**روزانه:**
- [ ] Pull latest: `git pull origin master`
- [ ] Update issue comments with progress
- [ ] Run tests before committing
- [ ] Create PR when feature is ready
- [ ] Respond to code review feedback

---

## 🎯 Next Steps (Implementation)

1. **Immediate (Day 1):**
   - [ ] Create .github/ templates
   - [ ] Create scripts/
   - [ ] Configure branch protection
   - [ ] Create milestones
   - [ ] Create Sprint 2 issues

2. **Week 1:**
   - [ ] Test full workflow with Sprint 2
   - [ ] Refine automation rules
   - [ ] Train team on workflow
   - [ ] Generate first sprint report

3. **Ongoing:**
   - [ ] Weekly velocity tracking
   - [ ] Monthly retrospectives
   - [ ] Quarterly roadmap review
   - [ ] Continuous improvement

---

**با این سیستم:**
- ✅ هر تسک قابل پیگیری است
- ✅ هیچ کاری بدون تست و review merge نمی‌شود
- ✅ Coverage به صورت خودکار enforce می‌شود
- ✅ پیشرفت قابل مشاهده است (dashboards)
- ✅ تیم یک workflow استاندارد دارد

**نتیجه:** پروژه از یک roadmap به یک دستگاه اجرایی تبدیل می‌شود! 🚀
