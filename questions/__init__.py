#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Questions Package
Enthält alle Fragen für verschiedene Themen
"""

from .signalverarbeitung import get_questions as get_signal_questions
from .computergrafik import get_questions as get_cg_questions

__all__ = [
    'get_signal_questions',
    'get_cg_questions',
]
