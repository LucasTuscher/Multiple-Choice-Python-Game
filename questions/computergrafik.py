#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fragen zum Thema: Computergrafik
Umfassende Fragensammlung zu: Mathematische Grundlagen, Grafik-Pipeline, Geometrische Modellierung,
Transformationen, Licht und Farbe, Beleuchtungsmodelle, Globale Beleuchtung, Texture Mapping, Shader
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quiz_engine import Question
from typing import List


def get_questions() -> List[Question]:
    """Gibt alle Fragen zur Computergrafik zurück"""
    return [
        # ============================================================
        # MATHEMATISCHE GRUNDLAGEN
        # ============================================================
        Question(
            prompt="Was ist ein Vektor in der Computergrafik?",
            options={
                "A": "Ein Punkt im Raum ohne Richtung",
                "B": "Eine gerichtete Groesse mit Betrag und Richtung",
                "C": "Eine Matrix mit einer Zeile",
                "D": "Ein Farbwert"
            },
            correct={"B"},
            explain_correct="Ein Vektor ist eine gerichtete Groesse, die durch Betrag (Laenge) und "
                          "Richtung definiert ist. In der Computergrafik werden Vektoren fuer Positionen, "
                          "Richtungen (z.B. Normalen, Blickrichtung), Geschwindigkeiten und Kraefte verwendet. "
                          "Sie werden meist als (x, y, z) oder (x, y, z, w) in homogenen Koordinaten dargestellt.",
            explain_wrong={
                "A": "Ein Punkt hat keine Richtung, ein Vektor schon.",
                "C": "Eine Matrix mit einer Zeile ist ein Zeilenvektor, aber Vektor ist allgemeiner.",
                "D": "Farbwerte koennen als Vektoren dargestellt werden, sind aber nicht die Definition."
            },
            topic="Computergrafik - Mathematik"
        ),

        Question(
            prompt="Was ist das Skalarprodukt (Dot Product) zweier Vektoren? (Mehrfachauswahl)",
            options={
                "A": "Ergibt einen Skalar (einzelne Zahl)",
                "B": "Ergibt einen neuen Vektor",
                "C": "Misst den Winkel zwischen zwei Vektoren",
                "D": "a·b = |a||b|cos(theta)"
            },
            correct={"A", "C", "D"},
            explain_correct="Das Skalarprodukt (Dot Product) zweier Vektoren ergibt eine einzelne Zahl (Skalar). "
                          "Die Formel ist a·b = |a||b|cos(theta), wobei theta der Winkel zwischen den Vektoren ist. "
                          "Es wird haeufig verwendet um: Winkel zu berechnen, zu pruefen ob Vektoren senkrecht stehen "
                          "(dot=0), oder fuer Beleuchtungsberechnungen (Lambertsches Gesetz).",
            explain_wrong={
                "B": "Das Ergebnis ist ein Skalar, kein Vektor. Das Kreuzprodukt ergibt einen Vektor."
            },
            topic="Computergrafik - Mathematik"
        ),

        Question(
            prompt="Was ist das Kreuzprodukt (Cross Product) zweier Vektoren? (Mehrfachauswahl)",
            options={
                "A": "Ergibt einen Vektor senkrecht zu beiden Eingabevektoren",
                "B": "Ergibt einen Skalar",
                "C": "Wird fuer Normalenberechnung verwendet",
                "D": "a x b = |a||b|sin(theta)"
            },
            correct={"A", "C", "D"},
            explain_correct="Das Kreuzprodukt zweier Vektoren a und b ergibt einen neuen Vektor, "
                          "der senkrecht auf beiden steht. Der Betrag ist |a||b|sin(theta). "
                          "Es wird haeufig verwendet um: Flaechennormalen zu berechnen, "
                          "die Orientierung von Dreiecken zu bestimmen, oder Drehachsen zu finden.",
            explain_wrong={
                "B": "Das Kreuzprodukt ergibt einen Vektor, nicht einen Skalar."
            },
            topic="Computergrafik - Mathematik"
        ),

        Question(
            prompt="Was ist eine Matrix in der Computergrafik?",
            options={
                "A": "Ein einzelner Zahlenwert",
                "B": "Ein rechteckiges Zahlenschema zur Darstellung linearer Transformationen",
                "C": "Ein Bild",
                "D": "Eine Textur"
            },
            correct={"B"},
            explain_correct="Eine Matrix ist ein rechteckiges Schema von Zahlen. In der Computergrafik werden "
                          "meist 4x4-Matrizen verwendet, um Transformationen (Translation, Rotation, Skalierung) "
                          "darzustellen. Durch Matrixmultiplikation koennen mehrere Transformationen kombiniert werden. "
                          "Die Model-View-Projection-Matrix (MVP) ist das Produkt dreier solcher Matrizen.",
            explain_wrong={
                "A": "Ein einzelner Wert ist ein Skalar.",
                "C": "Ein Bild kann als Matrix dargestellt werden, ist aber nicht die Definition.",
                "D": "Texturen sind Bilddaten, keine Matrizen im mathematischen Sinn."
            },
            topic="Computergrafik - Mathematik"
        ),

        Question(
            prompt="Warum verwendet man homogene Koordinaten (4D statt 3D)?",
            options={
                "A": "Weil 4D-Grafiken schoener aussehen",
                "B": "Um Translation als Matrixmultiplikation darstellen zu koennen",
                "C": "Weil die GPU nur 4D kann",
                "D": "Fuer bessere Farbdarstellung"
            },
            correct={"B"},
            explain_correct="Mit homogenen Koordinaten (x, y, z, w) kann man Translation als 4x4-Matrix ausdruecken. "
                          "In 3D ist Translation keine lineare Transformation und kann nicht als 3x3-Matrix dargestellt werden. "
                          "Mit der vierten Koordinate w koennen alle affinen Transformationen (Translation, Rotation, "
                          "Skalierung) einheitlich als Matrixmultiplikation behandelt und kombiniert werden.",
            explain_wrong={
                "A": "Die Dimension hat nichts mit der Optik zu tun.",
                "C": "GPUs koennen auch mit 3D arbeiten.",
                "D": "Farben werden separat behandelt (RGB/RGBA)."
            },
            topic="Computergrafik - Mathematik"
        ),

        Question(
            prompt="Was bedeutet w=0 bei homogenen Koordinaten?",
            options={
                "A": "Der Punkt liegt im Unendlichen / es ist ein Richtungsvektor",
                "B": "Der Punkt liegt im Ursprung",
                "C": "Die Koordinate ist ungueltig",
                "D": "Der Punkt ist unsichtbar"
            },
            correct={"A"},
            explain_correct="Bei homogenen Koordinaten bedeutet w=0, dass es sich um einen Richtungsvektor "
                          "(keinen Punkt) handelt, oder dass der Punkt im Unendlichen liegt. "
                          "Bei w=1 ist es ein normaler Punkt. Werte dazwischen entstehen bei perspektivischer "
                          "Projektion und werden durch Division durch w normalisiert (perspektivische Division).",
            explain_wrong={
                "B": "Der Ursprung hat w=1, nicht w=0.",
                "C": "w=0 ist gueltig fuer Richtungsvektoren.",
                "D": "Sichtbarkeit haengt von anderen Faktoren ab."
            },
            topic="Computergrafik - Mathematik"
        ),

        # ============================================================
        # DIE GRAFIK-PIPELINE
        # ============================================================
        Question(
            prompt="Was ist die richtige Reihenfolge der Rendering Pipeline?",
            options={
                "A": "Fragment Shader -> Vertex Shader -> Rasterization",
                "B": "Vertex Shader -> Rasterization -> Fragment Shader",
                "C": "Rasterization -> Vertex Shader -> Fragment Shader",
                "D": "Fragment Shader -> Rasterization -> Vertex Shader"
            },
            correct={"B"},
            explain_correct="Die korrekte Reihenfolge ist: 1) Vertex Shader (transformiert Vertices mit MVP-Matrix), "
                          "2) Primitive Assembly & Clipping (Dreiecke zusammenbauen, zuschneiden), "
                          "3) Rasterization (Dreiecke in Fragmente umwandeln), "
                          "4) Fragment Shader (Farbe jedes Fragments berechnen), "
                          "5) Per-Fragment Operations (Depth Test, Blending).",
            explain_wrong={
                "A": "Fragment Shader kommt nach der Rasterisierung, nicht davor.",
                "C": "Vertex Shader kommt zuerst, dann wird rasterisiert.",
                "D": "Komplett falsche Reihenfolge."
            },
            topic="Computergrafik - Pipeline"
        ),

        Question(
            prompt="Was macht der Vertex Shader?",
            options={
                "A": "Faerbt Pixel ein",
                "B": "Transformiert Vertices und berechnet ihre Eigenschaften",
                "C": "Laedt Texturen",
                "D": "Komprimiert Daten"
            },
            correct={"B"},
            explain_correct="Der Vertex Shader ist ein Programm, das fuer jeden Vertex ausgefuehrt wird. "
                          "Seine Hauptaufgabe ist die Transformation der Vertex-Position mit der MVP-Matrix "
                          "(Model-View-Projection). Er kann auch andere Attribute berechnen wie transformierte "
                          "Normalen, Texturkoordinaten, oder Beleuchtungswerte fuer Gouraud-Shading.",
            explain_wrong={
                "A": "Das macht der Fragment Shader.",
                "C": "Texturen werden im Fragment Shader gesampelt.",
                "D": "Kompression ist kein Teil der Grafik-Pipeline."
            },
            topic="Computergrafik - Pipeline"
        ),

        Question(
            prompt="Was macht der Fragment Shader (Pixel Shader)?",
            options={
                "A": "Transformiert Vertices",
                "B": "Berechnet die Farbe jedes Pixels/Fragments",
                "C": "Erstellt Dreiecke aus Vertices",
                "D": "Sortiert die Dreiecke"
            },
            correct={"B"},
            explain_correct="Der Fragment Shader wird fuer jedes Fragment (potenzielles Pixel) ausgefuehrt "
                          "und berechnet dessen finale Farbe. Er verwendet dafuer interpolierte Werte vom "
                          "Vertex Shader, Texturen, Beleuchtungsberechnungen (Phong-Modell), und andere Effekte. "
                          "Pro Fragment koennen komplexe Berechnungen wie Normal Mapping oder PBR stattfinden.",
            explain_wrong={
                "A": "Das macht der Vertex Shader.",
                "C": "Das macht die Primitive Assembly.",
                "D": "Sortierung passiert beim Depth Test."
            },
            topic="Computergrafik - Pipeline"
        ),

        Question(
            prompt="Was ist Rasterization?",
            options={
                "A": "Die Umwandlung von Vektorgrafik in Pixel/Fragmente",
                "B": "Das Laden von Texturen",
                "C": "Die Kompression von Bildern",
                "D": "Die Berechnung von Schatten"
            },
            correct={"A"},
            explain_correct="Rasterization (Rasterisierung) wandelt geometrische Primitive (Dreiecke) in diskrete "
                          "Fragmente um. Fuer jedes Pixel, das von einem Dreieck ueberdeckt wird, wird ein Fragment "
                          "erzeugt. Dabei werden die Vertex-Attribute (Position, Farbe, Texturkoordinaten, Normalen) "
                          "per baryzentrischer Interpolation ueber das Dreieck verteilt.",
            explain_wrong={
                "B": "Texturen werden separat geladen.",
                "C": "Kompression ist ein separater Prozess.",
                "D": "Schatten werden in Shadern oder extra Paessen berechnet."
            },
            topic="Computergrafik - Pipeline"
        ),

        Question(
            prompt="Was ist der Depth Buffer (Z-Buffer)?",
            options={
                "A": "Speichert die Farbe jedes Pixels",
                "B": "Speichert die Tiefe jedes Pixels fuer verdeckte Flaechen",
                "C": "Speichert die Texturkoordinaten",
                "D": "Speichert die Vertex-Positionen"
            },
            correct={"B"},
            explain_correct="Der Z-Buffer (Depth Buffer) speichert fuer jedes Pixel die Tiefe (Z-Koordinate, "
                          "Entfernung zur Kamera) des naechsten sichtbaren Fragments. Beim Rendern wird geprueft, "
                          "ob ein neues Fragment naeher ist als der gespeicherte Wert. Nur wenn ja, wird das Pixel "
                          "aktualisiert. So werden verdeckte Flaechen korrekt behandelt ohne Sortierung.",
            explain_wrong={
                "A": "Das ist der Color/Frame Buffer.",
                "C": "Texturkoordinaten werden anders gespeichert.",
                "D": "Vertices werden in Vertex Buffern gespeichert."
            },
            topic="Computergrafik - Pipeline"
        ),

        Question(
            prompt="Was ist der Stencil Buffer?",
            options={
                "A": "Speichert Farbwerte",
                "B": "Speichert Tiefenwerte",
                "C": "Speichert ganzzahlige Werte fuer Masken und Spezialeffekte",
                "D": "Speichert Texturkoordinaten"
            },
            correct={"C"},
            explain_correct="Der Stencil Buffer speichert einen ganzzahligen Wert (meist 8 Bit) pro Pixel. "
                          "Er wird verwendet fuer: Schattenvolumen (Shadow Volumes), Spiegeleffekte, "
                          "Portal-Rendering, Outline-Effekte, und andere Masken. Man kann damit bestimmte "
                          "Bildschirmbereiche markieren und spaeter gezielt rendern oder aussparen.",
            explain_wrong={
                "A": "Farbwerte sind im Color Buffer.",
                "B": "Tiefenwerte sind im Depth Buffer.",
                "D": "Texturkoordinaten werden anders behandelt."
            },
            topic="Computergrafik - Pipeline"
        ),

        Question(
            prompt="Welche Stufen der Rendering-Pipeline sind programmierbar (Shader)? (Mehrfachauswahl)",
            options={
                "A": "Vertex Shader",
                "B": "Fragment Shader",
                "C": "Geometry Shader",
                "D": "Rasterization"
            },
            correct={"A", "B", "C"},
            explain_correct="Die programmierbaren Shader-Stufen sind: Vertex Shader (pro Vertex), "
                          "Geometry Shader (kann Geometrie erzeugen/aendern, optional), "
                          "Tessellation Shaders (fuer Unterteilung, optional), und Fragment Shader (pro Fragment). "
                          "Rasterization ist eine feste Funktion (Fixed Function) und nicht programmierbar.",
            explain_wrong={
                "D": "Rasterization ist hardware-implementiert und nicht programmierbar."
            },
            topic="Computergrafik - Pipeline"
        ),

        # ============================================================
        # GEOMETRISCHE MODELLIERUNG
        # ============================================================
        Question(
            prompt="Was ist ein Vertex?",
            options={
                "A": "Ein Dreieck",
                "B": "Ein Eckpunkt mit Position und optionalen Attributen",
                "C": "Eine Textur",
                "D": "Ein Shader-Programm"
            },
            correct={"B"},
            explain_correct="Ein Vertex ist ein Eckpunkt im 3D-Raum. Er hat mindestens eine Position (x,y,z), "
                          "kann aber viele weitere Attribute haben: Normale (fuer Beleuchtung), Texturkoordinaten (UV), "
                          "Vertex-Farbe, Tangente (fuer Normal Mapping), Bone-Gewichte (fuer Skelett-Animation), etc. "
                          "Vertices werden zu Primitiven (meist Dreiecken) verbunden.",
            explain_wrong={
                "A": "Ein Dreieck besteht aus 3 Vertices.",
                "C": "Texturen sind Bilddaten.",
                "D": "Shader sind Programme."
            },
            topic="Computergrafik - Geometrie"
        ),

        Question(
            prompt="Was sind Normalen in der Computergrafik?",
            options={
                "A": "Standardwerte fuer Variablen",
                "B": "Vektoren die senkrecht zur Oberflaeche stehen",
                "C": "Durchschnittliche Farbwerte",
                "D": "Komprimierte Texturen"
            },
            correct={"B"},
            explain_correct="Normalen sind Einheitsvektoren (Laenge 1) die senkrecht zur Oberflaeche stehen. "
                          "Sie sind essentiell fuer Beleuchtungsberechnungen: Das Skalarprodukt zwischen Normale "
                          "und Lichtrichtung bestimmt die Helligkeit (Lambertsches Gesetz). "
                          "Face-Normalen gelten pro Dreieck, Vertex-Normalen pro Vertex (fuer glatte Schattierung).",
            explain_wrong={
                "A": "Das hat nichts mit Normalen in der Grafik zu tun.",
                "C": "Farben sind separate Attribute.",
                "D": "Texturen werden anders komprimiert."
            },
            topic="Computergrafik - Geometrie"
        ),

        Question(
            prompt="Was sind UV-Koordinaten?",
            options={
                "A": "Position eines Vertex im 3D-Raum",
                "B": "Koordinaten die angeben, welcher Teil einer Textur auf ein Polygon gemappt wird",
                "C": "Ultraviolett-Werte fuer Beleuchtung",
                "D": "Kameraposition"
            },
            correct={"B"},
            explain_correct="UV-Koordinaten (U=horizontal, V=vertikal) geben an, welcher Punkt einer 2D-Textur "
                          "auf welchen Punkt der 3D-Oberflaeche gemappt wird. Der Wertebereich ist meist 0-1, "
                          "kann aber auch ausserhalb liegen (dann wird die Textur gekachelt oder geklemmt). "
                          "UV-Mapping ist der Prozess der Zuweisung dieser Koordinaten zu den Vertices.",
            explain_wrong={
                "A": "Das sind die XYZ-Koordinaten.",
                "C": "UV steht nicht fuer Ultraviolett.",
                "D": "Die Kamera hat eigene Koordinaten."
            },
            topic="Computergrafik - Geometrie"
        ),

        Question(
            prompt="Was ist ein Mesh?",
            options={
                "A": "Eine Sammlung von Vertices und Faces die ein 3D-Objekt bilden",
                "B": "Ein einzelnes Dreieck",
                "C": "Eine Textur",
                "D": "Ein Beleuchtungsmodell"
            },
            correct={"A"},
            explain_correct="Ein Mesh (Polygonnetz) ist eine Sammlung von Vertices, Edges und Faces, "
                          "die zusammen die Oberflaeche eines 3D-Objekts beschreiben. Die Faces sind "
                          "meist Dreiecke (triangle mesh) oder Vierecke (quad mesh). Ein Mesh enthaelt "
                          "auch Zusatzinformationen wie Normalen, UV-Koordinaten und Materialdaten.",
            explain_wrong={
                "B": "Ein Dreieck ist ein einzelnes Face/Primitive.",
                "C": "Texturen sind Bilddaten.",
                "D": "Beleuchtung ist ein separates Konzept."
            },
            topic="Computergrafik - Geometrie"
        ),

        Question(
            prompt="Warum werden Dreiecke als Grundprimitiv verwendet?",
            options={
                "A": "Weil sie am schoensten aussehen",
                "B": "Weil sie immer planar sind und einfach zu rasterisieren",
                "C": "Weil Quads verboten sind",
                "D": "Aus historischen Gruenden"
            },
            correct={"B"},
            explain_correct="Dreiecke sind das einfachste Polygon und haben wichtige Eigenschaften: "
                          "Sie sind immer planar (liegen in einer Ebene), konvex, und haben keine Loecher. "
                          "Das macht sie einfach zu rasterisieren und mathematisch zu behandeln. "
                          "Quads und komplexere Polygone werden intern in Dreiecke zerlegt (Triangulation).",
            explain_wrong={
                "A": "Die Optik haengt nicht von der Primitiv-Wahl ab.",
                "C": "Quads werden oft verwendet, aber in Dreiecke zerlegt.",
                "D": "Es gibt handfeste technische Gruende."
            },
            topic="Computergrafik - Geometrie"
        ),

        Question(
            prompt="Was ist der Unterschied zwischen konvexen und konkaven Polygonen?",
            options={
                "A": "Konvex hat alle Innenwinkel < 180 Grad, konkav hat mindestens einen > 180 Grad",
                "B": "Konkav hat mehr Ecken",
                "C": "Konvex ist farbig, konkav ist grau",
                "D": "Es gibt keinen Unterschied"
            },
            correct={"A"},
            explain_correct="Ein konvexes Polygon hat alle Innenwinkel kleiner als 180 Grad - "
                          "eine Linie zwischen zwei Punkten im Polygon liegt immer vollstaendig im Polygon. "
                          "Konkave Polygone haben 'Einbuchtungen' (mindestens ein Winkel > 180 Grad). "
                          "Konvexe Polygone sind einfacher zu triangulieren und zu rasterisieren.",
            explain_wrong={
                "B": "Die Anzahl der Ecken ist unabhaengig von Konvexitaet.",
                "C": "Farbe hat nichts mit Konvexitaet zu tun.",
                "D": "Der Unterschied ist geometrisch relevant."
            },
            topic="Computergrafik - Geometrie"
        ),

        # ============================================================
        # TRANSFORMATIONEN
        # ============================================================
        Question(
            prompt="Welche grundlegenden Transformationen gibt es in der Computergrafik? (Mehrfachauswahl)",
            options={
                "A": "Translation (Verschiebung)",
                "B": "Rotation (Drehung)",
                "C": "Skalierung",
                "D": "Rasterisierung"
            },
            correct={"A", "B", "C"},
            explain_correct="Translation (Verschiebung um einen Vektor), Rotation (Drehung um eine Achse/Winkel), "
                          "und Skalierung (Vergroesserung/Verkleinerung) sind die drei grundlegenden affinen "
                          "Transformationen. Zusaetzlich gibt es Scherung (Shearing) und Spiegelung. "
                          "In homogenen Koordinaten koennen alle als 4x4-Matrizen dargestellt werden.",
            explain_wrong={
                "D": "Rasterisierung ist keine Transformation, sondern die Umwandlung von Vektorgrafik in Pixel."
            },
            topic="Computergrafik - Transformationen"
        ),

        Question(
            prompt="In welcher Reihenfolge werden Transformationen typischerweise angewendet?",
            options={
                "A": "Translation -> Rotation -> Skalierung",
                "B": "Skalierung -> Rotation -> Translation (SRT)",
                "C": "Rotation -> Translation -> Skalierung",
                "D": "Die Reihenfolge ist egal"
            },
            correct={"B"},
            explain_correct="Die SRT-Reihenfolge (Scale-Rotate-Translate) ist Standard: "
                          "Erst wird im lokalen Ursprung skaliert, dann rotiert, dann an die Zielposition verschoben. "
                          "Andere Reihenfolgen fuehren zu unerwarteten Ergebnissen, da Matrixmultiplikation "
                          "nicht kommutativ ist (A*B != B*A).",
            explain_wrong={
                "A": "Diese Reihenfolge fuehrt zu falschen Ergebnissen.",
                "C": "Diese Reihenfolge fuehrt zu falschen Ergebnissen.",
                "D": "Matrixmultiplikation ist nicht kommutativ - Reihenfolge ist sehr wichtig!"
            },
            topic="Computergrafik - Transformationen"
        ),

        Question(
            prompt="Was ist die Model-Matrix?",
            options={
                "A": "Transformiert von Weltkoordinaten zu Kamerakoordinaten",
                "B": "Transformiert von lokalen Objektkoordinaten zu Weltkoordinaten",
                "C": "Projiziert 3D auf 2D",
                "D": "Definiert die Bildschirmaufloesung"
            },
            correct={"B"},
            explain_correct="Die Model-Matrix (auch World Matrix) transformiert ein Objekt aus seinem lokalen "
                          "Koordinatensystem (Objekt bei Ursprung, Ausrichtung entlang Achsen) in das "
                          "Weltkoordinatensystem (Position, Rotation, Groesse in der Szene). "
                          "Sie enthaelt die SRT-Transformationen des Objekts.",
            explain_wrong={
                "A": "Das ist die View-Matrix.",
                "C": "Das ist die Projection-Matrix.",
                "D": "Das ist die Viewport-Transformation."
            },
            topic="Computergrafik - Transformationen"
        ),

        Question(
            prompt="Was macht die View-Matrix?",
            options={
                "A": "Platziert Objekte in der Welt",
                "B": "Transformiert die Welt aus Sicht der Kamera",
                "C": "Projiziert 3D auf 2D",
                "D": "Berechnet Beleuchtung"
            },
            correct={"B"},
            explain_correct="Die View-Matrix transformiert von Weltkoordinaten in Kamerakoordinaten "
                          "(Camera Space / Eye Space). Sie ist mathematisch die Inverse der Kamera-Transformation: "
                          "Statt die Kamera zu bewegen, wird die gesamte Welt so transformiert, dass die Kamera "
                          "im Ursprung sitzt und entlang der -Z-Achse schaut.",
            explain_wrong={
                "A": "Das ist die Model-Matrix.",
                "C": "Das ist die Projection-Matrix.",
                "D": "Beleuchtung wird separat berechnet."
            },
            topic="Computergrafik - Transformationen"
        ),

        Question(
            prompt="Was macht die Projection-Matrix?",
            options={
                "A": "Platziert Objekte in der Welt",
                "B": "Transformiert aus Kameraperspektive",
                "C": "Projiziert 3D-Koordinaten auf 2D (mit Perspektive oder orthografisch)",
                "D": "Faerbt die Pixel ein"
            },
            correct={"C"},
            explain_correct="Die Projection-Matrix transformiert von Kamerakoordinaten in Clip-Koordinaten "
                          "und definiert das Sichtvolumen (View Frustum). Bei perspektivischer Projektion "
                          "werden entfernte Objekte kleiner (Field of View, Aspect Ratio). "
                          "Bei orthografischer Projektion bleibt die Groesse konstant.",
            explain_wrong={
                "A": "Das ist die Model-Matrix.",
                "B": "Das ist die View-Matrix.",
                "D": "Das macht der Fragment Shader."
            },
            topic="Computergrafik - Transformationen"
        ),

        Question(
            prompt="Was ist der Unterschied zwischen perspektivischer und orthografischer Projektion?",
            options={
                "A": "Perspektivisch ist schneller",
                "B": "Bei perspektivisch werden entfernte Objekte kleiner",
                "C": "Orthografisch braucht mehr Speicher",
                "D": "Es gibt keinen Unterschied"
            },
            correct={"B"},
            explain_correct="Perspektivische Projektion simuliert das menschliche Sehen: Weiter entfernte Objekte "
                          "erscheinen kleiner (perspektivische Verkuerzung). Sie wird definiert durch "
                          "Field of View (Oeffnungswinkel), Aspect Ratio, Near Plane und Far Plane. "
                          "Orthografische Projektion erhielt parallele Linien und konstante Groessen - "
                          "verwendet fuer CAD, 2D-Spiele, oder isometrische Ansichten.",
            explain_wrong={
                "A": "Beide sind aehnlich schnell.",
                "C": "Der Speicherbedarf ist gleich.",
                "D": "Der visuelle Unterschied ist erheblich."
            },
            topic="Computergrafik - Transformationen"
        ),

        Question(
            prompt="Was ist das View Frustum?",
            options={
                "A": "Ein Wuerfel",
                "B": "Der pyramidenfoermige/quaderfoermige Sichtbereich der Kamera",
                "C": "Ein Texturtyp",
                "D": "Ein Shader"
            },
            correct={"B"},
            explain_correct="Das View Frustum ist das Sichtvolumen der Kamera - bei perspektivischer Projektion "
                          "eine abgestumpfte Pyramide (Kegelstumpf), bei orthografischer ein Quader. "
                          "Es wird durch 6 Ebenen begrenzt: Near Plane, Far Plane, und 4 Seiten (links, rechts, oben, unten). "
                          "Nur Geometrie innerhalb des Frustums wird gerendert.",
            explain_wrong={
                "A": "Ein Wuerfel entsteht nur bei orthografischer Projektion mit gleichem Aspect Ratio.",
                "C": "Das Frustum hat nichts mit Texturen zu tun.",
                "D": "Das Frustum ist kein Shader."
            },
            topic="Computergrafik - Transformationen"
        ),

        Question(
            prompt="Was ist die MVP-Matrix?",
            options={
                "A": "Eine spezielle Farbmatrix",
                "B": "Model * View * Projection - kombiniert alle Transformationen",
                "C": "Eine Texturmatrix",
                "D": "Eine Normalen-Matrix"
            },
            correct={"B"},
            explain_correct="Die MVP-Matrix ist das Produkt von Model, View und Projection Matrix. "
                          "Sie transformiert einen Vertex direkt von lokalen Objektkoordinaten "
                          "in Clip-Koordinaten (bereit fuer Rasterisierung). Oft wird sie einmal pro Frame "
                          "berechnet und an den Vertex Shader uebergeben, um Rechenaufwand zu sparen.",
            explain_wrong={
                "A": "Farben werden anders behandelt.",
                "C": "Texturkoordinaten haben eigene Matrizen.",
                "D": "Normalen brauchen spezielle Behandlung (Inverse Transpose)."
            },
            topic="Computergrafik - Transformationen"
        ),

        # ============================================================
        # LICHT UND FARBE
        # ============================================================
        Question(
            prompt="Was ist das RGB-Farbmodell?",
            options={
                "A": "Ein subtraktives Farbmodell",
                "B": "Ein additives Farbmodell mit Rot, Gruen, Blau",
                "C": "Ein Druckfarbmodell",
                "D": "Ein Modell fuer Schwarzweiss-Bilder"
            },
            correct={"B"},
            explain_correct="RGB ist ein additives Farbmodell: Rot, Gruen und Blau werden gemischt, "
                          "wobei volle Intensitaet aller drei Weiss ergibt und keine Farbe Schwarz. "
                          "Es wird fuer selbstleuchtende Displays (Monitore, TVs) verwendet. "
                          "Jeder Kanal hat typisch 8 Bit (0-255) oder normalisiert 0.0-1.0.",
            explain_wrong={
                "A": "RGB ist additiv, nicht subtraktiv.",
                "C": "Druck verwendet CMYK (subtraktiv).",
                "D": "RGB ist ein Vollfarben-Modell."
            },
            topic="Computergrafik - Licht und Farbe"
        ),

        Question(
            prompt="Was ist das RGBA-Farbmodell?",
            options={
                "A": "RGB ohne Rot",
                "B": "RGB plus Alpha-Kanal fuer Transparenz",
                "C": "Ein alternatives Farbmodell",
                "D": "RGB mit Reflektion"
            },
            correct={"B"},
            explain_correct="RGBA erweitert RGB um einen vierten Kanal: Alpha (A). Der Alpha-Kanal speichert "
                          "die Transparenz/Deckkraft des Pixels. A=1.0 (oder 255) bedeutet voellig undurchsichtig, "
                          "A=0.0 bedeutet voellig durchsichtig. RGBA ist essentiell fuer Compositing, "
                          "transparente Texturen, und Blending-Effekte.",
            explain_wrong={
                "A": "Alle Farbkanaele sind enthalten.",
                "C": "RGBA basiert direkt auf RGB.",
                "D": "Reflektion ist kein Teil des Farbmodells."
            },
            topic="Computergrafik - Licht und Farbe"
        ),

        Question(
            prompt="Was ist der Unterschied zwischen additivem und subtraktivem Farbmischen?",
            options={
                "A": "Additiv: Lichter ueberlagern sich (RGB). Subtraktiv: Farben absorbieren Licht (CMYK)",
                "B": "Additiv ist fuer Druck, subtraktiv fuer Bildschirme",
                "C": "Es gibt keinen Unterschied",
                "D": "Additiv erzeugt dunklere Farben"
            },
            correct={"A"},
            explain_correct="Additives Farbmischen (RGB): Lichtquellen ueberlagern sich, mehr Farbe = heller, "
                          "alle drei = Weiss. Verwendet bei Monitoren, die Licht emittieren. "
                          "Subtraktives Farbmischen (CMYK): Pigmente absorbieren Lichtanteile, "
                          "mehr Farbe = dunkler, alle = Schwarz. Verwendet bei Druck auf Papier.",
            explain_wrong={
                "B": "Es ist genau umgekehrt.",
                "C": "Der Unterschied ist fundamental.",
                "D": "Additiv erzeugt hellere Farben."
            },
            topic="Computergrafik - Licht und Farbe"
        ),

        Question(
            prompt="Was beschreibt der HSV/HSB-Farbraum? (Mehrfachauswahl)",
            options={
                "A": "Hue (Farbton)",
                "B": "Saturation (Saettigung)",
                "C": "Value/Brightness (Helligkeit)",
            },
            correct={"A", "B", "C"},
            explain_correct="HSV (Hue, Saturation, Value) bzw. HSB (Hue, Saturation, Brightness) beschreibt Farben "
                          "intuitiver als RGB: Hue ist der Farbton (0-360 Grad auf dem Farbkreis), "
                          "Saturation die Saettigung (0=grau bis 1=volle Farbe), "
                          "Value/Brightness die Helligkeit (0=schwarz bis 1=hell). Ideal fuer Farbauswahl-Tools.",
            explain_wrong={},
            topic="Computergrafik - Licht und Farbe"
        ),

        Question(
            prompt="Was ist der Gammakorrektur (Gamma Correction)?",
            options={
                "A": "Eine Farbfiltertechnik",
                "B": "Anpassung der Helligkeitskurve an die nichtlineare Wahrnehmung/Displays",
                "C": "Eine Texturkompression",
                "D": "Ein Beleuchtungsmodell"
            },
            correct={"B"},
            explain_correct="Gammakorrektur kompensiert die nichtlineare Beziehung zwischen elektrischem Signal "
                          "und Leuchtdichte bei Displays. Auch das menschliche Auge nimmt Helligkeit nichtlinear wahr. "
                          "sRGB (Standard fuer Monitore) hat Gamma ≈ 2.2. Fuer korrekte Berechnungen muss man "
                          "in linearen Farbraum konvertieren, rechnen, und dann zurueck zu Gamma.",
            explain_wrong={
                "A": "Gamma ist keine Filtertechnik.",
                "C": "Kompression ist ein anderes Thema.",
                "D": "Gamma beeinflusst die Darstellung, nicht das Beleuchtungsmodell."
            },
            topic="Computergrafik - Licht und Farbe"
        ),

        Question(
            prompt="Was ist der Unterschied zwischen sRGB und linearem Farbraum?",
            options={
                "A": "sRGB hat Gammakorrektur angewendet, linear nicht",
                "B": "Linear hat mehr Farben",
                "C": "sRGB ist veraltet",
                "D": "Es gibt keinen Unterschied"
            },
            correct={"A"},
            explain_correct="sRGB ist der Standard-Farbraum mit eingebauter Gammakorrektur (~2.2). "
                          "Bilder und Texturen sind meist in sRGB kodiert. Fuer physikalisch korrekte "
                          "Beleuchtungsberechnungen muss in linearen Farbraum konvertiert werden "
                          "(Entfernung des Gammas), dann gerechnet, und am Ende zurueck zu sRGB fuer die Ausgabe.",
            explain_wrong={
                "B": "Beide koennen gleich viele Farben darstellen.",
                "C": "sRGB ist der aktuelle Standard.",
                "D": "Der Unterschied ist wichtig fuer korrekte Berechnungen."
            },
            topic="Computergrafik - Licht und Farbe"
        ),

        Question(
            prompt="Was beschreibt die Farbtiefe (Color Depth / Bit Depth)?",
            options={
                "A": "Die Anzahl der darstellbaren Farben pro Pixel",
                "B": "Die Bildaufloesung",
                "C": "Die Helligkeit",
                "D": "Die Texturgroesse"
            },
            correct={"A"},
            explain_correct="Die Farbtiefe gibt an, wie viele Bits pro Pixel (oder pro Kanal) verwendet werden. "
                          "8 Bit pro Kanal (24 Bit total bei RGB) ergibt 16.7 Millionen Farben. "
                          "10 oder 12 Bit pro Kanal (HDR) ergibt feinere Abstufungen und weniger Banding. "
                          "32 Bit Float pro Kanal wird in professionellen Anwendungen verwendet.",
            explain_wrong={
                "B": "Die Aufloesung ist die Pixelanzahl, nicht die Farbtiefe.",
                "C": "Helligkeit ist ein Aspekt der Farbe, nicht der Farbtiefe.",
                "D": "Texturgroesse ist separat."
            },
            topic="Computergrafik - Licht und Farbe"
        ),

        Question(
            prompt="Welche Eigenschaften hat Licht in der Computergrafik? (Mehrfachauswahl)",
            options={
                "A": "Farbe/Spektrum",
                "B": "Intensitaet",
                "C": "Richtung",
            },
            correct={"A", "B", "C"},
            explain_correct="Licht in der Computergrafik wird beschrieben durch: "
                          "Farbe (RGB oder Spektrum), Intensitaet (wie hell), Richtung (woher es kommt), "
                          "Position (bei Punktlicht), und Abnahme mit Entfernung (Attenuation). "
                          "Verschiedene Lichtquellen (Directional, Point, Spot) unterscheiden sich in diesen Eigenschaften.",
            explain_wrong={},
            topic="Computergrafik - Licht und Farbe"
        ),

        Question(
            prompt="Welche Lichtquellen-Typen gibt es in der Computergrafik? (Mehrfachauswahl)",
            options={
                "A": "Directional Light (Sonnenlicht)",
                "B": "Point Light (Punktlicht)",
                "C": "Spot Light (Scheinwerfer)",
                "D": "Ambient Light (Umgebungslicht)"
            },
            correct={"A", "B", "C", "D"},
            explain_correct="Directional Light: Parallele Strahlen aus unendlicher Entfernung (Sonne). "
                          "Point Light: Strahlt in alle Richtungen von einem Punkt (Gluehbirne). "
                          "Spot Light: Kegel aus einem Punkt (Taschenlampe). "
                          "Ambient Light: Konstantes Licht ueberall, simuliert indirektes Licht. "
                          "Area Light: Licht von einer Flaeche (realistisch, aber aufwendig).",
            explain_wrong={},
            topic="Computergrafik - Licht und Farbe"
        ),

        Question(
            prompt="Was ist Attenuation (Lichtabnahme)?",
            options={
                "A": "Die Farbaenderung mit Entfernung",
                "B": "Die Intensitaetsabnahme des Lichts mit zunehmender Entfernung",
                "C": "Die Richtungsaenderung des Lichts",
                "D": "Die Texturverzerrung"
            },
            correct={"B"},
            explain_correct="Attenuation beschreibt, wie die Lichtintensitaet mit der Entfernung abnimmt. "
                          "Physikalisch korrekt waere 1/d² (inverse square law), aber in Spielen werden oft "
                          "kuenstliche Formeln verwendet: 1/(1 + c1*d + c2*d²) mit einstellbaren Konstanten. "
                          "Directional Lights haben keine Attenuation (unendlich weit entfernt).",
            explain_wrong={
                "A": "Die Farbe bleibt gleich, nur die Intensitaet nimmt ab.",
                "C": "Die Richtung aendert sich nicht.",
                "D": "Texturen sind unabhaengig von Attenuation."
            },
            topic="Computergrafik - Licht und Farbe"
        ),

        # ============================================================
        # BELEUCHTUNGSMODELLE
        # ============================================================
        Question(
            prompt="Welche Komponenten hat das Phong-Beleuchtungsmodell? (Mehrfachauswahl)",
            options={
                "A": "Ambient (Umgebungslicht)",
                "B": "Diffuse (gestreutes Licht)",
                "C": "Specular (Glanzlicht)",
            },
            correct={"A", "B", "C"},
            explain_correct="Das Phong-Beleuchtungsmodell besteht aus drei Komponenten: "
                          "Ambient = konstantes Umgebungslicht, simuliert indirektes Licht. "
                          "Diffuse = gestreutes Licht abhaengig vom Winkel Licht-Normale (Lambert). "
                          "Specular = Glanzpunkte abhaengig vom Winkel Reflexion-Betrachter. "
                          "Endergebnis = ka*Ia + kd*Id*max(0,N·L) + ks*Is*max(0,R·V)^n",
            explain_wrong={},
            topic="Computergrafik - Beleuchtung"
        ),

        Question(
            prompt="Was beschreibt das Lambertsche Gesetz?",
            options={
                "A": "Die Reflexion an glatten Oberflaechen",
                "B": "Die diffuse Reflexion: Intensitaet ~ cos(Winkel zwischen Normale und Licht)",
                "C": "Die Lichtbrechung",
                "D": "Die Farbmischung"
            },
            correct={"B"},
            explain_correct="Das Lambertsche Kosinusgesetz beschreibt ideale diffuse Reflexion: "
                          "Die reflektierte Intensitaet ist proportional zum Kosinus des Winkels zwischen "
                          "Oberflaechennormale und Lichtrichtung. Mathematisch: I_diffuse = k_d * I_light * max(0, N·L). "
                          "Dadurch werden Flaechen, die dem Licht zugewandt sind, heller.",
            explain_wrong={
                "A": "Glatte Reflexion wird durch Specular beschrieben.",
                "C": "Lichtbrechung ist ein anderes Phaenomen.",
                "D": "Farbmischung ist ein separates Thema."
            },
            topic="Computergrafik - Beleuchtung"
        ),

        Question(
            prompt="Was ist der Specular-Exponent (Shininess) im Phong-Modell?",
            options={
                "A": "Die Farbe des Glanzlichts",
                "B": "Steuert die Groesse/Schaerfe des Glanzpunkts",
                "C": "Die Position der Lichtquelle",
                "D": "Die Texturaufloesung"
            },
            correct={"B"},
            explain_correct="Der Specular-Exponent (n oder shininess) steuert die Groesse des Glanzpunkts: "
                          "Ein niedriger Wert (z.B. 2) ergibt einen grossen, weichen Glanz (matte Oberflaeche). "
                          "Ein hoher Wert (z.B. 256) ergibt einen kleinen, scharfen Glanzpunkt (polierte Oberflaeche). "
                          "Die Formel ist (R·V)^n - der Exponent komprimiert den Winkelbereich.",
            explain_wrong={
                "A": "Die Farbe wird durch k_s und I_s bestimmt.",
                "C": "Die Lichtposition ist separat.",
                "D": "Texturen sind unabhaengig."
            },
            topic="Computergrafik - Beleuchtung"
        ),

        Question(
            prompt="Was ist der Unterschied zwischen Gouraud und Phong Shading?",
            options={
                "A": "Gouraud interpoliert Farben pro Vertex, Phong interpoliert Normalen pro Pixel",
                "B": "Phong ist aelter als Gouraud",
                "C": "Gouraud ist fotorealistisch, Phong nicht",
                "D": "Es gibt keinen Unterschied"
            },
            correct={"A"},
            explain_correct="Gouraud-Shading (1971): Beleuchtung wird pro Vertex berechnet, "
                          "die resultierenden Farben werden ueber das Dreieck interpoliert. Schnell, aber "
                          "Glanzpunkte koennen verloren gehen. "
                          "Phong-Shading (1975): Normalen werden pro Pixel interpoliert, Beleuchtung pro Pixel berechnet. "
                          "Bessere Qualitaet (scharfe Glanzpunkte), aber aufwendiger.",
            explain_wrong={
                "B": "Gouraud kam vor Phong (1971 vs 1975).",
                "C": "Phong ist genauer als Gouraud.",
                "D": "Der Qualitaetsunterschied ist sichtbar."
            },
            topic="Computergrafik - Beleuchtung"
        ),

        Question(
            prompt="Was ist Flat Shading?",
            options={
                "A": "Jedes Dreieck hat eine einheitliche Farbe basierend auf seiner Normale",
                "B": "Farben werden ueber das Dreieck interpoliert",
                "C": "Normalen werden pro Pixel interpoliert",
                "D": "Eine Texturmethode"
            },
            correct={"A"},
            explain_correct="Flat Shading ist die einfachste Schattierungsmethode: Jedes Dreieck wird "
                          "mit einer einzigen Farbe gefuellt, berechnet aus der Face-Normale. "
                          "Das Ergebnis sieht facettiert aus (man sieht die einzelnen Dreiecke). "
                          "Schnell, aber fuer organische Formen ungeeignet.",
            explain_wrong={
                "B": "Das ist Gouraud-Shading.",
                "C": "Das ist Phong-Shading.",
                "D": "Flat Shading ist eine Beleuchtungsmethode."
            },
            topic="Computergrafik - Beleuchtung"
        ),

        Question(
            prompt="Was ist PBR (Physically Based Rendering)?",
            options={
                "A": "Eine Texturart",
                "B": "Ein Beleuchtungsmodell das physikalische Gesetze simuliert",
                "C": "Eine Kompressionsart",
                "D": "Ein Dateiformat"
            },
            correct={"B"},
            explain_correct="PBR ist ein modernes Beleuchtungsmodell, das physikalische Gesetze beachtet: "
                          "Energieerhaltung (reflektiertes Licht <= einfallendes Licht), "
                          "Fresnel-Effekt (mehr Reflexion bei flachen Winkeln), "
                          "Mikrofacetten-Theorie (rauhe Oberflaechen). Parameter sind meist: "
                          "Albedo/Base Color, Metallic, Roughness, Normal Map, Ambient Occlusion.",
            explain_wrong={
                "A": "PBR verwendet Texturen, ist aber selbst ein Beleuchtungsmodell.",
                "C": "Kompression ist ein anderes Thema.",
                "D": "PBR ist kein Dateiformat."
            },
            topic="Computergrafik - Beleuchtung"
        ),

        Question(
            prompt="Was ist der Fresnel-Effekt?",
            options={
                "A": "Ein Farbfilter",
                "B": "Staerkere Reflexion bei flachen Betrachtungswinkeln",
                "C": "Ein Texturtyp",
                "D": "Eine Schattenart"
            },
            correct={"B"},
            explain_correct="Der Fresnel-Effekt beschreibt, dass Oberflaechen bei flachen Betrachtungswinkeln "
                          "(Blickrichtung fast parallel zur Oberflaeche) mehr reflektieren als bei steilen Winkeln. "
                          "Ein See erscheint bei flachem Blick spiegelnd, bei steilem Blick durchsichtig. "
                          "PBR-Shader nutzen die Fresnel-Gleichungen fuer realistische Reflexionen.",
            explain_wrong={
                "A": "Fresnel ist kein Filter.",
                "C": "Fresnel ist ein physikalischer Effekt.",
                "D": "Fresnel betrifft Reflexion, nicht Schatten."
            },
            topic="Computergrafik - Beleuchtung"
        ),

        # ============================================================
        # GLOBALE BELEUCHTUNG
        # ============================================================
        Question(
            prompt="Was ist der Unterschied zwischen lokaler und globaler Beleuchtung?",
            options={
                "A": "Lokal beruecksichtigt nur direkte Beleuchtung, global auch indirekte (Reflexionen, Lichtbounces)",
                "B": "Global ist schneller",
                "C": "Lokal ist realistischer",
                "D": "Es gibt keinen Unterschied"
            },
            correct={"A"},
            explain_correct="Lokale Beleuchtung (z.B. Phong) berechnet nur direkte Beleuchtung - Licht von "
                          "der Quelle direkt zur Oberflaeche. Globale Beleuchtung beruecksichtigt auch "
                          "indirekte Beleuchtung: Licht das von anderen Objekten reflektiert wird, "
                          "durch Materialien transmittiert wird, etc. Ergebnis ist realistischer, aber aufwendiger.",
            explain_wrong={
                "B": "Globale Beleuchtung ist deutlich aufwendiger.",
                "C": "Globale Beleuchtung ist realistischer.",
                "D": "Der Unterschied ist sehr gross."
            },
            topic="Computergrafik - Globale Beleuchtung"
        ),

        Question(
            prompt="Was ist Ray Tracing?",
            options={
                "A": "Ein Texturfilter",
                "B": "Simulation von Lichtstrahlen durch die Szene fuer realistische Beleuchtung",
                "C": "Ein Kompressionsverfahren",
                "D": "Eine Animationstechnik"
            },
            correct={"B"},
            explain_correct="Ray Tracing verfolgt Lichtstrahlen (meist von der Kamera in die Szene - Backwards Ray Tracing). "
                          "Fuer jeden Pixel wird ein Strahl geschickt, Schnittpunkte mit Geometrie berechnet, "
                          "und von dort weitere Strahlen (Shadow, Reflection, Refraction) ausgesendet. "
                          "Ergebnis: Realistische Reflexionen, Schatten, Brechungen. Modern: Real-time Ray Tracing mit RTX.",
            explain_wrong={
                "A": "Ray Tracing ist kein Texturfilter.",
                "C": "Kompression ist ein anderes Thema.",
                "D": "Ray Tracing betrifft Rendering, nicht Animation."
            },
            topic="Computergrafik - Globale Beleuchtung"
        ),

        Question(
            prompt="Was ist Path Tracing?",
            options={
                "A": "Navigation in Spielen",
                "B": "Monte-Carlo-Methode zur Berechnung globaler Beleuchtung durch zufaellige Strahlenverfolgung",
                "C": "Ein Texturtyp",
                "D": "Eine Animationskurve"
            },
            correct={"B"},
            explain_correct="Path Tracing ist eine fortgeschrittene Ray Tracing Variante, die Monte-Carlo-Integration "
                          "verwendet. Fuer jeden Pixel werden viele zufaellige Pfade durch die Szene verfolgt, "
                          "die an Oberflaechen abprallen. Durch Mittelung ueber viele Samples konvergiert das "
                          "Ergebnis zur korrekten globalen Beleuchtung. Sehr realistisch, aber rechenintensiv und rauschig.",
            explain_wrong={
                "A": "Pathfinding ist ein anderes Thema.",
                "C": "Path Tracing erzeugt keine Texturen.",
                "D": "Animation ist ein anderes Thema."
            },
            topic="Computergrafik - Globale Beleuchtung"
        ),

        Question(
            prompt="Was ist Ambient Occlusion?",
            options={
                "A": "Ein Farbmodell",
                "B": "Abdunkelung in Ecken und engen Bereichen wo weniger Umgebungslicht hinkommt",
                "C": "Eine Texturart",
                "D": "Ein Shader-Typ"
            },
            correct={"B"},
            explain_correct="Ambient Occlusion (AO) simuliert, wie viel Umgebungslicht an jeden Punkt gelangt. "
                          "In Ecken, Ritzen und engen Bereichen wird weniger Licht erreichen -> diese werden dunkler. "
                          "AO wird oft als Textur vorberechnet (Baked AO) oder in Echtzeit als Screen Space AO (SSAO) "
                          "berechnet. Es fuegt Tiefe und Realismus hinzu, ist aber eine Approximation.",
            explain_wrong={
                "A": "AO ist kein Farbmodell.",
                "C": "AO kann als Textur gespeichert werden, ist aber ein Beleuchtungseffekt.",
                "D": "AO ist ein Effekt, kein Shader-Typ."
            },
            topic="Computergrafik - Globale Beleuchtung"
        ),

        Question(
            prompt="Was ist Radiosity?",
            options={
                "A": "Eine Texturmethode",
                "B": "Berechnung diffuser Interreflexionen zwischen Flaechen",
                "C": "Ein Kompressionsverfahren",
                "D": "Eine Animationstechnik"
            },
            correct={"B"},
            explain_correct="Radiosity berechnet den Lichtaustausch zwischen diffusen Oberflaechen. "
                          "Anders als Ray Tracing ist es ansichtsunabhaengig - die Loesung kann einmal berechnet "
                          "und dann aus beliebigen Blickwinkeln betrachtet werden (gut fuer statische Szenen). "
                          "Es erzeugt weiche Schatten und Color Bleeding (Farbuebertraege zwischen Oberflaechen).",
            explain_wrong={
                "A": "Radiosity erzeugt Lightmaps, ist aber selbst keine Texturmethode.",
                "C": "Kompression ist ein anderes Thema.",
                "D": "Radiosity betrifft Beleuchtung."
            },
            topic="Computergrafik - Globale Beleuchtung"
        ),

        # ============================================================
        # TEXTURE MAPPING
        # ============================================================
        Question(
            prompt="Was ist Texture Mapping?",
            options={
                "A": "Das Auftragen von 2D-Bildern auf 3D-Oberflaechen",
                "B": "Das Erstellen von 3D-Modellen",
                "C": "Die Animation von Objekten",
                "D": "Die Beleuchtungsberechnung"
            },
            correct={"A"},
            explain_correct="Texture Mapping ist die Technik, 2D-Bilder (Texturen) auf 3D-Oberflaechen zu projizieren. "
                          "UV-Koordinaten an jedem Vertex geben an, welcher Teil der Textur dort angezeigt wird. "
                          "Zwischen Vertices werden die UVs interpoliert. So koennen komplexe Details "
                          "(Holzmaserung, Ziegelmauer) ohne zusaetzliche Geometrie dargestellt werden.",
            explain_wrong={
                "B": "Modellierung ist ein anderer Prozess.",
                "C": "Animation ist ein anderer Bereich.",
                "D": "Beleuchtung verwendet Texturen, ist aber nicht Mapping selbst."
            },
            topic="Computergrafik - Texturen"
        ),

        Question(
            prompt="Was ist Texture Filtering?",
            options={
                "A": "Das Entfernen von Texturen",
                "B": "Die Interpolation von Texelwerten beim Sampling",
                "C": "Das Komprimieren von Texturen",
                "D": "Das Laden von Texturen"
            },
            correct={"B"},
            explain_correct="Texture Filtering bestimmt, wie Texelwerte ermittelt werden, wenn die Texturkoordinaten "
                          "nicht exakt auf Texel-Zentren fallen. Nearest-Neighbor: naechster Texel (pixelig). "
                          "Bilinear: gewichteter Durchschnitt der 4 naechsten Texel. "
                          "Trilinear: Bilinear + Interpolation zwischen Mipmap-Stufen. "
                          "Anisotropic: beruecksichtigt Blickwinkel auf die Textur.",
            explain_wrong={
                "A": "Filtering entfernt keine Texturen.",
                "C": "Kompression ist ein separater Prozess.",
                "D": "Laden ist vor dem Filtering."
            },
            topic="Computergrafik - Texturen"
        ),

        Question(
            prompt="Was sind Mipmaps?",
            options={
                "A": "Kleine Vorschaubilder",
                "B": "Vorberechnete verkleinerte Versionen einer Textur fuer verschiedene Distanzen",
                "C": "Komprimierte Texturen",
                "D": "Animierte Texturen"
            },
            correct={"B"},
            explain_correct="Mipmaps sind vorberechnete verkleinerte Versionen einer Textur (je halb so gross: "
                          "Original, 1/2, 1/4, 1/8... bis 1x1). Je nach Entfernung/Groesse auf dem Bildschirm "
                          "wird die passende Stufe verwendet. Dies reduziert Aliasing (Flimmern bei kleinen "
                          "Texturen) und verbessert die Cache-Effizienz. Kostet nur 33% mehr Speicher.",
            explain_wrong={
                "A": "Mipmaps dienen dem Rendering, nicht der Vorschau.",
                "C": "Kompression ist unabhaengig von Mipmaps.",
                "D": "Animation hat nichts mit Mipmaps zu tun."
            },
            topic="Computergrafik - Texturen"
        ),

        Question(
            prompt="Was ist Normal Mapping?",
            options={
                "A": "Standard-Texturmapping",
                "B": "Simulation von Oberflaechendetails durch Normalen-Texturen",
                "C": "Ein Kompressionsverfahren",
                "D": "Eine Animationstechnik"
            },
            correct={"B"},
            explain_correct="Normal Mapping verwendet eine spezielle Textur (Normal Map), die pro Texel eine "
                          "Normale speichert (als RGB kodiert). Diese ersetzt/modifiziert die geometrische Normale "
                          "bei der Beleuchtungsberechnung. So koennen feine Oberflaechendetails (Rillen, Poren, Nieten) "
                          "ohne zusaetzliche Geometrie dargestellt werden. Die Silhouette bleibt aber glatt.",
            explain_wrong={
                "A": "Normal Mapping ist eine fortgeschrittene Technik.",
                "C": "Kompression ist ein anderes Thema.",
                "D": "Animation ist ein anderes Thema."
            },
            topic="Computergrafik - Texturen"
        ),

        Question(
            prompt="Was ist Parallax Mapping / Displacement Mapping?",
            options={
                "A": "Standard-Texturmapping",
                "B": "Techniken zur Simulation von Tiefe/Geometrie durch Texturen",
                "C": "Ein Soundeffekt",
                "D": "Eine Netzwerkprotokoll"
            },
            correct={"B"},
            explain_correct="Parallax Mapping verschiebt Texturkoordinaten basierend auf einer Height Map "
                          "und dem Blickwinkel - erzeugt Illusion von Tiefe ohne Geometrie. "
                          "Displacement Mapping geht weiter und verschiebt tatsaechlich die Geometrie "
                          "(meist im Tessellation Shader). Ergebnis: Realistische 3D-Oberflaechen "
                          "mit korrekten Silhouetten und Selbstschattierung.",
            explain_wrong={
                "A": "Diese Techniken sind fortgeschrittener.",
                "C": "Hat nichts mit Sound zu tun.",
                "D": "Hat nichts mit Netzwerk zu tun."
            },
            topic="Computergrafik - Texturen"
        ),

        Question(
            prompt="Was ist Anisotropic Filtering?",
            options={
                "A": "Ein Kompressionsverfahren",
                "B": "Texturfilterung die den Blickwinkel beruecksichtigt",
                "C": "Eine Beleuchtungsmethode",
                "D": "Ein Shader-Typ"
            },
            correct={"B"},
            explain_correct="Anisotropic Filtering (AF) ist eine verbesserte Texturfilterung, die den Blickwinkel "
                          "auf die texturierte Oberflaeche beruecksichtigt. Bei flachen Winkeln (z.B. Strasse in die Ferne) "
                          "sampelt es mehr Texel in Richtung der Verzerrung. Ergebnis: Scharfe Texturen auch bei "
                          "schraegen Winkeln, ohne uebertriebene Unschaerfe. Einstellbar: 2x, 4x, 8x, 16x AF.",
            explain_wrong={
                "A": "AF ist keine Kompression.",
                "C": "AF ist Texturfilterung, nicht Beleuchtung.",
                "D": "AF ist kein Shader-Typ, sondern eine Filtereinstellung."
            },
            topic="Computergrafik - Texturen"
        ),

        # ============================================================
        # SHADER
        # ============================================================
        Question(
            prompt="Was ist ein Shader? (Mehrfachauswahl)",
            options={
                "A": "Ein Programm das auf der GPU laeuft",
                "B": "Berechnet visuelle Eigenschaften wie Farbe, Position, Beleuchtung",
                "C": "Wird fuer jeden Vertex oder jedes Fragment ausgefuehrt",
            },
            correct={"A", "B", "C"},
            explain_correct="Ein Shader ist ein Programm, das auf der GPU laeuft und einen Teil der Rendering-Pipeline "
                          "steuert. Vertex Shader transformieren Vertices, Fragment Shader berechnen Pixelfarben. "
                          "Shader werden massiv parallel ausgefuehrt - die gleiche Anweisung fuer viele Vertices/Fragmente "
                          "gleichzeitig. Geschrieben in GLSL (OpenGL), HLSL (DirectX), oder anderen Shadersprachen.",
            explain_wrong={},
            topic="Computergrafik - Shader"
        ),

        Question(
            prompt="Welche Shader-Typen gibt es in der modernen Grafik-Pipeline? (Mehrfachauswahl)",
            options={
                "A": "Vertex Shader",
                "B": "Fragment Shader (Pixel Shader)",
                "C": "Geometry Shader",
                "D": "Compute Shader"
            },
            correct={"A", "B", "C", "D"},
            explain_correct="Moderne GPUs unterstuetzen verschiedene Shader-Stufen: "
                          "Vertex Shader (pro Vertex, Pflicht), Fragment/Pixel Shader (pro Fragment, Pflicht), "
                          "Geometry Shader (kann Geometrie erzeugen, optional), "
                          "Tessellation Shaders (Hull + Domain, fuer Unterteilung, optional), "
                          "Compute Shader (allgemeine Berechnungen, nicht Teil der Rendering-Pipeline).",
            explain_wrong={},
            topic="Computergrafik - Shader"
        ),

        Question(
            prompt="Was ist GLSL?",
            options={
                "A": "Eine Programmiersprache fuer OpenGL-Shader",
                "B": "Ein Bildformat",
                "C": "Ein 3D-Modell-Format",
                "D": "Eine Texturkompression"
            },
            correct={"A"},
            explain_correct="GLSL (OpenGL Shading Language) ist die Shader-Programmiersprache fuer OpenGL/OpenGL ES. "
                          "Sie hat eine C-aehnliche Syntax mit speziellen Typen fuer Vektoren (vec2, vec3, vec4), "
                          "Matrizen (mat3, mat4), und Texturen (sampler2D). Shader werden zur Laufzeit kompiliert. "
                          "Alternativen: HLSL (DirectX), Metal Shading Language (Apple), SPIR-V (Vulkan).",
            explain_wrong={
                "B": "GLSL ist kein Bildformat.",
                "C": "GLSL ist keine Modell-Datei.",
                "D": "GLSL ist keine Kompression."
            },
            topic="Computergrafik - Shader"
        ),

        Question(
            prompt="Was ist ein Compute Shader?",
            options={
                "A": "Ein Shader fuer Vertex-Transformation",
                "B": "Ein Shader fuer allgemeine Berechnungen (GPGPU), nicht Teil der Rendering-Pipeline",
                "C": "Ein Shader fuer Pixelfarben",
                "D": "Ein Shader fuer Audio"
            },
            correct={"B"},
            explain_correct="Compute Shader sind fuer allgemeine Berechnungen auf der GPU (GPGPU - General Purpose GPU). "
                          "Sie sind nicht Teil der Rendering-Pipeline und haben keine festen Ein-/Ausgaben. "
                          "Verwendet fuer: Partikel-Physik, Post-Processing, Simulation, Machine Learning, etc. "
                          "Sie arbeiten in Arbeitsgruppen (Work Groups) und koennen auf Texturen und Buffer zugreifen.",
            explain_wrong={
                "A": "Vertex-Transformation macht der Vertex Shader.",
                "C": "Pixelfarben berechnet der Fragment Shader.",
                "D": "Audio-Verarbeitung laeuft meist auf der CPU."
            },
            topic="Computergrafik - Shader"
        ),

        Question(
            prompt="Was sind Uniforms in Shadern?",
            options={
                "A": "Variablen die fuer alle Vertices/Fragmente gleich sind (von CPU gesetzt)",
                "B": "Variablen die pro Vertex unterschiedlich sind",
                "C": "Ausgabewerte des Shaders",
                "D": "Texturkoordinaten"
            },
            correct={"A"},
            explain_correct="Uniforms sind Shader-Variablen, die von der CPU gesetzt werden und fuer alle "
                          "Vertices/Fragmente im Draw Call gleich sind. Typische Uniforms: MVP-Matrix, "
                          "Lichtpositionen, Materialeigenschaften, Zeit, Textur-Sampler. "
                          "Sie werden einmal pro Frame/Objekt aktualisiert, nicht pro Vertex.",
            explain_wrong={
                "B": "Pro-Vertex-Variablen sind Vertex Attributes.",
                "C": "Ausgaben heissen Outputs oder varying/out.",
                "D": "Texturkoordinaten sind Vertex Attributes oder interpoliert."
            },
            topic="Computergrafik - Shader"
        ),

        Question(
            prompt="Was ist ein Varying (oder in/out zwischen Shader-Stufen)?",
            options={
                "A": "Eine Konstante",
                "B": "Werte die vom Vertex Shader zum Fragment Shader interpoliert werden",
                "C": "Eine Textur",
                "D": "Eine Matrix"
            },
            correct={"B"},
            explain_correct="Varying (in GLSL 'out' vom Vertex Shader, 'in' im Fragment Shader) sind Werte, "
                          "die vom Vertex Shader berechnet und per Rasterisierung ueber das Dreieck "
                          "zum Fragment Shader interpoliert werden. Typische Varyings: Texturkoordinaten, "
                          "Normalen, Positionen, Farben. Die Interpolation ist standardmaessig perspektivisch korrekt.",
            explain_wrong={
                "A": "Varyings aendern sich pro Fragment.",
                "C": "Texturen werden ueber Sampler zugegriffen.",
                "D": "Matrizen sind meist Uniforms."
            },
            topic="Computergrafik - Shader"
        ),

        # ============================================================
        # CLIPPING & CULLING
        # ============================================================
        Question(
            prompt="Was ist Backface Culling?",
            options={
                "A": "Das Entfernen von Dreiecken die von der Kamera weg zeigen",
                "B": "Das Entfernen aller Dreiecke",
                "C": "Das Sortieren von Dreiecken",
                "D": "Das Faerben der Rueckseite"
            },
            correct={"A"},
            explain_correct="Backface Culling entfernt Dreiecke, deren Normale von der Kamera weg zeigt "
                          "(Rueckseite). Bei geschlossenen Objekten ist die Rueckseite nie sichtbar. "
                          "Die Vorderseite wird durch die Vertex-Reihenfolge bestimmt (Counter-Clockwise = Front). "
                          "Spart ca. 50% Rendering-Arbeit. Kann deaktiviert werden fuer transparente oder "
                          "doppelseitige Objekte.",
            explain_wrong={
                "B": "Nur Rueckseiten werden entfernt.",
                "C": "Sortieren ist ein anderer Prozess.",
                "D": "Die Rueckseite wird verworfen, nicht gefaerbt."
            },
            topic="Computergrafik - Optimierung"
        ),

        Question(
            prompt="Was ist Frustum Culling?",
            options={
                "A": "Das Entfernen von Objekten ausserhalb des Sichtbereichs der Kamera",
                "B": "Das Entfernen von Texturen",
                "C": "Das Entfernen von Lichtquellen",
                "D": "Das Entfernen von Shadern"
            },
            correct={"A"},
            explain_correct="Frustum Culling entfernt ganze Objekte, die vollstaendig ausserhalb des "
                          "View Frustums (Sichtpyramide der Kamera) liegen, bevor sie an die GPU gesendet werden. "
                          "Pruefung erfolgt mit Bounding Volumes (Bounding Box, Bounding Sphere). "
                          "Wichtige CPU-seitige Optimierung, besonders bei grossen Szenen.",
            explain_wrong={
                "B": "Texturen werden nicht durch Culling entfernt.",
                "C": "Lichtquellen werden anders behandelt.",
                "D": "Shader werden nicht 'ge-culled'."
            },
            topic="Computergrafik - Optimierung"
        ),

        Question(
            prompt="Was ist Clipping?",
            options={
                "A": "Das Abschneiden von Geometrie an den Frustum-Grenzen",
                "B": "Das Komprimieren von Texturen",
                "C": "Das Faerben von Pixeln",
                "D": "Das Laden von Modellen"
            },
            correct={"A"},
            explain_correct="Clipping schneidet Primitive (Dreiecke) an den Grenzen des View Frustums ab. "
                          "Ein Dreieck das teilweise ausserhalb liegt, wird an der Near/Far Plane oder "
                          "den Seitenflaechen abgeschnitten und kann in mehrere kleinere Dreiecke zerlegt werden. "
                          "Passiert nach dem Vertex Shader, vor der Rasterisierung. Ist eine Fixed Function.",
            explain_wrong={
                "B": "Kompression ist ein anderer Prozess.",
                "C": "Pixelfaerben macht der Fragment Shader.",
                "D": "Modell-Laden ist vor dem Rendering."
            },
            topic="Computergrafik - Optimierung"
        ),

        Question(
            prompt="Was ist Occlusion Culling?",
            options={
                "A": "Entfernen von Objekten die von anderen Objekten vollstaendig verdeckt werden",
                "B": "Entfernen der Rueckseiten",
                "C": "Entfernen von kleinen Objekten",
                "D": "Entfernen von Farben"
            },
            correct={"A"},
            explain_correct="Occlusion Culling identifiziert und entfernt Objekte, die zwar im Frustum liegen, "
                          "aber vollstaendig von anderen Objekten verdeckt werden (occluded). "
                          "Techniken: Hardware Occlusion Queries, Software Rasterization, Hierarchische Z-Buffer. "
                          "Wichtig fuer Innenraeume und dichte Szenen. Komplexer als Frustum Culling.",
            explain_wrong={
                "B": "Das ist Backface Culling.",
                "C": "Kleine Objekte zu entfernen waere LOD.",
                "D": "Farben werden nicht 'ge-culled'."
            },
            topic="Computergrafik - Optimierung"
        ),

        Question(
            prompt="Was ist LOD (Level of Detail)?",
            options={
                "A": "Eine Beleuchtungsmethode",
                "B": "Verwendung vereinfachter Modelle fuer entfernte Objekte",
                "C": "Eine Texturkompression",
                "D": "Ein Soundeffekt"
            },
            correct={"B"},
            explain_correct="Level of Detail (LOD) ist eine Optimierungstechnik, bei der fuer entfernte Objekte "
                          "vereinfachte Versionen (weniger Polygone) verwendet werden. Je naeher das Objekt, "
                          "desto detaillierter das Modell. Das spart Rendering-Zeit ohne sichtbare Qualitaetseinbussen, "
                          "da kleine Objekte ohnehin wenige Pixel bedecken. Aehnliches Konzept wie Mipmaps fuer Texturen.",
            explain_wrong={
                "A": "LOD ist eine Geometrie-Optimierung.",
                "C": "Mipmaps sind LOD fuer Texturen, aber LOD allgemein bezieht sich auf Geometrie.",
                "D": "LOD hat nichts mit Sound zu tun."
            },
            topic="Computergrafik - Optimierung"
        ),

        # ============================================================
        # MODERNE RENDERING-TECHNIKEN
        # ============================================================
        Question(
            prompt="Was ist Deferred Shading?",
            options={
                "A": "Direkte Beleuchtungsberechnung pro Dreieck",
                "B": "Zweistufiges Rendering: erst Geometrie-Info speichern (G-Buffer), dann Beleuchtung",
                "C": "Eine Texturmethode",
                "D": "Eine Animationstechnik"
            },
            correct={"B"},
            explain_correct="Deferred Shading trennt Geometrie- und Beleuchtungs-Pass. Im ersten Pass werden "
                          "Geometrie-Informationen (Position, Normale, Albedo, Specular) in den G-Buffer gerendert. "
                          "Im zweiten Pass wird die Beleuchtung pro Pixel nur einmal berechnet (nicht pro Licht pro Dreieck). "
                          "Vorteil: Viele Lichter effizient. Nachteil: Hoher Speicherbedarf, Probleme mit Transparenz.",
            explain_wrong={
                "A": "Das waere Forward Shading.",
                "C": "Deferred Shading ist eine Rendering-Technik.",
                "D": "Deferred Shading betrifft kein Animation."
            },
            topic="Computergrafik - Moderne Techniken"
        ),

        Question(
            prompt="Was ist Forward Shading?",
            options={
                "A": "Traditionelles Rendering: Beleuchtung wird direkt beim Rendern jedes Objekts berechnet",
                "B": "Rendering in zwei Paessen",
                "C": "Nur fuer 2D-Grafik",
                "D": "Eine Kompression"
            },
            correct={"A"},
            explain_correct="Forward Shading ist der traditionelle Ansatz: Jedes Objekt wird gerendert und "
                          "dabei direkt beleuchtet. Fuer jedes Fragment werden alle Lichter berechnet. "
                          "Vorteil: Einfach, funktioniert mit Transparenz und MSAA. "
                          "Nachteil: Bei vielen Lichtern langsam (O(Objekte * Lichter * Pixel)).",
            explain_wrong={
                "B": "Zwei Paesse sind Deferred Shading.",
                "C": "Forward Shading funktioniert auch in 3D.",
                "D": "Forward Shading ist keine Kompression."
            },
            topic="Computergrafik - Moderne Techniken"
        ),

        Question(
            prompt="Was ist HDR (High Dynamic Range) Rendering?",
            options={
                "A": "Rendern mit hoeherer Aufloesung",
                "B": "Rendern mit erweitertem Helligkeitsbereich (ueber 0-1)",
                "C": "Rendern mit mehr Polygonen",
                "D": "Rendern ohne Farben"
            },
            correct={"B"},
            explain_correct="HDR Rendering arbeitet mit einem erweiterten Helligkeitsbereich - Werte koennen "
                          "groesser als 1.0 sein (z.B. eine Sonne mit Intensitaet 10.0). Das Rendering erfolgt "
                          "in einem Float-Buffer. Am Ende wird Tone Mapping angewendet, um den HDR-Bereich "
                          "auf den darstellbaren LDR-Bereich (0-1) zu komprimieren und Bloom-Effekte zu erzeugen.",
            explain_wrong={
                "A": "Aufloesung ist unabhaengig von HDR.",
                "C": "Polygonzahl ist unabhaengig von HDR.",
                "D": "HDR hat mehr Farb-/Helligkeitsinformation, nicht weniger."
            },
            topic="Computergrafik - Moderne Techniken"
        ),

        Question(
            prompt="Was ist Tone Mapping?",
            options={
                "A": "Eine Audioverarbeitung",
                "B": "Umwandlung von HDR nach LDR unter Erhaltung visueller Details",
                "C": "Eine Texturkompression",
                "D": "Eine Animationstechnik"
            },
            correct={"B"},
            explain_correct="Tone Mapping ist der Prozess, HDR-Bilder (hoher Dynamikumfang) auf "
                          "LDR-Displays (niedriger Dynamikumfang, 8 Bit) abzubilden. Es komprimiert "
                          "den Helligkeitsbereich auf eine kuenstlerisch ansprechende Weise, "
                          "erhaelt Details in hellen und dunklen Bereichen. Bekannte Operatoren: "
                          "Reinhard, ACES, Filmic. Oft kombiniert mit Exposure-Kontrolle.",
            explain_wrong={
                "A": "Tone Mapping ist fuer Bilder, nicht Audio.",
                "C": "Kompression ist ein anderes Thema.",
                "D": "Animation ist ein anderes Thema."
            },
            topic="Computergrafik - Moderne Techniken"
        ),

        Question(
            prompt="Was ist Post-Processing in der Computergrafik?",
            options={
                "A": "Effekte die auf das fertig gerenderte Bild angewendet werden",
                "B": "Die Vorbereitung von 3D-Modellen",
                "C": "Das Laden von Texturen",
                "D": "Die Vertex-Transformation"
            },
            correct={"A"},
            explain_correct="Post-Processing sind Bildeffekte, die auf das fertig gerenderte Bild "
                          "(als Textur) angewendet werden. Typische Effekte: Bloom (Leuchteffekte), "
                          "Motion Blur, Depth of Field (Tiefenunschaerfe), Color Grading, SSAO, FXAA/TAA, "
                          "Vignette, Chromatic Aberration. Sie werden in Screen Space berechnet.",
            explain_wrong={
                "B": "Modellvorbereitung ist vor dem Rendering.",
                "C": "Texturladen ist vor dem Rendering.",
                "D": "Vertex-Transformation ist Teil der Pipeline, nicht Post-Processing."
            },
            topic="Computergrafik - Moderne Techniken"
        ),

        Question(
            prompt="Was ist Screen Space Ambient Occlusion (SSAO)?",
            options={
                "A": "Eine Textur",
                "B": "Echtzeit-AO basierend auf dem Depth-Buffer",
                "C": "Ein Kompressionsverfahren",
                "D": "Eine Animationstechnik"
            },
            correct={"B"},
            explain_correct="SSAO ist eine Echtzeit-Approximation von Ambient Occlusion im Screen Space. "
                          "Es verwendet den Depth-Buffer um abzuschaetzen, wie viel Umgebungslicht "
                          "jeden Pixel erreicht. Samples werden in einer Halbkugel um jeden Pixel genommen "
                          "und gegen den Depth-Buffer geprueft. Schnell, aber nur Screen Space (keine verdeckten Bereiche).",
            explain_wrong={
                "A": "SSAO erzeugt Daten, ist aber keine Textur.",
                "C": "SSAO ist ein Rendering-Effekt.",
                "D": "SSAO betrifft Beleuchtung, nicht Animation."
            },
            topic="Computergrafik - Moderne Techniken"
        ),

        Question(
            prompt="Was ist Anti-Aliasing in der Computergrafik? (Mehrfachauswahl)",
            options={
                "A": "Glaettung von Treppeneffekten an Kanten",
                "B": "MSAA (Multi-Sample Anti-Aliasing)",
                "C": "FXAA (Fast Approximate Anti-Aliasing)",
            },
            correct={"A", "B", "C"},
            explain_correct="Anti-Aliasing reduziert 'Treppchen' (Jaggies) an Kanten. "
                          "MSAA: Mehrere Samples pro Pixel an Dreieckskanten, hochwertig aber aufwendig. "
                          "SSAA: Rendering in hoeherer Aufloesung, dann Downscaling (sehr aufwendig). "
                          "FXAA/SMAA: Post-Processing basiert, schnell aber kann Details weichzeichnen. "
                          "TAA: Temporal, nutzt Daten aus vorherigen Frames, gute Qualitaet bei Bewegung.",
            explain_wrong={},
            topic="Computergrafik - Moderne Techniken"
        ),
    ]
