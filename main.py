#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Multiple-Choice-Quiz - Hauptprogramm
Startet das Quiz mit Begrüßung und Themenauswahl
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from quiz_engine import QuizEngine
from questions.signalverarbeitung import get_questions as get_signal_questions
from questions.computergrafik import get_questions as get_cg_questions


def clear_screen():
    """Bildschirm leeren"""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_greeting():
    """Begrüßung anzeigen"""
    clear_screen()
    print("=" * 70)
    print()
    print("    WILLKOMMEN ZUM LERN-QUIZ!")
    print()
    print("=" * 70)
    print()
    print("    Teste dein Wissen in verschiedenen Themenbereichen!")
    print()
    print("    So funktioniert's:")
    print("    - Wähle ein oder mehrere Themen aus")
    print("    - Beantworte die Fragen (z.B. 'B')")
    print("    - Stelle vor dem Start die Runde ein (Zufall/Wiederholung)")
    print("    - Nach jeder Antwort bekommst du eine Erklärung")
    print()
    print("    Befehle während des Quiz:")
    print("    - 'weiter' = Frage überspringen")
    print("    - 'quit'   = Quiz beenden")
    print()
    print("=" * 70)
    input("\nDrücke ENTER um fortzufahren...")


def prompt_yes_no(prompt: str, default: bool) -> bool:
    """Ja/Nein Eingabe abfragen."""
    suffix = " [J/n]" if default else " [j/N]"
    while True:
        value = input(f"{prompt}{suffix}: ").strip().lower()
        if not value:
            return default
        if value in {"j", "ja", "y", "yes"}:
            return True
        if value in {"n", "nein", "no"}:
            return False
        print("  Bitte 'j' oder 'n' eingeben.")


def prompt_int(prompt: str, default: int, min_value: int = 0) -> int:
    """Integer-Eingabe abfragen."""
    while True:
        value = input(f"{prompt} [{default}]: ").strip()
        if not value:
            return default
        try:
            parsed = int(value)
        except ValueError:
            print("  Bitte eine Zahl eingeben.")
            continue
        if parsed < min_value:
            print(f"  Bitte eine Zahl >= {min_value} eingeben.")
            continue
        return parsed


def get_quiz_settings(total_questions: int) -> dict:
    """Einstellungen für die Runde abfragen."""
    clear_screen()
    print("=" * 70)
    print("                    EINSTELLUNGEN")
    print("=" * 70)
    print()
    print(f"  Verfügbare Fragen: {total_questions}")
    print()

    shuffle_questions = prompt_yes_no("  Fragen zufällig mischen?", True)
    shuffle_answers = prompt_yes_no("  Antwortoptionen zufällig mischen?", True)
    allow_repeats = prompt_yes_no("  Fragen dürfen sich wiederholen (Training)?", False)
    print()

    if allow_repeats:
        question_limit = prompt_int("  Wie viele Fragen möchtest du üben?", max(20, total_questions), min_value=1)
        cooldown = prompt_int("  Cooldown (Abstand bis Wiederholung möglich)", 3, min_value=0)
    else:
        while True:
            limit_raw = input("  Wie viele Fragen in dieser Runde? (ENTER/0 = alle): ").strip()
            if not limit_raw or limit_raw == "0":
                question_limit = None
                break
            try:
                parsed = int(limit_raw)
            except ValueError:
                print("  Bitte eine Zahl eingeben.")
                continue
            if parsed < 1:
                print("  Bitte eine Zahl >= 1 eingeben (oder ENTER/0 für alle).")
                continue
            question_limit = parsed
            break
        cooldown = 3

    print()
    print("=" * 70)
    input("  ENTER um zu starten...")

    return {
        "shuffle_questions": shuffle_questions,
        "shuffle_answers": shuffle_answers,
        "allow_repeats": allow_repeats,
        "question_limit": question_limit,
        "cooldown": cooldown,
    }


def show_topic_menu():
    """Themenauswahl anzeigen"""
    clear_screen()
    print("=" * 70)
    print("                    THEMENAUSWAHL")
    print("=" * 70)
    print()
    print("  Verfügbare Themen:")
    print()
    print("  [1] Signalverarbeitung")
    print("  [2] Computergrafik")
    print()
    print("  [A] Alle Themen")
    print("  [Q] Beenden")
    print()
    print("=" * 70)
    print()
    print("  Du kannst mehrere Themen wählen (z.B. '1 2' oder '12')")
    print()


def get_selected_topics():
    """Ausgewählte Themen zurückgeben"""
    topics = {
        '1': ('Signalverarbeitung', get_signal_questions),
        '2': ('Computergrafik', get_cg_questions),
    }

    while True:
        show_topic_menu()
        choice = input("  Deine Wahl: ").strip().lower()

        if choice == 'q':
            return None

        if choice == 'a':
            selected = []
            for key, (name, func) in topics.items():
                selected.append((name, func()))
            return selected

        selected = []
        seen = set()

        for char in choice:
            if char in topics and char not in seen:
                seen.add(char)
                name, func = topics[char]
                selected.append((name, func()))

        if selected:
            return selected

        print("\n  Ungültige Auswahl! Bitte wähle 1, 2, A oder Q.")
        input("  Drücke ENTER...")


def show_results(correct: int, total: int):
    """Ergebnisse anzeigen"""
    clear_screen()
    print("=" * 70)
    print("                    QUIZ BEENDET!")
    print("=" * 70)
    print()

    percentage = (correct / total * 100) if total > 0 else 0

    print(f"  Richtige Antworten: {correct} von {total}")
    print(f"  Prozent: {percentage:.1f}%")
    print()

    if percentage == 100:
        print("  PERFEKT! Du bist ein Experte!")
    elif percentage >= 80:
        print("  SEHR GUT! Nur kleine Lücken!")
    elif percentage >= 60:
        print("  GUT! Du bist auf dem richtigen Weg!")
    elif percentage >= 40:
        print("  OKAY! Da geht noch mehr!")
    else:
        print("  WEITER ÜBEN! Du schaffst das!")

    print()
    print("=" * 70)


def main():
    """Hauptfunktion"""
    show_greeting()

    while True:
        selected_topics = get_selected_topics()

        if selected_topics is None:
            print("\n  Auf Wiedersehen!")
            break

        all_questions = []
        topic_names = []

        for name, questions in selected_topics:
            topic_names.append(name)
            all_questions.extend(questions)

        if not all_questions:
            print("\n  Keine Fragen verfügbar!")
            input("  Drücke ENTER...")
            continue

        settings = get_quiz_settings(len(all_questions))

        engine = QuizEngine(all_questions, cooldown=settings["cooldown"])
        correct, total = engine.run(
            question_limit=settings["question_limit"],
            allow_repeats=settings["allow_repeats"],
            shuffle_questions=settings["shuffle_questions"],
            shuffle_answers=settings["shuffle_answers"],
        )

        show_results(correct, total)

        again = input("\n  Noch eine Runde? (j/n): ").strip().lower()
        if again != 'j':
            print("\n  Auf Wiedersehen!")
            break


if __name__ == "__main__":
    main()
