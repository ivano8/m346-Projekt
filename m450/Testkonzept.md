# Testkonzept Zeiterfassungssystem

| | |
|---|---|
| **Projektname** | Softwaretest Zeiterfassungssystem (STZ) |
| **Projektnummer** | 28170907 |
| **Ergebnisname** | Testkonzept |
| **Doc_ID** | STZ-TK-01 |
| **Modul** | M450 – Applikationen testen (Gruppe 1, eigene M306-Projektgruppe) |
| **Projektleitung** | Paulo Capelos Viana |
| **Auftraggeber** | Ricardo Russo (Engineering-Firma, Fallbeispiel) |
| **Autoren** | Ivano Pervan, Paulo Capelos Viana, Tom Nielsen, Sai Ragavan |
| **Initiale** | IP / PCV / TN / SR |
| **Testobjekt** | Zeiterfassungssystem der Engineering-Firma (ca. 50 Mitarbeitende), bereitgestellte Testumgebung |
| **Dokumentversion** | 0.2 (Entwurf) |
| **Stand** | 19.11.2026 |
| **Status** | In Arbeit: Kapitel 1–3 befüllt, Kapitel 4–8 folgen |

**Legende**

- **F01–F11 / N01–N06** = funktionale bzw. nichtfunktionale Anforderung aus unserem Pflichtenheft STZ-PH-01, Fundstellen siehe [Anhang A](#anhang-a-anforderungen-und-fundstellen)
- **Fundstelle «PH Kap. x»** = Pflichtenheft STZ-PH-01, Version 1.0 vom 22.10.2026, Kapitel x
- **Fundstelle «AS S. x»** = Aufgabenstellung Softwaretest – Zeiterfassungssystem, gbssg.ch 2026, Seite x
- **[Annahme Ax]** = Annahme des Testteams, noch nicht vom Auftraggeber bestätigt (Liste in Kapitel 1.6)
- **[FF-x]** = offene Fachfrage an den Auftraggeber (Kapitel 1.5)
- **Prioritäten:** P1 = Muss, P2 = Kann, P3 = Ausbau (gleiche Stufen wie PH Kap. 6, siehe Kapitel 3.1)

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

Eine Engineering-Firma mit rund 50 Mitarbeitenden hat ein Zeiterfassungssystem entwickeln lassen. Die Software ist implementiert und steht in einer Testumgebung bereit. Bisher wurde sie hauptsächlich vom Entwicklungsteam selbst geprüft. Ein unabhängiger, systematischer Test fehlt noch (AS S. 2, Projektskizze; PH Kap. 3).

Die Geschäftsleitung will vor der Einführung wissen, ob die Anwendung die Anforderungen erfüllt und im Arbeitsalltag zuverlässig eingesetzt werden kann. Unser Projektteam testet die Anwendung unabhängig und liefert die Entscheidungsgrundlage für die Einführung. Wir entwickeln keine eigene Anwendung (PH Kap. 1).

Das Projektteam hat die Testsoftware noch nicht untersucht. Softwareversion, Konfiguration, Zugänge, Berechnungsregeln und Testdaten sind noch zu klären (PH Kap. 4). Alles, was in diesem Dokument darauf aufbaut, ist deshalb als Annahme markiert.

**Rahmenbedingungen** (AS S. 2, Budget und Terminrahmen; PH Kap. 7):

- Team: Paulo Capelos Viana (Projektleitung) und drei Tester: Ivano Pervan, Sai Ragavan, Tom Nielsen
- Ressourcen: zwei Schullektionen pro Woche plus Eigenarbeit
- Zwischenstandsbericht bis **18.12.2026**
- Re-Tests und Abschlussbericht bis **14.01.2027** (verbindlicher Endtermin)
- Fehler behebt das Entwicklungsteam. Wir prüfen die gelieferten Korrekturen erneut (Nachtest und Regression) (AS S. 3; PH Kap. 6.2, N04)

### 1.2 Auftrag

Wir planen und organisieren das Testvorhaben. Wir erstellen Testkonzept und Testfälle mit Testdaten und erwarteten Ergebnissen, führen die Tests durch und protokollieren die Ergebnisse. Abweichungen dokumentieren wir reproduzierbar. Am Schluss geben wir eine begründete Freigabeempfehlung ab (AS S. 3, Aufgabe).

**Lieferobjekte** (PH Kap. 7): Projektplanung, Testkonzept, Testfälle, Testprotokolle, Fehlerberichte, Zwischenstandsbericht, Abschlussbericht mit begründeter Freigabeempfehlung.

### 1.3 Testbasis

Gegen diese Dokumente wird getestet. Jedes erwartete Ergebnis in einem Testfall muss sich auf eine dieser Quellen zurückführen lassen.

| Nr. | Dokument | Inhalt | Stand |
|---|---|---|---|
| D1 | **Auftrag:** Aufgabenstellung Softwaretest – Zeiterfassungssystem, gbssg.ch 2026 | Projektskizze, Vorgaben, Budget, Termine, Erwartungen aus dem ersten Auftraggebergespräch | S. 2–3, verbindlich |
| D2 | **Eigenes Pflichtenheft** STZ-PH-01, Projektteam Gruppe 1 | Ziele (Kap. 5), funktionale Anforderungen F01–F11 (Kap. 6.1), nichtfunktionale Anforderungen N01–N06 (Kap. 6.2), Rahmenbedingungen (Kap. 7) | Version 1.0 vom 22.10.2026, Genehmigung durch den Auftraggeber ausstehend |
| D3 | Projektauftrag | Zielgrössen, Meilensteine, Planwerte | Version 0.4 vom 21.10.2026 (Referenz in PH Kap. 2) |
| D4 | Dokumentation des Entwicklungsteams (Benutzerhandbuch, Rollenbeschreibung, Release Notes) | Bedienung, Rollen, bekannte Einschränkungen | **noch anzufordern** [Annahme A1] |
| D5 | Antworten auf die offenen Fachfragen (Kapitel 1.5) | Berechnungsregeln, Rollen, Testzugänge | ausstehend |

Unklare oder fehlende Angaben klären wir mit dem Auftraggeber. Bis dahin halten wir Annahmen fest (AS S. 2, Ausgangslage Punkt 4; PH Kap. 7, Voraussetzungen).

### 1.4 Testziele

Das Pflichtenheft nennt die Zielgrössen aus dem Projektauftrag: mindestens 99 % korrekt gespeicherte gültige Eingaben, keine Berechnungsabweichungen in den geprüften Fällen, keine unberechtigten Zugriffe und nachvollziehbare Fehlermeldungen (PH Kap. 5). Daraus leiten wir messbare Testziele ab. Für jedes Ziel ist festgelegt, wann es erreicht ist.

| ID | Testziel (messbar) | Erfüllt, wenn … | Anforderungen | Prio |
|---|---|---|---|---|
| **TZ-1** | **Abrechnung korrekt:** Alle vereinbarten Referenzfälle für Vollzeit, Teilzeit, Abwesenheiten und Korrekturen liefern den Sollsaldo. | 100 % der Referenzfälle RF-01 bis RF-08 (siehe unten) ergeben Monatssumme, Projektsumme und Gleitzeitsaldo **auf die Minute genau** wie die manuelle Kontrollrechnung. 0 Berechnungsabweichungen. | F04, F05, F06, F02 | P1 |
| **TZ-2** | **Berechtigungen dicht:** Keine Rolle kann Daten sehen oder ändern, für die sie keine Berechtigung hat. | 100 % der Gegenversuche werden abgewiesen. Geprüft wird mit den Testkonten Mitarbeitende und Projektleitung, je über die Oberfläche **und** über eine direkt geänderte URL bzw. ID. 0 erfolgreiche unberechtigte Zugriffe. | F07, F08 | P1 |
| TZ-3 | **Gültige Eingaben werden korrekt gespeichert.** | Mindestens 99 % der gültigen Zeiteinträge und Korrekturen (mind. 30 Einträge) werden nach erneutem Öffnen unverändert und korrekt angezeigt. | F01, F02 | P1 |
| TZ-4 | **Fehleingaben verständlich und ohne Datenverlust.** | 100 % der definierten ungültigen Eingaben (mind. 10 Fälle, z. B. Ende vor Start, Überlappung, mehr als 24 h, leere Pflichtfelder) werden abgewiesen. Die Meldung nennt Feld und Ursache. In 0 Fällen gehen bereits gespeicherte Daten verloren. | F03, N05 | P1 |

TZ-1 und TZ-2 sind die beiden Kernziele aus dem Gruppenauftrag. TZ-3 und TZ-4 setzen die übrigen Zielgrössen aus PH Kap. 5 um.

**Referenzfälle für TZ-1** (Entwurf; die Sollwerte berechnen wir, sobald FF-1 bis FF-3 geklärt sind)

Das Pflichtenheft verlangt mindestens einen Teilzeitfall und einen Abwesenheitsfall (F06). Wir decken bewusst mehr ab, weil hier das höchste Risiko liegt (R1). Seltene, kombinierte Sonderfälle sind Ausbau (F11) und nur optional.

| Ref | Fall | Pensum | Prüft | Anforderung | Prio |
|---|---|---|---|---|---|
| RF-01 | Normaler Monat ohne Abwesenheiten | 100 % | Sollzeit, Monatssumme, Saldo | F05 | P1 |
| RF-02 | Normaler Monat ohne Abwesenheiten | 80 % | Teilzeit-Sollzeit | F06 | P1 |
| RF-03 | Normaler Monat ohne Abwesenheiten | 50 % | Teilzeit-Sollzeit | F06 | P1 |
| RF-04 | 1 Woche Ferien | 100 % | Abwesenheit | F06 | P1 |
| RF-05 | 1 Woche Ferien | 60 % | Abwesenheit bei Teilzeit | F06 | P1 |
| RF-06 | Monat mit Feiertagen (Dezember 2026: 25./26.12.) | 100 % und 80 % | Feiertagsgutschrift | F06 | P1 |
| RF-07 | Mehrere Einträge auf zwei Projekte | 100 % | Projektsumme | F04 | P1 |
| RF-08 | Nachträgliche Korrektur im laufenden Monat | 100 % | Korrektur in Saldo **und** Projektsumme | F02, F04, F05 | P1 |
| RF-09 | Pensumwechsel mitten im Monat (100 % → 60 %) | gemischt | anteilige Sollzeit | F11 | P3 |
| RF-10 | Korrektur in bereits abgeschlossenem Vormonat | 80 % | Übertrag, Monatsabschluss | F11 | P3 |
| RF-11 | Buchung über Mitternacht (22:00–02:00) | 100 % | Tageswechsel | F11 | P3 |

### 1.5 Offene Fachfragen

Diese Fragen müssen wir mit dem Auftraggeber klären, bevor wir die Sollwerte der Testfälle festlegen. Ohne Antwort wissen wir nicht, welches Ergebnis «richtig» ist (PH Kap. 4).

| ID | Offene Fachfrage | Warum wichtig | Betrifft | Annahme bis zur Klärung |
|---|---|---|---|---|
| **FF-1** | **Sollzeit und Rundung:** Wie hoch ist die tägliche Sollarbeitszeit bei 100 % (z. B. 8 h 24 min oder 8 h 30 min)? Wird auf 1, 5 oder 15 Minuten gerundet, und wann (pro Buchung, pro Tag oder pro Monat)? | Ohne diese Regel können wir keine Kontrollrechnung machen. Rundet das System pro Buchung statt pro Monat, kann das im Monat mehrere Stunden Unterschied ergeben. | TZ-1, F05, F06 | **[Annahme A2]** 42 h/Woche bei 100 % (8 h 24 min/Tag), minutengenaue Erfassung, keine Rundung. |
| **FF-2** | **Pausen:** Erfassen die Mitarbeitenden ihre Pausen selbst, oder werden sie automatisch abgezogen? Gilt eine Mindestpause, z. B. 30 Min. ab 7 h Arbeit (analog ArG Art. 15)? | Ein automatischer Abzug verändert jede Tagessumme und damit den Saldo. | TZ-1, F05 | **[Annahme A3]** Pausen werden manuell erfasst, kein automatischer Abzug. |
| **FF-3** | **Abwesenheiten bei Teilzeit:** Wie viele Stunden werden für Ferien, Krankheit oder Feiertage gutgeschrieben? Die volle Tagessollzeit oder die Sollzeit gemäss Pensum? Gibt es halbe Tage? Was gilt, wenn ein Feiertag auf einen freien Tag einer Teilzeitperson fällt? | Genau hier erwartet der Auftraggeber Probleme (AS S. 3, Erwartung 2). Das ist unser höchstes Risiko R1. | TZ-1, F06 | **[Annahme A4]** Gutschrift = Tagessollzeit × Pensum, halbe Tage sind möglich. Feiertage an freien Tagen werden nicht gutgeschrieben. |
| FF-4 | **Korrekturen:** Bis wann dürfen Mitarbeitende Zeiten rückwirkend ändern («im zulässigen Umfang», F02)? Wird ein Monat abgeschlossen? Wer darf danach noch korrigieren? | Ohne diese Regel wissen wir nicht, ob eine abgewiesene Korrektur ein Fehler oder korrektes Verhalten ist. | TZ-1, TZ-2, F02 | **[Annahme A5]** Eigene Korrekturen sind bis zum Monatsabschluss durch das Personalbüro möglich, danach nur noch durch das Personalbüro. |
| FF-5 | **Rollen und Rechte:** Was darf jede der vier Rollen genau sehen und ändern? Darf eine Projektleitung Zeiten ihrer Projektmitarbeitenden korrigieren? Sieht sie Abwesenheitsgründe wie Krankheit? | Grundlage für die Gegenversuche in TZ-2. Gesundheitsdaten sind besonders schützenswert. | TZ-2, F07, F08 | **[Annahme A6]** Die Rechte gelten wie in Kapitel 2.2 (TB-3) beschrieben. Die Projektleitung sieht nur Projektstunden, keine Abwesenheitsgründe, und kann nichts ändern. |
| FF-6 | **Testumgebung und Zugänge:** Welche Softwareversion ist installiert? Erhalten wir Testkonten für alle vier Rollen? Sind Pensen und Feiertagskalender bereits konfiguriert? | Ohne Zugänge können die Muss-Tests nicht starten. Sie würden als blockiert dokumentiert (PH Kap. 6). | alle | **[Annahme A1]** Zugänge und Dokumentation werden vor dem Teststart bereitgestellt. |

FF-1 bis FF-3 sind für die Abrechnung entscheidend und kommen zuerst. Wir schicken die Liste nach der Abgabe dieses Entwurfs an den Auftraggeber.

### 1.6 Annahmen

| ID | Annahme | Zu bestätigen durch |
|---|---|---|
| A1 | Das Entwicklungsteam stellt Softwareversion, Benutzerhandbuch, Rollenbeschreibung und Testkonten für alle vier Rollen bereit. | Auftraggeber / Entwicklungsteam (FF-6) |
| A2 | Die Sollzeit beträgt 42 h/Woche bei 100 %. Erfasst wird minutengenau, ohne Rundung. | Personalbüro (FF-1) |
| A3 | Pausen werden manuell erfasst, kein automatischer Abzug. | Personalbüro (FF-2) |
| A4 | Abwesenheitsgutschrift = Tagessollzeit × Pensum, halbe Tage möglich. | Personalbüro (FF-3) |
| A5 | Rückwirkende Korrekturen sind bis zum Monatsabschluss möglich, danach nur durch das Personalbüro. | Personalbüro (FF-4) |
| A6 | Es gibt die vier Rollen Mitarbeitende, Projektleitung, Entwicklungsleitung und Personalbüro, mit den Rechten gemäss TB-3. | Auftraggeber (FF-5) |
| A7 | Die Anwendung ist eine Webanwendung und läuft im Browser auf Desktop und Smartphone (keine native App). | Entwicklungsteam |

---

## 2 Testumfang und Nicht-Ziele

### 2.1 Testobjekt

Getestet wird das Zeiterfassungssystem in der bereitgestellten Testumgebung. Softwareversion, Build und Konfiguration (Pensen, Feiertagskalender, Rollen) halten wir beim Teststart fest, damit alle Ergebnisse nachvollziehbar sind (AS S. 2, Ausgangslage Punkt 6; PH Kap. 7, Voraussetzungen). Getestet wird nur mit fiktiven oder freigegebenen Personendaten (N03).

### 2.2 Testbereiche (im Testumfang)

Die Zuständigkeiten entsprechen der Rollenverteilung im Pflichtenheft (PH Kap. 7).

| ID | Testbereich | Was wir prüfen | Qualitätsmerkmal | Anforderungen | Verantwortlich | Prio |
|---|---|---|---|---|---|---|
| **TB-1** | **Zeiten erfassen und korrigieren** | Arbeitszeit auf Projekte buchen, nach erneutem Öffnen kontrollieren, ändern. Ungültige Eingaben und Grenzwerte: Ende vor Start, Überlappung, mehr als 24 h, 0 Minuten, leere Pflichtfelder. Bleiben gespeicherte Daten nach einer Fehleingabe erhalten? | Funktionalität, Fehlertoleranz | F01, F02, F03 | Ivano Pervan | P1 |
| **TB-2** | **Projekt- und Monatssummen, Teilzeit und Abwesenheiten** | Projektsumme, Monatsstunden und Gleitzeitsaldo gegen manuelle Kontrollrechnung, mit Referenzfällen RF-01 bis RF-08. Sollzeit nach Pensum, Ferien, Feiertage, Wirkung von Korrekturen auf alle Summen. | Funktionalität (Richtigkeit) | F04, F05, F06 | Sai Ragavan | P1 |
| **TB-3** | **Rollenrechte** | Mitarbeitende sehen und ändern nur eigene Daten. Projektleitung sieht nur Stunden ihrer Projekte, Entwicklungsleitung die Gesamtübersicht, Personalbüro Abrechnungen, Saldi und Abwesenheiten. Gegenversuche über die Oberfläche und über geänderte URL bzw. ID. | Sicherheit (Zugriffsschutz) | F07, F08 | Tom Nielsen | P1 |
| **TB-4** | **Nutzung unterwegs, im Homeoffice und parallel** | Eine Zeiterfassung auf einem zweiten Gerät (Smartphone) oder aus einem anderen Netzwerk. Zwei Testkonten speichern gleichzeitig. Verständlichkeit von Navigation, Beschriftungen und Fehlermeldungen. | Bedienbarkeit, Zuverlässigkeit | F09, F10, N05 | gemeinsam | P2 |

TB-1 bis TB-3 sind die Muss-Testgruppen und müssen für den Abschluss vollständig bearbeitet oder als blockiert dokumentiert sein (PH Kap. 7, Abschluss). TB-4 testen wir, soweit Zeit und Zugang reichen.

Für alle Bereiche gelten zusätzlich die Dokumentationsanforderungen: Jeder Testfall hat ID, Anforderung, Rolle, Testdaten, Soll- und Ist-Ergebnis, Status und Datum (N01). Jede Abweichung erhält einen reproduzierbaren Fehlerbericht (N02). Gelieferte Korrekturen werden nachgetestet (N04).

### 2.3 Nicht-Ziele (ausserhalb des Testumfangs)

Die Zeit bis 14.01.2027 ist knapp: zwei Lektionen pro Woche, dazu die Weihnachtsferien. Wir klammern deshalb bewusst Bereiche aus (AS S. 2, Ausgangslage Punkt 7). Für jedes Nicht-Ziel halten wir das Restrisiko fest. Es erscheint im Abschlussbericht.

| ID | Nicht-Ziel | Begründung | Restrisiko |
|---|---|---|---|
| **NZ-1** | **Fehler selbst beheben, Quellcode prüfen, neue Funktionen entwickeln** | Fehlerkorrekturen liegen laut Auftrag beim Entwicklungsteam (AS S. 3; PH Kap. 3). Wir testen als Black-Box ohne Quellcode-Audit (PH Kap. 7, Vorgehen). Würden wir selbst Code ändern, würden wir unsere eigenen Änderungen testen und wären nicht mehr unabhängig. | Gering. Fehler werden reproduzierbar gemeldet, und Korrekturen werden nachgetestet (N02, N04). Fehler im Code, die über die Oberfläche nicht sichtbar sind, finden wir nicht. |
| **NZ-2** | **Automatisierte Last- und Penetrationstests, umfassende Browser- und Gerätematrix** | Ist im Pflichtenheft als Ausbau ausgeschlossen (N06). Dafür fehlen Zeit, Spezialwerkzeuge und eine Erlaubnis des Betreibers. Die Firma hat nur rund 50 Mitarbeitende. Wir prüfen nur eine einfache Parallelnutzung (F10) und ein Zweitgerät (F09). | Mittel. Antwortzeiten unter Spitzenlast und Sicherheitslücken in der Infrastruktur bleiben ungetestet. Beides wird im Abschlussbericht offengelegt. |
| NZ-3 | **Umfangreiche kombinierte Abrechnungsvarianten und seltene Sonderfälle** (z. B. Pensumwechsel im Monat, Korrektur in abgeschlossenem Monat, Buchung über Mitternacht) | Ist im Pflichtenheft als Ausbau eingestuft (F11). Wir decken die häufigen Fälle vollständig ab (RF-01 bis RF-08). RF-09 bis RF-11 testen wir nur, wenn Zeit bleibt. | Mittel. Seltene Konstellationen können falsche Saldi liefern. Wir empfehlen, sie vor oder kurz nach der Einführung zu prüfen. |
| NZ-4 | **Firmenweite Einführung, Datenmigration und Schulung** | Wir liefern die *Entscheidungsgrundlage* für die Einführung, nicht die Einführung selbst (AS S. 2, Projektskizze; PH Kap. 5). | Mittel. Fehler bei der Übernahme alter Saldi werden nicht gefunden. Wir empfehlen einen Migrationstest vor dem Go-Live. |

Änderungen am Umfang stimmen wir mit dem Auftraggeber ab und halten sie in der Versionsgeschichte fest.

---

## 3 Risiken und Prioritäten

### 3.1 Bewertungsmethode

Wir bewerten Produktrisiken nachvollziehbar:

**Risikoscore = Wahrscheinlichkeit (W) × Schaden (S)**

| Wert | Wahrscheinlichkeit W | Schaden S |
|---|---|---|
| 1 | gering: nur in seltenen Sonderfällen | gering: kosmetisch, keine Auswirkung auf die Arbeit |
| 2 | mittel: kommt bei einem Teil der Benutzer vor | mittel: Mehraufwand, Workaround möglich |
| 3 | hoch: betrifft regelmässig viele Benutzer oder komplexe Logik | hoch: falsche Abrechnung, Datenverlust oder Datenschutzverletzung |

**Zuordnung zur Priorität** (P-Stufen entsprechen den Prioritäten im Pflichtenheft, PH Kap. 6)

| Priorität | Pflichtenheft | Score | Typische Inhalte | Vorgehen |
|---|---|---|---|---|
| **P1 zwingend** | Prio 1 Muss | 6–9 | Abrechnung, Berechtigungen, Datenerhalt | Früh testen, nach jeder Korrektur erneut prüfen (Regression). |
| **P2 wichtig** | Prio 2 Kann | 3–4 | Bedienbarkeit, Zweitgerät, Parallelnutzung | Nach P1 testen. Bei hohem Betriebsrisiko auf P1 hochstufen. |
| **P3 nachrangig** | Prio 3 Ausbau | 1–2 | Kosmetische Details, seltene Sonderfälle | Bei Engpässen zurückstellen und Restrisiko festhalten. |

Die Prioritäten sind ein Vorschlag. Am Ende entscheidet das Risiko im konkreten Projekt. Wo wir abweichen, begründen wir es.

### 3.2 Produktrisiken

Werte mit **[Annahme]** beruhen auf unserer Einschätzung. Wir prüfen sie nach dem Gespräch mit dem Auftraggeber.

| ID | Möglicher Fehler | W | S | Score | Prio | Begründung | Bereich / Anf. |
|---|---|:-:|:-:|:-:|:-:|---|---|
| **R1** | **Teilzeitpensum erzeugt einen falschen Gleitzeitsaldo** (Sollzeit oder Abwesenheit wird mit 100 % statt mit dem Pensum gerechnet) | 3 | 3 | **9** | **P1** | W=3: Teilzeit zusammen mit Abwesenheiten ist die komplexeste Rechenlogik, und die Regeln sind noch unklar (FF-1, FF-3). Der Auftraggeber nennt sie ausdrücklich (AS S. 3). S=3: Falsche Saldi wirken direkt auf Lohn und Ferien. **[Annahme]** Ein grosser Teil der 50 Mitarbeitenden arbeitet Teilzeit. | TB-2, F06 |
| **R2** | **Eine Rolle kann fremde Arbeitszeiten oder Personaldaten einsehen oder verändern** (z. B. über eine geänderte ID in der URL, oder die Projektleitung sieht Krankheitsabwesenheiten) | 2 | 3 | **6** | **P1** | W=2: Das Entwicklungsteam hat vermutlich die Oberfläche getestet, aber kaum direkte Zugriffe über URL oder ID. S=3: Verletzung des Datenschutzes (Gesundheitsdaten sind nach DSG besonders schützenswert) und mögliche Manipulation der Abrechnung. | TB-3, F07, F08 |
| **R3** | **Eine nachträgliche Korrektur fehlt in der Projekt- oder Monatssumme** (der Saldo wird nachgeführt, die Projektsumme nicht, oder umgekehrt) | 2 | 3 | **6** | **P1** | W=2: Eine Korrektur muss mehrere Summen gleichzeitig nachführen, eine typische Fehlerquelle. Der Auftraggeber nennt Korrekturen ausdrücklich. S=3: Falsche Projektabrechnung gegenüber Kunden und falsche Monatsabrechnung. | TB-1, TB-2, F02, F04 |
| **R4** | **Bereits gespeicherte Daten gehen bei einer Fehleingabe verloren** (z. B. die ganze Woche wird verworfen, oder ein Eintrag wird doppelt gespeichert) | 2 | 3 | **6** | **P1** | W=2: Fehlerbehandlung wird oft nur für den Normalfall gebaut. S=3: Datenverlust führt zu falschen Abrechnungen und Vertrauensverlust. Der Auftraggeber verlangt ausdrücklich, dass keine Daten verloren gehen (AS S. 3, Erwartung 4). | TB-1, F03 |
| R5 | **Feiertage werden falsch gutgeschrieben** (z. B. ein Feiertag am freien Tag einer 80-%-Person) | 2 | 3 | **6** | P1 | W=2: Kommt nur an einigen Tagen vor, im Testzeitraum aber real (Weihnachten, Neujahr). Die Regel ist unklar (FF-3). S=3: Wirkt direkt auf den Saldo. **[Annahme]** Im System ist ein Feiertagskalender hinterlegt. | TB-2, F06 |
| R6 | **Fehlermeldungen sind unverständlich** oder werden auf dem Smartphone abgeschnitten, sodass niemand weiss, was falsch ist | 2 | 2 | 4 | P2 | W=2: Meldungen werden oft nur auf dem Desktop geprüft. S=2: Mehraufwand und Frust, aber keine falschen Daten, solange die Eingabe abgewiesen wird. | TB-4, N05 |
| R7 | **Gleichzeitiges Speichern führt zu Fehlern** (Einträge überschreiben sich, oder die Anwendung wird langsam) | 1 | 3 | 3 | P2 | W=1: Bei rund 50 Mitarbeitenden ist die Last klein. S=3: Falls dabei Daten überschrieben werden, wäre die Abrechnung falsch. Wir prüfen nur einen einfachen Paralleltest (F10). Automatisierte Lasttests sind ausgeschlossen (N06). | TB-4, F10 |
| R8 | **Kosmetische Darstellungsfehler** (Ausrichtung, Schriftgrösse, Tippfehler) | 2 | 1 | 2 | P3 | W=2: In neuen Anwendungen häufig. S=1: Kein Einfluss auf die Arbeit. Wird bei Zeitmangel zurückgestellt und im Bericht festgehalten. | TB-4 |

**Risikomatrix (Übersicht)**

| W \ S | S=1 gering | S=2 mittel | S=3 hoch |
|---|---|---|---|
| **W=3 hoch** | | | **R1** (9) |
| **W=2 mittel** | R8 (2) | R6 (4) | **R2, R3, R4, R5** (6) |
| **W=1 gering** | | | R7 (3) |

### 3.3 Projektrisiken

Diese Risiken betreffen nicht die Software, sondern unser Testvorhaben.

| ID | Risiko | W | S | Score | Massnahme |
|---|---|:-:|:-:|:-:|---|
| PR1 | Die Fachfragen FF-1 bis FF-3 werden nicht rechtzeitig beantwortet. Ohne Sollwerte können wir TZ-1 nicht prüfen. | 2 | 3 | 6 | Fragen sofort stellen und einen Antworttermin vereinbaren. Bis dahin mit markierten Annahmen arbeiten. |
| PR2 | Mit zwei Lektionen pro Woche und den Weihnachtsferien (ca. 21.12.2026–03.01.2027) ist die Zeit bis 14.01.2027 knapp. Auch das Entwicklungsteam ist in den Ferien abwesend. | 3 | 2 | 6 | P1-Tests bis zum Zwischenstand am 18.12.2026 abschliessen. Januar für Nachtests reservieren. |
| PR3 | Testzugänge für alle vier Rollen fehlen, oder die Testumgebung wird ohne Absprache geändert. | 2 | 2 | 4 | Zugänge früh anfordern (FF-6). Version beim Teststart festhalten. Fehlende Zugänge als blockiert dokumentieren (PH Kap. 6). |
| PR4 | Ein Teammitglied fällt aus (3 Tester, wenig Reserve). | 1 | 2 | 2 | Testfälle so dokumentieren, dass jedes Teammitglied sie ausführen kann (N01). |

### 3.4 Prioritäten für das Testvorgehen

Daraus ergibt sich die Reihenfolge der Tests. Wie vom Auftraggeber verlangt, testen wir zuerst die Abläufe, deren Ausfall Betrieb oder Abrechnung am stärksten beeinträchtigen würde (AS S. 3, Erwartung 6).

| Reihenfolge | Priorität | Risiken | Testbereiche | Vorgehen |
|---|---|---|---|---|
| 1 | **P1 zwingend (Muss)** | R1, R2, R3, R4, R5 | TB-2, TB-3, TB-1 | Bis 18.12.2026 vollständig testen. Kritische Fehler sofort melden. Nach jeder Korrektur Nachtest und Regression der P1-Fälle (N04). |
| 2 | **P2 wichtig (Kann)** | R6, R7 | TB-4 | Nach P1, soweit Zeit und Zugang reichen. Falls bei R7 Daten überschrieben werden, wie P1 behandeln. |
| 3 | P3 nachrangig (Ausbau) | R8, Sonderfälle RF-09 bis RF-11 | TB-2, TB-4 | Nur wenn Zeit bleibt. Sonst als nicht getesteter Bereich im Abschlussbericht. |

---

## 4 Teststrategie

*Wird in der nächsten Lektion ergänzt.*

Bereits festgelegt (PH Kap. 7): risikobasierte, manuelle Black-Box-Tests mit gültigen und ungültigen Eingaben, Grenzwerten, Kontrollrechnungen und Rollen-Gegenproben. Werkzeuge: Microsoft Excel (Testfälle, Protokolle, Fehlerliste), Microsoft Word (Berichte), Browser und Bildschirmaufnahmen.

Noch zu ergänzen: Teststufen, Testmethoden pro Testbereich (Äquivalenzklassen, Grenzwertanalyse, Entscheidungstabelle für Pensum und Abwesenheit, Berechtigungsmatrix) und eine Begründung, warum wir nicht automatisieren.

## 5 Organisation und Umgebung

*Wird ergänzt.*

Bereits festgelegt (PH Kap. 7): Paulo Capelos Viana (Projektleitung), Ivano Pervan (Zeiterfassung und Korrektur), Sai Ragavan (Abrechnung und Teilzeit), Tom Nielsen (Rollenrechte und Fehlerberichte). Dokumentation und Nachtests machen wir gemeinsam.

Noch zu ergänzen: Testumgebung, Softwareversion, Testkonten, Testdaten, Geräte und Browser.

## 6 Aktivitäten und Zeitplanung

*Wird ergänzt.*

Meilensteine (PH Kap. 7): Testkonzept und Testfälle bis 20.11.2026, Testdurchführung und Zwischenstandsbericht bis 18.12.2026, Re-Tests und Abschlussbericht bis 14.01.2027.

## 7 Eintritts- und Abschlusskriterien

*Wird ergänzt.*

Bereits festgelegt (PH Kap. 7):

- **Eintritt:** Testumgebung freigegeben, Softwareversion und Konfiguration bekannt, Testkonten für alle vier Rollen, Testdaten für Pensen und Abwesenheiten vorhanden.
- **Abschluss:** Alle Muss-Testgruppen sind bearbeitet oder als blockiert dokumentiert. Gefundene Fehler sind reproduzierbar erfasst, gemeldete Behebungen erneut geprüft. Kritische offene Fehler verhindern eine vorbehaltlose Freigabeempfehlung.

## 8 Ergebnisse und Berichterstattung

*Wird ergänzt.*

Geplant: Testprotokolle und Fehlerliste in Excel, Fehlerberichte mit Schweregrad und Behebungspriorität (N02), Zwischenstandsbericht (18.12.2026), Abschlussbericht mit Testabdeckung, offenen Fehlern, Restrisiken, nicht getesteten Bereichen und Freigabeempfehlung (14.01.2027).

---

## Anhang A: Anforderungen und Fundstellen

Diese Tabelle verbindet jede Anforderung aus unserem Pflichtenheft (PH) mit ihrer Fundstelle und der Erwartung des Auftraggebers in der Aufgabenstellung (AS). Sie zeigt auch, wo die Anforderung in diesem Testkonzept verwendet wird.

### A.1 Funktionale Anforderungen (PH Kap. 6.1)

| ID | Prio PH | Anforderung (Kurzform) | Fundstelle PH | Ursprung AS | Testkonzept |
|---|---|---|---|---|---|
| F01 | Muss | Gültiger Zeiteintrag wird gespeichert und nach erneutem Öffnen korrekt angezeigt. | Kap. 6.1, F01 | S. 2, Ausgangslage Pkt. 1; S. 3, Erw. 1 | TZ-3, TB-1 |
| F02 | Muss | Zeiteintrag lässt sich im zulässigen Umfang korrigieren, der neue Wert wird übernommen. | Kap. 6.1, F02 | S. 3, Erw. 2 | TZ-1, TZ-3, TB-1, R3 |
| F03 | Muss | Unzulässiger Zeitwert wird abgewiesen oder verständlich beanstandet, gespeicherte Daten bleiben erhalten. | Kap. 6.1, F03 | S. 3, Erw. 4 | TZ-4, TB-1, R4 |
| F04 | Muss | Projektsumme entspricht dem berechneten Sollwert. | Kap. 6.1, F04 | S. 2, Ausgangslage Pkt. 1; S. 3, Erw. 2 | TZ-1, TB-2, R3 |
| F05 | Muss | Monatsstunden stimmen mit der manuellen Kontrollrechnung überein. | Kap. 6.1, F05 | S. 2, Ausgangslage Pkt. 2; S. 3, Erw. 2 | TZ-1, TB-2 |
| F06 | Muss | Teilzeitfall und Abwesenheitsfall liefern die erwarteten Monats- und Gleitzeitwerte. | Kap. 6.1, F06 | S. 2, Ausgangslage Pkt. 2; S. 3, Erw. 2 | TZ-1, TB-2, R1, R5 |
| F07 | Muss | Mitarbeitenden-Konto kann keine fremden Personal- oder Zeitdaten einsehen oder ändern. | Kap. 6.1, F07 | S. 2, Ausgangslage Pkt. 3; S. 3, Erw. 3 | TZ-2, TB-3, R2 |
| F08 | Muss | Projektleitung sieht berechtigte Projektstunden, Gegenversuch auf nicht berechtigte Daten. | Kap. 6.1, F08 | S. 2, Ausgangslage Pkt. 1 und 3; S. 3, Erw. 3 | TZ-2, TB-3, R2 |
| F09 | Kann | Erfassung auf einem zweiten Gerät oder aus einem anderen Netzwerk. | Kap. 6.1, F09 | S. 2, Ausgangslage Pkt. 3; S. 3, Erw. 1 | TB-4 |
| F10 | Kann | Zwei Testkonten führen gleichzeitig einen Vorgang aus. | Kap. 6.1, F10 | S. 3, Erw. 5 | TB-4, R7 |
| F11 | Ausbau | Kombinierte Abrechnungsvarianten und seltene Sonderfälle werden nicht vollständig untersucht. | Kap. 6.1, F11 | S. 2, Ausgangslage Pkt. 7 | NZ-3, RF-09 bis RF-11 |

### A.2 Nichtfunktionale Anforderungen (PH Kap. 6.2)

| ID | Prio PH | Anforderung (Kurzform) | Fundstelle PH | Ursprung AS | Testkonzept |
|---|---|---|---|---|---|
| N01 | Muss | Jeder Testfall hat ID, Anforderung, Rolle, Testdaten, Soll/Ist, Status, Datum. | Kap. 6.2, N01 | S. 3, Aufgabe | Kap. 2.2, PR4 |
| N02 | Muss | Jede Abweichung erhält Fehler-ID, Reproduktionsschritte, Soll/Ist, Schweregrad, Behebungspriorität. | Kap. 6.2, N02 | S. 3, Erw. 7; S. 3, Aufgabe | Kap. 2.2, Kap. 8 |
| N03 | Muss | Test nur mit freigegebenen bzw. fiktiven Personendaten. | Kap. 6.2, N03 | S. 2, Ausgangslage Pkt. 6 | Kap. 2.1 |
| N04 | Muss | Gelieferte Korrekturen werden nachgetestet, benachbarte Abläufe bei Bedarf mitgeprüft. | Kap. 6.2, N04 | S. 3, Aufgabe | Kap. 3.4, NZ-1 |
| N05 | Kann | Verständlichkeit von Navigation, Beschriftungen und Fehlermeldungen. | Kap. 6.2, N05 | S. 3, Erw. 1 und 4 | TZ-4, TB-4, R6 |
| N06 | Ausbau | Keine automatisierten Lasttests, Penetrationstests und keine umfassende Browser-/Gerätematrix. | Kap. 6.2, N06 | S. 2, Ausgangslage Pkt. 5 und 7 | NZ-2 |

---

### Versionsgeschichte

| Version | Datum | Änderung | Name |
|---|---|---|---|
| 0.1 | 19.11.2026 | Gliederung mit 8 Kapiteln erstellt, Kapitel 1–3 befüllt | Projektteam |
| 0.2 | 19.11.2026 | An Pflichtenheft STZ-PH-01 v1.0 angepasst: Anforderungs-IDs F01–N06 mit Fundstellen, Prioritäten Muss/Kann/Ausbau, Zuständigkeiten, Meilensteine, Testziele gemäss PH Kap. 5 | Projektteam |
