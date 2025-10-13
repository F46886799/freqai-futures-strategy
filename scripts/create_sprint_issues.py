#!/usr/bin/env python3
"""
Create GitHub Issues for all User Stories in a Sprint

Usage:
    $env:GITHUB_TOKEN="ghp_your_token_here"
    python scripts/create_sprint_issues.py --sprint 2
"""

import os
import argparse
from github import Github


SPRINT_STORIES = {
    2: [
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
- [ ] Documentation updated
""",
            "labels": [
                "user-story",
                "p1-high",
                "sprint-2",
                "epic-1-foundation",
                "component-strategy",
            ],
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
- [ ] Update DEVELOPMENT_GUIDE.md (if exists)
- [ ] Create/update CURRENT_STATUS.md
- [ ] Update UNIFIED_ARCHITECTURE.md
- [ ] Review LSTM_ARCHITECTURE_DESIGN.md
- [ ] Review MVP_DOCUMENTATION.md
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
- [ ] Sprint 2 complete marker added
""",
            "labels": [
                "user-story",
                "p2-medium",
                "sprint-2",
                "epic-1-foundation",
                "documentation",
            ],
            "milestone": "Sprint 2",
            "assignees": ["aminak58"],
        },
    ],
}


def create_issues(repo_name: str, token: str, sprint: int):
    """Create GitHub Issues from sprint data"""
    g = Github(token)
    repo = g.get_repo(repo_name)

    stories = SPRINT_STORIES.get(sprint)
    if not stories:
        print(f"❌ No stories defined for Sprint {sprint}")
        return

    # Get or create milestone
    milestone = None
    try:
        milestones = repo.get_milestones(state="open")
        milestone = next((m for m in milestones if m.title == f"Sprint {sprint}"), None)

        if not milestone:
            print(f"⚠️  Milestone 'Sprint {sprint}' not found. Creating it...")
            # Create milestone with appropriate due date
            due_dates = {
                2: "2025-11-10T23:59:59Z",
                3: "2026-01-19T23:59:59Z",
            }
            milestone = repo.create_milestone(
                f"Sprint {sprint}",
                description=f"Sprint {sprint} milestone",
                due_on=due_dates.get(sprint),
            )
            print(f"✅ Created milestone: Sprint {sprint}")
        else:
            print(f"ℹ️  Milestone 'Sprint {sprint}' already exists")
    except Exception as e:
        print(f"⚠️  Could not get/create milestone: {e}")

    # Create issues
    created = 0
    for story in stories:
        try:
            issue = repo.create_issue(
                title=story["title"],
                body=story["body"],
                labels=story["labels"],
                milestone=milestone,
                assignees=story.get("assignees", []),
            )
            print(f"✅ Created issue #{issue.number}: {story['title']}")
            created += 1
        except Exception as e:
            print(f"❌ Failed to create issue '{story['title']}': {e}")

    print(f"\n📊 Summary: Created {created}/{len(stories)} issues for Sprint {sprint}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create GitHub issues for a sprint")
    parser.add_argument("--sprint", type=int, default=2, help="Sprint number")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN environment variable not set")
        print("   Set it with: $env:GITHUB_TOKEN='ghp_your_token_here'")
        exit(1)

    create_issues("aminak58/freqai-futures-strategy", token, args.sprint)
