# Testkonzept Zeiterfassungssystem

| | |
|---|---|
| **Modul** | M450 – Applikationen testen |
| **Projektgruppe** | Gruppe 1 (eigene M306-Projektgruppe) |
| **Testobjekt** | Zeiterfassungssystem der Engineering-Firma (ca. 50 Mitarbeitende), Testumgebung |
| **Dokumentversion** | 0.1 (Entwurf) |
| **Stand** | 19.11.2026 |
| **Status** | Kapitel 1–3 in Bearbeitung, Kapitel 4–8 folgen |

**Legende**

- **[ANF-xx]** = Anforderung aus der Testbasis, Fundstelle siehe [Anhang A](#anhang-a-anforderungen-und-fundstellen)
- **[Annahme Ax]** = Annahme des Testteams, noch nicht durch den Auftraggeber bestätigt (Liste in Kapitel 1.6)
- **[FF-x]** = offene Fachfrage an den Auftraggeber (Kapitel 1.5)
- **Fundstelle «AS S. x»** = Aufgabenstellung Softwaretest, gbssg.ch, Seite x

## Inhaltsverzeichnis

1. Ausgangslage und Testziele
2. Testumfang und Nicht-Ziele
3. Risiken und Prioritäten
4. Teststrategie
5. Organisation und Umgebung
6. Aktivitäten und Zeitplanung
7. Eintritts- und Abschlusskriterien
8. Ergebnisse und Berichterstattung

Anhang A: Anforderungen und Fundstellen

---

## 1 Ausgangslage und Testziele

### 1.1 Ausgangslage

Eine Engineering-Firma mit rund 50 Mitarbeitenden hat ein Zeiterfassungssystem entwickeln lassen. Die Software ist implementiert und steht in einer Testumgebung bereit. Bisher wurde sie hauptsächlich vom Entwicklungsteam selbst geprüft; ein unabhängiger, systematischer Test fehlt noch (AS S. 2, Projektskizze).

Die Geschäftsleitung will vor der Einführung wissen, ob die Anwendung die Anforderungen erfüllt und im Arbeitsalltag zuverlässig eingesetzt werden kann. Unser Projektteam übernimmt diesen Testauftrag und liefert die Entscheidungsgrundlage für die Einführung.

**Rahmenbedingungen** (AS S. 2, Budget und Terminrahmen):

- Personal: 3 Tester und 1 Projektleitung (Testleitung)
- Endtermin: Testing abgeschlossen bis **14.01.2027**
- Zwischenstand an den Auftraggeber: Zeitpunkt schlägt das Team vor (Vorschlag folgt in Kapitel 6 und 8)
- Fehlerbehebung macht das Entwicklungsteam, wir prüfen die Korrekturen erneut (Retest und Regressionstest) (AS S. 3, Aufgabe)

### 1.2 Auftrag

Wir planen und organisieren das Testvorhaben, erstellen Testkonzept und Testfälle mit Testdaten und erwarteten Ergebnissen, führen die Tests durch, protokollieren die Ergebnisse, dokumentieren Abweichungen reproduzierbar und geben am Schluss eine begründete Freigabeempfehlung ab (AS S. 3, Aufgabe).

**Abzugebende Ergebnisse:** Projektplanung, Testkonzept, Testfälle, Testprotokolle, Fehlerberichte, Abschlussbericht mit Freigabeempfehlung.

### 1.3 Testbasis

Gegen diese Dokumente wird getestet. Ein Testfall gilt nur dann als bestanden oder nicht bestanden, wenn sich das erwartete Ergebnis auf eine dieser Quellen zurückführen lässt.

| Nr. | Dokument | Inhalt | Stand / Bemerkung |
|---|---|---|---|
| TB-D1 | **Auftrag:** «Aufgabenstellung Softwaretest – Zeiterfassungssystem», gbssg.ch 2026 | Projektskizze, Vorgaben, Budget, Termine, Erwartungen des Auftraggebers | S. 2–3, verbindlich |
| TB-D2 | **Eigenes Pflichtenheft** der Gruppe 1 (Auszug in [Anhang A](#anhang-a-anforderungen-und-fundstellen)) | Aus TB-D1 abgeleitete, nummerierte und überprüfbare Anforderungen ANF-01 bis ANF-12 | v0.1, wird nach Klärung der Fachfragen ergänzt |
| TB-D3 | Notizen aus dem ersten Auftraggebergespräch | 8 Erwartungen des Auftraggebers | in TB-D1 S. 3 enthalten |
| TB-D4 | Dokumentation des Entwicklungsteams (Benutzerhandbuch, Rollenbeschreibung, Release Notes) | Bedienung, Rollen, bekannte Einschränkungen | **noch anzufordern** [Annahme A1] |
| TB-D5 | Antworten auf die offenen Fachfragen (Kapitel 1.5) | Rechenregeln, Rollen, Zielwerte | ausstehend |

Unklare oder fehlende Angaben klären wir mit dem Auftraggeber. Bis zur Klärung halten wir Annahmen fest und kennzeichnen sie (AS S. 2, Ausgangslage Punkt 4).

### 1.4 Testziele

Die Aussagen des Auftraggebers (AS S. 3) sind noch nicht überprüfbar. «Die Monatsabrechnungen müssen stimmen» sagt zum Beispiel nicht, wann eine Abrechnung stimmt. Wir übersetzen sie deshalb in messbare Testziele. Jedes Ziel hat ein klares Kriterium, wann es erreicht ist.

| ID | Testziel (messbar) | Erfüllt, wenn … | Bezug | Prio |
|---|---|---|---|---|
| **TZ-1** | **Abrechnung korrekt:** Alle vereinbarten Referenzfälle für Vollzeit, Teilzeit, Abwesenheiten und nachträgliche Korrekturen liefern den Sollsaldo. | 100 % der Referenzfälle (mind. 12, siehe unten) ergeben Gleitzeitsaldo, Monatssumme und Projektsumme **auf die Minute genau** wie das von Hand berechnete Sollergebnis. | ANF-04, ANF-05, ANF-06, ANF-07 | P1 |
| **TZ-2** | **Berechtigungen dicht:** Keine Rolle kann Daten sehen oder ändern, für die sie keine Berechtigung hat. | 100 % der Negativtests der Berechtigungsmatrix (jede Rolle × jede geschützte Funktion, über Oberfläche **und** direkte URL) werden abgewiesen. 0 erfolgreiche unberechtigte Zugriffe. | ANF-03, ANF-09 | P1 |
| TZ-3 | **Fehleingaben sicher:** Ungültige Eingaben werden verständlich gemeldet, gespeicherte Daten bleiben erhalten. | 100 % der definierten ungültigen Eingaben (mind. 15 Fälle, z. B. Ende vor Start, Überlappung, 25 h/Tag) werden mit einer Meldung abgewiesen, die Feld und Ursache nennt. In 0 Fällen gehen bereits gespeicherte Daten verloren. | ANF-10 | P1 |
| TZ-4 | **Antwortzeiten ausreichend:** Die Anwendung bleibt bei gleichzeitiger Nutzung schnell und stabil. | Bei 25 gleichzeitigen Benutzern [Annahme A4] werden 95 % der Speicher- und Ladeaktionen in **≤ 2 s** ausgeführt, 0 Abbrüche oder Fehlerseiten während 30 Min. | ANF-11 | P2 |

TZ-1 und TZ-2 sind die beiden Kernziele aus dem Gruppenauftrag. TZ-3 und TZ-4 ergänzen sie, weil der Auftraggeber diese Punkte ausdrücklich nennt.

**Referenzfälle für TZ-1 (Entwurf, Sollwerte werden nach Klärung von FF-1 bis FF-3 berechnet):**

| Ref | Fall | Pensum | Prüft |
|---|---|---|---|
| RF-01 | Normaler Monat ohne Abwesenheiten | 100 % | Sollzeit, Saldo |
| RF-02 | Normaler Monat ohne Abwesenheiten | 80 % | Teilzeit-Sollzeit |
| RF-03 | Normaler Monat ohne Abwesenheiten | 50 % | Teilzeit-Sollzeit |
| RF-04 | Pensumwechsel mitten im Monat (100 % → 60 %) | gemischt | anteilige Sollzeit |
| RF-05 | 1 Woche Ferien | 100 % | Abwesenheit |
| RF-06 | 1 Woche Ferien | 60 % | Abwesenheit bei Teilzeit |
| RF-07 | 2 Krankheitstage, davon 1 halber Tag | 80 % | Abwesenheit, halbe Tage |
| RF-08 | Monat mit Feiertagen (Dezember 2026: 25./26.12.) | 100 % und 80 % | Feiertagsgutschrift |
| RF-09 | Nachträgliche Korrektur im laufenden Monat | 100 % | Korrektur in Saldo **und** Projektsumme |
| RF-10 | Nachträgliche Korrektur im bereits abgeschlossenen Vormonat | 80 % | Übertrag, Abschluss |
| RF-11 | Buchung über Mitternacht (22:00–02:00) | 100 % | Tageswechsel |
| RF-12 | Überzeit > Gleitzeitmaximum | 100 % | Grenzwert Saldo |

### 1.5 Offene Fachfragen

Die folgenden Fragen müssen mit dem Auftraggeber geklärt werden, bevor wir die Sollwerte für die Testfälle festlegen können. Ohne Antwort wissen wir nicht, welches Ergebnis «richtig» ist.

| ID | Offene Fachfrage | Warum wichtig | Betrifft | Annahme bis zur Klärung |
|---|---|---|---|---|
| **FF-1** | **Sollzeit und Rundung:** Wie hoch ist die Sollarbeitszeit pro Tag bei 100 % (z. B. 8 h 24 min oder 8 h 30 min)? Wird auf Minuten, 5 oder 15 Minuten gerundet, und wann (pro Buchung, pro Tag, pro Monat)? | Ohne diese Regel lässt sich kein Sollsaldo berechnen. Rundung pro Buchung statt pro Monat kann pro Monat mehrere Stunden Unterschied ergeben. | TZ-1, ANF-04, ANF-05 | **[Annahme A2]** 42 h/Woche bei 100 % (8 h 24 min/Tag), Erfassung auf die Minute genau, keine Rundung. |
| **FF-2** | **Pausen:** Werden Pausen manuell erfasst oder automatisch abgezogen? Gilt eine Mindestpause (z. B. 30 Min. ab 7 h Arbeit, analog ArG Art. 15)? | Ein automatischer Pausenabzug verändert jede Tagessumme und damit den Saldo. | TZ-1, ANF-05 | **[Annahme A3]** Pausen werden manuell erfasst, kein automatischer Abzug. Fehlt die Pause ab 7 h, gibt es eine Warnung. |
| **FF-3** | **Bewertung von Abwesenheiten bei Teilzeit:** Wie viele Stunden werden für Ferien, Krankheit oder Feiertag gutgeschrieben – die volle Tagessollzeit oder die anteilige Sollzeit gemäss Pensum? Gibt es halbe Tage? | Genau hier vermutet der Auftraggeber Fehler («Teilzeitpensen, Abwesenheiten»). Höchstes Einzelrisiko R1. | TZ-1, ANF-06 | **[Annahme A5]** Gutschrift = Tagessollzeit × Pensum. Halbe Tage sind möglich. |
| FF-4 | **Nachträgliche Korrekturen:** Bis wann darf eine Mitarbeiterin oder ein Mitarbeiter Zeiten rückwirkend ändern? Wird ein Monat abgeschlossen, und wer darf danach noch korrigieren (Personalbüro)? Muss jede Änderung protokolliert werden? | Bestimmt die Testfälle für Korrekturen (RF-09, RF-10) und die Berechtigungsmatrix. | TZ-1, TZ-2, ANF-07 | **[Annahme A6]** Eigene Korrektur bis zum Monatsabschluss durch das Personalbüro, danach nur noch Personalbüro. Jede Änderung wird mit Benutzer und Zeitpunkt protokolliert. |
| FF-5 | **Rollen und Rechte:** Welche Rollen gibt es genau, und was darf jede Rolle sehen und ändern? Darf eine Projektleitung Zeiten ihrer Projektmitarbeitenden korrigieren? Sieht sie Abwesenheitsgründe (z. B. Krankheit)? | Grundlage für die Berechtigungsmatrix in TZ-2. Abwesenheitsgründe sind besonders schützenswerte Daten. | TZ-2, ANF-03 | **[Annahme A7]** 4 Rollen gemäss Anhang A, ANF-03. Projektleitung sieht nur Projektstunden, keine Abwesenheitsgründe, und darf nichts ändern. |
| FF-6 | **Antwortzeiten:** Welche Antwortzeit gilt als «ausreichend schnell»? Wie viele Personen arbeiten zur Spitzenzeit (z. B. Monatsende) gleichzeitig? | Ohne Zielwert ist TZ-4 nicht prüfbar. | TZ-4, ANF-11 | **[Annahme A4]** 25 gleichzeitige Benutzer (50 % der Belegschaft), Zielwert ≤ 2 s. |

Die Fragen FF-1 bis FF-3 sind für die Abrechnung entscheidend und werden zuerst geklärt. Wir schicken die Liste nach der Abgabe dieses Entwurfs an den Auftraggeber.

### 1.6 Annahmen

| ID | Annahme | Zu bestätigen durch |
|---|---|---|
| A1 | Das Entwicklungsteam stellt Benutzerhandbuch, Rollenbeschreibung und Release Notes der Testversion zur Verfügung. | Auftraggeber / Entwicklungsteam |
| A2 | Sollzeit 42 h/Woche bei 100 %, Erfassung minutengenau ohne Rundung. | Personalbüro (FF-1) |
| A3 | Pausen werden manuell erfasst, kein automatischer Abzug. | Personalbüro (FF-2) |
| A4 | Spitzenlast 25 gleichzeitige Benutzer, Zielwert Antwortzeit ≤ 2 s. | Auftraggeber (FF-6) |
| A5 | Abwesenheitsgutschrift = Tagessollzeit × Pensum, halbe Tage möglich. | Personalbüro (FF-3) |
| A6 | Rückwirkende Korrektur durch Mitarbeitende bis zum Monatsabschluss, danach nur Personalbüro, alle Änderungen protokolliert. | Personalbüro (FF-4) |
| A7 | Rollen: Mitarbeitende, Projektleitung, Entwicklungsleitung, Personalbüro (Rechte siehe ANF-03). | Auftraggeber (FF-5) |
| A8 | Die Anwendung ist eine Webanwendung und wird auf Desktop-Browser und Smartphone-Browser genutzt (keine native App). | Entwicklungsteam |
| A9 | Die Testumgebung enthält keine echten Personaldaten. Wir dürfen eigene Testbenutzer und Testdaten anlegen. | Auftraggeber |

---

## 2 Testumfang und Nicht-Ziele

### 2.1 Testobjekt

Getestet wird das Zeiterfassungssystem in der bereitgestellten Testumgebung. Softwareversion, Build-Nummer und Konfiguration (Pensen, Feiertagskalender, Rollen) halten wir zu Beginn der Testdurchführung fest, damit alle Ergebnisse nachvollziehbar sind (AS S. 2, Ausgangslage Punkt 6). Die genaue Versionsnummer liefert das Entwicklungsteam [Annahme A1].

### 2.2 Testbereiche (im Testumfang)

| ID | Testbereich | Was wir prüfen | Qualitätsmerkmal | Anforderungen | Prio |
|---|---|---|---|---|---|
| **TB-1** | **Zeiten erfassen und korrigieren** | Arbeitszeit auf Projekte buchen, ändern, löschen. Nachträgliche Korrekturen. Ungültige Eingaben (Ende vor Start, Überlappung, mehr als 24 h, leere Pflichtfelder, Buchung über Mitternacht). | Funktionalität, Fehlertoleranz | ANF-01, ANF-07, ANF-10 | P1 |
| **TB-2** | **Monatsabrechnung, Gleitzeitsaldo und Projektsummen** | Sollzeit nach Pensum, Gleitzeitsaldo, Abwesenheiten (Ferien, Krankheit, Feiertage), Pensumwechsel, Projekt- und Monatssummen, Wirkung von Korrekturen auf alle Summen. Referenzfälle RF-01 bis RF-12. | Funktionalität (Richtigkeit) | ANF-04, ANF-05, ANF-06, ANF-07, ANF-08 | P1 |
| **TB-3** | **Rollenrechte und Datenerhalt** | Berechtigungsmatrix für 4 Rollen: Wer sieht und ändert welche Zeiten und Personaldaten? Zugriff über die Oberfläche und über direkte URL bzw. geänderte IDs. Bleiben Daten nach Fehleingabe, Abmeldung oder Sitzungsablauf erhalten? | Sicherheit (Zugriffsschutz), Zuverlässigkeit | ANF-03, ANF-09, ANF-10 | P1 |
| **TB-4** | **Nutzung unterwegs und im Homeoffice** | Erfassen und Korrigieren auf Smartphone (iOS/Android, je 1 aktueller Browser) und Laptop. Verständliche Fehlermeldungen auf kleinem Bildschirm. Verhalten bei langsamer oder unterbrochener Verbindung (keine doppelte oder verlorene Buchung). | Bedienbarkeit, Zuverlässigkeit | ANF-02, ANF-10 | P2 |
| TB-5 | **Antwortzeiten bei gleichzeitiger Nutzung** | Speichern einer Buchung und Laden der Monatsübersicht mit 25 gleichzeitigen Benutzern [Annahme A4]. Einfacher Lasttest, kein Stresstest. | Effizienz (Antwortzeit), Stabilität | ANF-11 | P2 |

Die Bereiche TB-1 bis TB-4 bilden den Kern. TB-5 testen wir mit reduziertem Aufwand (ein Lastszenario), weil die Firma nur rund 50 Mitarbeitende hat und Spitzenlast vor allem am Monatsende auftritt.

### 2.3 Nicht-Ziele (ausserhalb des Testumfangs)

Die Zeit bis zum 14.01.2027 ist begrenzt, inklusive Weihnachtsferien. Wir müssen deshalb bewusst Bereiche ausklammern (AS S. 2, Ausgangslage Punkt 7). Für jedes Nicht-Ziel halten wir das Restrisiko fest, damit es im Abschlussbericht erscheint.

| ID | Nicht-Ziel | Begründung | Restrisiko |
|---|---|---|---|
| **NZ-1** | **Fehler selbst beheben und neue Funktionen entwickeln** | Die Fehlerbehebung übernimmt laut Auftrag das Entwicklungsteam (AS S. 3, Aufgabe). Unsere Rolle ist der unabhängige Test. Würden wir selbst Code ändern, wären wir nicht mehr unabhängig und würden unsere eigenen Änderungen testen. | Gering. Wir melden Fehler reproduzierbar und prüfen die Korrekturen erneut (Retest und Regression). |
| **NZ-2** | **Firmenweite Einführung, Datenmigration und Schulung der Mitarbeitenden** | Der Auftrag liefert die *Entscheidungsgrundlage* für die Einführung, nicht die Einführung selbst (AS S. 2, Projektskizze). Migration und Schulung gehören zum Einführungsprojekt danach. | Mittel. Fehler bei der Übernahme alter Saldi werden nicht gefunden. Wir empfehlen im Abschlussbericht einen Migrationstest vor dem Go-Live. |
| NZ-3 | **Penetrationstest und Prüfung der Server-Infrastruktur** (Netzwerk, Betriebssystem, Backup) | Dafür braucht es Spezialwissen, Werkzeuge und eine schriftliche Erlaubnis des Betreibers. Wir prüfen die Berechtigungen auf Anwendungsebene (TB-3), aber keine Angriffe auf die Infrastruktur. | Mittel. Wird im Abschlussbericht als nicht getesteter Bereich aufgeführt. |
| NZ-4 | **Last- und Stresstests über 50 Benutzer hinaus, Test auf älteren Browsern und Geräten** | Die Firma hat rund 50 Mitarbeitende. Mehr Last ist im Betrieb nicht realistisch. Wir testen nur je einen aktuellen Browser pro Plattform. | Gering bis mittel. Darstellungsprobleme auf alten Geräten sind möglich (meist P3). |

### 2.4 Abgrenzung zur Freigabe

Die Abgrenzung stimmen wir mit dem Auftraggeber ab. Ändert der Auftraggeber den Umfang, passen wir Kapitel 2 und 3 an und vermerken die Änderung in der Versionsgeschichte.

---

## 3 Risiken und Prioritäten

### 3.1 Bewertungsmethode

Wir bewerten Produktrisiken nachvollziehbar mit:

**Risikoscore = Wahrscheinlichkeit (W) × Schaden (S)**

| Wert | Wahrscheinlichkeit W | Schaden S |
|---|---|---|
| 1 | gering – nur in seltenen Sonderfällen | gering – kosmetisch, keine Auswirkung auf die Arbeit |
| 2 | mittel – kommt bei einem Teil der Benutzer vor | mittel – Mehraufwand, Workaround möglich |
| 3 | hoch – betrifft regelmässig viele Benutzer oder komplexe Logik | hoch – falsche Abrechnung, Datenverlust oder Datenschutzverletzung |

**Zuordnung zur Priorität:**

| Priorität | Score | Bedeutung | Vorgehen |
|---|---|---|---|
| **P1 zwingend** | 6–9 | Abrechnung, Berechtigungen, Datenerhalt | Früh testen, nach jeder Korrektur erneut prüfen (Regression). |
| **P2 wichtig** | 3–4 | Bedienbarkeit, vereinbarte Antwortzeiten | Testen nach P1. Bei hohem Betriebsrisiko ebenfalls als P1 einstufen. |
| **P3 nachrangig** | 1–2 | Kosmetische Details ohne Einfluss auf die Arbeit | Bei Engpässen zurückstellen und Risiko festhalten. |

Die Prioritäten sind ein Vorschlag. Am Ende entscheidet das Risiko im konkreten Projekt. Wo wir von der Tabelle abweichen, begründen wir es.

### 3.2 Produktrisiken

Werte mit **[Annahme]** beruhen auf unserer Einschätzung und werden nach dem Gespräch mit dem Auftraggeber überprüft.

| ID | Möglicher Fehler | W | S | Score | Prio | Begründung | Testbereich |
|---|---|:-:|:-:|:-:|:-:|---|---|
| **R1** | **Teilzeitpensum erzeugt einen falschen Gleitzeitsaldo** (z. B. Sollzeit oder Abwesenheit wird mit 100 % statt mit dem Pensum gerechnet) | 3 | 3 | **9** | **P1** | W=3: Teilzeit kombiniert mit Abwesenheiten und Pensumwechsel ist die komplexeste Rechenlogik, und der Auftraggeber nennt sie ausdrücklich. Die Regeln sind noch unklar (FF-1, FF-3). S=3: Falsche Saldi wirken sich direkt auf Lohn und Ferien aus und betreffen viele Mitarbeitende. **[Annahme]** Ein relevanter Anteil der 50 Mitarbeitenden arbeitet Teilzeit. | TB-2 |
| **R2** | **Eine Rolle kann fremde Arbeitszeiten oder Personaldaten einsehen oder verändern** (z. B. Mitarbeitende über geänderte ID in der URL, Projektleitung sieht Krankheitsabwesenheiten) | 2 | 3 | **6** | **P1** | W=2: Das Entwicklungsteam hat vermutlich die Oberfläche getestet, aber kaum direkte Zugriffe über URL/IDs. S=3: Verletzung des Datenschutzes (Gesundheitsdaten sind besonders schützenswert nach DSG) und mögliche Manipulation der Abrechnung. | TB-3 |
| **R3** | **Eine nachträgliche Korrektur fehlt in der Projekt- oder Monatssumme** (Saldo wird nachgeführt, Projektsumme nicht, oder umgekehrt) | 2 | 3 | **6** | **P1** | W=2: Korrekturen müssen mehrere Summen gleichzeitig nachführen, das ist eine typische Fehlerquelle. Der Auftraggeber nennt Korrekturen ausdrücklich. S=3: Falsche Projektabrechnung gegenüber Kunden und falsche Monatsabrechnung. | TB-1, TB-2 |
| **R4** | **Bereits gespeicherte Daten gehen verloren** bei Fehleingabe, Sitzungsablauf oder Verbindungsunterbruch unterwegs (z. B. ganze Woche wird verworfen, Buchung doppelt gespeichert) | 2 | 3 | **6** | **P1** | W=2: Die mobile Nutzung mit instabiler Verbindung ist laut Auftrag üblich. S=3: Datenverlust führt zu falscher Abrechnung und Vertrauensverlust. Der Auftraggeber verlangt ausdrücklich, dass keine Daten verloren gehen. | TB-3, TB-4 |
| R5 | **Feiertage oder halbe Abwesenheitstage werden falsch gutgeschrieben** (z. B. Feiertag bei 80 %-Pensum an einem freien Tag) | 2 | 3 | **6** | P1 | W=2: Sonderfall, im Testzeitraum aber real (Weihnachten, Neujahr). Die Regel ist unklar (FF-3). S=3: Wirkt direkt auf den Saldo. **[Annahme]** Es gibt einen hinterlegten Feiertagskalender. | TB-2 |
| R6 | **Fehlermeldung auf dem Smartphone ist unverständlich** oder wird abgeschnitten, Benutzer weiss nicht, was falsch ist | 2 | 2 | 4 | P2 | W=2: Meldungen werden oft nur auf dem Desktop getestet. S=2: Mehraufwand und Frust, aber keine falschen Daten, solange die Eingabe abgewiesen wird. | TB-4 |
| R7 | **Antwortzeiten zu lang oder Abbrüche bei gleichzeitiger Nutzung** am Monatsende | 2 | 2 | 4 | P2 | W=2: 25 gleichzeitige Benutzer sind eine eher kleine Last **[Annahme A4]**. S=2: Wartezeit und Mehraufwand. Wenn es dabei zu Datenverlust kommt, wird das Risiko auf P1 hochgestuft (siehe R4). | TB-5 |
| R8 | **Kosmetische Darstellungsfehler** (Ausrichtung, Schriftgrösse, Übersetzungsfehler) | 2 | 1 | 2 | P3 | W=2: In neuen Anwendungen häufig. S=1: Kein Einfluss auf die Arbeit. Wird bei Zeitmangel zurückgestellt und im Bericht festgehalten. | TB-4 |

**Risikomatrix (Übersicht)**

| W \ S | S=1 gering | S=2 mittel | S=3 hoch |
|---|---|---|---|
| **W=3 hoch** | | | **R1** (9) |
| **W=2 mittel** | R8 (2) | R6, R7 (4) | **R2, R3, R4, R5** (6) |
| **W=1 gering** | | | |

### 3.3 Projektrisiken

Diese Risiken betreffen nicht die Software, sondern unser Testvorhaben.

| ID | Risiko | W | S | Score | Massnahme |
|---|---|:-:|:-:|:-:|---|
| PR1 | Offene Fachfragen (FF-1 bis FF-3) werden nicht rechtzeitig beantwortet. Ohne Sollwerte können wir TZ-1 nicht prüfen. | 2 | 3 | 6 | Fragen sofort stellen, Termin für Antwort vereinbaren. Bis dahin mit markierten Annahmen arbeiten. |
| PR2 | Weihnachts- und Neujahrsferien (ca. 21.12.2026–03.01.2027) verkürzen die verfügbare Zeit bis 14.01.2027 stark. Auch das Entwicklungsteam ist abwesend, Korrekturen verzögern sich. | 3 | 2 | 6 | P1-Tests vor den Ferien abschliessen. Zwischenstand vor den Ferien. Retests im Januar einplanen. |
| PR3 | Testumgebung ist nicht verfügbar oder wird während des Tests ohne Absprache geändert. | 2 | 2 | 4 | Version beim Teststart festhalten, Änderungen nur nach Absprache. |
| PR4 | Ein Teammitglied fällt aus (3 Tester, wenig Reserve). | 1 | 2 | 2 | Testfälle so dokumentieren, dass jedes Teammitglied sie ausführen kann. |

### 3.4 Prioritäten für das Testvorgehen

Daraus ergibt sich die Reihenfolge der Tests. Wir testen zuerst die Abläufe, deren Ausfall Betrieb oder Abrechnung am stärksten beeinträchtigen würde, wie es der Auftraggeber verlangt (AS S. 3, Erwartung 6).

| Reihenfolge | Priorität | Risiken | Testbereiche | Vorgehen |
|---|---|---|---|---|
| 1 | **P1 zwingend** | R1, R2, R3, R4, R5 | TB-2, TB-3, TB-1 | Vor den Weihnachtsferien vollständig testen. Kritische Fehler sofort melden. Nach jeder Korrektur Regressionstest der P1-Fälle. |
| 2 | **P2 wichtig** | R6, R7 | TB-4, TB-5 | Nach P1. Falls bei R7 Datenverlust auftritt, als P1 behandeln. |
| 3 | P3 nachrangig | R8 | TB-4 | Nur wenn Zeit bleibt. Sonst als nicht getestetes Restrisiko im Abschlussbericht. |

---

## 4 Teststrategie

*Wird in der nächsten Lektion ergänzt.*

Geplanter Inhalt: Teststufen (Systemtest, Abnahmetest), Testmethoden (Äquivalenzklassen und Grenzwerte für Eingaben, Entscheidungstabelle für Sollzeit/Pensum/Abwesenheit, Berechtigungsmatrix, explorative Tests), Werkzeuge, Begründung einer allfälligen Testautomatisierung (z. B. Regression der Referenzfälle RF-01 bis RF-12).

## 5 Organisation und Umgebung

*Wird ergänzt.*

Geplanter Inhalt: Rollen im Team (1 Testleitung, 3 Tester), Zuständigkeiten pro Testbereich, Testumgebung, Softwareversion und Konfiguration, Testbenutzer und Testdaten, Geräte und Browser.

## 6 Aktivitäten und Zeitplanung

*Wird ergänzt.*

Geplanter Inhalt: Aktivitäten, Aufwand und Termine bis 14.01.2027, Zeitpunkt für den Zwischenstand (Vorschlag: vor den Weihnachtsferien), Puffer für Retests.

## 7 Eintritts- und Abschlusskriterien

*Wird ergänzt.*

Geplanter Inhalt: Voraussetzungen für den Teststart (z. B. Fachfragen FF-1 bis FF-3 beantwortet, Testumgebung verfügbar), Abschlusskriterien (z. B. alle P1-Testfälle durchgeführt, keine offenen kritischen Fehler).

## 8 Ergebnisse und Berichterstattung

*Wird ergänzt.*

Geplanter Inhalt: Testprotokolle, Fehlerberichte mit Schweregrad und Behebungspriorität, Zwischenstandsbericht, Abschlussbericht mit Testabdeckung, offenen Fehlern, Restrisiken, nicht getesteten Bereichen und Freigabeempfehlung.

---

## Anhang A: Anforderungen und Fundstellen

Auszug aus unserem Pflichtenheft. Jede Anforderung verweist auf ihre Fundstelle in der Aufgabenstellung (AS).

| ID | Anforderung | Fundstelle |
|---|---|---|
| ANF-01 | Mitarbeitende erfassen und bearbeiten ihre Arbeitszeiten auf Projekten. | AS S. 2, Ausgangslage, Punkt 1 |
| ANF-02 | Die Erfassung ist einfach und zuverlässig möglich, im Büro, im Homeoffice und unterwegs. | AS S. 2, Ausgangslage, Punkt 3; AS S. 3, Erwartung 1 |
| ANF-03 | Rollen sehen nur berechtigte Daten und Funktionen: Mitarbeitende = eigene Zeiten; Projektleitung = Stunden ihrer Projekte; Entwicklungsleitung = Gesamtübersicht; Personalbüro = Monatsabrechnungen, Saldi, Abwesenheiten. *(Rollenumfang: Annahme A7)* | AS S. 2, Ausgangslage, Punkte 1–3 |
| ANF-04 | Das Personalbüro erhält korrekte Monatsabrechnungen. | AS S. 2, Ausgangslage, Punkt 2; AS S. 3, Erwartung 2 |
| ANF-05 | Gleitzeitsaldi werden korrekt berechnet, unterschiedliche Arbeitspensen werden berücksichtigt. | AS S. 2, Ausgangslage, Punkt 2; AS S. 3, Erwartung 2 |
| ANF-06 | Abwesenheiten werden erfasst und korrekt in Saldo und Abrechnung berücksichtigt. | AS S. 2, Ausgangslage, Punkt 2; AS S. 3, Erwartung 2 |
| ANF-07 | Nachträgliche Korrekturen werden korrekt in alle Summen übernommen. | AS S. 3, Erwartung 2 |
| ANF-08 | Projektsummen stimmen. Projektleitungen sehen die Stunden ihrer Projekte, die Entwicklungsleitung erhält eine Gesamtübersicht. | AS S. 2, Ausgangslage, Punkt 1; AS S. 3, Erwartung 2 |
| ANF-09 | Niemand darf Arbeitszeiten oder Personaldaten einsehen oder verändern, für die er oder sie keine Berechtigung hat. | AS S. 3, Erwartung 3 |
| ANF-10 | Fehleingaben werden verständlich gemeldet, bereits gespeicherte Daten gehen dabei nicht verloren. | AS S. 3, Erwartung 4 |
| ANF-11 | Die Anwendung bleibt bei gleichzeitiger Nutzung durch mehrere Mitarbeitende ausreichend schnell und stabil. *(Zielwert: Annahme A4)* | AS S. 3, Erwartung 5 |
| ANF-12 | Gefundene Fehler sind für das Entwicklungsteam nachvollziehbar dokumentiert, kritische Probleme werden früh gemeldet. | AS S. 3, Erwartung 7 |

---

### Versionsgeschichte

| Version | Datum | Änderung |
|---|---|---|
| 0.1 | 19.11.2026 | Gliederung mit 8 Kapiteln erstellt, Kapitel 1–3 befüllt (Testbasis, Testziele, Fachfragen, Testumfang, Nicht-Ziele, Risiken) |
