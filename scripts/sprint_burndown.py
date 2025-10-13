#!/usr/bin/env python3
"""
Generate sprint burndown report

Usage:
    $env:GITHUB_TOKEN="ghp_your_token_here"
    python scripts/sprint_burndown.py --sprint 2
"""

import os
import argparse
from datetime import datetime
from github import Github


def get_story_points(issue):
    """Extract story points from issue labels or title"""
    for label in issue.labels:
        if label.name.startswith("points-"):
            return int(label.name.split("-")[1])
    
    # Try to extract from body
    if issue.body and "Story Points:" in issue.body:
        for line in issue.body.split("\n"):
            if "Story Points:" in line and "**" in line:
                try:
                    # Extract from **Story Points:** X format
                    parts = line.split(":")
                    if len(parts) >= 2:
                        points_str = parts[-1].strip().replace("*", "").strip()
                        return int(points_str)
                except:
                    pass
    
    return 0


def get_sprint_burndown(repo_name: str, token: str, sprint_number: int):
    """Generate burndown report for a sprint"""
    g = Github(token)
    repo = g.get_repo(repo_name)

    # Get milestone
    milestones = repo.get_milestones(state="all")
    milestone = next(
        (m for m in milestones if m.title == f"Sprint {sprint_number}"), None
    )

    if not milestone:
        print(f"❌ Sprint {sprint_number} milestone not found")
        return

    # Get issues
    issues = list(repo.get_issues(milestone=milestone, state="all"))

    # Calculate story points
    total_points = 0
    completed_points = 0
    in_progress_points = 0

    print(f"\n📊 Sprint {sprint_number} Burndown Report")
    print("=" * 60)
    print(f"Milestone: {milestone.title}")
    print(f"Due Date: {milestone.due_on.strftime('%Y-%m-%d') if milestone.due_on else 'Not set'}")
    print(f"Total Issues: {len(issues)}")
    print()

    for issue in issues:
        points = get_story_points(issue)
        total_points += points

        status = "❓"
        if issue.state == "closed":
            completed_points += points
            status = "✅"
        else:
            # Check if in progress
            has_in_progress = any(
                label.name == "in-progress" for label in issue.labels
            )
            if has_in_progress:
                in_progress_points += points
                status = "🔄"
            else:
                status = "⏳"

        print(f"{status} #{issue.number}: {issue.title} ({points} pts)")

    remaining_points = total_points - completed_points

    print()
    print("=" * 60)
    print(f"📈 Total Story Points: {total_points}")
    
    if total_points > 0:
        print(f"✅ Completed: {completed_points} ({completed_points/total_points*100:.1f}%)")
        print(f"🔄 In Progress: {in_progress_points} ({in_progress_points/total_points*100:.1f}%)")
        print(f"⏳ Remaining: {remaining_points} ({remaining_points/total_points*100:.1f}%)")
    else:
        print(f"✅ Completed: {completed_points}")
        print(f"🔄 In Progress: {in_progress_points}")
        print(f"⏳ Remaining: {remaining_points}")
        print("\n⚠️  Note: Story points not found in issue labels.")
        print("   Story points are extracted from issue body 'Story Points: X'.")

    if milestone.due_on:
        days_remaining = (milestone.due_on.date() - datetime.now().date()).days
        print(f"📅 Days Remaining: {days_remaining}")

        if days_remaining > 0 and remaining_points > 0:
            burn_rate = remaining_points / days_remaining
            print(f"🔥 Required Burn Rate: {burn_rate:.1f} pts/day")

    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate sprint burndown report")
    parser.add_argument("--sprint", type=int, default=2, help="Sprint number")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN environment variable not set")
        print("   Set it with: $env:GITHUB_TOKEN='ghp_your_token_here'")
        exit(1)

    get_sprint_burndown("aminak58/freqai-futures-strategy", token, args.sprint)
