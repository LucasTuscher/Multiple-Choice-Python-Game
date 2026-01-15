#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Multiple-Choice-Quiz - Moderne GUI
Plattformuebergreifende GUI mit CustomTkinter
Funktioniert auf macOS, Windows und Linux
"""

import customtkinter as ctk
from tkinter import messagebox
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from quiz_engine import Question
from questions.signalverarbeitung import get_questions as get_signal_questions
from questions.computergrafik import get_questions as get_cg_questions


# Appearance Mode und Farbschema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class QuizGUI(ctk.CTk):
    """Hauptklasse für die Quiz-GUI"""

    def __init__(self):
        super().__init__()

        # Fenster-Einstellungen
        self.title("Lern-Quiz")
        self.geometry("950x750")
        self.minsize(850, 650)

        # Farben
        self.colors = {
            'bg': '#1a1a2e',
            'card': '#252542',
            'card_hover': '#2d2d4a',
            'accent': '#6366f1',
            'accent_hover': '#818cf8',
            'success': '#22c55e',
            'error': '#ef4444',
            'warning': '#f59e0b',
            'text': '#f8fafc',
            'text_muted': '#94a3b8',
        }

        # Hintergrundfarbe
        self.configure(fg_color=self.colors['bg'])

        # Variablen
        self.all_questions: list[Question] = []
        self.current_questions: list[Question] = []
        self.current_index = 0
        self.selected_answers: set[str] = set()
        self.correct_count = 0
        self.total_answered = 0
        self.answer_buttons: dict[str, ctk.CTkButton] = {}

        # Themen
        self.topics = {
            'Signalverarbeitung': get_signal_questions,
            'Computergrafik': get_cg_questions,
        }
        self.selected_topics: dict[str, ctk.BooleanVar] = {}

        # Hauptcontainer
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=30, pady=30)

        # Startbildschirm
        self.show_welcome_screen()

    def clear_container(self):
        """Entfernt alle Widgets"""
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        """Zeigt den Willkommensbildschirm"""
        self.clear_container()

        # Zentrierter Container
        center_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Logo / Titel
        title_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        title_frame.pack(pady=(0, 20))

        title = ctk.CTkLabel(
            title_frame,
            text="LERN-QUIZ",
            font=ctk.CTkFont(size=52, weight="bold"),
            text_color=self.colors['accent']
        )
        title.pack()

        subtitle = ctk.CTkLabel(
            title_frame,
            text="Teste dein Wissen!",
            font=ctk.CTkFont(size=18),
            text_color=self.colors['text_muted']
        )
        subtitle.pack(pady=(5, 0))

        # Info-Karte
        info_card = ctk.CTkFrame(
            center_frame,
            fg_color=self.colors['card'],
            corner_radius=15
        )
        info_card.pack(pady=30, padx=20)

        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(padx=40, pady=30)

        info_title = ctk.CTkLabel(
            info_inner,
            text="So funktioniert's:",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['text']
        )
        info_title.pack(anchor="w", pady=(0, 15))

        instructions = [
            ("1.", "Waehle ein oder mehrere Themen aus"),
            ("2.", "Klicke auf die Antworten (mehrere moeglich)"),
            ("3.", "Bestatige mit dem Pruefen-Button"),
            ("4.", "Lerne aus den ausfuehrlichen Erklaerungen"),
        ]

        for num, text in instructions:
            row = ctk.CTkFrame(info_inner, fg_color="transparent")
            row.pack(anchor="w", pady=4)

            ctk.CTkLabel(
                row,
                text=num,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=self.colors['accent'],
                width=30
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=text,
                font=ctk.CTkFont(size=14),
                text_color=self.colors['text_muted']
            ).pack(side="left", padx=(5, 0))

        # Start Button
        start_btn = ctk.CTkButton(
            center_frame,
            text="Quiz starten",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            corner_radius=10,
            height=50,
            width=250,
            command=self.show_topic_selection
        )
        start_btn.pack(pady=30)

    def show_topic_selection(self):
        """Zeigt die Themenauswahl"""
        self.clear_container()

        # Zentrierter Container
        center_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Titel
        title = ctk.CTkLabel(
            center_frame,
            text="Themenauswahl",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=self.colors['text']
        )
        title.pack(pady=(0, 10))

        subtitle = ctk.CTkLabel(
            center_frame,
            text="Waehle die Themen, die du ueben moechtest",
            font=ctk.CTkFont(size=14),
            text_color=self.colors['text_muted']
        )
        subtitle.pack(pady=(0, 30))

        # Themen-Karte
        topics_card = ctk.CTkFrame(
            center_frame,
            fg_color=self.colors['card'],
            corner_radius=15
        )
        topics_card.pack(pady=10)

        topics_inner = ctk.CTkFrame(topics_card, fg_color="transparent")
        topics_inner.pack(padx=50, pady=35)

        self.selected_topics.clear()

        for topic_name in self.topics.keys():
            var = ctk.BooleanVar(value=False)
            self.selected_topics[topic_name] = var

            topic_frame = ctk.CTkFrame(topics_inner, fg_color="transparent")
            topic_frame.pack(anchor="w", pady=12)

            cb = ctk.CTkCheckBox(
                topic_frame,
                text=topic_name,
                variable=var,
                font=ctk.CTkFont(size=16),
                text_color=self.colors['text'],
                fg_color=self.colors['accent'],
                hover_color=self.colors['accent_hover'],
                border_color=self.colors['text_muted'],
                checkmark_color=self.colors['text'],
                corner_radius=5,
                border_width=2
            )
            cb.pack(side="left")

            num_questions = len(self.topics[topic_name]())
            count_label = ctk.CTkLabel(
                topic_frame,
                text=f"({num_questions} Fragen)",
                font=ctk.CTkFont(size=13),
                text_color=self.colors['text_muted']
            )
            count_label.pack(side="left", padx=(15, 0))

        # Alle auswaehlen Button
        all_btn = ctk.CTkButton(
            topics_inner,
            text="Alle auswaehlen",
            font=ctk.CTkFont(size=13),
            fg_color="transparent",
            hover_color=self.colors['card_hover'],
            border_color=self.colors['text_muted'],
            border_width=1,
            text_color=self.colors['text_muted'],
            corner_radius=8,
            height=35,
            command=lambda: [var.set(True) for var in self.selected_topics.values()]
        )
        all_btn.pack(pady=(25, 0))

        # Buttons
        button_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        button_frame.pack(pady=35)

        back_btn = ctk.CTkButton(
            button_frame,
            text="Zurueck",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['card'],
            hover_color=self.colors['card_hover'],
            corner_radius=10,
            height=45,
            width=150,
            command=self.show_welcome_screen
        )
        back_btn.pack(side="left", padx=10)

        start_btn = ctk.CTkButton(
            button_frame,
            text="Quiz starten",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            corner_radius=10,
            height=45,
            width=150,
            command=self.start_quiz
        )
        start_btn.pack(side="left", padx=10)

    def start_quiz(self):
        """Startet das Quiz"""
        self.all_questions = []

        for topic_name, var in self.selected_topics.items():
            if var.get():
                questions = self.topics[topic_name]()
                self.all_questions.extend(questions)

        if not self.all_questions:
            messagebox.showwarning(
                "Keine Themen",
                "Bitte waehle mindestens ein Thema aus!"
            )
            return

        self.current_questions = self.all_questions.copy()
        random.shuffle(self.current_questions)

        self.current_index = 0
        self.correct_count = 0
        self.total_answered = 0
        self.selected_answers.clear()

        self.show_question()

    def show_question(self):
        """Zeigt die aktuelle Frage"""
        self.clear_container()
        self.selected_answers.clear()
        self.answer_buttons.clear()

        if self.current_index >= len(self.current_questions):
            self.show_results()
            return

        question = self.current_questions[self.current_index]

        # Header
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))

        # Fortschritt links
        progress_text = f"Frage {self.current_index + 1} von {len(self.current_questions)}"
        progress_label = ctk.CTkLabel(
            header_frame,
            text=progress_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['text_muted']
        )
        progress_label.pack(side="left")

        # Score rechts
        if self.total_answered > 0:
            score_text = f"Richtig: {self.correct_count}/{self.total_answered}"
            score_label = ctk.CTkLabel(
                header_frame,
                text=score_text,
                font=ctk.CTkFont(size=13),
                text_color=self.colors['success']
            )
            score_label.pack(side="right")

        # Thema-Badge
        if question.topic:
            topic_badge = ctk.CTkLabel(
                header_frame,
                text=question.topic,
                font=ctk.CTkFont(size=11),
                text_color=self.colors['text'],
                fg_color=self.colors['card'],
                corner_radius=5,
                padx=10,
                pady=3
            )
            topic_badge.pack(side="right", padx=(0, 15))

        # Fortschrittsbalken
        progress_bar = ctk.CTkProgressBar(
            self.main_container,
            progress_color=self.colors['accent'],
            fg_color=self.colors['card'],
            height=6,
            corner_radius=3
        )
        progress_bar.pack(fill="x", pady=(0, 20))
        progress_bar.set((self.current_index + 1) / len(self.current_questions))

        # Frage-Karte
        question_card = ctk.CTkFrame(
            self.main_container,
            fg_color=self.colors['card'],
            corner_radius=12
        )
        question_card.pack(fill="x", pady=(0, 20))

        question_inner = ctk.CTkFrame(question_card, fg_color="transparent")
        question_inner.pack(padx=25, pady=20, fill="x")

        question_label = ctk.CTkLabel(
            question_inner,
            text=question.prompt,
            font=ctk.CTkFont(size=15),
            text_color=self.colors['text'],
            wraplength=800,
            justify="left"
        )
        question_label.pack(anchor="w")

        # Mehrfachauswahl-Hinweis
        if len(question.correct) > 1:
            hint_label = ctk.CTkLabel(
                question_inner,
                text="(Mehrfachauswahl moeglich)",
                font=ctk.CTkFont(size=12, slant="italic"),
                text_color=self.colors['warning']
            )
            hint_label.pack(anchor="w", pady=(10, 0))

        # Scrollbarer Bereich für Antworten
        answers_scroll = ctk.CTkScrollableFrame(
            self.main_container,
            fg_color="transparent",
            height=280
        )
        answers_scroll.pack(fill="both", expand=True, pady=(0, 15))

        # Antwort-Buttons
        for key in sorted(question.options.keys()):
            option_text = question.options[key]
            self.create_answer_button(answers_scroll, key, option_text)

        # Action Buttons
        button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

        # Links: Skip und Quit
        left_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        left_buttons.pack(side="left")

        skip_btn = ctk.CTkButton(
            left_buttons,
            text="Ueberspringen",
            font=ctk.CTkFont(size=13),
            fg_color=self.colors['card'],
            hover_color=self.colors['card_hover'],
            corner_radius=8,
            height=42,
            width=130,
            command=self.skip_question
        )
        skip_btn.pack(side="left", padx=(0, 10))

        quit_btn = ctk.CTkButton(
            left_buttons,
            text="Beenden",
            font=ctk.CTkFont(size=13),
            fg_color=self.colors['card'],
            hover_color=self.colors['card_hover'],
            corner_radius=8,
            height=42,
            width=100,
            command=self.confirm_quit
        )
        quit_btn.pack(side="left")

        # Rechts: Pruefen
        check_btn = ctk.CTkButton(
            button_frame,
            text="Pruefen",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            corner_radius=8,
            height=42,
            width=140,
            command=self.check_answer
        )
        check_btn.pack(side="right")

    def create_answer_button(self, parent, key: str, text: str):
        """Erstellt einen Antwort-Button"""
        btn = ctk.CTkButton(
            parent,
            text=f"  {key})   {text}",
            font=ctk.CTkFont(size=13),
            fg_color=self.colors['card'],
            hover_color=self.colors['card_hover'],
            text_color=self.colors['text'],
            anchor="w",
            corner_radius=10,
            height=55,
            border_width=2,
            border_color=self.colors['card'],
            command=lambda k=key: self.toggle_answer(k)
        )
        btn.pack(fill="x", pady=5)
        self.answer_buttons[key] = btn

    def toggle_answer(self, key: str):
        """Togglet eine Antwort"""
        btn = self.answer_buttons[key]

        if key in self.selected_answers:
            self.selected_answers.remove(key)
            btn.configure(
                fg_color=self.colors['card'],
                border_color=self.colors['card']
            )
        else:
            self.selected_answers.add(key)
            btn.configure(
                fg_color=self.colors['accent'],
                border_color=self.colors['accent_hover']
            )

    def check_answer(self):
        """Prueft die Antwort"""
        if not self.selected_answers:
            messagebox.showinfo("Hinweis", "Bitte waehle mindestens eine Antwort aus!")
            return

        question = self.current_questions[self.current_index]
        is_correct = self.selected_answers == question.correct

        if is_correct:
            self.correct_count += 1
        self.total_answered += 1

        self.show_feedback(question, is_correct)

    def show_feedback(self, question: Question, is_correct: bool):
        """Zeigt das Feedback"""
        self.clear_container()

        # Scrollbarer Bereich
        scroll_frame = ctk.CTkScrollableFrame(
            self.main_container,
            fg_color="transparent"
        )
        scroll_frame.pack(fill="both", expand=True)

        # Ergebnis-Banner
        result_color = self.colors['success'] if is_correct else self.colors['error']
        result_text = "RICHTIG!" if is_correct else "FALSCH!"

        result_frame = ctk.CTkFrame(
            scroll_frame,
            fg_color=result_color,
            corner_radius=12
        )
        result_frame.pack(fill="x", pady=(0, 20))

        result_label = ctk.CTkLabel(
            result_frame,
            text=result_text,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        )
        result_label.pack(pady=18)

        # Antwort-Vergleich
        compare_card = ctk.CTkFrame(
            scroll_frame,
            fg_color=self.colors['card'],
            corner_radius=12
        )
        compare_card.pack(fill="x", pady=(0, 15))

        compare_inner = ctk.CTkFrame(compare_card, fg_color="transparent")
        compare_inner.pack(padx=25, pady=18)

        your_answer = "  ".join(sorted(self.selected_answers)) if self.selected_answers else "(keine)"
        correct_answer = "  ".join(sorted(question.correct))

        ctk.CTkLabel(
            compare_inner,
            text=f"Deine Antwort:      {your_answer}",
            font=ctk.CTkFont(size=14),
            text_color=self.colors['text']
        ).pack(anchor="w", pady=3)

        ctk.CTkLabel(
            compare_inner,
            text=f"Richtige Antwort:  {correct_answer}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['success']
        ).pack(anchor="w", pady=3)

        # Erklaerung
        explain_card = ctk.CTkFrame(
            scroll_frame,
            fg_color=self.colors['card'],
            corner_radius=12
        )
        explain_card.pack(fill="x", pady=(0, 15))

        explain_inner = ctk.CTkFrame(explain_card, fg_color="transparent")
        explain_inner.pack(padx=25, pady=18, fill="x")

        ctk.CTkLabel(
            explain_inner,
            text="Erklaerung",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['accent']
        ).pack(anchor="w", pady=(0, 12))

        ctk.CTkLabel(
            explain_inner,
            text=question.explain_correct,
            font=ctk.CTkFont(size=13),
            text_color=self.colors['text'],
            wraplength=750,
            justify="left"
        ).pack(anchor="w")

        # Falsche Optionen
        wrong_options = set(question.options.keys()) - question.correct
        if wrong_options and question.explain_wrong:
            wrong_card = ctk.CTkFrame(
                scroll_frame,
                fg_color=self.colors['card'],
                corner_radius=12
            )
            wrong_card.pack(fill="x", pady=(0, 15))

            wrong_inner = ctk.CTkFrame(wrong_card, fg_color="transparent")
            wrong_inner.pack(padx=25, pady=18, fill="x")

            ctk.CTkLabel(
                wrong_inner,
                text="Warum die anderen Optionen falsch sind",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=self.colors['text_muted']
            ).pack(anchor="w", pady=(0, 12))

            for opt in sorted(wrong_options):
                if opt in question.explain_wrong:
                    opt_frame = ctk.CTkFrame(wrong_inner, fg_color="transparent")
                    opt_frame.pack(anchor="w", pady=4, fill="x")

                    ctk.CTkLabel(
                        opt_frame,
                        text=f"{opt})",
                        font=ctk.CTkFont(size=12, weight="bold"),
                        text_color=self.colors['error'],
                        width=25
                    ).pack(side="left", anchor="n")

                    ctk.CTkLabel(
                        opt_frame,
                        text=question.explain_wrong[opt],
                        font=ctk.CTkFont(size=12),
                        text_color=self.colors['text_muted'],
                        wraplength=700,
                        justify="left"
                    ).pack(side="left", padx=(8, 0), anchor="w")

        # Weiter-Button
        next_btn = ctk.CTkButton(
            scroll_frame,
            text="Naechste Frage",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            corner_radius=10,
            height=48,
            width=200,
            command=self.next_question
        )
        next_btn.pack(pady=25)

    def next_question(self):
        """Naechste Frage"""
        self.current_index += 1
        self.show_question()

    def skip_question(self):
        """Ueberspringt die Frage"""
        self.current_index += 1
        self.show_question()

    def confirm_quit(self):
        """Bestaetigung zum Beenden"""
        if messagebox.askyesno("Quiz beenden", "Moechtest du das Quiz wirklich beenden?"):
            self.show_results()

    def show_results(self):
        """Zeigt die Ergebnisse"""
        self.clear_container()

        # Zentrierter Container
        center_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Titel
        ctk.CTkLabel(
            center_frame,
            text="Quiz beendet!",
            font=ctk.CTkFont(size=38, weight="bold"),
            text_color=self.colors['text']
        ).pack(pady=(0, 30))

        # Ergebnis-Karte
        result_card = ctk.CTkFrame(
            center_frame,
            fg_color=self.colors['card'],
            corner_radius=20
        )
        result_card.pack(pady=10)

        result_inner = ctk.CTkFrame(result_card, fg_color="transparent")
        result_inner.pack(padx=60, pady=40)

        if self.total_answered > 0:
            percentage = (self.correct_count / self.total_answered) * 100
        else:
            percentage = 0

        # Prozent-Anzeige
        percent_color = self.colors['success'] if percentage >= 60 else self.colors['error']

        ctk.CTkLabel(
            result_inner,
            text=f"{percentage:.0f}%",
            font=ctk.CTkFont(size=64, weight="bold"),
            text_color=percent_color
        ).pack()

        ctk.CTkLabel(
            result_inner,
            text=f"{self.correct_count} von {self.total_answered} richtig",
            font=ctk.CTkFont(size=18),
            text_color=self.colors['text']
        ).pack(pady=(10, 20))

        # Bewertung
        if percentage == 100:
            rating = "PERFEKT! Du bist ein Experte!"
            rating_color = self.colors['success']
        elif percentage >= 80:
            rating = "SEHR GUT! Nur kleine Luecken!"
            rating_color = self.colors['success']
        elif percentage >= 60:
            rating = "GUT! Du bist auf dem richtigen Weg!"
            rating_color = self.colors['warning']
        elif percentage >= 40:
            rating = "OKAY! Da geht noch mehr!"
            rating_color = self.colors['warning']
        else:
            rating = "WEITER UEBEN! Du schaffst das!"
            rating_color = self.colors['error']

        ctk.CTkLabel(
            result_inner,
            text=rating,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=rating_color
        ).pack()

        # Buttons
        button_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        button_frame.pack(pady=40)

        retry_btn = ctk.CTkButton(
            button_frame,
            text="Nochmal spielen",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            corner_radius=10,
            height=48,
            width=170,
            command=self.show_topic_selection
        )
        retry_btn.pack(side="left", padx=10)

        quit_btn = ctk.CTkButton(
            button_frame,
            text="Beenden",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['card'],
            hover_color=self.colors['card_hover'],
            corner_radius=10,
            height=48,
            width=140,
            command=self.quit
        )
        quit_btn.pack(side="left", padx=10)


def main():
    """Hauptfunktion"""
    app = QuizGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
