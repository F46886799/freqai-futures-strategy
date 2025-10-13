#!/usr/bin/env python3
"""
Track team velocity across sprints

Usage:
    $env:GITHUB_TOKEN="ghp_your_token_here"
    python scripts/velocity_tracking.py
"""

import os
from github import Github


def get_story_points(issue):
    """Extract story points from issue"""
    for label in issue.labels:
        if label.name.startswith("points-"):
            return int(label.name.split("-")[1])

    if "Story Points:" in issue.body:
        for line in issue.body.split("\n"):
            if "Story Points:" in line:
                try:
                    return int(line.split(":")[-1].strip())
                except:
                    pass

    return 0


def calculate_velocity(repo_name: str, token: str):
    """Track team velocity across all sprints"""
    g = Github(token)
    repo = g.get_repo(repo_name)

    # Get all milestones
    milestones = list(repo.get_milestones(state="all"))

    # Filter sprint milestones and sort
    sprint_milestones = [m for m in milestones if m.title.startswith("Sprint")]
    sprint_milestones.sort(
        key=lambda m: int(m.title.split()[1]) if m.title.split()[1].isdigit() else 0
    )

    velocity_data = []

    print("\n📈 Team Velocity Tracking")
    print("=" * 80)

    for milestone in sprint_milestones:
        # Get closed issues
        issues = list(repo.get_issues(milestone=milestone, state="closed"))

        # Sum story points
        sprint_points = sum(get_story_points(issue) for issue in issues)

        velocity_data.append(
            {
                "sprint": milestone.title,
                "points": sprint_points,
                "issues": len(issues),
            }
        )

        status_icon = "✅" if sprint_points > 0 else "⏳"
        print(
            f"{status_icon} {milestone.title:15} | {sprint_points:3} pts | {len(issues):2} issues"
        )

    print("=" * 80)

    if velocity_data:
        # Filter sprints with actual work
        completed_sprints = [s for s in velocity_data if s["points"] > 0]

        if completed_sprints:
            total_points = sum(s["points"] for s in completed_sprints)
            avg_velocity = total_points / len(completed_sprints)
            max_velocity = max(s["points"] for s in completed_sprints)
            min_velocity = min(s["points"] for s in completed_sprints)

            print(f"\n📊 Velocity Statistics:")
            print(f"   Average Velocity: {avg_velocity:.1f} pts/sprint")
            print(f"   Max Velocity: {max_velocity} pts")
            print(f"   Min Velocity: {min_velocity} pts")
            print(f"   Completed Sprints: {len(completed_sprints)}")

            # Forecast
            remaining_sprints = len(velocity_data) - len(completed_sprints)
            if remaining_sprints > 0:
                print(f"\n🔮 Forecast:")
                print(f"   Expected velocity for remaining sprints: {avg_velocity:.1f} pts/sprint")
        else:
            print("\n⚠️  No completed sprints with story points yet")
    else:
        print("\n⚠️  No sprint milestones found")

    print("=" * 80)


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN environment variable not set")
        print("   Set it with: $env:GITHUB_TOKEN='ghp_your_token_here'")
        exit(1)

    calculate_velocity("aminak58/freqai-futures-strategy", token)
