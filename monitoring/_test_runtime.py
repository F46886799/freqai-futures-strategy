"""Test governance runtime adapter."""
from monitoring.governance_runtime import get_governance_state

state = get_governance_state(
    policy_path="config/governance_policy.yaml",
    decisions_path="monitoring/governance_decisions.jsonl"
)

print("Governance State:")
print(f"  Status: {state.status}")
print(f"  Risk Multiplier: {state.risk_multiplier}")
print(f"  Tighten Stop Factor: {state.tighten_stop_factor}")
print(f"  Disable Shorts: {state.disable_shorts}")
print(f"  Max Leverage (policy): {state.max_leverage}")
print(f"  Min Stop %: {state.min_stop_pct}")
print(f"  Max Stop %: {state.max_stop_pct}")

# Simulate what strategy would do
if state.status == 'halt':
    print("\n❌ HALT: No new entries allowed")
elif state.status == 'warn':
    print(f"\n⚠️  WARN: Risk reduced to {state.risk_multiplier}x")
elif state.status == 'degrade':
    print(f"\n⚠️  DEGRADE: Risk cut to {state.risk_multiplier}x, shorts={'disabled' if state.disable_shorts else 'enabled'}")
else:
    print("\n✅ NORMAL: All systems operational")
