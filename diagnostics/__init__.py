"""
Diagnostics Package

Provides diagnostic tools for analyzing trading strategy performance:
- Signal audit: Track gating funnel and rejection reasons
- Visualization: Interactive notebooks for diagnostic analysis

Author: Strategy Team
Version: 1.0.0
"""

from diagnostics.signal_audit import (
    SignalAuditLogger,
    SignalAuditConfig,
    SignalAuditRecord,
    GatingStats,
)

__all__ = [
    'SignalAuditLogger',
    'SignalAuditConfig',
    'SignalAuditRecord',
    'GatingStats',
]
