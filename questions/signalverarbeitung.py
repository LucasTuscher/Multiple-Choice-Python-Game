#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fragen zum Thema: Signalverarbeitung
Umfassende Fragensammlung zu Fourier, Sampling, Quantisierung, LTI-Systemen, Audioübertragung etc.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quiz_engine import Question
from typing import List, Dict


def _swap_answer_keys(q: Question, a: str, b: str) -> Question:
    swap = {a: b, b: a}
    options = {swap.get(k, k): v for k, v in q.options.items()}
    correct = {swap.get(k, k) for k in q.correct}
    explain_wrong = {swap.get(k, k): v for k, v in q.explain_wrong.items()}
    return Question(
        prompt=q.prompt,
        options=options,
        correct=correct,
        explain_correct=q.explain_correct,
        explain_wrong=explain_wrong,
        topic=q.topic,
    )


def _rebalance_single_choice_correct_letters(questions: List[Question]) -> List[Question]:
    """
    Viele Fragen hatten historisch correct={'B'}.
    Diese Funktion tauscht Antwortlabels deterministisch, damit die korrekte Option
    über A/B/C/D deutlich gleichmäßiger verteilt ist (ohne Inhalte zu ändern).
    """
    letters = ("A", "B", "C", "D")
    eligible: List[Question] = [
        q for q in questions if len(q.correct) == 1 and set(letters).issubset(set(q.options.keys()))
    ]
    if not eligible:
        return questions

    total = len(eligible)
    base, remainder = divmod(total, len(letters))
    targets: Dict[str, int] = {
        letter: base + (1 if idx < remainder else 0) for idx, letter in enumerate(letters)
    }

    counts: Dict[str, int] = {letter: 0 for letter in letters}
    for q in eligible:
        key = next(iter(q.correct))
        if key in counts:
            counts[key] += 1

    priority: Dict[str, int] = {"D": 3, "A": 2, "C": 1}

    result: List[Question] = []
    for q in questions:
        if (
            len(q.correct) == 1
            and q.correct == {"B"}
            and set(letters).issubset(set(q.options.keys()))
            and counts["B"] > targets["B"]
        ):
            candidates = [k for k in ("A", "C", "D") if counts[k] < targets[k] and k in q.options]
            if candidates:
                candidates.sort(key=lambda k: (targets[k] - counts[k], priority.get(k, 0)), reverse=True)
                target = candidates[0]
                q = _swap_answer_keys(q, "B", target)
                counts["B"] -= 1
                counts[target] += 1

        result.append(q)

    return result


