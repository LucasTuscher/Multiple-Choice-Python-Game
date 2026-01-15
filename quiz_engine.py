#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quiz-Engine
Verwaltet die Quiz-Logik, Zufallsauswahl und Auswertung
"""

import os
import random
from dataclasses import dataclass
from typing import Dict, Set, List, Tuple
from collections import deque


@dataclass
class Question:
    """Datenstruktur für eine Frage"""
    prompt: str                          # Die Frage selbst
    options: Dict[str, str]              # Antwortmöglichkeiten (A, B, C, D ...)
    correct: Set[str]                    # Menge der richtigen Antworten
    explain_correct: str                 # Erklärung, warum die Lösung richtig ist
    explain_wrong: Dict[str, str]        # Erklärung, warum die falschen Antworten falsch sind
    topic: str = ""                      # Optionales Thema der Frage


class QuizEngine:
    """Verwaltet das Quiz mit zufälliger Fragenauswahl"""

    def __init__(self, questions: List[Question], cooldown: int = 3):
        """
        Initialisiert die Quiz-Engine.

        Args:
            questions: Liste aller Fragen
            cooldown: Wie viele andere Fragen gestellt werden müssen,
                      bevor eine Frage wiederholt werden kann
        """
        self.all_questions = questions.copy()
        self.cooldown = min(cooldown, len(questions) - 1) if len(questions) > 1 else 0
        self.recently_asked: deque = deque(maxlen=self.cooldown)
        self.correct_count = 0
        self.total_answered = 0

    def clear_screen(self):
        """Bildschirm leeren"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_available_questions(self) -> List[Question]:
        """Gibt alle Fragen zurück, die nicht kürzlich gestellt wurden"""
        if not self.recently_asked:
            return self.all_questions.copy()

        return [q for q in self.all_questions if q not in self.recently_asked]

    def get_next_question(self) -> Question:
        """Wählt zufällig eine Frage aus (nicht kürzlich gestellt)"""
        available = self.get_available_questions()

        if not available:
            # Falls alle Fragen im Cooldown sind, älteste freigeben
            available = self.all_questions.copy()

        question = random.choice(available)
        self.recently_asked.append(question)
        return question

    def normalize_answer(self, raw: str) -> Set[str]:
        """
        Eingabe des Users normalisieren
        (z.B. "b d", "BD", "b,d" → {"B", "D"})
        """
        raw = raw.strip().lower()

        # Trennzeichen vereinheitlichen
        for sep in [',', ';', '|', '/']:
            raw = raw.replace(sep, ' ')

        parts = raw.split()

        # Falls z.B. "bd" eingegeben wurde
        if len(parts) == 1:
            letters = [ch for ch in parts[0] if ch.isalpha()]
        else:
            letters = []
            for p in parts:
                letters.extend([ch for ch in p if ch.isalpha()])

        return {ch.upper() for ch in letters}

    def format_set(self, s: Set[str]) -> str:
        """Hilfsfunktion zur Ausgabe von Antwortmengen"""
        return " ".join(sorted(s)) if s else "(keine)"

    def display_question(self, q: Question, current: int, total: int) -> None:
        """Eine Frage anzeigen"""
        self.clear_screen()
        print()
        print("=" * 70)
        print(f"  Frage {current}/{total}")
        if q.topic:
            print(f"  Thema: {q.topic}")
        print("=" * 70)
        print()
        print()
        print(f"  {q.prompt}")
        print()
        print()
        print("-" * 70)
        print()
        for key in sorted(q.options.keys()):
            print(f"    {key})  {q.options[key]}")
            print()
        print("-" * 70)
        print()
        print()
        print("  Antwort eingeben (z.B. 'A', 'a', 'B D' oder 'bd')")
        print("  Mehrere Antworten moeglich!")
        print()
        print("  Befehle: 'weiter' = ueberspringen, 'quit' = beenden")
        print()

    def evaluate(self, q: Question, user_set: Set[str]) -> Tuple[bool, str]:
        """Antwort auswerten und erklären"""
        valid = set(q.options.keys())

        # Ungültige Eingaben prüfen
        invalid = user_set - valid
        if invalid:
            return False, f"  Ungültige Auswahl: {self.format_set(invalid)}"

        # Prüfen, ob die Antwort exakt stimmt
        is_correct = user_set == q.correct

        lines: List[str] = []
        lines.append("")
        lines.append("")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"  Deine Antwort:    {self.format_set(user_set)}")
        lines.append(f"  Richtige Antwort: {self.format_set(q.correct)}")
        lines.append("")

        if is_correct:
            lines.append("  *** RICHTIG! ***")
        else:
            lines.append("  *** FALSCH! ***")

        lines.append("")
        lines.append("")
        lines.append("-" * 70)
        lines.append("")

        # Erklärung der richtigen Lösung
        lines.append("  ERKLAERUNG:")
        lines.append("")
        lines.append(f"  {q.explain_correct}")
        lines.append("")
        lines.append("")

        # Erklärung der falschen Optionen
        wrong_options = valid - q.correct
        if wrong_options:
            lines.append("-" * 70)
            lines.append("")
            lines.append("  WARUM DIE ANDEREN OPTIONEN FALSCH SIND:")
            lines.append("")
            for opt in sorted(wrong_options):
                explanation = q.explain_wrong.get(opt, 'Keine Erklaerung vorhanden')
                lines.append(f"    {opt})  {explanation}")
                lines.append("")

        lines.append("")
        lines.append("=" * 70)

        return is_correct, "\n".join(lines)

    def run(self) -> Tuple[int, int]:
        """
        Quiz durchführen.

        Returns:
            Tuple (richtige Antworten, Gesamtzahl beantworteter Fragen)
        """
        total = len(self.all_questions)
        current = 0
        self.correct_count = 0
        self.total_answered = 0

        # Mische die Fragen für diese Runde
        shuffled = self.all_questions.copy()
        random.shuffle(shuffled)

        for question in shuffled:
            current += 1
            self.display_question(question, current, total)

            user_input = input("  Deine Eingabe: ").strip().lower()

            if user_input == "quit":
                print("\n  Quiz wird beendet...")
                break

            if user_input == "weiter":
                print("\n  Frage übersprungen.")
                input("  Drücke ENTER...")
                continue

            user_set = self.normalize_answer(user_input)

            if not user_set:
                print("\n  Keine gültige Antwort eingegeben.")
                input("  Drücke ENTER...")
                continue

            is_correct, explanation = self.evaluate(question, user_set)
            print(explanation)

            if is_correct:
                self.correct_count += 1

            self.total_answered += 1
            self.recently_asked.append(question)

            input("\n  Drücke ENTER für die nächste Frage...")

        return self.correct_count, self.total_answered
