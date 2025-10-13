#!/usr/bin/env python3
"""
Create GitHub Milestones for all 16 sprints

Usage:
    $env:GITHUB_TOKEN="ghp_your_token_here"
    python scripts/create_milestones.py
"""

import os
from datetime import datetime
from github import Github


SPRINTS = [
    {
        "title": "Sprint 1",
        "due_date": "2025-10-27",
        "description": "Foundation: Evaluation Protocol + Signal Audit + Baseline Review",
    },
    {
        "title": "Sprint 2",
        "due_date": "2025-11-10",
        "description": "Foundation: Test Coverage 60%+ + Documentation Update",
    },
    {
        "title": "Sprint 3",
        "due_date": "2026-01-19",
        "description": "Contextual Bandit: Model Foundation",
    },
    {
        "title": "Sprint 4",
        "due_date": "2026-02-02",
        "description": "Contextual Bandit: Replay Buffer & Data Pipeline",
    },
    {
        "title": "Sprint 5",
        "due_date": "2026-02-16",
        "description": "Contextual Bandit: Offline Training Pipeline",
    },
    {
        "title": "Sprint 6",
        "due_date": "2026-03-02",
        "description": "Contextual Bandit: FreqAI Integration + A/B Testing",
    },
    {
        "title": "Sprint 7",
        "due_date": "2026-03-16",
        "description": "Contextual Bandit: Validation",
    },
    {
        "title": "Sprint 8",
        "due_date": "2026-04-20",
        "description": "Actor-Critic: Architecture (Part 1)",
    },
    {
        "title": "Sprint 9",
        "due_date": "2026-05-03",
        "description": "Actor-Critic: Architecture (Part 2)",
    },
    {
        "title": "Sprint 10",
        "due_date": "2026-05-17",
        "description": "Actor-Critic: PPO Training",
    },
    {
        "title": "Sprint 11",
        "due_date": "2026-05-31",
        "description": "Actor-Critic: Online Fine-tuning",
    },
    {
        "title": "Sprint 12",
        "due_date": "2026-06-14",
        "description": "Actor-Critic: Comprehensive Validation",
    },
    {
        "title": "Sprint 13",
        "due_date": "2026-07-12",
        "description": "Production: Gradual Rollout (Part 1)",
    },
    {
        "title": "Sprint 14",
        "due_date": "2026-07-28",
        "description": "Production: Gradual Rollout (Part 2)",
    },
    {
        "title": "Sprint 15",
        "due_date": "2026-08-11",
        "description": "Production: Monitoring & Alerting System",
    },
    {
        "title": "Sprint 16",
        "due_date": "2026-08-25",
        "description": "Production: Complete Documentation & Handoff",
    },
]


def create_milestones(repo_name: str, token: str):
    """Create GitHub Milestones for all sprints"""
    g = Github(token)
    repo = g.get_repo(repo_name)

    created = 0
    skipped = 0

    for sprint in SPRINTS:
        try:
            due_date = datetime.strptime(sprint["due_date"], "%Y-%m-%d")
            milestone = repo.create_milestone(
                title=sprint["title"],
                description=sprint["description"],
                due_on=due_date,
            )
            print(f"✅ Created milestone: {sprint['title']} (due {sprint['due_date']})")
            created += 1
        except Exception as e:
            if "already_exists" in str(e).lower() or "errors" in str(e).lower():
                print(f"ℹ️  Milestone '{sprint['title']}' already exists, skipping")
                skipped += 1
            else:
                print(f"⚠️  Failed to create milestone '{sprint['title']}': {e}")

    print(f"\n📊 Summary: Created {created} milestones, Skipped {skipped}")


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN environment variable not set")
        print("   Set it with: $env:GITHUB_TOKEN='ghp_your_token_here'")
        exit(1)

    create_milestones("aminak58/freqai-futures-strategy", token)
