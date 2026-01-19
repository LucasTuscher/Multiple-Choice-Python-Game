#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quiz-Engine
Verwaltet die Quiz-Logik, Zufallsauswahl und Auswertung
"""

import os
import random
import re
from dataclasses import dataclass
from typing import Dict, Set, List, Tuple, Optional
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


_MULTI_CHOICE_HINT_RE = re.compile(
    r"\s*\(\s*Mehrfachauswahl(?:\s+(?:möglich|moeglich))?\s*\)\s*$",
    re.IGNORECASE,
)


def sanitize_prompt(prompt: str) -> str:
    """Entfernt Hinweise wie '(Mehrfachauswahl ...)' aus dem Prompt."""
    return _MULTI_CHOICE_HINT_RE.sub("", prompt).strip()


def _index_to_letters(index: int) -> str:
    """0 -> A, 1 -> B, ..., 25 -> Z, 26 -> AA, ..."""
    index += 1
    letters: List[str] = []
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        letters.append(chr(ord("A") + remainder))
    return "".join(reversed(letters))


def prepare_question(
    question: Question,
    rng: Optional[random.Random] = None,
    shuffle_answers: bool = True,
) -> Question:
    """
    Erstellt eine Anzeige-/Quiz-Variante der Frage:
    - Entfernt Mehrfachauswahl-Hinweise im Prompt
    - Mischt Antwortoptionen und remappt correct/explain_wrong
    """
    if not shuffle_answers:
        return Question(
            prompt=sanitize_prompt(question.prompt),
            options=question.options.copy(),
            correct=set(question.correct),
            explain_correct=question.explain_correct,
            explain_wrong=question.explain_wrong.copy(),
            topic=question.topic,
        )

    rng = rng or random

    option_items = sorted(question.options.items(), key=lambda kv: kv[0])
    if not option_items:
        return Question(
            prompt=sanitize_prompt(question.prompt),
            options={},
            correct=set(),
            explain_correct=question.explain_correct,
            explain_wrong={},
            topic=question.topic,
        )

    rng.shuffle(option_items)

    key_map: Dict[str, str] = {}
    new_options: Dict[str, str] = {}

    for idx, (old_key, text) in enumerate(option_items):
        new_key = _index_to_letters(idx)
        key_map[old_key] = new_key
        new_options[new_key] = text

    new_correct = {key_map[k] for k in question.correct if k in key_map}
    new_explain_wrong = {key_map[k]: v for k, v in question.explain_wrong.items() if k in key_map}

    return Question(
        prompt=sanitize_prompt(question.prompt),
        options=new_options,
        correct=new_correct,
        explain_correct=question.explain_correct,
        explain_wrong=new_explain_wrong,
        topic=question.topic,
    )


def format_selected_options(q: Question, keys: Set[str]) -> str:
    """Formatiert eine Auswahl als 'A) Text' Zeilen."""
    if not keys:
        return "    (keine)"

    lines: List[str] = []
    for key in sorted(keys):
        text = q.options.get(key, "")
        if text:
            lines.append(f"    {key}) {text}")
        else:
            lines.append(f"    {key})")
    return "\n".join(lines)


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
        return prepare_question(question)

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
        print("  Antwort eingeben (z.B. 'A')")
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
        lines.append("  Deine Auswahl:")
        lines.append(format_selected_options(q, user_set))
        lines.append("")
        lines.append("  Richtige Auswahl:")
        lines.append(format_selected_options(q, q.correct))
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

    def run(
        self,
        question_limit: Optional[int] = None,
        allow_repeats: bool = False,
        shuffle_questions: bool = True,
        shuffle_answers: bool = True,
    ) -> Tuple[int, int]:
        """
        Quiz durchführen.

        Args:
            question_limit: Maximale Anzahl der Fragen (None/<=0 = alle).
            allow_repeats: Wenn True, können Fragen wiederholt werden (mit Cooldown).
            shuffle_questions: Wenn True, werden Fragen zufällig gewählt/gemischt.
            shuffle_answers: Wenn True, werden Antwortoptionen pro Frage gemischt.

        Returns:
            Tuple (richtige Antworten, Gesamtzahl beantworteter Fragen)
        """
        self.correct_count = 0
        self.total_answered = 0
        self.recently_asked.clear()

        total_available = len(self.all_questions)
        if total_available == 0:
            return 0, 0

        if question_limit is None or question_limit <= 0:
            question_limit = total_available

        if not allow_repeats:
            # Ohne Wiederholung (jede Frage max. 1x)
            questions = self.all_questions.copy()
            if shuffle_questions:
                random.shuffle(questions)

            questions = questions[: min(question_limit, len(questions))]
            total = len(questions)
            current = 0

            for question in questions:
                current += 1
                prepared = prepare_question(question, shuffle_answers=shuffle_answers)
                self.display_question(prepared, current, total)

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

                is_correct, explanation = self.evaluate(prepared, user_set)
                print(explanation)

                if is_correct:
                    self.correct_count += 1

                self.total_answered += 1

                input("\n  Drücke ENTER für die nächste Frage...")

            return self.correct_count, self.total_answered

        # Mit Wiederholung (Training): Fragen können erneut kommen, aber nicht direkt (Cooldown)
        total = question_limit

        current = 0
        while current < total:
            current += 1

            available = self.get_available_questions()
            if not available:
                available = self.all_questions.copy()

            question = random.choice(available) if shuffle_questions else self.all_questions[(current - 1) % total_available]
            self.recently_asked.append(question)

            prepared = prepare_question(question, shuffle_answers=shuffle_answers)
            self.display_question(prepared, current, total)

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

            is_correct, explanation = self.evaluate(prepared, user_set)
            print(explanation)

            if is_correct:
                self.correct_count += 1

            self.total_answered += 1
            input("\n  Drücke ENTER für die nächste Frage...")

        return self.correct_count, self.total_answered
