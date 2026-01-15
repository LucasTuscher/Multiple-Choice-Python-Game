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
    print("    - Beantworte die Fragen (z.B. 'B' oder 'B D' für mehrere)")
    print("    - Die Fragen kommen zufällig, aber nicht direkt doppelt")
    print("    - Nach jeder Antwort bekommst du eine Erklärung")
    print()
    print("    Befehle während des Quiz:")
    print("    - 'weiter' = Frage überspringen")
    print("    - 'quit'   = Quiz beenden")
    print()
    print("=" * 70)
    input("\nDrücke ENTER um fortzufahren...")


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

        clear_screen()
        print(f"\n  Starte Quiz mit: {', '.join(topic_names)}")
        print(f"  Anzahl Fragen: {len(all_questions)}")
        input("\n  Drücke ENTER um zu starten...")

        engine = QuizEngine(all_questions)
        correct, total = engine.run()

        show_results(correct, total)

        again = input("\n  Noch eine Runde? (j/n): ").strip().lower()
        if again != 'j':
            print("\n  Auf Wiedersehen!")
            break


if __name__ == "__main__":
    main()
