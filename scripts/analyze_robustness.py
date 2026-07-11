#!/usr/bin/env python3
"""Analyze subject-level BCI robustness results and build a dashboard.

This script consumes real benchmark CSV outputs. It does not simulate data.
It creates:
- subject risk cards
- intervention/montage-rescue metrics
- paired dropout-vs-clean statistics
- an interactive HTML dashboard
"""
