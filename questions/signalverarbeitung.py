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
from typing import List


def get_questions() -> List[Question]:
    """Gibt alle Fragen zur Signalverarbeitung zurück"""
    return [
        # ============================================================
        # FOURIER-TRANSFORMATION
        # ============================================================
        Question(
            prompt="Unter Anwendung welches Prinzips kann man die Darstellung eines Signals im Zeit- und Frequenzbereich ändern - und zurück?",
            options={
                "A": "Laplace-Transformation",
                "B": "Fourierprinzip / Fouriertransformation",
                "C": "Nyquist-Theorem",
                "D": "Shannon-Theorem"
            },
            correct={"B"},
            explain_correct="Das Fourierprinzip ermöglicht die Umwandlung zwischen Zeit- und Frequenzbereich. "
                          "Die Fouriersynthese baut ein Signal aus Sinusschwingungen auf. "
                          "Die DFT (Diskrete Fourier-Transformation) wandelt vom Zeitbereich in den Frequenzbereich, "
                          "die IDFT (Inverse DFT) macht dies rückgängig.",
            explain_wrong={
                "A": "Die Laplace-Transformation ist eine Verallgemeinerung, wird aber nicht primär für Zeit-Frequenz-Umwandlung verwendet.",
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
            prompt="Was ist der Unterschied zwischen DFT und FFT?",
            options={
                "A": "FFT ist eine schnelle Implementierung der DFT",
                "B": "DFT ist für analoge, FFT für digitale Signale",
                "C": "FFT liefert genauere Ergebnisse",
                "D": "Es gibt keinen Unterschied"
            },
            correct={"A"},
            explain_correct="Die FFT (Fast Fourier Transform) ist ein effizienter Algorithmus zur "
                          "Berechnung der DFT. Waehrend die direkte DFT O(N^2) Operationen benötigt, "
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
                "B": "Von der höchsten vorkommenden Frequenz des Signals",
                "C": "Von der Laenge des Signals",
                "D": "Von der Bittiefe"
            },
            correct={"B"},
            explain_correct="Nach dem Nyquist-Shannon-Theorem muss die Abtastrate mindestens doppelt so hoch sein "
                          "wie die höchste im Signal vorkommende Frequenz. Bei einem Signal mit maximal 20 kHz "
                          "(menschliches Hoeren) braucht man also mindestens 40 kHz Abtastrate. "
                          "CDs verwenden 44.1 kHz, um etwas Spielraum zu haben.",
            explain_wrong={
                "A": "Die Amplitude beeinflusst die nötige Bittiefe, nicht die Abtastrate.",
                "C": "Die Signallänge ist irrelevant für die Abtastrate.",
                "D": "Die Bittiefe betrifft die Quantisierung, nicht das Sampling."
            },
            topic="Signalverarbeitung - Sampling"
        ),

        Question(
            prompt="Wie groß muss die Abtastrate mindestens sein? (Mehrfachauswahl möglich)",
            options={
                "A": "Mindestens gleich der höchsten Signalfrequenz",
                "B": "Mindestens 2x die höchste Signalfrequenz (Nyquist-Theorem)",
                "C": "Mindestens 10x die höchste Signalfrequenz",
                "D": "Die Abtastrate ist egal"
            },
            correct={"B"},
            explain_correct="Das Nyquist-Shannon-Theorem besagt: Die Abtastfrequenz muss mindestens "
                          "doppelt so hoch sein wie die höchste Signalfrequenz (fs >= 2 * fmax). "
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
                "B": "Aliasing",
                "C": "Rauschen",
                "D": "Verstärkung"
            },
            correct={"B"},
            explain_correct="Aliasing tritt auf, wenn die Abtastrate zu niedrig ist (unter dem Nyquist-Limit). "
                          "Hohe Frequenzen werden dann fälschlicherweise als niedrigere Frequenzen interpretiert - "
                          "sie 'spiegeln' sich am Nyquist-Punkt. Das führt zu hoerbaren Artefakten und "
                          "Verzerrungen, die nicht mehr rückgängig gemacht werden können.",
            explain_wrong={
                "A": "Clipping entsteht durch Übersteuerung, nicht durch niedrige Abtastrate.",
                "C": "Rauschen hat andere Ursachen.",
                "D": "Verstärkung ist unabhaengig von der Abtastrate."
            },
            topic="Signalverarbeitung - Sampling"
        ),

        Question(
            prompt="Welchen technischen Zusatz verwendet man, um Aliasing zu vermeiden?",
            options={
                "A": "Verstaerker",
                "B": "Anti-Aliasing-Filter (Tiefpassfilter)",
                "C": "Kompressor",
                "D": "Equalizer"
            },
            correct={"B"},
            explain_correct="Ein Anti-Aliasing-Filter ist ein Tiefpassfilter, der vor dem A/D-Wandler geschaltet wird. "
                          "Er entfernt alle Frequenzen oberhalb der halben Abtastfrequenz (Nyquist-Frequenz), "
                          "bevor das Signal abgetastet wird. So wird sichergestellt, dass das Nyquist-Theorem "
                          "eingehalten wird und kein Aliasing entstehen kann.",
            explain_wrong={
                "A": "Ein Verstaerker aendert nur die Amplitude.",
                "C": "Ein Kompressor reduziert die Dynamik.",
                "D": "Ein Equalizer formt das Frequenzspektrum, verhindert aber nicht Aliasing."
            },
            topic="Signalverarbeitung - Sampling"
        ),

        Question(
            prompt="Welche Abtastraten und Quantisierungen sind in der Audiotechnik üblich? (Mehrfachauswahl)",
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
            prompt="Ein analoges Signal besteht aus Sinustoenen mit Periodendauern T1=3.79ms, T2=3.03ms, T3=2.53ms. "
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
                "D": "1584 Hz waere mehr als nötig (4x statt 2x)."
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
            prompt="Was sind Vorteile der symmetrischen gegenüber der asymmetrischen Signaluebertragung? (Mehrfachauswahl)",
            options={
                "A": "Bessere Störunterdrückung durch Gleichtaktunterdrückung",
                "B": "Längere Kabelwege möglich",
                "C": "Günstiger und einfacher",
                "D": "A und B sind richtig"
            },
            correct={"A", "B", "D"},
            explain_correct="Bei symmetrischer Übertragung wird das Signal zweimal geführt: normal und invertiert. "
                          "Am Empfaenger wird die Differenz gebildet - Störungen, die auf beide Leiter gleich wirken, "
                          "heben sich dabei auf (Gleichtaktunterdrückung). Dadurch sind laengere Kabelwege möglich. "
                          "Nachteile: höhere Kosten und Komplexitaet (3 Leiter statt 2).",
            explain_wrong={
                "C": "Asymmetrische Übertragung ist guenstiger und einfacher."
            },
            topic="Signalverarbeitung - Übertragung"
        ),

        Question(
            prompt="Welche Steckverbinder nutzt man typischerweise für asymmetrische Signaluebertragung? (Mehrfachauswahl)",
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
                "B": "Signal-to-Noise Ratio (Signal-Rausch-Abstand)",
                "C": "Sample Nyquist Rate",
                "D": "Stereo Normalizing Range"
            },
            correct={"B"},
            explain_correct="SNR steht für Signal-to-Noise Ratio, auf Deutsch Signal-Rausch-Abstand. "
                          "Es beschreibt das Verhältnis zwischen Nutzsignal und Störsignal (Rauschen), "
                          "angegeben in dB. Ein höherer SNR bedeutet weniger Rauschen relativ zum Signal. "
                          "Gute Audiogeräte haben SNR-Werte von 90-120 dB.",
            explain_wrong={
                "A": "Signal Noise Reduction waere eine Rauschunterdrückungstechnik.",
                "C": "Das ist keine gängige Abkürzung.",
                "D": "Das ist keine gängige Abkürzung."
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
                "A": "Die Lautstaerke eines Tons",
                "B": "Der Tonhoehenabstand zwischen zwei Tönen",
                "C": "Die Dauer eines Tons",
                "D": "Die Klangfarbe eines Instruments"
            },
            correct={"B"},
            explain_correct="Ein Intervall beschreibt den Tonhoehenabstand zwischen zwei Tönen. "
                          "Intervalle haben Namen wie Sekunde, Terz, Quarte, Quinte, Oktave usw. "
                          "Sie werden durch das Frequenzverhaeltnis der beiden Toene bestimmt. "
                          "Eine Oktave entspricht einer Frequenzverdopplung (2:1).",
            explain_wrong={
                "A": "Die Lautstaerke wird durch die Amplitude bestimmt.",
                "C": "Die Dauer ist der Notenwert.",
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
                "A": "Die Quinte hat das Frequenzverhaeltnis 3:2.",
                "B": "Die Quarte hat das Frequenzverhaeltnis 4:3.",
                "D": "Die große Terz hat das Frequenzverhaeltnis 5:4."
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
            prompt="Was sind Obertoene?",
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
                "B": "Linear Time Invariant (linear und zeitinvariant)",
                "C": "Logarithmic Transfer Interface",
                "D": "Limited Transfer Integration"
            },
            correct={"B"},
            explain_correct="LTI steht für Linear Time Invariant - ein System das linear ist "
                          "(Skalierung und Additivitaet gelten) und zeitinvariant (das Verhalten "
                          "aendert sich nicht mit der Zeit). LTI-Systeme sind mathematisch gut "
                          "beschreibbar und bilden die Grundlage der klassischen Signalverarbeitung.",
            explain_wrong={
                "A": "Das ist keine korrekte Bedeutung.",
                "C": "Das ist keine korrekte Bedeutung.",
                "D": "Das ist keine korrekte Bedeutung."
            },
            topic="Signalverarbeitung - LTI"
        ),

        Question(
            prompt="Was ist die Impulsantwort eines Systems?",
            options={
                "A": "Die maximale Verstärkung",
                "B": "Die Antwort auf einen idealen Impuls (Dirac-Stoss)",
                "C": "Die minimale Latenz",
                "D": "Die Grenzfrequenz"
            },
            correct={"B"},
            explain_correct="Die Impulsantwort ist die Reaktion eines Systems auf einen idealen Impuls "
                          "(Dirac-Stoss). Sie beschreibt ein LTI-System vollständig - kennt man die "
                          "Impulsantwort, kann man die Ausgabe für jedes beliebige Eingangssignal berechnen "
                          "(durch Faltung). Die Impulsantwort ist sozusagen der 'Fingerabdruck' des Systems.",
            explain_wrong={
                "A": "Die Verstärkung ist nur ein Aspekt des Systemverhaltens.",
                "C": "Die Latenz ist nicht durch die Impulsantwort allein definiert.",
                "D": "Die Grenzfrequenz gehoert zum Frequenzgang."
            },
            topic="Signalverarbeitung - LTI"
        ),

        Question(
            prompt="Was benötigt man, um ein LTI-System vollständig zu beschreiben? (Mehrfachauswahl)",
            options={
                "A": "Die Impulsantwort",
                "B": "Die Übertragungsfunktion (Frequenzgang)",
                "C": "Die Farbe des Geraets",
                "D": "A oder B genuegen jeweils"
            },
            correct={"A", "B", "D"},
            explain_correct="Ein LTI-System ist vollständig durch seine Impulsantwort ODER seine "
                          "Übertragungsfunktion beschrieben - beide enthalten die gleiche Information, "
                          "nur in verschiedenen Darstellungen (Zeitbereich vs. Frequenzbereich). "
                          "Sie sind durch die Fouriertransformation ineinander umrechenbar.",
            explain_wrong={
                "C": "Die physische Erscheinung ist für das Systemverhalten irrelevant."
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
            prompt="Was ist eine Faltung im Frequenzbereich?",
            options={
                "A": "Entspricht einer Addition im Zeitbereich",
                "B": "Entspricht einer Multiplikation im Zeitbereich",
                "C": "Entspricht einer Faltung im Zeitbereich",
                "D": "Hat keine Entsprechung im Zeitbereich"
            },
            correct={"B"},
            explain_correct="Faltung im Frequenzbereich entspricht Multiplikation im Zeitbereich - "
                          "das ist das 'Gegenstück' zum Faltungssatz. Wenn man zwei Spektren faltet, "
                          "multipliziert man die Zeitsignale. Dies ist z.B. relevant bei "
                          "Amplitudenmodulation (Traeger * Modulationssignal).",
            explain_wrong={
                "A": "Addition im Frequenzbereich entspricht Addition im Zeitbereich.",
                "C": "Faltung im Zeitbereich entspricht Multiplikation im Frequenzbereich.",
                "D": "Es gibt sehr wohl eine Entsprechung."
            },
            topic="Signalverarbeitung - LTI"
        ),

        Question(
            prompt="Je grober die Zeitaufloesung, desto ...?",
            options={
                "A": "Schlechter die Frequenzaufloesung",
                "B": "Besser die Frequenzaufloesung",
                "C": "Gleich bleibt die Frequenzaufloesung",
                "D": "Zufaellig aendert sich die Frequenzaufloesung"
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
            prompt="Welche Filtertypen gibt es? (Mehrfachauswahl)",
            options={
                "A": "Tiefpass",
                "B": "Hochpass",
                "C": "Bandpass",
                "D": "Bandsperre (Notch)"
            },
            correct={"A", "B", "C", "D"},
            explain_correct="Alle vier sind grundlegende Filtertypen: "
                          "Tiefpass laesst niedrige Frequenzen durch (unter Cutoff), "
                          "Hochpass laesst hohe Frequenzen durch (ueber Cutoff), "
                          "Bandpass laesst einen Frequenzbereich durch, "
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
                "B": "Frequenzverfaelschung durch zu niedrige Abtastrate",
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
            prompt="Wovon hängt der elektrische Widerstand eines Leiters ab? (Mehrfachauswahl möglich)",
            options={
                "A": "Von der Leiterlaenge l",
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
            prompt="Ein Spannungsteiler besteht aus zwei gleichen Widerstaenden in Reihe an U=230V. Wie groß ist U1 ueber dem ersten Widerstand?",
            options={
                "A": "230 V",
                "B": "115 V",
                "C": "57.5 V",
                "D": "0 V"
            },
            correct={"B"},
            explain_correct="Bei zwei gleichen Widerstaenden teilt sich die Spannung gleich auf: U1 = 230 V / 2 = 115 V.",
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
            prompt="Warum kann Powerline Communication (PLC) Daten ueber Stromkabel übertragen, obwohl dort schon 50 Hz Netzspannung anliegt?",
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
                "A": "Je hoeher die Frequenz, desto groesser die Wellenlaenge und die Antenne",
                "B": "Je hoeher die Frequenz, desto kleiner die Wellenlaenge und desto kleiner kann die Antenne sein",
                "C": "Frequenz und Wellenlaenge sind unabhaengig",
                "D": "Antennegroesse hängt nur von der Sendeleistung ab"
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
            explain_correct="FIFO bedeutet First In / First Out: Das aelteste Element im Buffer wird zuerst wieder ausgegeben.",
            explain_wrong={
                "A": "Keine gängige Bedeutung.",
                "C": "Nicht korrekt.",
                "D": "Nicht korrekt."
            },
            topic="Signalverarbeitung - Netzwerke"
        ),

        Question(
            prompt="Welche Aussagen treffen typischerweise auf UDP im Vergleich zu TCP zu? (Mehrfachauswahl möglich)",
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
            explain_correct="Typischer Farbcode am PC: Gruen = Line Out, Blau = Line In, Rot/Pink = Mic In.",
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
    ]