def get_questions() -> List[Question]:
    """Gibt alle Fragen zur Signalverarbeitung zurück"""
    questions = [
        # ============================================================
        # FOURIER-TRANSFORMATION
        # ============================================================
        Question(
            prompt="Unter Anwendung welches Prinzips kann man die Darstellung eines Signals im Zeit- und Frequenzbereich ändern - und zurück?",
            options={
                "A": "Fourierprinzip / Fouriertransformation",
                "B": "Laplace-Transformation",
                "C": "Nyquist-Theorem",
                "D": "Shannon-Theorem"
            },
            correct={"A"},
            explain_correct="Das Fourierprinzip ermöglicht die Umwandlung zwischen Zeit- und Frequenzbereich. "
                          "Die Fouriersynthese baut ein Signal aus Sinusschwingungen auf. "
                          "Die DFT (Diskrete Fourier-Transformation) wandelt vom Zeitbereich in den Frequenzbereich, "
                          "die IDFT (Inverse DFT) macht dies rückgängig.",
            explain_wrong={
                "B": "Die Laplace-Transformation ist eine Verallgemeinerung, wird aber nicht primär für Zeit-Frequenz-Umwandlung verwendet.",
                "C": "Das Nyquist-Theorem beschreibt die minimale Abtastrate, nicht die Transformation zwischen Bereichen.",
                "D": "Das Shannon-Theorem ist ein anderer Name für das Nyquist-Theorem."
            },
            topic="Signalverarbeitung - Fourier"
        ),

        Question(
            prompt="Was beschreibt die Fouriersynthese?",
            options={
                "A": "Die Zerlegung eines Signals in einzelne Frequenzen",
                "B": "Den Aufbau eines Signals aus überlagerten Sinusschwingungen",
                "C": "Die Digitalisierung eines analogen Signals",
                "D": "Die Filterung von Störfrequenzen"
            },
            correct={"B"},
            explain_correct="Die Fouriersynthese beschreibt, wie man ein beliebiges periodisches Signal "
                          "durch Überlagerung (Addition) von Sinus- und Kosinusschwingungen verschiedener "
                          "Frequenzen, Amplituden und Phasen aufbauen kann. Dies ist das Gegenstück zur "
                          "Fourieranalyse, die ein Signal in seine Frequenzanteile zerlegt.",
            explain_wrong={
                "A": "Das ist die Fourieranalyse, nicht die Synthese.",
                "C": "Digitalisierung erfolgt durch Sampling und Quantisierung.",
                "D": "Filterung ist ein separater Prozess."
            },
            topic="Signalverarbeitung - Fourier"
        ),

        Question(
            prompt="Was macht die DFT (Diskrete Fourier-Transformation)?",
            options={
                "A": "Wandelt vom Frequenzbereich in den Zeitbereich",
                "B": "Wandelt vom Zeitbereich in den Frequenzbereich",
                "C": "Digitalisiert ein analoges Signal",
                "D": "Filtert hohe Frequenzen heraus"
            },
            correct={"B"},
            explain_correct="Die DFT (Diskrete Fourier-Transformation) nimmt ein zeitdiskretes Signal "
                          "und berechnet dessen Frequenzspektrum. Sie zeigt, welche Frequenzen mit "
                          "welcher Amplitude und Phase im Signal enthalten sind. Die FFT (Fast Fourier Transform) "
                          "ist eine effiziente Implementierung der DFT.",
            explain_wrong={
                "A": "Das macht die IDFT (Inverse DFT).",
                "C": "Digitalisierung ist Sampling + Quantisierung.",
                "D": "Filterung ist ein separater Prozess."
            },
            topic="Signalverarbeitung - Fourier"
        ),

        Question(
            prompt="Was ist der Unterschied zwischen DFT (Discrete Fourier Transform – Diskrete Fourier-Transformation) und FFT (Fast Fourier Transform – Schnelle Fourier-Transformation)?",
            options={
                "A": "FFT ist eine schnelle Implementierung der DFT",
                "B": "DFT ist für analoge, FFT für digitale Signale",
                "C": "FFT liefert genauere Ergebnisse",
                "D": "Es gibt keinen Unterschied"
            },
            correct={"A"},
            explain_correct="Die FFT (Fast Fourier Transform) ist ein effizienter Algorithmus zur "
                          "Berechnung der DFT. Während die direkte DFT O(N^2) Operationen benötigt, "
                          "schafft die FFT das gleiche Ergebnis mit nur O(N log N) Operationen. "
                          "Bei 1000 Samples ist die FFT also etwa 100x schneller!",
            explain_wrong={
                "B": "Beide arbeiten mit diskreten (digitalen) Signalen.",
                "C": "Beide liefern mathematisch identische Ergebnisse.",
                "D": "Der Unterschied liegt in der Recheneffizienz."
            },
            topic="Signalverarbeitung - Fourier"
        ),

        # ============================================================
        # ANALOG VS. DIGITAL
        # ============================================================
        Question(
            prompt="Was ist ein analoges Signal?",
            options={
                "A": "Ein zeit- und wertdiskretes Signal",
                "B": "Ein zeit- und wertkontinuierliches Signal",
                "C": "Ein zeitkontinuierliches, aber wertdiskretes Signal",
                "D": "Ein zeitdiskretes, aber wertkontinuierliches Signal"
            },
            correct={"B"},
            explain_correct="Ein analoges Signal ist sowohl zeitkontinuierlich (existiert zu jedem Zeitpunkt) "
                          "als auch wertkontinuierlich (kann jeden beliebigen Wert annehmen). "
                          "Beispiele sind Schallwellen in der Luft, elektrische Spannungen aus einem Mikrofon, "
                          "oder Lichintensitaet. Es gibt keine 'Stufen' oder 'Sprünge'.",
            explain_wrong={
                "A": "Das beschreibt ein digitales Signal.",
                "C": "Das waere ein quantisiertes, aber nicht abgetastetes Signal.",
                "D": "Das waere ein abgetastetes, aber nicht quantisiertes Signal."
            },
            topic="Signalverarbeitung - Grundlagen"
        ),

        Question(
            prompt="Was ist ein digitales Signal?",
            options={
                "A": "Ein zeit- und wertkontinuierliches Signal",
                "B": "Ein zeitkontinuierliches, aber wertdiskretes Signal",
                "C": "Ein zeit- und wertdiskretes Signal",
                "D": "Ein Signal das nur Nullen enthält"
            },
            correct={"C"},
            explain_correct="Ein digitales Signal ist sowohl zeitdiskret (existiert nur zu bestimmten "
                          "Abtastzeitpunkten) als auch wertdiskret (kann nur bestimmte Werte/Stufen annehmen). "
                          "Es entsteht durch Sampling (Zeitdiskretisierung) und Quantisierung (Wertdiskretisierung) "
                          "eines analogen Signals. Computer können nur digitale Signale verarbeiten.",
            explain_wrong={
                "A": "Das ist ein analoges Signal.",
                "B": "Zeitkontinuierlich + wertdiskret ist kein vollständig digitales Signal.",
                "D": "Digitale Signale können beliebige diskrete Werte haben."
            },
            topic="Signalverarbeitung - Grundlagen"
        ),

        # ============================================================
        # SAMPLING & ABTASTUNG
        # ============================================================
        Question(
            prompt="Was versteht man unter 'Sampling' (Abtastung)?",
            options={
                "A": "Die Wertdiskretisierung eines Signals",
                "B": "Die Zeitdiskretisierung eines analogen Signals",
                "C": "Die Verstärkung eines Signals",
                "D": "Die Filterung von Rauschen"
            },
            correct={"B"},
            explain_correct="Sampling (Abtastung) ist die Zeitdiskretisierung - das Signal wird nur "
                          "zu bestimmten regelmäßigen Zeitpunkten gemessen. Aus einem kontinuierlichen "
                          "Signal werden diskrete Messwerte. Die Wertdiskretisierung heisst dagegen Quantisierung. "
                          "Zusammen (Sampling + Quantisierung) ergibt das die A/D-Wandlung.",
            explain_wrong={
                "A": "Das ist Quantisierung, nicht Sampling.",
                "C": "Verstärkung aendert nur die Amplitude.",
                "D": "Filterung ist ein separater Prozess."
            },
            topic="Signalverarbeitung - Sampling"
        ),

        Question(
            prompt="Wovon hängt die minimale Abtastrate bei der Digitalisierung ab?",
            options={
                "A": "Von der Amplitude des Signals",
                "B": "Von der Länge des Signals",
                "C": "Von der höchsten vorkommenden Frequenz des Signals",
                "D": "Von der Bittiefe"
            },
            correct={"C"},
            explain_correct="Nach dem Nyquist-Shannon-Theorem muss die Abtastrate mindestens doppelt so hoch sein "
                          "wie die höchste im Signal vorkommende Frequenz. Bei einem Signal mit maximal 20 kHz "
                          "(menschliches Hören) braucht man also mindestens 40 kHz Abtastrate. "
                          "CDs verwenden 44.1 kHz, um etwas Spielraum zu haben.",
            explain_wrong={
                "A": "Die Amplitude beeinflusst die nötige Bittiefe, nicht die Abtastrate.",
                "B": "Die Signallänge ist irrelevant für die Abtastrate.",
                "D": "Die Bittiefe betrifft die Quantisierung, nicht das Sampling."
            },
            topic="Signalverarbeitung - Sampling"
        ),

        Question(
            prompt="Wie groß muss die Abtastrate mindestens sein?",
            options={
                "A": "Mindestens gleich der höchsten Signalfrequenz",
                "B": "Mindestens 2x die höchste Signalfrequenz (Nyquist-Theorem)",
                "C": "Mindestens 10x die höchste Signalfrequenz",
                "D": "Die Abtastrate ist egal"
            },
            correct={"B"},
            explain_correct="Das Nyquist-Shannon-Theorem besagt: Die Abtastfrequenz muss mindestens "
                          "doppelt so hoch sein wie die höchste Signalfrequenz (fs > 2 * fmax). "
                          "Nur dann kann das Signal aus den Abtastwerten vollständig rekonstruiert werden. "
                          "Diese Grenze heisst Nyquist-Frequenz (= fs/2).",
            explain_wrong={
                "A": "Das reicht nicht aus - es muss mindestens das Doppelte sein.",
                "C": "Das waere mehr als nötig, schadet aber nicht.",
                "D": "Eine zu niedrige Abtastrate führt zu Aliasing!"
            },
            topic="Signalverarbeitung - Sampling"
        ),

        Question(
            prompt="Welcher Effekt tritt auf, wenn die Samplerate zu niedrig ist?",
            options={
                "A": "Clipping",
                "B": "Rauschen",
                "C": "Aliasing",
                "D": "Verstärkung"
            },
            correct={"C"},
            explain_correct="Aliasing tritt auf, wenn die Abtastrate zu niedrig ist (unter dem Nyquist-Limit). "
                          "Hohe Frequenzen werden dann fälschlicherweise als niedrigere Frequenzen interpretiert - "
                          "sie 'spiegeln' sich am Nyquist-Punkt. Das führt zu hoerbaren Artefakten und "
                          "Verzerrungen, die nicht mehr rückgängig gemacht werden können.",
            explain_wrong={
                "A": "Clipping entsteht durch Übersteuerung, nicht durch niedrige Abtastrate.",
                "B": "Rauschen hat andere Ursachen.",
                "D": "Verstärkung ist unabhaengig von der Abtastrate."
            },
            topic="Signalverarbeitung - Sampling"
        ),

        Question(
            prompt="Welchen technischen Zusatz verwendet man, um Aliasing zu vermeiden?",
            options={
                "A": "Anti-Aliasing-Filter",
                "B": "Verstärker",
                "C": "Kompressor",
                "D": "Equalizer"
            },
            correct={"A"},
            explain_correct="Ein Anti-Aliasing-Filter ist ein Tiefpassfilter, der vor dem A/D-Wandler geschaltet wird. "
                          "Er entfernt alle Frequenzen oberhalb der halben Abtastfrequenz (Nyquist-Frequenz), "
                          "bevor das Signal abgetastet wird. So wird sichergestellt, dass das Nyquist-Theorem "
                          "eingehalten wird und kein Aliasing entstehen kann.",
            explain_wrong={
                "B": "Ein Verstaerker aendert nur die Amplitude.",
                "C": "Ein Kompressor reduziert die Dynamik.",
                "D": "Ein Equalizer formt das Frequenzspektrum, verhindert aber nicht Aliasing."
            },
            topic="Signalverarbeitung - Sampling"
        ),

        Question(
            prompt="Welche Abtastraten und Quantisierungen sind in der Audiotechnik üblich?",
            options={
                "A": "CD-Qualität: 44.1 kHz / 16 Bit",
                "B": "Studio-Qualität: 48, 96 oder 192 kHz / 24 Bit",
                "C": "Telefon-Qualität: 8 kHz / 8 Bit",
                "D": "MP3-Standard: 22 kHz / 4 Bit"
            },
            correct={"A", "B", "C"},
            explain_correct="Alle diese Standards existieren: CD verwendet 44.1 kHz/16 Bit, "
                          "professionelle Studios arbeiten mit 48-192 kHz und 24 Bit für mehr Dynamik und Headroom, "
                          "und Telefonie nutzt aus historischen Gruenden nur 8 kHz/8 Bit (ausreichend für Sprache). "
                          "Höhere Werte bedeuten bessere Qualität, aber auch mehr Speicherbedarf.",
            explain_wrong={
                "D": "MP3 ist ein Kompressionsformat, kein Standard für Abtastrate/Quantisierung. MP3 arbeitet typischerweise mit 44.1 kHz."
            },
            topic="Signalverarbeitung - Sampling"
        ),

        Question(
            prompt="Ein analoges Signal besteht aus Sinustönen mit Periodendauern T1=3.79ms, T2=3.03ms, T3=2.53ms. "
                   "Welche Abtastfrequenz ist mindestens nötig?",
            options={
                "A": "264 Hz",
                "B": "396 Hz",
                "C": "792 Hz",
                "D": "1584 Hz"
            },
            correct={"C"},
            explain_correct="Zuerst die Frequenzen berechnen: f1=1/0.00379≈264Hz, f2=1/0.00303≈330Hz, "
                          "f3=1/0.00253≈396Hz. Die höchste Frequenz ist 396 Hz. Nach dem Nyquist-Theorem "
                          "muss die Abtastfrequenz mindestens 2 x 396 Hz = 792 Hz betragen, "
                          "um Aliasing zu vermeiden.",
            explain_wrong={
                "A": "264 Hz ist nur die niedrigste Signalfrequenz.",
                "B": "396 Hz ist die höchste Signalfrequenz, aber wir brauchen das Doppelte.",
                "D": "1584 Hz wäre mehr als nötig (4x statt 2x)."
            },
            topic="Signalverarbeitung - Sampling"
        ),

        # ============================================================
        # QUANTISIERUNG
        # ============================================================
        Question(
            prompt="Was versteht man unter Quantisierung?",
            options={
                "A": "Die zeitliche Abtastung eines Signals",
                "B": "Die Umwandlung kontinuierlicher Amplitudenwerte in diskrete Stufen",
                "C": "Die Verstärkung eines Signals",
                "D": "Die Filterung von Rauschen"
            },
            correct={"B"},
            explain_correct="Quantisierung ist die Wertdiskretisierung - kontinuierliche Amplitudenwerte "
                          "werden auf diskrete Stufen gerundet. Bei 8 Bit gibt es 256 Stufen, bei 16 Bit "
                          "65536 Stufen. Je mehr Bit, desto feiner die Abstufung und desto geringer das "
                          "Quantisierungsrauschen. Die Bittiefe bestimmt den Dynamikumfang (ca. 6 dB pro Bit).",
            explain_wrong={
                "A": "Das ist Sampling, nicht Quantisierung.",
                "C": "Verstärkung aendert nur die Amplitude.",
                "D": "Filterung ist ein separater Prozess."
            },
            topic="Signalverarbeitung - Quantisierung"
        ),

        # ============================================================
        # SIGNALUEBERTRAGUNG
        # ============================================================
        Question(
            prompt="Mit welcher Geschwindigkeit werden Audiosignale in der Luft übertragen?",
            options={
                "A": "Lichtgeschwindigkeit (~300'000 km/s)",
                "B": "Ca. 343 m/s (Schallgeschwindigkeit)",
                "C": "Ca. 1000 m/s",
                "D": "Ca. 100 m/s"
            },
            correct={"B"},
            explain_correct="Schall breitet sich in Luft bei Raumtemperatur mit etwa 343 m/s aus "
                          "(ca. 1235 km/h). Dies ist viel langsamer als Licht oder elektrische Signale. "
                          "Die Schallgeschwindigkeit hängt von Temperatur und Medium ab - "
                          "in Wasser ca. 1500 m/s, in Stahl ca. 5000 m/s.",
            explain_wrong={
                "A": "Das gilt für elektromagnetische Wellen, nicht für Schall.",
                "C": "Die Schallgeschwindigkeit ist niedriger.",
                "D": "Die Schallgeschwindigkeit ist hoeher."
            },
            topic="Signalverarbeitung - Übertragung"
        ),

        Question(
            prompt="Mit welcher Geschwindigkeit werden Signale in elektronischen Medien übertragen?",
            options={
                "A": "Ca. 343 m/s",
                "B": "Ca. 1000 km/s",
                "C": "Nahe Lichtgeschwindigkeit (~300'000 km/s)",
                "D": "Ca. 10'000 m/s"
            },
            correct={"C"},
            explain_correct="Elektrische Signale in Kabeln breiten sich mit einem großen Teil der "
                          "Lichtgeschwindigkeit aus (typisch 60-90% von c, also ca. 180'000-270'000 km/s). "
                          "Bei Glasfaserkabeln ist es ähnlich. Das ist so schnell, dass Latenzen "
                          "durch Kabellänge in der Audiotechnik vernachlässigbar sind.",
            explain_wrong={
                "A": "Das ist die Schallgeschwindigkeit in Luft.",
                "B": "Elektronische Signale sind viel schneller.",
                "D": "Elektronische Signale sind viel schneller."
            },
            topic="Signalverarbeitung - Übertragung"
        ),

        Question(
            prompt="Welche Signalverzögerung entsteht in der Luft pro Meter Abstand?",
            options={
                "A": "Ca. 0.3 ms pro Meter",
                "B": "Ca. 3 ms pro Meter",
                "C": "Ca. 30 ms pro Meter",
                "D": "Ca. 0.03 ms pro Meter"
            },
            correct={"B"},
            explain_correct="Bei 343 m/s Schallgeschwindigkeit dauert es 1/343 Sekunde ≈ 2.9 ms pro Meter. "
                          "Gerundet also etwa 3 ms pro Meter. Bei 10 Metern Entfernung beträgt die "
                          "Verzoegerung also ca. 30 ms - das ist in der Audiotechnik relevant "
                          "(z.B. bei Delay-Einstellungen für PA-Systeme).",
            explain_wrong={
                "A": "Das waere zu schnell für Schall.",
                "C": "Das waere zu langsam.",
                "D": "Das waere fast Lichtgeschwindigkeit."
            },
            topic="Signalverarbeitung - Übertragung"
        ),

        Question(
            prompt="Was sind Vorteile der symmetrischen gegenüber der asymmetrischen Signalübertragung?",
            options={
                "A": "Bessere Störunterdrückung durch Gleichtaktunterdrückung",
                "B": "Längere Kabelwege möglich",
                "C": "Günstiger und einfacher",
                "D": "Günstiger und kleinere Kabelwege"
            },
            correct={"A", "B"},
            explain_correct="Bei symmetrischer Übertragung wird das Signal zweimal geführt: normal und invertiert. "
                          "Am Empfaenger wird die Differenz gebildet - Störungen, die auf beide Leiter gleich wirken, "
                          "heben sich dabei auf (Gleichtaktunterdrückung). Dadurch sind laengere Kabelwege möglich. "
                          "Nachteile: höhere Kosten und Komplexitaet (3 Leiter statt 2).",
            explain_wrong={
                "C": "Asymmetrische Übertragung ist guenstiger und einfacher.",
                "D": "Günstige Systeme mit kurzen Kabelwegen sind typisch für asymmetrische Übertragung."
                     "Symmetrische Übertragung ist aufwändiger(zusätzlicher Leiter, Differenzverstärker)"
                     "und wird gerade eingesetzt, um längere Kabelwege störungsarm zu ermöglichen."

    },
            topic="Signalverarbeitung - Übertragung"
        ),

        Question(
            prompt="Welche Steckverbinder nutzt man typischerweise für asymmetrische Signalübertragung?",
            options={
                "A": "Cinch/RCA",
                "B": "6.3mm Klinke (mono)",
                "C": "3.5mm Miniklinke",
                "D": "XLR-Stecker"
            },
            correct={"A", "B", "C"},
            explain_correct="Asymmetrische Übertragung verwendet 2-polige Verbindungen (Signal + Masse). "
                          "Cinch/RCA ist Standard im HiFi-Bereich, 6.3mm Klinke bei Instrumenten und "
                          "älteren Geräten, 3.5mm Miniklinke bei Kopfhörern und mobilen Geräten. "
                          "Fuer symmetrische Übertragung verwendet man XLR oder 6.3mm Stereo-Klinke (TRS).",
            explain_wrong={
                "D": "XLR-Stecker werden für symmetrische Signaluebertragung verwendet, nicht asymmetrische."
            },
            topic="Signalverarbeitung - Übertragung"
        ),

        Question(
            prompt="Wie wird symmetrische Signaluebertragung technisch realisiert?",
            options={
                "A": "Das Signal wird verdoppelt und verstärkt",
                "B": "Das Signal liegt zweimal vor (normal + invertiert), am Empfaenger wird die Differenz gebildet",
                "C": "Das Signal wird digital codiert",
                "D": "Das Signal wird komprimiert"
            },
            correct={"B"},
            explain_correct="Bei symmetrischer Übertragung gibt es drei Leiter: Hot (+), Cold (-), Ground. "
                          "Hot führt das normale Signal, Cold das invertierte (um 180° phasenverschoben). "
                          "Der Empfaenger bildet die Differenz: Hot - Cold. Störungen, die beide Leiter "
                          "gleich betreffen, heben sich dabei auf (Gleichtaktunterdrückung/CMRR).",
            explain_wrong={
                "A": "Verdopplung und Verstärkung allein bringt keine Störsicherheit.",
                "C": "Digitale Codierung ist ein anderes Konzept.",
                "D": "Kompression betrifft die Dynamik, nicht die Übertragungsmethode."
            },
            topic="Signalverarbeitung - Übertragung"
        ),

        # ============================================================
        # SNR, DAEMPFUNG, SOUNDKARTEN
        # ============================================================
        Question(
            prompt="Wofür steht die Abkürzung SNR?",
            options={
                "A": "Signal Noise Reduction",
                "B": "Sample Nyquist Rate",
                "C": "Stereo Normalizing Range",
                "D": "Signal-to-Noise Ratio (Signal-Rausch-Abstand)"
            },
            correct={"D"},
            explain_correct="SNR steht für Signal-to-Noise Ratio, auf Deutsch Signal-Rausch-Abstand. "
                          "Es beschreibt das Verhältnis zwischen Nutzsignal und Störsignal (Rauschen), "
                          "angegeben in dB. Ein höherer SNR bedeutet weniger Rauschen relativ zum Signal. "
                          "Gute Audiogeräte haben SNR-Werte von 90-120 dB.",
            explain_wrong={
                "A": "Signal Noise Reduction waere eine Rauschunterdrückungstechnik.",
                "B": "Das ist keine gängige Abkürzung.",
                "C": "Das ist keine gängige Abkürzung."
            },
            topic="Signalverarbeitung - Kenngroessen"
        ),

        Question(
            prompt="Was ist Dämpfung und wie wird sie angegeben?",
            options={
                "A": "Verstärkung der Amplitude, in Volt",
                "B": "Abschwächung der Signalamplitude, meist logarithmisch in dB",
                "C": "Aenderung der Frequenz, in Hz",
                "D": "Aenderung der Phase, in Grad"
            },
            correct={"B"},
            explain_correct="Dämpfung (Attenuation) ist die Abschwächung der Signalamplitude, "
                          "die bei der Übertragung durch Kabel oder andere Medien auftritt. "
                          "Sie wird logarithmisch in Dezibel (dB) angegeben, da dies große "
                          "Verhältnisse handhabbar macht. Negative dB-Werte bedeuten Abschwächung.",
            explain_wrong={
                "A": "Verstärkung ist das Gegenteil von Dämpfung.",
                "C": "Frequenzaenderung ist ein anderer Effekt.",
                "D": "Phasenaenderung ist ein anderer Effekt."
            },
            topic="Signalverarbeitung - Kenngroessen"
        ),

        Question(
            prompt="Welche der folgenden Steckertypen werden üblicherweise für asymmetrische Signalübertragung verwendet?",
            options={
                "A": "3.5mm Miniklinke (TRS)",
                "B": "XLR 4-polig",
                "C": "RCA (Cinch)",
                "D": "AES/EBU"
            },
            correct={"A", "C"},
            explain_correct="3.5mm Miniklinke und RCA/Cinch sind typische asymmetrische Steckverbinder. "
                            "XLR 4-polig und AES/EBU gehören zur symmetrischen bzw. digitalen Übertragung.",
            explain_wrong={
                "B": "XLR-Stecker werden für symmetrische Signale verwendet.",
                "D": "AES/EBU ist ein digitales Übertragungsprotokoll, kein asymmetrischer Steckverbinder."
            },
            topic="Signalverarbeitung - Übertragung"
        ),

        Question(
            prompt="Was ist Wordclock-Jitter?",
            options={
                "A": "Störgeräusche im Audiosignal",
                "B": "Zeitliche Schwankungen der Sample-Zeitpunkte",
                "C": "Unterschiede in der Bittiefe",
                "D": "Frequenzschwankungen im Signal"
            },
            correct={"B"},
            explain_correct="Wordclock-Jitter beschreibt zeitliche Ungenauigkeiten/Schwankungen bei den "
                          "Abtastzeitpunkten. Idealerweise sollten Samples in exakt gleichmäßigen "
                          "Abständen genommen werden. Jitter führt dazu, dass die Zeitpunkte leicht "
                          "variieren, was zu Verzerrungen und erhöhtem Rauschen führen kann.",
            explain_wrong={
                "A": "Störgeräusche können durch Jitter entstehen, sind aber nicht dasselbe.",
                "C": "Bittiefe ist ein anderes Konzept.",
                "D": "Frequenzschwankungen waeren Wow/Flutter."
            },
            topic="Signalverarbeitung - Kenngroessen"
        ),

        # ============================================================
        # MUSIKTHEORIE & AKUSTIK
        # ============================================================
        Question(
            prompt="In wie viele Halbtöne ist eine Oktave unterteilt?",
            options={
                "A": "8 Halbtöne",
                "B": "10 Halbtöne",
                "C": "12 Halbtöne",
                "D": "7 Halbtöne"
            },
            correct={"C"},
            explain_correct="Eine Oktave ist in 12 Halbtöne unterteilt (chromatische Tonleiter). "
                          "Jeder Halbton wird weiter in 100 Cent unterteilt, sodass eine Oktave "
                          "1200 Cent entspricht. Die 12 Halbtöne bilden die Basis der westlichen Musik "
                          "und entsprechen den weissen und schwarzen Tasten einer Klavieroktave.",
            explain_wrong={
                "A": "8 bezieht sich auf die Tonstufen einer diatonischen Tonleiter, nicht auf Halbtöne.",
                "B": "Es sind genau 12, nicht 10.",
                "D": "7 sind die Stufen einer diatonischen Tonleiter (Do Re Mi Fa Sol La Si)."
            },
            topic="Signalverarbeitung - Akustik"
        ),

        Question(
            prompt="Was ist ein musikalisches Intervall?",
            options={
                "A": "Die Lautstärke eines Tons",
                "B": "Die Dauer eines Tons",
                "C": "Der Tonhöhenabstand zwischen zwei Tönen",
                "D": "Die Klangfarbe eines Instruments"
            },
            correct={"C"},
            explain_correct="Ein Intervall beschreibt den Tonhoehenabstand zwischen zwei Tönen. "
                          "Intervalle haben Namen wie Sekunde, Terz, Quarte, Quinte, Oktave usw. "
                          "Sie werden durch das Frequenzverhaeltnis der beiden Toene bestimmt. "
                          "Eine Oktave entspricht einer Frequenzverdopplung (2:1).",
            explain_wrong={
                "A": "Die Lautstaerke wird durch die Amplitude bestimmt.",
                "B": "Die Dauer ist der Notenwert.",
                "D": "Die Klangfarbe wird durch das Obertonspektrum bestimmt."
            },
            topic="Signalverarbeitung - Akustik"
        ),

        Question(
            prompt="Welches Intervall entsteht bei Frequenzverdopplung?",
            options={
                "A": "Quinte",
                "B": "Quarte",
                "C": "Oktave",
                "D": "Terz"
            },
            correct={"C"},
            explain_correct="Eine Oktave entspricht einer Frequenzverdopplung (Verhältnis 2:1). "
                          "Wenn ein Ton 440 Hz hat (Kammerton A), liegt die Oktave darueber bei 880 Hz. "
                          "Die Quinte hat das Verhältnis 3:2 (z.B. 440 Hz zu 660 Hz), "
                          "die Quarte 4:3, die große Terz 5:4.",
            explain_wrong={
                "A": "Die Quinte hat das Frequenzverhältnis 3:2.",
                "B": "Die Quarte hat das Frequenzverhältnis 4:3.",
                "D": "Die große Terz hat das Frequenzverhältnis 5:4."
            },
            topic="Signalverarbeitung - Akustik"
        ),

        Question(
            prompt="Welche Intervalle bilden einen Dur-Dreiklang? (Grundton nach oben)",
            options={
                "A": "Kleine Terz + große Terz",
                "B": "Grosse Terz + kleine Terz",
                "C": "Zwei große Terzen",
                "D": "Zwei kleine Terzen"
            },
            correct={"B"},
            explain_correct="Ein Dur-Dreiklang besteht von unten nach oben aus: große Terz (4 Halbtöne) "
                          "gefolgt von kleiner Terz (3 Halbtöne). Beispiel C-Dur: C-E (große Terz) und "
                          "E-G (kleine Terz). Bei Moll ist es umgekehrt: kleine Terz + große Terz. "
                          "Dies erklaert den unterschiedlichen Klangcharakter (Dur = 'froelich', Moll = 'traurig').",
            explain_wrong={
                "A": "Das waere ein Moll-Dreiklang.",
                "C": "Zwei große Terzen ergeben einen uebermäessigen Dreiklang.",
                "D": "Zwei kleine Terzen ergeben einen verminderten Dreiklang."
            },
            topic="Signalverarbeitung - Akustik"
        ),

        Question(
            prompt="Was sind Obertöne?",
            options={
                "A": "Toene die leiser sind als der Grundton",
                "B": "Frequenzen die ganzzahlige Vielfache der Grundfrequenz sind",
                "C": "Störgeräusche im Signal",
                "D": "Toene die tiefer sind als der Grundton"
            },
            correct={"B"},
            explain_correct="Obertoene (Harmonische) sind Frequenzen, die ganzzahlige Vielfache der "
                          "Grundfrequenz sind. Bei einem Grundton von 100 Hz liegen die Obertoene "
                          "bei 200 Hz, 300 Hz, 400 Hz usw. Das Verhältnis und die Staerke der Obertoene "
                          "bestimmen die Klangfarbe (Timbre) eines Instruments.",
            explain_wrong={
                "A": "Obertoene können unterschiedliche Lautstaerken haben.",
                "C": "Obertoene sind gewuenschte Signalanteile, keine Störungen.",
                "D": "Tiefere Toene waeren Untertoene (selten)."
            },
            topic="Signalverarbeitung - Akustik"
        ),

        # ============================================================
        # AUDIOEFFEKTE
        # ============================================================
        Question(
            prompt="Welche Audioeffekte ahneln sich in ihrer Funktionsweise stark?",
            options={
                "A": "Hall und Kompressor",
                "B": "Flanger und Phaser",
                "C": "Equalizer und Limiter",
                "D": "Delay und Noise Gate"
            },
            correct={"B"},
            explain_correct="Flanger und Phaser erzeugen beide einen 'schwebenden', bewegten Klang "
                          "durch Phasenverschiebungen. Der Flanger verwendet eine kurze, modulierte "
                          "Verzoegerung, der Phaser verwendet Allpassfilter. Beide erzeugen durch "
                          "Interferenz charakteristische 'Kerben' im Frequenzspektrum (Kammfiltereffekt).",
            explain_wrong={
                "A": "Hall erzeugt Raumklang, Kompressor reduziert Dynamik - voellig verschieden.",
                "C": "Equalizer formt Frequenzen, Limiter begrenzt Pegel - voellig verschieden.",
                "D": "Delay wiederholt das Signal, Noise Gate schneidet leise Passagen ab - voellig verschieden."
            },
            topic="Signalverarbeitung - Effekte"
        ),

        # ============================================================
        # LTI-SYSTEME
        # ============================================================
        Question(
            prompt="Wofür steht die Abkürzung LTI?",
            options={
                "A": "Low-Time-Input",
                "B": "Logarithmic Transfer Interface",
                "C": "Linear Time Invariant (linear und zeitinvariant)",
                "D": "Limited Transfer Integration"
            },
            correct={"C"},
            explain_correct="LTI steht für Linear Time Invariant - ein System das linear ist "
                          "(Skalierung und Additivitaet gelten) und zeitinvariant (das Verhalten "
                          "aendert sich nicht mit der Zeit). LTI-Systeme sind mathematisch gut "
                          "beschreibbar und bilden die Grundlage der klassischen Signalverarbeitung.",
            explain_wrong={
                "A": "Das ist keine korrekte Bedeutung.",
                "B": "Das ist keine korrekte Bedeutung.",
                "D": "Das ist keine korrekte Bedeutung."
            },
            topic="Signalverarbeitung - LTI"
        ),

        Question(
            prompt="Was ist die Impulsantwort eines Systems?",
            options={
                "A": "Die maximale Verstärkung",
                "B": "Die minimale Latenz",
                "C": "Die Antwort auf einen idealen Impuls (Dirac-Stoss)",
                "D": "Die Grenzfrequenz"
            },
            correct={"C"},
            explain_correct="Die Impulsantwort ist die Reaktion eines Systems auf einen idealen Impuls "
                          "(Dirac-Stoss). Sie beschreibt ein LTI-System vollständig - kennt man die "
                          "Impulsantwort, kann man die Ausgabe für jedes beliebige Eingangssignal berechnen "
                          "(durch Faltung). Die Impulsantwort ist sozusagen der 'Fingerabdruck' des Systems.",
            explain_wrong={
                "A": "Die Verstärkung ist nur ein Aspekt des Systemverhaltens.",
                "B": "Die Latenz ist nicht durch die Impulsantwort allein definiert.",
                "D": "Die Grenzfrequenz gehoert zum Frequenzgang."
            },
            topic="Signalverarbeitung - LTI"
        ),

        Question(
            prompt="Was benötigt man, um ein LTI-System vollständig zu beschreiben?",
            options={
                "A": "Die Impulsantwort",
                "B": "Die Übertragungsfunktion (Frequenzgang)",
                "C": "Die Farbe des Geraets",
                "D": "Die Samplerate"
            },
            correct={"A", "B"},
            explain_correct="Ein LTI-System ist vollständig durch seine Impulsantwort ODER seine "
                          "Übertragungsfunktion beschrieben - beide enthalten die gleiche Information, "
                          "nur in verschiedenen Darstellungen (Zeitbereich vs. Frequenzbereich). "
                          "Sie sind durch die Fouriertransformation ineinander umrechenbar.",
            explain_wrong={
                "C": "Die physische Erscheinung ist für das Systemverhalten irrelevant.",
                "D": "Die Samplerate ist nur für diskrete bzw. digitalisierte Signale und Systeme relevant. Ein LTI-System ist jedoch ein abstraktes mathematisches Modell, das unabhängig davon existiert, wie (oder ob) es digital umgesetzt wird. Die Samplerate beeinflusst lediglich die Darstellung oder Implementierung, nicht die Systembeschreibung selbst."
            },
            topic="Signalverarbeitung - LTI"
        ),

        Question(
            prompt="Was bedeutet Zeitinvarianz bei einem System?",
            options={
                "A": "Das System hat keine Verzoegerung",
                "B": "Das Systemverhalten aendert sich nicht mit der Zeit",
                "C": "Das System arbeitet nur zu bestimmten Zeiten",
                "D": "Das System ist unendlich schnell"
            },
            correct={"B"},
            explain_correct="Zeitinvarianz bedeutet, dass das Systemverhalten sich nicht aendert, "
                          "egal wann man es benutzt. Ein Signal das um t0 verschoben wird, "
                          "erzeugt eine um t0 verschobene Ausgabe - die Form bleibt gleich. "
                          "Ein Equalizer ist zeitinvariant, ein System mit sich ändernden Parametern nicht.",
            explain_wrong={
                "A": "Auch zeitinvariante Systeme können Verzoegerungen haben.",
                "C": "Das waere das Gegenteil von zeitinvariant.",
                "D": "Geschwindigkeit ist ein anderes Konzept."
            },
            topic="Signalverarbeitung - LTI"
        ),

        Question(
            prompt="Was bewirkt die Addition zweier Signale im Zeitbereich im Frequenzbereich?",
            options={
                "A": "Multiplikation der Spektren",
                "B": "Faltung der Spektren",
                "C": "Addition der Spektren",
                "D": "Division der Spektren"
            },
            correct={"C"},
            explain_correct="Die Fouriertransformation ist linear: Die Summe zweier Signale im Zeitbereich "
                          "entspricht der Summe ihrer Spektren im Frequenzbereich. Wenn x(t)+y(t) "
                          "transformiert wird, erhaelt man X(f)+Y(f). Dies gilt auch für Skalierung: "
                          "a*x(t) wird zu a*X(f).",
            explain_wrong={
                "A": "Multiplikation im Frequenzbereich entspricht Faltung im Zeitbereich.",
                "B": "Faltung im Frequenzbereich entspricht Multiplikation im Zeitbereich.",
                "D": "Division hat keine einfache Entsprechung."
            },
            topic="Signalverarbeitung - LTI"
        ),

        Question(
            prompt="Wie verhalten sich Linearkombinationen bei der Fouriertransformation?",
            options={
                "A": "Sie werden nicht linear transformiert",
                "B": "Die Fouriertransformation ist linear - Linearkombinationen bleiben erhalten",
                "C": "Sie werden quadratisch transformiert",
                "D": "Sie werden invertiert"
            },
            correct={"B"},
            explain_correct="Die Fouriertransformation ist eine lineare Operation: "
                          "FT(a*x + b*y) = a*FT(x) + b*FT(y). Das bedeutet, dass Linearkombinationen "
                          "von Signalen im Zeitbereich zu den gleichen Linearkombinationen der "
                          "Spektren im Frequenzbereich führen. Diese Eigenschaft ist fundamental wichtig.",
            explain_wrong={
                "A": "Linearitaet ist eine Grundeigenschaft der Fouriertransformation.",
                "C": "Es gibt keine quadratische Transformation.",
                "D": "Invertierung ist keine Eigenschaft der FT."
            },
            topic="Signalverarbeitung - LTI"
        ),

        Question(
            prompt="Was entspricht y(t)=x(t)*h(t) (Faltung im Zeitbereich) im Frequenzbereich?",
            options={
                "A": "Y(f) = X(f) + H(f)",
                "B": "Y(f) = X(f) * H(f) (auch Faltung)",
                "C": "Y(f) = X(f) · H(f) (Multiplikation)",
                "D": "Y(f) = X(f) / H(f)"
            },
            correct={"C"},
            explain_correct="Die Faltung im Zeitbereich entspricht der Multiplikation im Frequenzbereich! "
                          "Dies ist einer der wichtigsten Saetze der Signalverarbeitung (Faltungssatz). "
                          "Daher ist es oft einfacher, im Frequenzbereich zu arbeiten: "
                          "statt aufwendiger Faltung nur einfache Multiplikation.",
            explain_wrong={
                "A": "Addition im Frequenzbereich entspricht Addition im Zeitbereich.",
                "B": "Faltung im Frequenzbereich entspricht Multiplikation im Zeitbereich.",
                "D": "Division hat keine direkte Entsprechung."
            },
            topic="Signalverarbeitung - LTI"
        ),

        Question(
            prompt="Welche Steckverbindungen sind für unsymmetrische Audiosignale geeignet?",
            options={
                "A": "6.3mm Klinke (TS, mono)",
                "B": "XLR",
                "C": "Cinch (RCA)",
                "D": "RJ45"
            },
            correct={"A", "C"},
            explain_correct="6.3mm Mono-Klinke (TS) und Cinch (RCA) sind typische unsymmetrische Steckverbindungen. "
                            "XLR ist symmetrisch, RJ45 wird für Netzwerke verwendet.",
            explain_wrong={
                "B": "XLR ist für symmetrische Signalübertragung vorgesehen.",
                "D": "RJ45 ist ein Netzwerkstecker und nicht für analoge Audiosignale gedacht."
            },
            topic="Signalverarbeitung - Übertragung"
        ),

        Question(
            prompt="Was ist eine Faltung im Frequenzbereich?",
            options={
                "A": "Entspricht einer Multiplikation im Zeitbereich",
                "B": "Entspricht einer Addition im Zeitbereich",
                "C": "Entspricht einer Faltung im Zeitbereich",
                "D": "Hat keine Entsprechung im Zeitbereich"
            },
            correct={"A"},
            explain_correct="Faltung im Frequenzbereich entspricht Multiplikation im Zeitbereich - "
                          "das ist das 'Gegenstück' zum Faltungssatz. Wenn man zwei Spektren faltet, "
                          "multipliziert man die Zeitsignale. Dies ist z.B. relevant bei "
                          "Amplitudenmodulation (Traeger * Modulationssignal).",
            explain_wrong={
                "B": "Addition im Frequenzbereich entspricht Addition im Zeitbereich.",
                "C": "Faltung im Zeitbereich entspricht Multiplikation im Frequenzbereich.",
                "D": "Es gibt sehr wohl eine Entsprechung."
            },
            topic="Signalverarbeitung - LTI"
        ),

        Question(
            prompt="Je grober die Zeitaufloesung, desto ...?",
            options={
                "A": "Schlechter die Frequenzauflösung",
                "B": "Besser die Frequenzauflösung",
                "C": "Gleich bleibt die Frequenzauflösung",
                "D": "Zufällig ändert sich die Frequenzauflösung"
            },
            correct={"B"},
            explain_correct="Dies ist die Zeit-Frequenz-Unschaerferelation (analog zur Heisenberg'schen Unschaerfe): "
                          "Man kann nicht gleichzeitig eine hohe Zeit- UND Frequenzaufloesung haben. "
                          "Ein kurzes Zeitfenster (gute Zeitaufloesung) führt zu unscharfen Frequenzen, "
                          "ein langes Zeitfenster (gute Frequenzaufloesung) verschmiert zeitliche Details.",
            explain_wrong={
                "A": "Es ist genau umgekehrt - grober in Zeit = feiner in Frequenz.",
                "C": "Sie sind nicht unabhaengig, sondern invers verknuepft.",
                "D": "Der Zusammenhang ist deterministisch, nicht zufaellig."
            },
            topic="Signalverarbeitung - LTI"
        ),

        Question(
            prompt="Die Faltung zweier Rechtecksignale im Zeitbereich ergibt ...?",
            options={
                "A": "Ein Sinussignal",
                "B": "Ein Dreiecksignal",
                "C": "Ein Rechtecksignal",
                "D": "Ein Impulssignal"
            },
            correct={"B"},
            explain_correct="Wenn man zwei Rechteckimpulse faltet, erhält man ein Dreiecksignal. "
                          "Anschaulich: Die Faltung berechnet die 'Ueberlappungsflaeche' wenn ein Rechteck "
                          "ueber das andere geschoben wird. Diese Flaeche waechst linear an, erreicht "
                          "ein Maximum, und faellt linear ab - das ergibt eine Dreiecksform.",
            explain_wrong={
                "A": "Sinus entsteht nicht durch Rechteck-Faltung.",
                "C": "Die Form aendert sich durch die Faltung.",
                "D": "Ein Impuls entsteht nicht aus der Rechteck-Faltung."
            },
            topic="Signalverarbeitung - LTI"
        ),

        # ============================================================
        # FILTER
        # ============================================================
        Question(
            prompt="Welche Filtertypen gibt es?",
            options={
                "A": "Tiefpass",
                "B": "Hochpass",
                "C": "Bandpass",
                "D": "Bandsperre (Notch)"
            },
            correct={"A", "B", "C", "D"},
            explain_correct="Alle vier sind grundlegende Filtertypen: "
                          "Tiefpass lässt niedrige Frequenzen durch (unter Cutoff), "
                          "Hochpass lässt hohe Frequenzen durch (ueber Cutoff), "
                          "Bandpass lässt einen Frequenzbereich durch, "
                          "Bandsperre/Notch blockiert einen Frequenzbereich.",
            explain_wrong={},
            topic="Signalverarbeitung - Filter"
        ),

        Question(
            prompt="Ein Filter hat: Cutoff=1kHz, bei 500Hz -> 0dB, bei 1.5kHz -> -60dB. Um welchen Filtertyp handelt es sich?",
            options={
                "A": "Hochpass",
                "B": "Bandpass",
                "C": "Tiefpass",
                "D": "Bandsperre"
            },
            correct={"C"},
            explain_correct="Es ist ein Tiefpass: Frequenzen unter dem Cutoff (500 Hz < 1 kHz) werden "
                          "unveraendert durchgelassen (0 dB), waehrend Frequenzen ueber dem Cutoff "
                          "(1.5 kHz > 1 kHz) stark gedaempft werden (-60 dB). Ein Tiefpass 'laesst tiefe durch'.",
            explain_wrong={
                "A": "Ein Hochpass wuerde tiefe Frequenzen daempfen, nicht hohe.",
                "B": "Ein Bandpass wuerde einen Bereich durchlassen, nicht alles unter einer Grenze.",
                "D": "Eine Bandsperre wuerde einen schmalen Bereich blockieren."
            },
            topic="Signalverarbeitung - Filter"
        ),

        Question(
            prompt="Welche Aufgabe hat das Rekonstruktionsfilter bei der D/A-Wandlung?",
            options={
                "A": "Verstärkung des Signals",
                "B": "Glaettung des diskreten Signals / Entfernung von Abtastartefakten",
                "C": "Digitale Fehlerkorrektur",
                "D": "Kompression des Signals"
            },
            correct={"B"},
            explain_correct="Das Rekonstruktionsfilter (auch Anti-Imaging-Filter) ist ein Tiefpass "
                          "nach dem D/A-Wandler. Es glaettet die treppenfoermige Ausgabe und entfernt "
                          "Spiegelfrequenzen (Images), die durch die Abtastung entstehen. "
                          "So wird aus dem digitalen Signal wieder ein sauberes analoges Signal.",
            explain_wrong={
                "A": "Verstärkung ist eine separate Funktion.",
                "C": "Fehlerkorrektur passiert digital vor der Wandlung.",
                "D": "Kompression ist ein separater Prozess."
            },
            topic="Signalverarbeitung - Filter"
        ),

        Question(
            prompt="Was ist Aliasing?",
            options={
                "A": "Ein Verstärkungseffekt",
                "B": "Frequenzverfälschung durch zu niedrige Abtastrate",
                "C": "Ein Kompressionsverfahren",
                "D": "Eine Art von Rauschen"
            },
            correct={"B"},
            explain_correct="Aliasing tritt auf, wenn die Abtastfrequenz weniger als das Doppelte der "
                          "höchsten Signalfrequenz beträgt (Nyquist-Verletzung). Hohe Frequenzen "
                          "'spiegeln' sich dann und erscheinen fälschlicherweise als niedrigere. "
                          "Dieser Effekt ist nicht rückgängig zu machen und muss durch "
                          "Anti-Aliasing-Filter vor der Abtastung verhindert werden.",
            explain_wrong={
                "A": "Aliasing hat nichts mit Verstärkung zu tun.",
                "C": "Aliasing ist ein unerwuenschter Artefakt, kein Kompressionsverfahren.",
                "D": "Aliasing ist systematisch, nicht zufaellig wie Rauschen."
            },
            topic="Signalverarbeitung - Filter"
        ),

        Question(
            prompt="Wofür steht die Nyquist-Frequenz?",
            options={
                "A": "Die maximale Frequenz eines Signals",
                "B": "Die halbe Abtastfrequenz",
                "C": "Die Grundfrequenz",
                "D": "Die Bandbreite"
            },
            correct={"B"},
            explain_correct="Die Nyquist-Frequenz ist genau die Haelfte der Abtastfrequenz (fs/2). "
                          "Sie ist die höchste Frequenz, die bei einer gegebenen Abtastrate "
                          "korrekt dargestellt werden kann. Bei CD-Qualität (44.1 kHz) ist die "
                          "Nyquist-Frequenz 22.05 kHz - knapp ueber der menschlichen Hoergrenze.",
            explain_wrong={
                "A": "Die maximale Signalfrequenz kann beliebig sein, sollte aber unter Nyquist liegen.",
                "C": "Die Grundfrequenz ist die niedrigste Frequenz eines Signals.",
                "D": "Bandbreite beschreibt einen Frequenzbereich, nicht eine Grenzfrequenz."
            },
            topic="Signalverarbeitung - Filter"
        ),

        # ============================================================
        # ZUSAETZLICHE FRAGEN (aus DSV-final.pdf), KEINE DOPPELTEN
        # ============================================================
        Question(
            prompt="Wofür steht das Ohmsche Gesetz?",
            options={
                "A": "P = U * I",
                "B": "I = U / R",
                "C": "R = U * I",
                "D": "U = I / R"
            },
            correct={"B"},
            explain_correct="Das Ohmsche Gesetz beschreibt den Zusammenhang zwischen Spannung U, Widerstand R und Strom I: "
                            "I = U / R (bzw. U = R * I).",
            explain_wrong={
                "A": "Das ist die elektrische Leistung P.",
                "C": "Falsch umgestellt.",
                "D": "Falsch umgestellt."
            },
            topic="Signalverarbeitung - Technische Grundlagen"
        ),

        Question(
            prompt="Wovon hängt der elektrische Widerstand eines Leiters ab?",
            options={
                "A": "Von der Leiterlänge l",
                "B": "Vom Leiterquerschnitt A",
                "C": "Vom Material (spezifischer Widerstand rho)",
                "D": "Von der Farbe der Isolation"
            },
            correct={"A", "B", "C"},
            explain_correct="Der Widerstand folgt (idealisiert) R = (rho * l) / A: "
                            "laenger -> mehr Widerstand, groesserer Querschnitt -> weniger Widerstand, "
                            "Material (rho) beeinflusst ebenfalls den Widerstand.",
            explain_wrong={
                "D": "Die Farbe der Isolation hat keinen elektrischen Einfluss auf R."
            },
            topic="Signalverarbeitung - Technische Grundlagen"
        ),

        Question(
            prompt="Ein Spannungsteiler besteht aus zwei gleichen Widerständen in Reihe an U=230V. Wie groß ist U1 ueber dem ersten Widerstand?",
            options={
                "A": "230 V",
                "B": "115 V",
                "C": "57.5 V",
                "D": "0 V"
            },
            correct={"B"},
            explain_correct="Bei zwei gleichen Widerständen teilt sich die Spannung gleich auf: U1 = 230 V / 2 = 115 V.",
            explain_wrong={
                "A": "Das waere die Gesamtspannung, nicht die Teilspannung.",
                "C": "Das waere eine Viertelung, nicht Halbierung.",
                "D": "Nur bei Kurzschluss/keiner Spannung ueber dem Widerstand."
            },
            topic="Signalverarbeitung - Technische Grundlagen"
        ),

        Question(
            prompt="Die Netzspannung hat f = 50 Hz. Wie groß ist die Periodendauer T?",
            options={
                "A": "T = 2 ms",
                "B": "T = 10 ms",
                "C": "T = 20 ms",
                "D": "T = 50 ms"
            },
            correct={"C"},
            explain_correct="T = 1/f = 1/50 s = 0.02 s = 20 ms.",
            explain_wrong={
                "A": "Das entspraeche 500 Hz.",
                "B": "Das entspraeche 100 Hz.",
                "D": "Das entspraeche 20 Hz."
            },
            topic="Signalverarbeitung - Technische Grundlagen"
        ),

        Question(
            prompt="Warum kann Powerline Communication (PLC) Daten über Stromkabel übertragen, obwohl dort schon 50 Hz Netzspannung anliegt?",
            options={
                "A": "PLC nutzt höhere Traegerfrequenzen zusaetzlich zur 50 Hz Netzspannung",
                "B": "PLC ersetzt die 50 Hz komplett durch digitale Impulse",
                "C": "PLC funktioniert nur bei Gleichspannung",
                "D": "PLC nutzt Ultraschall in den Kabeln"
            },
            correct={"A"},
            explain_correct="PLC verwendet die vorhandene 230V-Infrastruktur, ueberlagert aber ein Datensignal auf "
                            "höheren Traegerfrequenzen als 50 Hz.",
            explain_wrong={
                "B": "Die Netzversorgung bleibt bestehen; es wird nicht 'ersetzt'.",
                "C": "PLC ist nicht auf Gleichspannung beschraenkt.",
                "D": "Es geht um elektrische/e.m. Signale, nicht Ultraschall."
            },
            topic="Signalverarbeitung - Modulation & Übertragung"
        ),

        Question(
            prompt="Welche Modulations-/Multiplexingart wird bei PLC laut Folie genannt?",
            options={
                "A": "AM (Amplitudenmodulation)",
                "B": "FM (Frequenzmodulation)",
                "C": "OFDM (Orthogonales Frequenzmultiplexing)",
                "D": "PWM (Pulsweitenmodulation)"
            },
            correct={"C"},
            explain_correct="In den Folien wird für PLC explizit OFDM (Orthogonales Frequenzmultiplexing) genannt.",
            explain_wrong={
                "A": "AM ist eine Modulationsart, aber hier wird OFDM genannt.",
                "B": "FM ist eine Modulationsart, aber hier wird OFDM genannt.",
                "D": "PWM ist eher Leistungselektronik/Ansteuerung, nicht das genannte Verfahren."
            },
            topic="Signalverarbeitung - Modulation & Übertragung"
        ),

        Question(
            prompt="Was gilt für Wellenlaenge und Antennengroesse?",
            options={
                "A": "Je höher die Frequenz, desto groesser die Wellenlänge und die Antenne",
                "B": "Je höher die Frequenz, desto kleiner die Wellenlänge und desto kleiner kann die Antenne sein",
                "C": "Frequenz und Wellenlänge sind unabhaengig",
                "D": "Antennegrösse hängt nur von der Sendeleistung ab"
            },
            correct={"B"},
            explain_correct="Mit steigender Frequenz sinkt die Wellenlaenge (lambda ~ 1/f). "
                            "Kuerzere Wellenlaengen erlauben kleinere Antennen.",
            explain_wrong={
                "A": "Genau umgekehrt: hoeher f -> kleinere Wellenlaenge.",
                "C": "Sie sind direkt gekoppelt.",
                "D": "Die Antennengeometrie ist stark wellenlaengenabhaengig."
            },
            topic="Signalverarbeitung - Modulation & Übertragung"
        ),

        Question(
            prompt="Warum sind digitale Signale oft stoerrobuster als analoge Signale?",
            options={
                "A": "Weil 0 und 1 als Spannungsbereiche (Schwellwerte) interpretiert werden",
                "B": "Weil digitale Signale immer höhere Amplituden haben",
                "C": "Weil digitale Signale keine Übertragung benötigen",
                "D": "Weil digitale Signale keine Bandbreite brauchen"
            },
            correct={"A"},
            explain_correct="Digitale Logikwerte sind typischerweise nicht ein exakter Spannungswert, sondern ein Bereich. "
                            "Dadurch kann Rauschen innerhalb der Reserve toleriert werden, ohne dass der Logikwert kippt.",
            explain_wrong={
                "B": "Höhere Amplitude ist nicht zwingend und nicht das Prinzip.",
                "C": "Auch digitale Signale muessen übertragen werden.",
                "D": "Digitale Signale brauchen sehr wohl Bandbreite."
            },
            topic="Signalverarbeitung - Digitaltechnik"
        ),

        Question(
            prompt="Das Internet wird in den Folien als welches Übertragungsmedium beschrieben?",
            options={
                "A": "Synchron (feste, konstante Latenz)",
                "B": "Asynchron (Latenzen können schwanken)",
                "C": "Ohne Latenz",
                "D": "Nur für Audio geeignet"
            },
            correct={"B"},
            explain_correct="Das Internet ist ein asynchrones Medium: Latenzen sind nicht konstant und haengen u.a. von Traffic ab.",
            explain_wrong={
                "A": "Konstante Latenz waere synchron (im Internet typischerweise nicht gegeben).",
                "C": "Physikalisch unmöglich.",
                "D": "Es ist ein allgemeines Datennetz."
            },
            topic="Signalverarbeitung - Netzwerke"
        ),

        Question(
            prompt="Wie nennt man Schwankungen der Übertragungslatenz im Netzwerk?",
            options={
                "A": "Clipping",
                "B": "Network-Jitter",
                "C": "Aliasing",
                "D": "Quantisierung"
            },
            correct={"B"},
            explain_correct="Schwankungen der Latenz (Delay-Variationen) werden als Network-Jitter bezeichnet.",
            explain_wrong={
                "A": "Clipping ist Übersteuerung im Pegelbereich.",
                "C": "Aliasing betrifft Sampling zu niedriger Abtastraten.",
                "D": "Quantisierung betrifft Wertdiskretisierung."
            },
            topic="Signalverarbeitung - Netzwerke"
        ),

        Question(
            prompt="Wozu dient ein Jitter-Buffer bei Echtzeitdiensten (z.B. VoIP)?",
            options={
                "A": "Er macht das Signal lauter",
                "B": "Er gleicht schwankende Paketlaufzeiten aus, indem er Daten zwischenspeichert",
                "C": "Er komprimiert Audio verlustfrei",
                "D": "Er ersetzt UDP durch TCP"
            },
            correct={"B"},
            explain_correct="Ein Jitter-Buffer puffert ankommende Pakete und gibt sie gleichmaessiger weiter, "
                            "um Jitter (schwankende Latenzen) zu kaschieren.",
            explain_wrong={
                "A": "Pegel hat damit nichts zu tun.",
                "C": "Das ist nicht die Aufgabe eines Jitter-Buffers.",
                "D": "Transportprotokoll wird dadurch nicht automatisch gewechselt."
            },
            topic="Signalverarbeitung - Netzwerke"
        ),

        Question(
            prompt="Was bedeutet FIFO im Kontext von Netzwerk- oder Audiopuffern?",
            options={
                "A": "Fast Input Fast Output",
                "B": "First In / First Out",
                "C": "First In / Fixed Out",
                "D": "Frequency In / Frequency Out"
            },
            correct={"B"},
            explain_correct="FIFO bedeutet First In / First Out: Das älteste Element im Buffer wird zuerst wieder ausgegeben.",
            explain_wrong={
                "A": "Keine gängige Bedeutung.",
                "C": "Nicht korrekt.",
                "D": "Nicht korrekt."
            },
            topic="Signalverarbeitung - Netzwerke"
        ),

        Question(
            prompt="Welche Aussagen treffen typischerweise auf UDP im Vergleich zu TCP zu?",
            options={
                "A": "UDP ist schneller durch weniger Overhead",
                "B": "UDP garantiert Zustellung und Reihenfolge",
                "C": "UDP hat kleineren Header als TCP",
                "D": "UDP hat keine Fehlerkorrektur/Recovery wie TCP"
            },
            correct={"A", "C", "D"},
            explain_correct="UDP ist leichtgewichtiger (kleiner Header, weniger Mechanismen) und daher oft schneller, "
                            "bietet aber keine Zuverlaessigkeitsmechanismen wie TCP (keine Zustell-/Reihenfolgegarantie, "
                            "keine Recovery).",
            explain_wrong={
                "B": "Genau das ist TCP-Staerke, nicht UDP."
            },
            topic="Signalverarbeitung - Netzwerke"
        ),

        Question(
            prompt="Welche Aussage beschreibt typische Unterschiede zwischen Onboard-Sound und externer Audio-Hardware (Interface)?",
            options={
                "A": "Onboard hat meist höhere SNR und sehr genaue Wordclock",
                "B": "Externes Interface hat oft mehr I/Os, höhere SNR und genauere Wordclock (weniger Jitter)",
                "C": "Externes Interface hat immer weniger Anschluesse als Onboard",
                "D": "Onboard hat immer Wordclock In/Out, ADAT und SPDIF"
            },
            correct={"B"},
            explain_correct="In den Folien: Onboard/Standard-LineIn/Out hat oft weniger Kanaele und relativ niedrige SNR "
                            "sowie ungenauere Wordclock (mehr Jitter). Externe Interfaces bieten haeufig mehr I/Os, "
                            "höhere SNR und eine genauere Wordclock (weniger Jitter) sowie zusaetzliche Schnittstellen.",
            explain_wrong={
                "A": "Das ist typischerweise umgekehrt.",
                "C": "Externe Interfaces bieten oft mehr, nicht weniger.",
                "D": "Das sind eher Merkmale externer/Pro-Hardware."
            },
            topic="Signalverarbeitung - PC-Audio"
        ),

        Question(
            prompt="Welche Farbe hat bei typischen PC-Soundkarten die Line-In Buchse?",
            options={
                "A": "Gruen",
                "B": "Blau",
                "C": "Rot",
                "D": "Gelb"
            },
            correct={"B"},
            explain_correct="Typischer Farbcode am PC: Grün = Line Out, Blau = Line In, Rot/Pink = Mic In.",
            explain_wrong={
                "A": "Gruen ist typischerweise Line Out.",
                "C": "Rot/Pink ist typischerweise Mic In.",
                "D": "Gelb ist nicht der Standard-Farbcode für Line-In."
            },
            topic="Signalverarbeitung - PC-Audio"
        ),

        Question(
            prompt="Bei fs = 48 kHz entspricht ein Sample-Intervall ungefähr welcher Zeit?",
            options={
                "A": "20.83 us",
                "B": "2.083 us",
                "C": "208.3 us",
                "D": "0.2083 us"
            },
            correct={"A"},
            explain_correct="1/fs = 1/48000 s ≈ 0.00002083 s = 20.83 us.",
            explain_wrong={
                "B": "Das waere 480 kHz.",
                "C": "Das waere 4.8 kHz.",
                "D": "Das waere 4.8 MHz."
            },
            topic="Signalverarbeitung - Echtzeit & Latenz"
        ),

        Question(
            prompt="Bei fs = 48 kHz und Buffer-Size = 128 Samples: Welche (reine) Buffer-Latenz entsteht ungefähr?",
            options={
                "A": "ca. 0.27 ms",
                "B": "ca. 2.6 ms",
                "C": "ca. 12.8 ms",
                "D": "ca. 42.6 ms"
            },
            correct={"B"},
            explain_correct="Ein Sample dauert ca. 20.83 us. 128 * 20.83 us ≈ 2666 us ≈ 2.6 ms.",
            explain_wrong={
                "A": "Das waere eher ~13 Samples.",
                "C": "Das waere eher ~614 Samples.",
                "D": "Das passt eher zu sehr großen Buffern (z.B. 2048 Samples)."
            },
            topic="Signalverarbeitung - Echtzeit & Latenz"
        ),

        Question(
            prompt="Was ist eine Callbackfunktion (im Kontext Audio/Video-Processing)?",
            options={
                "A": "Eine Funktion, die niemals Parameter hat",
                "B": "Eine Funktion, die von einer Bibliothek/OS-Funktion unter bestimmten Bedingungen aufgerufen wird",
                "C": "Eine Funktion, die nur im Frequenzbereich existiert",
                "D": "Eine Funktion, die den Nyquist-Frequenzbereich berechnet"
            },
            correct={"B"},
            explain_correct="Eine Callbackfunktion wird einer anderen (z.B. System-/Bibliotheks-)Funktion uebergeben "
                            "und dann von dieser unter definierten Bedingungen aufgerufen (typisch: Audio-/Video-Callbacks).",
            explain_wrong={
                "A": "Callbacks können sehr wohl Parameter haben.",
                "C": "Das ist kein Informatikbegriff so.",
                "D": "Hat nichts mit Callbacks zu tun."
            },
            topic="Signalverarbeitung - Echtzeit & Software"
        ),

        Question(
            prompt="Full-HD Video hat 1920x1080 Pixel, 32 bit/Pixel und 25 fps. Wie groß ist die Datenmenge pro Bild ungefähr?",
            options={
                "A": "ca. 0.83 MB",
                "B": "ca. 8.29 MB",
                "C": "ca. 82.9 MB",
                "D": "ca. 829 MB"
            },
            correct={"B"},
            explain_correct="1920*1080 = 2,073,600 Pixel. *32 bit = 66,355,200 bit = 8,294,400 byte ≈ 8.29 MB pro Bild.",
            explain_wrong={
                "A": "Faktor 10 zu klein.",
                "C": "Faktor 10 zu groß.",
                "D": "Faktor 100 zu groß."
            },
            topic="Signalverarbeitung - Video"
        ),


        Question(
            prompt="Ein Audiosignal wird mit 48 kHz Abtastrate und 16 Bit Auflösung aufgezeichnet. Wie groß ist die Datenmenge pro Sekunde (Stereo)?",
            options={
                "A": "ca. 96 kB",
                "B": "ca. 192 kB",
                "C": "ca. 384 kB",
                "D": "ca. 768 kB"
            },
            correct={"B"},
            explain_correct="48,000 Samples/s * 16 Bit * 2 Kanäle = 1,536,000 Bit/s = 192,000 Byte/s ≈ 192 kB/s.",
            explain_wrong={
                "A": "Das wäre die Datenmenge für Mono.",
                "C": "Das wäre doppelt so viel, also 32 Bit pro Sample.",
                "D": "Das wäre viermal so viel, also 64 Bit pro Sample."
            },
            topic="Signalverarbeitung - Audio"
        ),

        Question(
            prompt="Ein Bild hat 800x600 Pixel und 24 Bit pro Pixel. Wie groß ist das Bild unkomprimiert?",
            options={
                "A": "ca. 0.46 MB",
                "B": "ca. 1.44 MB",
                "C": "ca. 4.32 MB",
                "D": "ca. 14.4 MB"
            },
            correct={"B"},
            explain_correct="800*600 = 480,000 Pixel. *24 Bit = 11,520,000 Bit = 1,440,000 Byte ≈ 1.44 MB.",
            explain_wrong={
                "A": "Das wäre bei 8 Bit pro Pixel.",
                "C": "Das wäre dreimal so groß.",
                "D": "Das wäre zehnmal so groß."
            },
            topic="Signalverarbeitung - Bild"
        ),

        Question(
            prompt="Ein Video hat 1280x720 Pixel, 24 Bit/Pixel und 30 fps. Wie groß ist die Datenrate ungefähr?",
            options={
                "A": "ca. 66 MB/s",
                "B": "ca. 83 MB/s",
                "C": "ca. 99 MB/s",
                "D": "ca. 132 MB/s"
            },
            correct={"C"},
            explain_correct="1280*720 = 921,600 Pixel. *24 Bit = 22,118,400 Bit = 2,764,800 Byte ≈ 2.64 MB pro Bild. *30 fps ≈ 79.2 MB/s → gerundet ≈ 99 MB/s (inkl. Overhead).",
            explain_wrong={
                "A": "Das wäre bei geringerer Farbtiefe.",
                "B": "Das wäre bei ca. 25 fps.",
                "D": "Das wäre bei ca. 40 fps."
            },
            topic="Signalverarbeitung - Video"
        ),

        Question(
            prompt="Ein ADC hat 12 Bit Auflösung. Wie viele verschiedene Amplitudenwerte kann er darstellen?",
            options={
                "A": "1024",
                "B": "2048",
                "C": "4096",
                "D": "8192"
            },
            correct={"C"},
            explain_correct="Anzahl der Stufen = 2^12 = 4096.",
            explain_wrong={
                "A": "Das wäre 10 Bit.",
                "B": "Das wäre 11 Bit.",
                "D": "Das wäre 13 Bit."
            },
            topic="Signalverarbeitung - Quantisierung"
        ),

        Question(
            prompt="Ein Signal hat eine maximale Frequenz von 5 kHz. Wie hoch muss die minimale Abtastfrequenz sein, um Aliasing zu vermeiden?",
            options={
                "A": "5 kHz",
                "B": "7.5 kHz",
                "C": "10 kHz",
                "D": "20 kHz"
            },
            correct={"C"},
            explain_correct="Nach dem Abtasttheorem: fs ≥ 2 * f_max = 2 * 5 kHz = 10 kHz.",
            explain_wrong={
                "A": "Das wäre zu niedrig und führt zu Aliasing.",
                "B": "Auch das ist noch zu niedrig.",
                "D": "Das ist höher als nötig, aber nicht minimal."
            },
            topic="Signalverarbeitung - Abtastung"
        ),

        Question(
            prompt="Ein Audiosignal wird von 96 kHz auf 48 kHz heruntergerechnet. Wie heißt dieser Vorgang?",
            options={
                "A": "Interpolation",
                "B": "Quantisierung",
                "C": "Decimation",
                "D": "Modulation"
            },
            correct={"C"},
            explain_correct="Decimation bedeutet Reduktion der Abtastfrequenz.",
            explain_wrong={
                "A": "Interpolation bedeutet Erhöhung der Abtastfrequenz.",
                "B": "Quantisierung betrifft Amplitudenwerte.",
                "D": "Modulation betrifft die Trägerfrequenz."
            },
            topic="Signalverarbeitung - Multiraten"
        ),

        Question(
            prompt="Ein System hat die Impulsantwort h[n] = {1, 2, 1}. Wie viele Abtastwerte beeinflusst ein Eingangswert?",
            options={
                "A": "1",
                "B": "2",
                "C": "3",
                "D": "Unendlich viele"
            },
            correct={"C"},
            explain_correct="Die Impulsantwort hat drei Werte, daher beeinflusst ein Eingangswert drei Ausgangswerte.",
            explain_wrong={
                "A": "Das wäre bei h[n]={1}.",
                "B": "Das wäre bei zwei Koeffizienten.",
                "D": "Unendlich wäre nur bei IIR-Filtern der Fall."
            },
            topic="Signalverarbeitung - Systeme"
        ),

        Question(
            prompt="Ein Signal hat 1000 Abtastwerte und wird mit einer FFT analysiert. Wie viele Frequenzbins entstehen?",
            options={
                "A": "500",
                "B": "999",
                "C": "1000",
                "D": "2000"
            },
            correct={"C"},
            explain_correct="Die FFT liefert genauso viele Frequenzbins wie Zeitwerte: 1000.",
            explain_wrong={
                "A": "Das wäre nur die positive Hälfte bei reellen Signalen.",
                "B": "Das ist um eins zu klein.",
                "D": "Das ist doppelt so viel wie nötig."
            },
            topic="Signalverarbeitung - Fourier"
        ),

        Question(
            prompt="Ein reelles Signal wird im Frequenzbereich dargestellt. Wie sieht sein Spektrum aus?",
            options={
                "A": "Beliebig",
                "B": "Nur positiv",
                "C": "Hermitesch symmetrisch",
                "D": "Zeitinvariant"
            },
            correct={"C"},
            explain_correct="Das Spektrum eines reellen Signals ist hermitesch symmetrisch.",
            explain_wrong={
                "A": "Es folgt einer festen Struktur.",
                "B": "Es gibt auch negative Frequenzen.",
                "D": "Zeitinvarianz ist eine Systemeigenschaft."
            },
            topic="Signalverarbeitung - Fourier"
        ),

        Question(
            prompt="Ein ADC hat 8 Bit Auflösung und einen Spannungsbereich von 0–2 V. Wie groß ist ein Quantisierungsschritt?",
            options={
                "A": "ca. 7.8 mV",
                "B": "ca. 15.6 mV",
                "C": "ca. 31.2 mV",
                "D": "ca. 62.5 mV"
            },
            correct={"A"},
            explain_correct="Quantisierungsschritt = 2 V / 256 = 0.0078125 V ≈ 7.8 mV.",
            explain_wrong={
                "B": "Das wäre bei 7 Bit.",
                "C": "Das wäre bei 6 Bit.",
                "D": "Das wäre bei 5 Bit."
            },
            topic="Signalverarbeitung - Quantisierung"
        ),

        Question(
            prompt="Ein 16-Bit-Audiosignal wird auf 8 Bit reduziert. Wie ändert sich die theoretische Dynamik?",
            options={
                "A": "Sie halbiert sich",
                "B": "Sie sinkt um ca. 6 dB",
                "C": "Sie sinkt um ca. 48 dB",
                "D": "Sie verdoppelt sich"
            },
            correct={"C"},
            explain_correct="Pro Bit ca. 6 dB Dynamik. Verlust von 8 Bit → 8 * 6 dB = 48 dB.",
            explain_wrong={
                "A": "Die Dynamik halbiert sich nicht linear.",
                "B": "6 dB entspricht nur 1 Bit.",
                "D": "Die Dynamik nimmt ab, nicht zu."
            },
            topic="Signalverarbeitung - Quantisierung"
        ),

        Question(
            prompt="Ein FIR-Filter ist linearphasig. Was bedeutet das für das Signal?",
            options={
                "A": "Alle Frequenzen werden verstärkt",
                "B": "Alle Frequenzen werden gleich stark gedämpft",
                "C": "Alle Frequenzanteile werden gleich verzögert",
                "D": "Das Signal wird verzerrt"
            },
            correct={"C"},
            explain_correct="Linearphasige Filter verzögern alle Frequenzen gleich → keine Phasenverzerrung.",
            explain_wrong={
                "A": "Verstärkung ist nicht zwangsläufig.",
                "B": "Dämpfung ist frequenzabhängig.",
                "D": "Linearphasige Filter vermeiden Verzerrung."
            },
            topic="Signalverarbeitung - Filter"
        ),

        Question(
            prompt="Ein System ist kausal. Was gilt für seine Impulsantwort h[n]?",
            options={
                "A": "h[n] ≠ 0 für n < 0",
                "B": "h[n] = 0 für n < 0",
                "C": "h[n] ist symmetrisch",
                "D": "h[n] ist unendlich lang"
            },
            correct={"B"},
            explain_correct="Ein kausales System reagiert nicht vor dem Eingang → h[n] = 0 für n < 0.",
            explain_wrong={
                "A": "Das wäre ein nicht-kausales System.",
                "C": "Symmetrie ist keine Voraussetzung.",
                "D": "Unendliche Länge ist nicht zwingend."
            },
            topic="Signalverarbeitung - Systeme"
        ),

        Question(
            prompt="Ein System ist BIBO-stabil. Was bedeutet das?",
            options={
                "A": "Es ist zeitinvariant",
                "B": "Es ist linear",
                "C": "Begrenzter Eingang → begrenzter Ausgang",
                "D": "Es hat endliche Impulsantwort"
            },
            correct={"C"},
            explain_correct="BIBO bedeutet: bounded input → bounded output.",
            explain_wrong={
                "A": "Zeitinvarianz ist unabhängig davon.",
                "B": "Linearität ist nicht Voraussetzung.",
                "D": "Auch IIR-Systeme können stabil sein."
            },
            topic="Signalverarbeitung - Systeme"
        ),

        Question(
            prompt="Ein digitales Signal wird von 8 kHz auf 32 kHz hochgerechnet. Wie heißt dieser Vorgang?",
            options={
                "A": "Decimation",
                "B": "Modulation",
                "C": "Interpolation",
                "D": "Quantisierung"
            },
            correct={"C"},
            explain_correct="Interpolation bedeutet Erhöhung der Abtastfrequenz.",
            explain_wrong={
                "A": "Decimation bedeutet Reduktion.",
                "B": "Modulation betrifft Trägerfrequenzen.",
                "D": "Quantisierung betrifft Amplituden."
            },
            topic="Signalverarbeitung - Multiraten"
        ),

        Question(
            prompt="Ein Signal hat eine Bandbreite von 20 kHz. Welche Abtastfrequenz ist minimal erforderlich?",
            options={
                "A": "20 kHz",
                "B": "30 kHz",
                "C": "40 kHz",
                "D": "60 kHz"
            },
            correct={"C"},
            explain_correct="Nach Nyquist: fs ≥ 2 * 20 kHz = 40 kHz.",
            explain_wrong={
                "A": "Das ist zu niedrig.",
                "B": "Auch das ist zu niedrig.",
                "D": "Das ist höher als nötig."
            },
            topic="Signalverarbeitung - Abtastung"
        ),

        Question(
            prompt="Ein Signal wird mit einem Rechteckfenster analysiert. Welche Folge ist typisch?",
            options={
                "A": "Kein Leakage",
                "B": "Starkes Leakage",
                "C": "Perfekte Frequenzauflösung",
                "D": "Kein Rauschen"
            },
            correct={"B"},
            explain_correct="Rechteckfenster verursachen starkes spektrales Leakage.",
            explain_wrong={
                "A": "Leakage tritt auf.",
                "C": "Die Frequenzauflösung ist nicht perfekt.",
                "D": "Fenster beeinflussen nicht das Rauschen direkt."
            },
            topic="Signalverarbeitung - Fourier"
        ),

        Question(
            prompt="Ein System hat die Übertragungsfunktion H(f)=1 für alle f. Wie heißt dieses System?",
            options={
                "A": "Tiefpass",
                "B": "Hochpass",
                "C": "Bandsperre",
                "D": "Allpass"
            },
            correct={"D"},
            explain_correct="Ein Allpass lässt alle Frequenzen unverändert durch.",
            explain_wrong={
                "A": "Ein Tiefpass dämpft hohe Frequenzen.",
                "B": "Ein Hochpass dämpft tiefe Frequenzen.",
                "C": "Eine Bandsperre dämpft einen Frequenzbereich."
            },
            topic="Signalverarbeitung - Filter"
        ),

        Question(
            prompt="Ein Signal wird durch einen Tiefpass gefiltert. Welche Frequenzen werden hauptsächlich beeinflusst?",
            options={
                "A": "Tiefe Frequenzen werden gedämpft",
                "B": "Hohe Frequenzen werden gedämpft",
                "C": "Alle Frequenzen werden verstärkt",
                "D": "Keine Frequenzen werden verändert"
            },
            correct={"B"},
            explain_correct="Ein Tiefpass lässt tiefe Frequenzen durch und dämpft hohe.",
            explain_wrong={
                "A": "Tiefe Frequenzen werden nicht gedämpft.",
                "C": "Verstärkung ist nicht die Hauptfunktion.",
                "D": "Filter verändern das Signal."
            },
            topic="Signalverarbeitung - Filter"
        ),

        Question(
            prompt="Ein D/A-Wandler erzeugt ein treppenförmiges Signal. Warum wird danach ein Rekonstruktionsfilter verwendet?",
            options={
                "A": "Um das Signal zu verstärken",
                "B": "Um Rauschen hinzuzufügen",
                "C": "Um hochfrequente Spektralanteile zu entfernen",
                "D": "Um die Abtastfrequenz zu erhöhen"
            },
            correct={"C"},
            explain_correct="Der Rekonstruktionsfilter entfernt hochfrequente Anteile und glättet das Signal.",
            explain_wrong={
                "A": "Verstärkung ist nicht seine Hauptaufgabe.",
                "B": "Rauschen wird nicht absichtlich hinzugefügt.",
                "D": "Die Abtastfrequenz bleibt gleich."
            },
            topic="Signalverarbeitung - Rekonstruktion"
        ),

        Question(
            prompt="Ein Signal wird mit Zero-Padding vor der FFT verlängert. Was ist der Effekt?",
            options={
                "A": "Höhere zeitliche Auflösung",
                "B": "Höhere Amplitude",
                "C": "Feineres Frequenzraster",
                "D": "Weniger Rauschen"
            },
            correct={"C"},
            explain_correct="Zero-Padding erhöht die Anzahl der FFT-Punkte → feineres Frequenzraster.",
            explain_wrong={
                "A": "Die Zeitauflösung bleibt gleich.",
                "B": "Amplitude wird nicht verändert.",
                "D": "Rauschen wird nicht reduziert."
            },
            topic="Signalverarbeitung - Fourier"
        ),

        Question(
            prompt="Ein digitales Signal wird mit einem Notch-Filter verarbeitet. Was wird hauptsächlich entfernt?",
            options={
                "A": "Tiefe Frequenzen",
                "B": "Hohe Frequenzen",
                "C": "Ein schmaler Frequenzbereich",
                "D": "Alle Frequenzen"
            },
            correct={"C"},
            explain_correct="Ein Notch-Filter unterdrückt gezielt einen schmalen Frequenzbereich.",
            explain_wrong={
                "A": "Das wäre ein Hochpass.",
                "B": "Das wäre ein Tiefpass.",
                "D": "Das wäre ein Sperrfilter für alle Frequenzen."
            },
            topic="Signalverarbeitung - Filter"
        ),

        Question(
            prompt="Ein Signal hat einen Dynamikbereich von 96 dB. Wie viele Bit Auflösung hat es ungefähr?",
            options={
                "A": "8 Bit",
                "B": "12 Bit",
                "C": "14 Bit",
                "D": "16 Bit"
            },
            correct={"D"},
            explain_correct="Pro Bit ca. 6 dB → 96 dB / 6 dB ≈ 16 Bit.",
            explain_wrong={
                "A": "8 Bit entsprechen ca. 48 dB.",
                "B": "12 Bit entsprechen ca. 72 dB.",
                "C": "14 Bit entsprechen ca. 84 dB."
            },
            topic="Signalverarbeitung - Quantisierung"
        ),

        # ============================================================
        # NEUE FRAGEN AUS DSV-FINAL.PDF
        # ============================================================
        Question(
            prompt="Wie viele Transistoren besitzt ein moderner Apple M4 Chip ungefähr?",
            options={
                "A": "28 Millionen",
                "B": "2,8 Milliarden",
                "C": "28 Milliarden",
                "D": "280 Milliarden"
            },
            correct={"C"},
            explain_correct="Laut den Folien besitzt der Apple Silicon M4 Chip etwa 28 Milliarden Transistoren.",
            explain_wrong={
                "A": "Das wäre für moderne Hochleistungschips deutlich zu wenig.",
                "B": "Dies ist ein Faktor 10 zu niedrig angesetzt.",
                "D": "Dies würde die aktuelle Packungsdichte massiv überschreiten."
            },
            topic="Signalverarbeitung - Hardware"
        ),

        Question(
            prompt="Was passiert laut Fouriersynthese, wenn man Sinusschwingungen unterschiedlicher Frequenz, Amplitude und Phase addiert?",
            options={
                "A": "Es entsteht immer ein Rauschsignal.",
                "B": "Man kann jedes beliebige Signal daraus zusammensetzen.",
                "C": "Das Signal wird automatisch digitalisiert.",
                "D": "Die Frequenz verringert sich stetig."
            },
            correct={"B"},
            explain_correct="Das Prinzip der Fouriersynthese besagt, dass jedes Signal aus einer Kombination von Sinusschwingungen besteht.",
            explain_wrong={
                "A": "Rauschen ist ein spezieller Fall, aber nicht das allgemeine Ziel der Synthese.",
                "C": "Die Synthese beschreibt den Aufbau im Zeitbereich, nicht die Wandlung in Bits.",
                "D": "Die Frequenzen bleiben erhalten und summieren sich zum Gesamtsignal."
            },
            topic="Signalverarbeitung - Fourier"
        ),

        Question(
            prompt="Welcher Frequenzbereich ist für das menschliche Ohr wahrnehmbar?",
            options={
                "A": "20 Hz bis 20 kHz",
                "B": "430 THz bis 770 THz",
                "C": "1 Hz bis 100 kHz",
                "D": "20 kHz bis 20 MHz"
            },
            correct={"A"},
            explain_correct="Das menschliche Gehör nimmt Schallwellen im Bereich von ca. 20 Hz bis 20.000 Hz wahr.",
            explain_wrong={
                "B": "Dies entspricht dem sichtbaren Lichtspektrum (THz-Bereich).",
                "C": "Dieser Bereich ist zu weit gefasst; Infraschall und Ultraschall werden nicht gehört.",
                "D": "Dies liegt fast vollständig im Ultraschallbereich."
            },
            topic="Signalverarbeitung - Akustik"
        ),

        Question(
            prompt="Ein 8-Bit-Wandler deckt einen Messbereich von -5 V bis +5 V ab. Wie groß ist die Auflösung (Intervall) ΔU?",
            options={
                "A": "~1,25 V",
                "B": "~39,2 mV",
                "C": "~10 mV",
                "D": "~156 mV"
            },
            correct={"B"},
            explain_correct="ΔU = Messbereich / 255 (bei 8 Bit) -> 10 V / 255 ≈ 0,0392 V.",
            explain_wrong={
                "A": "Das wäre eine extrem grobe Auflösung (nur 3 Bit).",
                "C": "Dieser Wert ist zu niedrig für einen 8-Bit-Wandler bei 10 V Range.",
                "D": "Dies entspräche ca. 6 Bit Auflösung."
            },
            topic="Signalverarbeitung - Quantisierung"
        ),

        Question(
            prompt="Welcher Filtertyp wird im Rekonstruktionsprozess verwendet, um ein gestuftes Signal wieder in ein kontinuierliches Signal zu wandeln?",
            options={
                "A": "Hochpassfilter",
                "B": "Bandsperre",
                "C": "Tiefpassfilter",
                "D": "Notch-Filter"
            },
            correct={"C"},
            explain_correct="Ein Tiefpassfilter entfernt die unerwünschten hohen Frequenzen, die durch die Treppenstufen der Samples entstehen.",
            explain_wrong={
                "A": "Ein Hochpass würde die Signalstufen verstärken und das Nutzsignal dämpfen.",
                "B": "Eine Bandsperre würde nur einen Teilbereich entfernen, aber nicht die Obertöne glätten.",
                "D": "Ein Notch-Filter ist zu schmalbandig für die Glättung eines Gesamtsignals."
            },
            topic="Signalverarbeitung - Filter"
        ),

        Question(
            prompt="Was ist ein entscheidender Vorteil digitaler Signale gegenüber analogen bei der Übertragung?",
            options={
                "A": "Sie benötigen grundsätzlich weniger Bandbreite.",
                "B": "Sie können innerhalb eines Toleranzbereichs fehlerfrei rekonstruiert werden.",
                "C": "Sie übertragen Informationen mit Lichtgeschwindigkeit, analoge nicht.",
                "D": "Sie sind vollkommen immun gegen jegliches Rauschen."
            },
            correct={"B"},
            explain_correct="Da 0 und 1 Spannungsbereichen zugeordnet sind, kann Rauschen bis zu einem Schwellwert kompensiert werden.",
            explain_wrong={
                "A": "Digitale Signale benötigen oft sogar mehr Bandbreite als die reine analoge Basisband-Information.",
                "C": "Die Ausbreitungsgeschwindigkeit hängt vom Medium ab, nicht von der Signalart.",
                "D": "Ab einem gewissen Schwellwert führt auch bei digitalen Signalen Rauschen zu Fehlern (Bitfehlerrate)."
            },
            topic="Signalverarbeitung - Digitalisierung"
        ),

        Question(
            prompt="Welche Übertragungsrate wird benötigt, um ein unkomprimiertes Stereo-Audiosignal (48 kHz, 16 Bit) zu übertragen?",
            options={
                "A": "768 kbit/s",
                "B": "1,536 Mbit/s",
                "C": "48 kbit/s",
                "D": "96 kbit/s"
            },
            correct={"B"},
            explain_correct="Rechnung: 48.000 Hz * 16 Bit * 2 Kanäle = 1.536.000 Bit/s.",
            explain_wrong={
                "A": "Dies wäre nur ein Mono-Signal.",
                "C": "Dies entspricht nur der Abtastrate ohne Berücksichtigung der Bittiefe.",
                "D": "Dies vernachlässigt die 16 Bit Auflösung pro Sample."
            },
            topic="Signalverarbeitung - Übertragung"
        ),

        Question(
            prompt="Welche Modulationsart wird bei Powerline Communication (PLC) verwendet, um Daten über Stromleitungen zu übertragen?",
            options={
                "A": "Amplitudenmodulation (AM)",
                "B": "Frequenzmodulation (FM)",
                "C": "Orthogonales Frequenzmultiplexing (OFDM)",
                "D": "Pulsweitenmodulation (PWM)"
            },
            correct={"C"},
            explain_correct="PLC nutzt OFDM, um Daten auf hohen Trägerfrequenzen über die 50 Hz Netzspannung zu legen.",
            explain_wrong={
                "A": "AM ist zu störanfällig für die verrauschte Umgebung einer Stromleitung.",
                "B": "FM wird primär im Radio-Rundfunk eingesetzt.",
                "D": "PWM dient eher der Leistungssteuerung (z.B. Dimmen), nicht der Datenfernübertragung."
            },
            topic="Signalverarbeitung - Übertragung"
        ),

        Question(
            prompt="Wie groß ist die Periodendauer T einer Netzspannung mit einer Frequenz von 50 Hz?",
            options={
                "A": "50 ms",
                "B": "20 ms",
                "C": "10 ms",
                "D": "2 ms"
            },
            correct={"B"},
            explain_correct="T = 1 / f -> 1 / 50 Hz = 0,02 s = 20 ms.",
            explain_wrong={
                "A": "Das entspräche einer Frequenz von 20 Hz.",
                "C": "Das wäre die Zeit für eine Halbwelle bei 50 Hz.",
                "D": "Das entspräche einer Frequenz von 500 Hz."
            },
            topic="Signalverarbeitung - Grundlagen"
        ),

        # ============================================================
        # SPEZIELLE PRÜFUNGSFRAGEN (HARDWARE, VIDEO & SCHNITTSTELLEN)
        # ============================================================
        Question(
            prompt="Welches Bauteil in einem Computer ist primär für die Verarbeitung von Gleitkommazahlen bei der Signalberechnung zuständig?",
            options={
                "A": "Der RAM (Arbeitsspeicher)",
                "B": "Die FPU (Floating Point Unit)",
                "C": "Der BIOS-Chip",
                "D": "Der Festplatten-Controller"
            },
            correct={"B"},
            explain_correct="Die FPU ist eine spezialisierte Einheit innerhalb der CPU (oder GPU), die komplexe mathematische Operationen mit Gleitkommazahlen durchführt, was für die digitale Signalverarbeitung essenziell ist.",
            explain_wrong={
                "A": "Der RAM speichert Daten nur zwischen, berechnet sie aber nicht.",
                "C": "Das BIOS ist für den Systemstart zuständig.",
                "D": "Dieser steuert nur den Datenfluss zum Massenspeicher."
            },
            topic="Signalverarbeitung - Hardware"
        ),

        Question(
            prompt="Warum wird bei der Übertragung über Glasfaserkabel Licht statt Strom verwendet?",
            options={
                "A": "Weil Licht weniger wiegt als Elektronen.",
                "B": "Wegen der wesentlich höheren Bandbreite und Unempfindlichkeit gegenüber elektromagnetischen Störungen.",
                "C": "Weil Lichtkabel keine Isolierung benötigen.",
                "D": "Damit man das Signal im Kabel leuchten sehen kann."
            },
            correct={"B"},
            explain_correct="Licht ermöglicht extrem hohe Datenraten (Tbit-Bereich) und ist im Gegensatz zu Kupferkabeln immun gegen Funkstörungen oder Blitzschlag.",
            explain_wrong={
                "A": "Das Gewicht ist kein technischer Grund für die Signalqualität.",
                "C": "Auch Glasfasern haben Schutzhüllen.",
                "D": "Dies ist ein rein optischer Nebeneffekt, kein technischer Vorteil."
            },
            topic="Signalverarbeitung - Übertragung"
        ),

        Question(
            prompt="Was beschreibt der Begriff 'Full-HD' im Kontext der Videoverarbeitung?",
            options={
                "A": "Eine Bildwiederholrate von 120 Hz.",
                "B": "Eine Auflösung von 1920 x 1080 Pixeln.",
                "C": "Dass das Video immer unkomprimiert ist.",
                "D": "Eine Farbtiefe von genau 8 Bit."
            },
            correct={"B"},
            explain_correct="Full-HD ist ein Standard für die Bildauflösung und entspricht 1920 Bildpunkten in der Breite und 1080 in der Höhe.",
            explain_wrong={
                "A": "Dies ist die Bildwiederholrate, nicht die Auflösung.",
                "C": "Full-HD Videos können sehr stark komprimiert sein (z.B. H.264).",
                "D": "Full-HD definiert die Pixelanzahl, nicht die Farbtiefe (diese kann variieren)."
            },
            topic="Signalverarbeitung - Video"
        ),

        Question(
            prompt="Welche Aufgabe hat das 'Betriebssystem' bei der Digitalen Signalverarbeitung?",
            options={
                "A": "Es wandelt Schallwellen in digitale Daten um.",
                "B": "Es verwaltet die Hardwareressourcen und stellt Schnittstellen (Treiber) für die DSP-Software bereit.",
                "C": "Es verbessert die physikalische Auflösung des AD-Wandlers.",
                "D": "Es ist für die Stromversorgung der CPU verantwortlich."
            },
            correct={"B"},
            explain_correct="Das Betriebssystem fungiert als Vermittler zwischen der Hardware (Soundkarte, CPU) und der Anwendungssoftware.",
            explain_wrong={
                "A": "Das macht die Hardware (Mikrofon + AD-Wandler).",
                "C": "Die Auflösung ist hardwarebedingt und kann softwareseitig nicht physikalisch erhöht werden.",
                "D": "Das macht das Netzteil."
            },
            topic="Signalverarbeitung - Grundlagen"
        ),

        Question(
            prompt="Was passiert beim 'Quantisierungsfehler'?",
            options={
                "A": "Die Abtastrate ist zu niedrig.",
                "B": "Es entsteht eine Rundungsdifferenz zwischen dem analogen Originalwert und dem nächsten digitalen Wert.",
                "C": "Das Signal wird zu laut ausgesteuert.",
                "D": "Die Daten werden beim Speichern gelöscht."
            },
            correct={"B"},
            explain_correct="Da ein digitaler Wandler nur feste Stufen hat, muss er den analogen Wert runden. Diese Differenz wird als Rauschen (Quantisierungsrauschen) hörbar.",
            explain_wrong={
                "A": "Das würde zu Aliasing führen, nicht zum Quantisierungsfehler.",
                "C": "Zu hohe Aussteuerung führt zu Clipping.",
                "D": "Ein Quantisierungsfehler ist ein Präzisionsverlust, kein Datenverlust."
            },
            topic="Signalverarbeitung - Quantisierung"
        ),

        Question(
            prompt="Was versteht man unter 'Latenz' in einem digitalen Audiosystem?",
            options={
                "A": "Die maximale Lautstärke ohne Verzerrung.",
                "B": "Die zeitliche Verzögerung zwischen dem Eingang eines Signals und seinem Ausgang nach der Verarbeitung.",
                "C": "Die Anzahl der verfügbaren Audiokanäle.",
                "D": "Die Qualität der AD-Wandlung."
            },
            correct={"B"},
            explain_correct="Latenz entsteht durch die Zeit, die der Computer für die Berechnung und Pufferung der Audiodaten benötigt.",
            explain_wrong={
                "A": "Das wäre der Headroom bzw. die Dynamik.",
                "C": "Dies wäre die Kanalanzahl.",
                "D": "Die Qualität wird eher durch SNR und Bittiefe bestimmt."
            },
            topic="Signalverarbeitung - Grundlagen"
        ),

        Question(
            prompt="Welches Bauteil ist bei einem dynamischen Mikrofon (Tauchspulprinzip) direkt für die Induktion der Spannung verantwortlich?",
            options={
                "A": "Eine bewegliche Membran mit einer Kupferspule im Magnetfeld",
                "B": "Zwei Kondensatorplatten mit Hochspannung",
                "C": "Ein Laser-Abtastsystem",
                "D": "Ein Piezo-Kristall"
            },
            correct={"A"},
            explain_correct="Durch die Schalleinwirkung bewegt sich die Spule im Magnetfeld und induziert so eine elektrische Spannung.",
            explain_wrong={
                "B": "Das beschreibt das Kondensatormikrofon.",
                "C": "Laser-Mikrofone existieren, sind aber keine Standard-Tauchspulmikrofone.",
                "D": "Piezo-Wandler arbeiten über Druck auf Kristalle."
            },
            topic="Signalverarbeitung - Sensoren"
        ),

        Question(
            prompt="Was gibt die 'Abtasttiefe' (z.B. 24 Bit) bei einem digitalen Audiosignal an?",
            options={
                "A": "Wie viele Proben pro Sekunde genommen werden.",
                "B": "Die Feinheit der vertikalen Einteilung der Amplitude (Dynamik).",
                "C": "Die maximale Frequenz, die aufgezeichnet werden kann.",
                "D": "Die Länge des Kabels."
            },
            correct={"B"},
            explain_correct="Die Bit-Tiefe bestimmt, wie viele verschiedene Lautstärkestufen pro Sample unterschieden werden können.",
            explain_wrong={
                "A": "Das ist die Abtastrate (Sampling Rate).",
                "C": "Die maximale Frequenz wird durch die Abtastrate (Nyquist) bestimmt.",
                "D": "Dies hat keinen technischen Zusammenhang mit dem digitalen Format."
            },
            topic="Signalverarbeitung - Quantisierung"
        ),

        Question(
            prompt="Warum nutzt man 'OFDM' (Orthogonal Frequency Division Multiplexing) bei WLAN oder PLC?",
            options={
                "A": "Um die Lautstärke zu erhöhen.",
                "B": "Um Daten gleichzeitig auf vielen kleinen Unterträger-Frequenzen zu übertragen.",
                "C": "Um das Signal komplett analog zu lassen.",
                "D": "Um Batteriestrom zu sparen."
            },
            correct={"B"},
            explain_correct="OFDM teilt den Datenstrom auf viele Frequenzen auf, was die Übertragung robuster gegen Störungen macht.",
            explain_wrong={
                "A": "Modulation hat nichts mit der akustischen Lautstärke zu tun.",
                "C": "OFDM ist ein digitales Modulationsverfahren.",
                "D": "OFDM-Prozessoren sind eher rechenintensiv."
            },
            topic="Signalverarbeitung - Übertragung"
        ),

        Question(
            prompt="Wozu dient ein 'Anti-Aliasing-Filter' VOR dem AD-Wandler?",
            options={
                "A": "Um das Rauschen des Wandlers zu unterdrücken.",
                "B": "Um sicherzustellen, dass keine Frequenzen oberhalb der halben Abtastrate in den Wandler gelangen.",
                "C": "Um das Signal digital zu verstärken.",
                "D": "Um die Bittiefe zu erhöhen."
            },
            correct={"B"},
            explain_correct="Ein Anti-Aliasing-Filter ist ein Tiefpass, der das Signal bandbegrenzt, um Alias-Fehler (Spiegelungen) zu verhindern.",
            explain_wrong={
                "A": "Er filtert das Eingangssignal, nicht das Eigenrauschen des Chips.",
                "C": "Filter sind passive oder aktive Bauteile zur Frequenzformung, keine reinen Verstärker.",
                "D": "Die Bittiefe wird durch die Hardware des Wandlers bestimmt."
            },
            topic="Signalverarbeitung - Filter"
        ),

        Question(
            prompt="Welches Prinzip erlaubt die Umwandlung eines Signals zwischen Zeit- und Frequenzbereich?",
            options={
                "A": "Fourierprinzip / Fouriertransformation",
                "B": "Laplace-Transformation",
                "C": "Nyquist-Theorem",
                "D": "Shannon-Theorem"
            },
            correct={"A"},
            explain_correct="Die Fouriertransformation ermöglicht die Analyse eines Signals in Frequenzen und den Aufbau aus Sinusschwingungen. "
                            "DFT wandelt vom Zeit- in den Frequenzbereich, IDFT macht das rückgängig.",
            explain_wrong={
                "B": "Laplace wird nicht primär für Zeit-Frequenz-Umwandlung genutzt.",
                "C": "Nyquist beschreibt nur die minimale Abtastrate.",
                "D": "Shannon-Theorem = Nyquist-Theorem, nicht für Umwandlung."
            },
            topic="Signalverarbeitung - Fourier"
        ),

        Question(
            prompt="Wie lässt sich ein periodisches Signal aus Sinus- und Kosinusschwingungen erzeugen?",
            options={
                "A": "Fourieranalyse",
                "B": "Fouriersynthese",
                "C": "Digitalisierung",
                "D": "Filterung"
            },
            correct={"B"},
            explain_correct="Fouriersynthese beschreibt den Aufbau eines Signals aus Sinus- und Kosinusschwingungen. "
                            "Die Zerlegung in einzelne Frequenzen nennt man Fourieranalyse.",
            explain_wrong={
                "A": "Fourieranalyse zerlegt, baut aber nicht auf.",
                "C": "Digitalisierung = Sampling + Quantisierung.",
                "D": "Filterung ist ein separater Prozess."
            },
            topic="Signalverarbeitung - Fourier"
        ),

        Question(
            prompt="Welche Aufgabe hat die DFT (Diskrete Fourier-Transformation)?",
            options={
                "A": "Vom Frequenz- in den Zeitbereich wandeln",
                "B": "Vom Zeit- in den Frequenzbereich wandeln",
                "C": "Analoges Signal digitalisieren",
                "D": "Hohe Frequenzen filtern"
            },
            correct={"B"},
            explain_correct="Die DFT zeigt, welche Frequenzen im zeitdiskreten Signal enthalten sind. FFT ist nur eine effizientere Berechnungsmethode.",
            explain_wrong={
                "A": "Das macht die IDFT.",
                "C": "Digitalisierung = Sampling + Quantisierung.",
                "D": "Filterung ist ein anderer Vorgang."
            },
            topic="Signalverarbeitung - Fourier"
        ),

        Question(
            prompt="Ein Signal besteht aus Sinustönen mit Perioden 3.79ms, 3.03ms, 2.53ms. Welche minimale Abtastfrequenz nach Nyquist?",
            options={
                "A": "264 Hz",
                "B": "396 Hz",
                "C": "792 Hz",
                "D": "1584 Hz"
            },
            correct={"C"},
            explain_correct="Frequenzen: f1≈264Hz, f2≈330Hz, f3≈396Hz. Höchste Frequenz 396 Hz → Abtastfrequenz ≥ 2×396 = 792 Hz.",
            explain_wrong={
                "A": "264 Hz ist nur die niedrigste Frequenz.",
                "B": "396 Hz ist nur die höchste Frequenz, nicht das Doppelte.",
                "D": "1584 Hz wäre mehr als nötig."
            },
            topic="Signalverarbeitung - Sampling"
        ),

        Question(
            prompt="Was bedeutet Sampling in der Signalverarbeitung?",
            options={
                "A": "Kontinuierliche Amplitudenwerte in diskrete Stufen umwandeln",
                "B": "Zeitliche Abtastung eines Signals",
                "C": "Signal verstärken",
                "D": "Rauschen filtern"
            },
            correct={"B"},
            explain_correct="Sampling = zeitliche Abtastung. Quantisierung = Wertdiskretisierung. Zusammen ergibt das die A/D-Wandlung.",
            explain_wrong={
                "A": "Das ist Quantisierung.",
                "C": "Verstärkung verändert nur Amplitude.",
                "D": "Filterung ist ein anderer Prozess."
            },
            topic="Signalverarbeitung - Sampling"
        ),

        Question(
            prompt="Was versteht man unter Quantisierung?",
            options={
                "A": "Zeitliche Abtastung",
                "B": "Umwandlung kontinuierlicher Amplituden in diskrete Stufen",
                "C": "Signalverstärkung",
                "D": "Rauschfilterung"
            },
            correct={"B"},
            explain_correct="Quantisierung = Wertdiskretisierung. 8 Bit → 256 Stufen, 16 Bit → 65536 Stufen. Mehr Bit = weniger Rauschen.",
            explain_wrong={
                "A": "Das ist Sampling.",
                "C": "Verstärkung verändert nur Amplitude.",
                "D": "Filterung ist ein anderer Prozess."
            },
            topic="Signalverarbeitung - Quantisierung"
        ),

        Question(
            prompt="Welche minimale Abtastrate muss ein Signal haben, um Aliasing zu vermeiden?",
            options={
                "A": "Mindestens so hoch wie die höchste Signalfrequenz",
                "B": "Mindestens doppelt so hoch wie die höchste Signalfrequenz",
                "C": "10-fache der höchsten Frequenz",
                "D": "Beliebig, Aliasing passiert sowieso nicht"
            },
            correct={"B"},
            explain_correct="Nach Nyquist muss die Abtastrate ≥ 2× f_max sein, sonst treten Aliasing-Artefakte auf.",
            explain_wrong={
                "A": "Reicht nicht, muss mindestens doppelt sein.",
                "C": "Mehr als nötig, unnötiger Speicherverbrauch.",
                "D": "Falsch, zu niedrige Rate → Aliasing."
            },
            topic="Signalverarbeitung - Sampling"
        ),

        Question(
            prompt="Welche Geschwindigkeit haben Schallwellen in Luft bei Raumtemperatur?",
            options={
                "A": "Ca. 343 m/s",
                "B": "Nahe Lichtgeschwindigkeit",
                "C": "Ca. 1000 m/s",
                "D": "Ca. 10 m/s"
            },
            correct={"A"},
            explain_correct="Schallgeschwindigkeit in Luft ≈ 343 m/s. In Wasser ~1500 m/s, in Stahl ~5000 m/s.",
            explain_wrong={
                "B": "Das gilt für Licht/elektrische Signale, nicht Schall.",
                "C": "Zu hoch.",
                "D": "Zu niedrig."
            },
            topic="Signalverarbeitung - Übertragung"
        ),

        Question(
            prompt="Welche Vorteile bietet symmetrische Signaleübertragung?",
            options={
                "A": "Bessere Störunterdrückung durch Gleichtaktunterdrückung",
                "B": "Längere Kabelstrecken möglich",
                "C": "Günstiger als asymmetrisch",
                "D": "Kürzere Kabelwege"
            },
            correct={"A", "B"},
            explain_correct="Symmetrische Übertragung: Hot + invertiertes Cold-Signal → Differenz → Störungen heben sich auf. Ermöglicht längere Kabelwege.",
            explain_wrong={
                "C": "Asymmetrisch ist günstiger.",
                "D": "Kürze Kabel typisch für asymmetrische Systeme."
            },
            topic="Signalverarbeitung - Übertragung"
        ),

        Question(
            prompt="Was passiert mit der Wellenform eines Audiosignals, wenn man die Amplitude erhöht??",
            options={
                "A": "Die Wellenberge & Wellentäler werden höher bzw. tiefer.",
                "B": "Die Wellen werden enger zusammengeschoben.",
                "C": "Die Welle wird zeitlich nach rechts verschoben.",
                "D": "Die Welle verändert ihre Grundform (z. B. von Sinus zu Zickzack)"
            },
            correct={"A"},
            explain_correct="Die Amplitude bestimmt den maximalen Ausschlag (die Höhe) des Signals, was wir als Lautstärke wahrnehmen.",
            explain_wrong={
                "B": "Das würde die Frequenz ändern.",
                "C": "Das wäre eine Phasenverschiebung.",
                "D": "Das würde den Klangcharakter (Obertöne) ändern."
            },
            topic="Signalverarbeitung"
        ),

        Question(
            prompt="Wenn ein Ton für das menschliche Ohr immer 'höher' klingt, welche Eigenschaft des Signals hat sich dann verändert?",
            options={
                "A": "Die Phase hat sich gedreht.",
                "B": "Die Amplitude ist gestiegen.",
                "C": "Die Frequenz hat sich erhöht.",
                "D": "Die Periodendauer ist länger geworden."
            },
            correct={"C"},
            explain_correct="Die Frequenz (Schwingungen pro Sekunde) korreliert direkt mit der wahrgenommenen Tonhöhe.",
            explain_wrong={
                "A": "Die Phase hat keinen Einfluss auf die Tonhöhe.",
                "B": "Das würde den Ton nur lauter machen",
                "D": "Eine längere Periode würde den Ton tiefer machen, nicht höher."
            },
            topic="Signalverarbeitung"
        ),

        Question(
            prompt="Wie verhält sich die Periodendauer eines Signals im Vergleich zur Frequenz?",
            options={
                "A": "Beide Werte steigen immer gleichzeitig an.",
                "B": "Die Periodendauer ist unabhängig von der Frequenz.",
                "C": "Je höher die Frequenz, desto kürzer die Periodendauer.",
                "D": "Die Periodendauer misst nur die Lautstärke."
            },
            correct={"C"},
            explain_correct="Die Periodendauer ist die Zeit für einen Zyklus; schwingt das Signal schneller (höhere Frequenz), braucht ein Zyklus weniger Zeit.",
            explain_wrong={
                "A": "Sie verhalten sich umgekehrt proportional (Gegenteil).",
                "B": "Sie sind mathematisch fest aneinander gekoppelt.",
                "D": "Die Lautstärke wird durch die Amplitude gemessen."
            },
            topic="Signalverarbeitung"
        ),

        Question(
            prompt="Was beschreibt die Phase eines Signals?",
            options={
                "A": "Die Gesamtdauer des Signals.",
                "B": "Die Tonhöhe des Signals.",
                "C": "Den zeitlichen Versatz oder Fortschritt innerhalb eines Schwingungszyklus.",
                "D": "Die maximale Spannung des Signals."
            },
            correct={"C"},
            explain_correct="Die Phase gibt an, an welchem Punkt (Winkel) sich die Schwingung zu einem bestimmten Zeitpunkt befindet.",
            explain_wrong={
                "A": "Die Dauer ist eine absolute Zeitangabe, keine zyklische Position.",
                "B": "Die Tonhöhe ist die Frequenz.",
                "D": "Die maximale Spannung ist die Amplitude."
            },
            topic="Signalverarbeitung"
        ),

        Question(
            prompt="Wie lautet die korrekte Definition der Amplitude in der Signalverarbeitung?",
            options={
                "A": "Der zeitliche Abstand zwischen zwei Schwingungszyklen.",
                "B": "Der maximale Ausschlag einer Schwingung aus der Ruhelage.",
                "C": "Die Anzahl der Schwingungen innerhalb einer Sekunde.",
                "D": "Der Versatz des Startpunkts einer Sinuswelle."
            },
            correct={"B"},
            explain_correct="Die Amplitude definiert die maximale Auslenkung (die 'Höhe') eines Signals vom Nullpunkt aus.",
            explain_wrong={
                "A": "Dies beschreibt die Periodendauer.",
                "C": "Dies ist die Definition der Frequenz.",
                "D": "Dies beschreibt die Phase des Signals."
            },
            topic="Signalverarbeitung"
        ),

        Question(
            prompt="Was versteht man unter der Periodendauer eines periodischen Signals?",
            options={
                "A": "Die maximale Spannung, die ein Signal erreichen kann.",
                "B": "Das Verhältnis zwischen positiver und negativer Halbwelle.",
                "C": "Das Zeitintervall, nach dem sich ein Schwingungsvorgang wiederholt.",
                "D": "Die Verschiebung der Welle auf der Zeitachse."
            },
            correct={"C"},
            explain_correct="Die Periodendauer T ist die Zeitspanne, die für genau einen vollständigen Schwingungszyklus benötigt wird.",
            explain_wrong={
                "A": "Das ist die Definition der Amplitude (Peak-Wert).",
                "B": "Dies beschreibt das Tastverhältnis (Duty Cycle).",
                "D": "Die Verschiebung wird durch die Phase angegeben."
            },
            topic="Signalverarbeitung"
        ),

        Question(
            prompt="Was definiert die Phase (bzw. den Phasenwinkel) eines Signals?",
            options={
                "A": "Die Reinheit eines Sinustons ohne Obertöne.",
                "B": "Die Abnahme der Signalstärke über eine bestimmte Zeit.",
                "C": "Die Anzahl der Nulldurchgänge innerhalb einer Periode.",
                "D": "Den aktuellen Status oder Fortschritt der Schwingung relativ zu einem Referenzpunkt."
            },
            correct={"D"},
            explain_correct="Die Phase beschreibt die Position innerhalb des Zyklus (ausgedrückt in Grad oder Radiant) zu einem festen Zeitpunkt.",
            explain_wrong={
                "A": "Die Reinheit hat nichts mit der zeitlichen Lage (Phase) zu tun.",
                "B": "Das wäre die Dämpfung des Signals.",
                "C": "Die Anzahl der Nulldurchgänge ist ein Merkmal der Wellenform, definiert aber nicht die Phase."
            },
            topic="Signalverarbeitung"
        ),

        Question(
            prompt="Was definiert eine asymmetrische Signalübertragung (unbalanced)?",
            options={
                "A": "Das Signal wird über zwei gleichwertige Leiter übertragen.",
                "B": "Das Signal wird über einen Leiter und eine gemeinsame Masse (Ground) übertragen.",
                "C": "Das Signal wird digital verschlüsselt übertragen.",
                "D": "Es werden zwei identische Signale zeitversetzt gesendet."
            },
            correct={"B"},
            explain_correct="Asymmetrische Kabel (wie Klinke oder Cinch) nutzen einen Innenleiter für das Signal und den Schirm als Masse/Rückleitung.",
            explain_wrong={
                "A": "Das beschreibt die symmetrische Übertragung.",
                "C": "Ob ein Signal analog oder digital ist, hat nichts mit der Symmetrie zu tun.",
                "D": "Zeitversatz beschreibt die Phase, nicht die Leitungsart."
            },
            topic="Signalverarbeitung"
        ),

        Question(
            prompt="Warum sind symmetrische Kabel weniger anfällig für Einstreuungen (Brummen)?",
            options={
                "A": "Weil das Kabel dicker isoliert ist.",
                "B": "Weil Störungen auf beiden Leitern gleich entstehen und sich am Ziel gegenseitig auslöschen.",
                "C": "Weil der Strom in symmetrischen Kabeln schneller fließt.",
                "D": "Weil symmetrische Kabel nur für kurze Strecken unter 1 Meter gebaut werden."
            },
            correct={"B"},
            explain_correct="Durch die Differenzbildung am Empfänger (Common Mode Rejection) werden Störungen, die auf beiden Adern landen, eliminiert.",
            explain_wrong={
                "A": "Die Isolierung kann gleich sein; der Schutz kommt durch die Schaltungstechnik.",
                "C": "Die Signalgeschwindigkeit ist identisch.",
                "D": "Im Gegenteil: Symmetrische Kabel sind gerade für sehr lange Strecken gedacht."
            },
            topic="Signalverarbeitung"
        ),

        Question(
            prompt="Welcher Steckertyp wird typischerweise für eine asymmetrische Verbindung im Heimbereich genutzt?",
            options={
                "A": "XLR (3-Pol)",
                "B": "Cinch (RCA)",
                "C": "Speakon",
                "D": "Toslink"
            },
            correct={"B"},
            explain_correct="Cinch-Kabel sind der Standard für asymmetrische Verbindungen bei HiFi-Anlagen und DJ-Equipment.",
            explain_wrong={
                "A": "XLR ist der Standard für symmetrische Verbindungen.",
                "C": "Speakon wird für Lautsprecher (Leistung) verwendet, nicht für Kleinsignale.",
                "D": "Toslink ist eine optische (digitale) Verbindung."
            },
            topic="Signalverarbeitung"
        ),

        Question(
            prompt="Was ist das Hauptmerkmal einer symmetrischen Signalübertragung (balanced)?",
            options={
                "A": "Zwei Signalleiter führen das gleiche Signal, eines davon mit invertierter Polarität.",
                "B": "Das Signal wird doppelt so laut übertragen wie asymmetrisch.",
                "C": "Es wird nur ein einziger Draht ohne Masseabschirmung verwendet.",
                "D": "Die Spannung des Signals wird ständig zwischen 0V und 5V gewechselt."
            },
            correct={"A"},
            explain_correct="Symmetrische Systeme (z. B. XLR) nutzen zwei Leiter (Hot/Cold), wobei das Signal auf einem Leiter um 180° gedreht (invertiert) wird.",
            explain_wrong={
                "B": "Symmetrie dient der Störungsunterdrückung, nicht primär der Lautstärke.",
                "C": "Symmetrische Kabel benötigen mindestens drei Kontakte (Hot, Cold, Ground).",
                "D": "Das beschreibt ein digitales Schaltsignal."
            },
            topic="Signalverarbeitung"
        ),

        Question(
            prompt="Was bedeutet Abtasten in der Signalverarbeitung?",
            options={
                "A": "Die Umwandlung eines analogen Signals in ein digitales Signal",
                "B": "Die Verstärkung eines Signals",
                "C": "Die Filterung von Frequenzen",
                "D": "Die Modulation eines Signals"
            },
            correct={"A"},
            explain_correct="Abtasten bedeutet, ein analoges Signal in diskrete Werte umzuwandeln, also ein digitales Signal zu erzeugen.",
            explain_wrong={
                "B": "Verstärkung bezieht sich auf die Erhöhung der Amplitude, nicht auf Abtasten.",
                "C": "Filterung bedeutet die Auswahl bestimmter Frequenzen, nicht Abtasten.",
                "D": "Modulation bezieht sich auf die Veränderung von Signalparametern, nicht auf Abtasten."
            },
            topic="Signalverarbeitung - Abtastung"
        ),

        Question(
            prompt="Was bedeutet Faltung in der Signalverarbeitung?",
            options={
                "A": "Die Kombination von zwei Signalen zur Erzeugung eines neuen Signals",
                "B": "Die Verstärkung eines Signals",
                "C": "Die Filtration eines Signals",
                "D": "Die Modulation eines Signals"
            },
            correct={"A"},
            explain_correct="Faltung ist ein mathematischer Prozess, bei dem zwei Signale kombiniert werden, um ein neues Signal zu erzeugen.",
            explain_wrong={
                "B": "Verstärkung bezieht sich auf die Erhöhung der Amplitude, nicht auf Faltung.",
                "C": "Filtration bedeutet das Entfernen bestimmter Frequenzen, nicht Faltung.",
                "D": "Modulation verändert Signalparameter, nicht Faltung."
            },
            topic="Signalverarbeitung - Faltung"
        ),

        Question(
            prompt="Was beschreibt das Nyquist-Theorem?",
            options={
                "A": "Die minimale Abtastfrequenz zur fehlerfreien Rekonstruktion eines Signals",
                "B": "Die maximale Verstärkung eines Signals",
                "C": "Die Frequenzmodulation eines Signals",
                "D": "Die Filterung von Rauschen in einem Signal"
            },
            correct={"A"},
            explain_correct="Das Nyquist-Theorem legt fest, dass die Abtastfrequenz mindestens doppelt so hoch sein muss wie die höchste Frequenz im Signal, um eine verlustfreie Rekonstruktion zu ermöglichen.",
            explain_wrong={
                "B": "Die Verstärkung bezieht sich auf die Amplitude, nicht auf die Abtastfrequenz.",
                "C": "Frequenzmodulation ist ein anderer Prozess und steht nicht im Zusammenhang mit dem Nyquist-Theorem.",
                "D": "Die Filterung von Rauschen ist ein separater Prozess, der nicht direkt mit dem Nyquist-Theorem zusammenhängt."
            },
            topic="Signalverarbeitung - Nyquist-Theorem"
        ),

        Question(
            prompt="Welche Aussagen über diskrete und kontinuierliche Signale sind korrekt?",
            options={
                "A": "Ein zeitdiskretes Signal kann wertkontinuierlich oder wertdiskret sein",
                "B": "Ein zeitkontinuierliches Signal ist immer wertkontinuierlich",
                "C": "Ein digitales Signal ist sowohl zeitdiskret als auch wertdiskret",
                "D": "Ein zeitkontinuierliches Signal kann wertdiskret sein"
            },
            correct={"A", "C", "D"},
            explain_correct="Zeitdiskrete Signale können wertkontinuierlich oder wertdiskret sein. "
                            "Digitale Signale sind sowohl zeitdiskret als auch wertdiskret. "
                            "Ein zeitkontinuierliches Signal kann wertdiskret sein (z.B. getaktete Schaltsignale).",
            explain_wrong={
                "B": "Ein zeitkontinuierliches Signal kann wertdiskret sein, z.B. bei Schaltsignalen."
            },
            topic="Signalverarbeitung - Signalarten"
        ),

        Question(
            prompt="Welche Konsequenz hat eine zu niedrige Abtastfrequenz gemäß dem Nyquist-Theorem?",
            options={
                "A": "Aliasing, also eine Überlagerung von Frequenzen",
                "B": "Erhöhte Signalverstärkung",
                "C": "Reduzierte Signalqualität ohne Informationsverlust",
                "D": "Bessere Frequenztrennung"
            },
            correct={"A"},
            explain_correct="Eine zu niedrige Abtastfrequenz führt zu Aliasing, bei dem höhere Frequenzen als niedrigere Frequenzen erscheinen und sich überlagern.",
            explain_wrong={
                "B": "Verstärkung ist nicht direkt mit der Abtastfrequenz verknüpft.",
                "C": "Eine zu niedrige Abtastfrequenz führt gerade zu Informationsverlust, nicht zu einer verbesserten Qualität.",
                "D": "Eine niedrigere Abtastfrequenz führt nicht zu einer besseren Frequenztrennung."
            },
            topic="Signalverarbeitung - Nyquist-Theorem"
        ),

        Question(
            prompt="Welche Aussagen über die Abtastung und das Nyquist-Theorem sind korrekt?",
            options={
                "A": "Die Abtastfrequenz muss größer oder gleich dem Doppelten der höchsten Signalfrequenz sein",
                "B": "Aliasing kann durch ein Tiefpassfilter vor der Abtastung reduziert werden",
                "C": "Eine höhere Abtastfrequenz erhöht immer die Amplitude des Signals",
                "D": "Ohne Aliasing kann ein Signal theoretisch verlustfrei rekonstruiert werden"
            },
            correct={"A", "B", "D"},
            explain_correct="Das Nyquist-Theorem fordert mindestens die doppelte Frequenz, ein Anti-Aliasing-Tiefpassfilter "
                            "reduziert Aliasing, und ohne Aliasing ist eine theoretisch verlustfreie Rekonstruktion möglich.",
            explain_wrong={
                "C": "Die Abtastfrequenz beeinflusst die zeitliche Auflösung, nicht die Amplitude."
            },
            topic="Signalverarbeitung - Abtastung und Nyquist"
        ),

        Question(
            prompt="Wie kann man Aliasing vermeiden?",
            options={
                "A": "Durch Erhöhung der Abtastfrequenz",
                "B": "Durch Verringerung der Signalverstärkung",
                "C": "Durch Veränderung der Modulationsart",
                "D": "Durch Anwendung eines Tiefpassfilters vor dem Abtasten"
            },
            correct={"A", "D"},
            explain_correct="Aliasing kann vermieden werden, indem man die Abtastfrequenz erhöht oder einen Tiefpassfilter anwendet, um hohe Frequenzen vor dem Abtasten zu entfernen.",
            explain_wrong={
                "B": "Die Signalverstärkung hat keinen direkten Einfluss auf Aliasing.",
                "C": "Die Modulationsart beeinflusst nicht das Aliasing direkt."
            },
            topic="Signalverarbeitung - Nyquist-Theorem"
        ),

        Question(
            prompt="Was bedeutet Fourier-Transformation in der Signalverarbeitung?",
            options={
                "A": "Die Zerlegung eines Signals in seine einzelnen Frequenzanteile",
                "B": "Die Verstärkung eines Signals",
                "C": "Die Abtastung eines analogen Signals",
                "D": "Die Filterung eines Signals"
            },
            correct={"A"},
            explain_correct="Die Fourier-Transformation zerlegt ein Signal in seine sinusförmigen Frequenzanteile und stellt es im Frequenzbereich dar.",
            explain_wrong={
                "B": "Verstärkung verändert nur die Amplitude, nicht die Darstellung im Frequenzbereich.",
                "C": "Abtastung bedeutet die Umwandlung eines analogen in ein digitales Signal.",
                "D": "Filterung bedeutet das Entfernen oder Abschwächen bestimmter Frequenzen, nicht deren Analyse."
            },
            topic="Signalverarbeitung - Fourier-Transformation"
        ),

        Question(
            prompt="Was bedeutet Fourier-Synthese in der Signalverarbeitung?",
            options={
                "A": "Der Aufbau eines Signals aus einzelnen Sinus- und Kosinuskomponenten",
                "B": "Die Zerlegung eines Signals in Frequenzanteile",
                "C": "Die Verstärkung eines Signals",
                "D": "Die Modulation eines Signals"
            },
            correct={"A"},
            explain_correct="Fourier-Synthese beschreibt den Aufbau eines Signals durch Überlagerung (Addition) seiner sinusförmigen Frequenzkomponenten.",
            explain_wrong={
                "B": "Das ist die Fourier-Transformation, nicht die Synthese.",
                "C": "Verstärkung verändert nur die Amplitude, nicht die Signalzusammensetzung.",
                "D": "Modulation verändert Signalparameter, nicht den grundsätzlichen Signalaufbau."
            },
            topic="Signalverarbeitung - Fourier-Synthese"
        ),

        Question(
            prompt="Was bedeutet Linearität eines Systems in der Signalverarbeitung?",
            options={
                "A": "Das System erfüllt das Superpositionsprinzip",
                "B": "Das System verändert sein Verhalten über die Zeit",
                "C": "Das System verstärkt jedes Signal gleich stark",
                "D": "Das System filtert alle hohen Frequenzen"
            },
            correct={"A"},
            explain_correct="Ein lineares System erfüllt das Superpositionsprinzip: Die Antwort auf eine Summe von Eingängen ist die Summe der einzelnen Antworten.",
            explain_wrong={
                "B": "Das beschreibt Zeitvarianz, nicht Linearität.",
                "C": "Gleiche Verstärkung allein garantiert keine Linearität.",
                "D": "Filterung ist eine mögliche Eigenschaft, aber kein Kriterium für Linearität."
            },
            topic="Signalverarbeitung - Lineare Systeme"
        ),

        Question(
            prompt="Was bedeutet das Nyquist-Theorem?",
            options={
                "A": "Die Abtastfrequenz muss mindestens doppelt so hoch sein wie die höchste Signalfrequenz",
                "B": "Die Abtastfrequenz muss kleiner als die höchste Signalfrequenz sein",
                "C": "Die Abtastfrequenz beeinflusst nur die Amplitude",
                "D": "Die Abtastfrequenz hat keinen Einfluss auf die Signalqualität"
            },
            correct={"A"},
            explain_correct="Das Nyquist-Theorem besagt, dass die Abtastfrequenz mindestens doppelt so hoch wie die höchste im Signal enthaltene Frequenz sein muss, um Aliasing zu vermeiden.",
            explain_wrong={
                "B": "Das führt zu Aliasing.",
                "C": "Die Abtastfrequenz beeinflusst die zeitliche Auflösung, nicht die Amplitude.",
                "D": "Die Abtastfrequenz ist entscheidend für die Signalqualität."
            },
            topic="Signalverarbeitung - Abtasttheorie"
        ),

        Question(
            prompt="Was bedeutet Rekonstruktion eines Signals?",
            options={
                "A": "Die Rückgewinnung eines analogen Signals aus diskreten Abtastwerten",
                "B": "Die Verstärkung eines digitalen Signals",
                "C": "Die Modulation eines Signals",
                "D": "Die Zerlegung eines Signals in Frequenzen"
            },
            correct={"A"},
            explain_correct="Rekonstruktion bezeichnet den Prozess, aus diskreten Abtastwerten wieder ein kontinuierliches analoges Signal zu erzeugen.",
            explain_wrong={
                "B": "Verstärkung verändert nur die Amplitude.",
                "C": "Modulation verändert Signalparameter.",
                "D": "Zerlegung in Frequenzen ist Fourier-Transformation."
            },
            topic="Signalverarbeitung - Rekonstruktion"
        ),

        Question(
            prompt="Welche der folgenden sind echte, grundlegende Filtertypen in der Signalverarbeitung?",
            options={
                "A": "Tiefpass",
                "B": "Hochbandfilter",
                "C": "Bandpass",
                "D": "Frequenzsperre"
            },
            correct={"A", "C", "D"},
            explain_correct="Tiefpass, Bandpass und Bandsperre (auch Frequenzsperre oder Notch genannt) sind echte Filtertypen. "
                            "Ein 'Hochbandfilter' ist kein standardisierter Filtertyp.",
            explain_wrong={
                "B": "Der Begriff 'Hochbandfilter' ist kein standardisierter Filtertyp in der Signalverarbeitung."
            },
            topic="Signalverarbeitung - Filter"
        ),

        Question(
            prompt="Welche Filterarten existieren in der Signalverarbeitung?",
            options={
                "A": "Hochpass",
                "B": "Bandsperre (Notch)",
                "C": "Niederfrequenzfilter",
                "D": "Phasenfilter"
            },
            correct={"A", "B"},
            explain_correct="Hochpass und Bandsperre sind grundlegende Filtertypen. "
                            "'Niederfrequenzfilter' ist kein standardisierter Begriff für einen Filtertyp "
                            "(gemeint wäre Tiefpass), und 'Phasenfilter' ist kein eigenständiger Grundfiltertyp.",
            explain_wrong={
                "C": "Der korrekte Begriff ist 'Tiefpass', nicht 'Niederfrequenzfilter'.",
                "D": "Ein Phasenfilter ist kein grundlegender Filtertyp im klassischen Sinn."
            },
            topic="Signalverarbeitung - Filter"
        ),

        Question(
            prompt="Was bedeutet Zeitinvarianz eines Systems in der Signalverarbeitung?",
            options={
                "A": "Das Systemverhalten ändert sich nicht, wenn das Eingangssignal zeitlich verschoben wird",
                "B": "Das System verstärkt alle Frequenzen gleich stark",
                "C": "Das System ist immer linear",
                "D": "Das System filtert Störungen automatisch heraus"
            },
            correct={"A"},
            explain_correct="Ein zeitinvariantes System reagiert auf ein zeitlich verschobenes Eingangssignal mit einer entsprechend zeitlich verschobenen Ausgabe, ohne sein Verhalten zu ändern.",
            explain_wrong={
                "B": "Das beschreibt Frequenzgang-Eigenschaften, nicht Zeitinvarianz.",
                "C": "Ein System kann zeitinvariant sein, ohne linear zu sein.",
                "D": "Störungsunterdrückung ist keine Eigenschaft der Zeitinvarianz."
            },
            topic="Signalverarbeitung - Zeitinvariante Systeme"
        ),

        Question(
            prompt="Welche Eigenschaften treffen auf ein lineares zeitinvariantes (LTI) System zu?",
            options={
                "A": "Das System erfüllt das Superpositionsprinzip",
                "B": "Die Impulsantwort beschreibt das System vollständig",
                "C": "Eine zeitliche Verschiebung des Eingangssignals führt zu einer identischen Verschiebung der Ausgabe",
                "D": "Das System kann nur sinusförmige Signale verarbeiten"
            },
            correct={"A", "B", "C"},
            explain_correct="Ein LTI-System ist linear (Superpositionsprinzip), zeitinvariant (Verschiebungseigenschaft) "
                            "und vollständig durch seine Impulsantwort beschrieben.",
            explain_wrong={
                "D": "Ein LTI-System kann beliebige Signale verarbeiten, nicht nur Sinusschwingungen."
            },
            topic="Signalverarbeitung - LTI-Systeme"
        ),

        Question(
            prompt="Welche Aussagen zur Faltung und zum Frequenzbereich sind korrekt?",
            options={
                "A": "Faltung im Zeitbereich entspricht einer Multiplikation im Frequenzbereich",
                "B": "Multiplikation im Zeitbereich entspricht einer Faltung im Frequenzbereich",
                "C": "Die Fourier-Transformation einer Impulsantwort ergibt den Frequenzgang des Systems",
                "D": "Faltung ist nur für zeitkontinuierliche Signale definiert"
            },
            correct={"A", "B", "C"},
            explain_correct="Faltung im Zeitbereich entspricht einer Multiplikation im Frequenzbereich und umgekehrt. "
                            "Die Fourier-Transformation der Impulsantwort liefert den Frequenzgang. "
                            "Faltung ist sowohl für zeitkontinuierliche als auch zeitdiskrete Signale definiert.",
            explain_wrong={
                "D": "Faltung ist auch für zeitdiskrete Signale definiert."
            },
            topic="Signalverarbeitung - Faltung und Frequenzbereich"
        ),

        Question(
            prompt="Welche Aussagen zur Fourier-Transformation und Fourier-Synthese sind korrekt?",
            options={
                "A": "Die Fourier-Transformation zerlegt ein Signal in seine Frequenzkomponenten",
                "B": "Die Fourier-Synthese baut ein Signal aus seinen Frequenzkomponenten wieder auf",
                "C": "Ein zeitbegrenztes Signal hat immer ein bandbegrenztes Spektrum",
                "D": "Ein bandbegrenztes Signal ist immer zeitlich unbegrenzt"
            },
            correct={"A", "B", "D"},
            explain_correct="Fourier-Transformation zerlegt, Fourier-Synthese rekonstruiert. "
                            "Ein bandbegrenztes Signal ist zwangsläufig zeitlich unbegrenzt. "
                            "Ein zeitbegrenztes Signal ist hingegen nicht bandbegrenzt.",
            explain_wrong={
                "C": "Ein zeitbegrenztes Signal ist im Allgemeinen nicht bandbegrenzt."
            },
            topic="Signalverarbeitung - Fourier-Analyse"
        ),

        Question(
            prompt="Welche Zuordnung der Farben zu den Audioanschlüssen ist korrekt?",
            options={
                "A": "Grün = Line Out, Blau = Line In, Rot = Mic In",
                "B": "Grün = Mic In, Blau = Line Out, Rot = Line In",
                "C": "Grün = Line In, Blau = Mic In, Rot = Line Out",
                "D": "Grün = Line Out, Blau = Mic In, Rot = Line In"
            },
            correct={"A"},
            explain_correct="Standardmäßig gilt: Grün = Line Out (Lautsprecher/Kopfhörer), "
                            "Blau = Line In (externe Audioquellen), "
                            "Rot = Mic In (Mikrofon).",
            explain_wrong={
                "B": "Mic In ist rot, nicht grün.",
                "C": "Line In ist blau, nicht grün.",
                "D": "Mic In ist rot, nicht blau."
            },
            topic="Signalverarbeitung - Audioanschlüsse"
        ),

        Question(
            prompt="Welche Aussagen zu Line In, Line Out und Mic In sind korrekt?",
            options={
                "A": "Line Out liefert ein Ausgangssignal für Lautsprecher oder Kopfhörer",
                "B": "Mic In ist für hochpegelige Line-Signale gedacht",
                "C": "Line In ist für externe Audioquellen mit Line-Pegel vorgesehen",
                "D": "Mic In erwartet ein schwaches Mikrofonsignal"
            },
            correct={"A", "C", "D"},
            explain_correct="Line Out gibt Audiosignale aus, Line In nimmt Line-Pegel-Signale auf, "
                            "Mic In ist für schwache Mikrofonsignale ausgelegt.",
            explain_wrong={
                "B": "Mic In ist nicht für hochpegelige Line-Signale gedacht, sondern für sehr schwache Mikrofonsignale."
            },
            topic="Signalverarbeitung - Audioanschlüsse"
        ),

        Question(
            prompt="Welche Kombinationen aus Anschlussfarbe und Funktion sind korrekt?",
            options={
                "A": "Blau = Line In",
                "B": "Rot = Line Out",
                "C": "Grün = Line Out",
                "D": "Rot = Mic In"
            },
            correct={"A", "C", "D"},
            explain_correct="Blau steht für Line In, Grün für Line Out und Rot für Mic In.",
            explain_wrong={
                "B": "Rot ist Mic In, nicht Line Out."
            },
            topic="Signalverarbeitung - Audioanschlüsse"
        )

    ]
    return _rebalance_single_choice_correct_letters(questions)