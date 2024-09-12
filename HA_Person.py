import json
from tkinter import *
import os

# Definiert die Klasse Student, die die Attribute und Methoden für die Studenten verwaltet
class Student:
    def __init__(self, vorname, geschlecht, alter, fachrichtung):
        self.__vorname = vorname  # Initialisiert den Vornamen
        self.__geschlecht = geschlecht  # Initialisiert das Geschlecht
        self.__alter = alter  # Initialisiert das Alter
        self.__fachrichtung = fachrichtung  # Initialisiert die Fachrichtung
    
    def hat_geburtstag(self):
        self.__alter += 1  # Erhöht das Alter um 1
        return self.__alter  # Gibt das neue Alter zurück
    
    def fachrichtung_wechseln(self, neue_fachrichtung):
        alte_fachrichtung = self.__fachrichtung  # Speichert die alte Fachrichtung
        self.__fachrichtung = neue_fachrichtung  # Setzt die neue Fachrichtung
        return alte_fachrichtung, neue_fachrichtung  # Gibt alte und neue Fachrichtung zurück
    
    @property
    def vorname(self):
        return self.__vorname  # Gibt den Vornamen zurück
    
    @vorname.setter
    def vorname(self, value):
        self.__vorname = value  # Setzt den Vornamen

    @property
    def geschlecht(self):
        return self.__geschlecht  # Gibt das Geschlecht zurück
    
    @geschlecht.setter
    def geschlecht(self, value):
        self.__geschlecht = value  # Setzt das Geschlecht

    @property
    def alter(self):
        return self.__alter  # Gibt das Alter zurück
    
    @alter.setter
    def alter(self, value):
        self.__alter = value  # Setzt das Alter

    @property
    def fachrichtung(self):
        return self.__fachrichtung  # Gibt die Fachrichtung zurück
    
    @fachrichtung.setter
    def fachrichtung(self, value):
        self.__fachrichtung = value  # Setzt die Fachrichtung
    
    def __str__(self):
        # Gibt eine string-Repräsentation des Studenten zurück
        return (f"Student: {self.__vorname}, Geschlecht: {self.__geschlecht}, "
                f"Alter: {self.__alter}, Fachrichtung: {self.__fachrichtung}")

    def to_dict(self):
        # Gibt die Attribute des Studenten als Dictionary zurück
        return {
            "vorname": self.__vorname,
            "geschlecht": self.__geschlecht,
            "alter": self.__alter,
            "fachrichtung": self.__fachrichtung
        }

    def from_dict(self, data):
        # Setzt die Attribute des Studenten aus einem Dictionary
        self.__vorname = data["vorname"]
        self.__geschlecht = data["geschlecht"]
        self.__alter = data["alter"]
        self.__fachrichtung = data["fachrichtung"]

# Definiert die Klasse StudentManager zur Verwaltung der Studenten
class StudentManager:
    def __init__(self):
        self.students = []  # Liste der Studenten
        self.current_index = 0  # Aktueller Index des Studenten
        self.current_student = None  # Der derzeit ausgewählte Student

    def load_from_file(self):
        # Lädt die Studentendaten aus einer Datei
        if os.path.exists("student_data.json"):  # Überprüft, ob die Datei existiert
            with open("student_data.json", "r") as file:
                data = json.load(file)  # Liest die Datei
                self.students = [Student(**item) for item in data]  # Erstellt Studentenobjekte
                self.current_student = self.students[0] if self.students else None  # Setzt den aktuellen Studenten

    def save_to_file(self):
        # Speichert die Studentendaten in eine Datei
        with open("student_data.json", "w") as file:
            json.dump([student.to_dict() for student in self.students], file)  # Schreibt die Daten in die Datei

    def add_student(self, student):
        # Fügt einen neuen Studenten zur Liste hinzu
        self.students.append(student)
        self.current_index = len(self.students) - 1  # Setzt den Index auf den letzten Student
        self.current_student = self.students[self.current_index]  # Setzt den aktuellen Studenten

    def delete_student(self):
        # Löscht den aktuellen Studenten aus der Liste
        if self.current_student:
            self.students.pop(self.current_index)  # Entfernt den Studenten
            if len(self.students) == 0:
                self.current_student = None
                self.current_index = 0
            else:
                self.current_index = min(self.current_index, len(self.students) - 1)  # Setzt den Index auf den letzten verbleibenden Student
                self.current_student = self.students[self.current_index]  # Setzt den aktuellen Studenten

    def get_current_student(self):
        return self.current_student  # Gibt den aktuellen Studenten zurück

    def get_next_student(self):
        # Gibt den nächsten Studenten zurück
        if self.students:
            self.current_index = (self.current_index + 1) % len(self.students)  # Erhöht den Index
            self.current_student = self.students[self.current_index]  # Setzt den aktuellen Studenten
            return self.current_student

    def get_prev_student(self):
        # Gibt den vorherigen Studenten zurück
        if self.students:
            self.current_index = (self.current_index - 1) % len(self.students)  # Verringert den Index
            self.current_student = self.students[self.current_index]  # Setzt den aktuellen Studenten
            return self.current_student

    def update_student(self, vorname, geschlecht, alter, fachrichtung):
        # Aktualisiert die Daten des aktuellen Studenten
        if self.current_student:
            self.current_student.vorname = vorname
            self.current_student.geschlecht = geschlecht
            self.current_student.alter = alter
            self.current_student.fachrichtung = fachrichtung

# Initialisiert den StudentManager und lädt Daten
student_manager = StudentManager()
student_manager.load_from_file()

# Erstellt einige Test-Studenten
susi = Student("Susi", "weiblich", 22, "Technik")
benno = Student("Benno", "männlich", 24, "Management")

# Führt einige Methoden für Testzwecke aus
benno.hat_geburtstag()
benno.hat_geburtstag()
susi.fachrichtung_wechseln("Organisation")

# Fügt die Test-Studenten zur Liste hinzu
student_manager.add_student(susi)
student_manager.add_student(benno)

def aktualisiere_student_info():
    # Aktualisiert die Anzeige der Studentendaten
    current_student = student_manager.get_current_student()
    if current_student:
        text_widget.delete(1.0, END)  # Löscht den aktuellen Text im Text-Widget
        text_widget.insert(INSERT, f"Student: ", "title")  # Fügt den Titel ein
        text_widget.insert(INSERT, f"{current_student.vorname}\n", "name")  # Fügt den Vornamen ein
        text_widget.insert(INSERT, f"Geschlecht: ", "label")  # Fügt das Label für das Geschlecht ein
        text_widget.insert(INSERT, f"{current_student.geschlecht}\n", "geschlecht")  # Fügt das Geschlecht ein
        text_widget.insert(INSERT, f"Alter: ", "label")  # Fügt das Label für das Alter ein
        text_widget.insert(INSERT, f"{current_student.alter}\n", "alter")  # Fügt das Alter ein
        text_widget.insert(INSERT, f"Fachrichtung: ", "label")  # Fügt das Label für die Fachrichtung ein
        text_widget.insert(INSERT, f"{current_student.fachrichtung}", "fachrichtung")  # Fügt die Fachrichtung ein
        
        # Aktualisiert die Eingabefelder mit den Daten des aktuellen Studenten
        entry_edit_vorname.delete(0, END)
        entry_edit_vorname.insert(0, current_student.vorname)
        entry_edit_geschlecht.delete(0, END)
        entry_edit_geschlecht.insert(0, current_student.geschlecht)
        entry_edit_alter.delete(0, END)
        entry_edit_alter.insert(0, str(current_student.alter))
        entry_edit_fachrichtung.delete(0, END)
        entry_edit_fachrichtung.insert(0, current_student.fachrichtung)

def geburtstag_feiern():
    # Feiern den Geburtstag des aktuellen Studenten
    current_student = student_manager.get_current_student()
    if current_student:
        neues_alter = current_student.hat_geburtstag()  # Erhöht das Alter
        text_widget.delete(1.0, END)  # Löscht den aktuellen Text im Text-Widget
        aktualisiere_student_info()  # Aktualisiert die Anzeige
        text_widget.insert(END, f"\n{current_student.vorname} hat Geburtstag! Alter: {neues_alter}", "info")  # Fügt eine Geburtstagsnachricht hinzu

def fachrichtung_aendern():
    current_student = student_manager.get_current_student()
    if current_student:
        alte_fachrichtung, neue_fachrichtung = current_student.fachrichtung_wechseln(neue_fachrichtung)  # Wechselt die Fachrichtung
        text_widget.insert(END, f"\n{current_student.vorname} hat die Fachrichtung gewechselt von {alte_fachrichtung} zu {neue_fachrichtung}", "info")  # Fügt eine Nachricht hinzu
        aktualisiere_student_info()  # Aktualisiert die Anzeige

def add_student():
    # Fügt einen neuen Studenten hinzu
    vorname = entry_new_vorname.get()  # Holt den Vornamen aus dem Eingabefeld
    geschlecht = entry_new_geschlecht.get()  # Holt das Geschlecht aus dem Eingabefeld
    alter = entry_new_alter.get()  # Holt das Alter aus dem Eingabefeld
    fachrichtung = entry_new_fachrichtung.get()  # Holt die Fachrichtung aus dem Eingabefeld
    
    if vorname and geschlecht and alter and fachrichtung:
        new_student = Student(vorname, geschlecht, int(alter), fachrichtung)  # Erstellt einen neuen Studenten
        student_manager.add_student(new_student)  # Fügt den neuen Studenten zur Liste hinzu
        aktualisiere_student_info()  # Aktualisiert die Anzeige
    else:
        print("Bitte füllen Sie alle Felder aus.")  # Fehlermeldung, wenn nicht alle Felder ausgefüllt sind

def delete_student():
    # Löscht den aktuellen Studenten
    student_manager.delete_student()  # Entfernt den aktuellen Studenten
    aktualisiere_student_info()  # Aktualisiert die Anzeige

def save_and_close():
    # Speichert die Daten und schließt das Fenster
    student_manager.save_to_file()  # Speichert die Studentendaten
    tkFenster.destroy()  # Schließt das Fenster

def next_student():
    # Wechselt zum nächsten Studenten
    student_manager.get_next_student()  # Holt den nächsten Studenten
    aktualisiere_student_info()  # Aktualisiert die Anzeige

def prev_student():
    # Wechselt zum vorherigen Studenten
    student_manager.get_prev_student()  # Holt den vorherigen Studenten
    aktualisiere_student_info()  # Aktualisiert die Anzeige

def edit_student():
    # Bearbeitet die Daten des aktuellen Studenten
    if student_manager.get_current_student():
        vorname = entry_edit_vorname.get()  # Holt den neuen Vornamen aus dem Eingabefeld
        geschlecht = entry_edit_geschlecht.get()  # Holt das neue Geschlecht aus dem Eingabefeld
        alter = entry_edit_alter.get()  # Holt das neue Alter aus dem Eingabefeld
        fachrichtung = entry_edit_fachrichtung.get()  # Holt die neue Fachrichtung aus dem Eingabefeld
        
        if vorname and geschlecht and alter and fachrichtung:
            student_manager.update_student(vorname, geschlecht, int(alter), fachrichtung)  # Aktualisiert die Daten des aktuellen Studenten
            aktualisiere_student_info()  # Aktualisiert die Anzeige
        else:
            print("Bitte füllen Sie alle Felder aus.")  # Fehlermeldung, wenn nicht alle Felder ausgefüllt sind

# Initialisiert das Hauptfenster von Tkinter
tkFenster = Tk()
tkFenster.title("Studentenverwaltung")  # Setzt den Titel des Fensters
tkFenster.configure(bg="light blue")  # Setzt die Hintergrundfarbe des Fensters

# Erstellt ein Text-Widget zur Anzeige von Studentendaten
text_widget = Text(tkFenster, wrap=WORD, height=6, width=80, bg="light blue", fg="black", font=("Helvetica", 16))
text_widget.pack(padx=10, pady=10)  # Fügt das Text-Widget dem Fenster hinzu
text_widget.tag_configure("title", font=("Helvetica", 16, "bold"))  # Konfiguriert den Titel-Stil
text_widget.tag_configure("name", foreground="green")  # Konfiguriert den Namen-Stil
text_widget.tag_configure("label", foreground="black")  # Konfiguriert den Label-Stil
text_widget.tag_configure("geschlecht", foreground="purple")  # Konfiguriert den Geschlecht-Stil
text_widget.tag_configure("alter", foreground="orange")  # Konfiguriert den Alter-Stil
text_widget.tag_configure("fachrichtung", foreground="blue")  # Konfiguriert den Fachrichtung-Stil
text_widget.tag_configure("info", foreground="red")  # Konfiguriert den Info-Stil

# Erstellt ein Frame für die Schaltflächen
frame = Frame(master=tkFenster, bg="light blue")
frame.pack(padx=10, pady=10, fill=X)  # Fügt das Frame dem Fenster hinzu

# Erstellt eine Schaltfläche, um den Geburtstag des aktuellen Studenten zu feiern
btn_geburtstag = Button(master=frame, text="Geburtstag feiern", command=geburtstag_feiern, bg="green", fg="white")
btn_geburtstag.grid(row=0, column=0, padx=5, pady=5, sticky=W)  # Platziert die Schaltfläche im Grid

# Erstellt Schaltflächen zum Wechseln zwischen vorherigem und nächstem Studenten
btn_prev = Button(master=frame, text="< Vorherige", command=prev_student, bg="blue", fg="white")
btn_prev.grid(row=2, column=0, padx=5, pady=5, sticky=W)

btn_next = Button(master=frame, text="Nächste >", command=next_student, bg="blue", fg="white")
btn_next.grid(row=2, column=1, padx=5, pady=5, sticky=W)

# Erstellt ein Frame für die Eingabefelder zur Hinzufügung eines neuen Studenten
frame_add_student = Frame(master=tkFenster, bg="light blue")
frame_add_student.pack(padx=10, pady=10, fill=X)

# Erstellt Eingabefelder und Labels für die Hinzufügung eines neuen Studenten
Label(master=frame_add_student, text="Neuer Vorname:", bg="light blue", foreground="green").grid(row=0, column=0, padx=5, pady=5, sticky=W)
entry_new_vorname = Entry(master=frame_add_student, width=20)
entry_new_vorname.grid(row=0, column=1, padx=5, pady=5, sticky=W)

Label(master=frame_add_student, text="Geschlecht:", bg="light blue", foreground="purple").grid(row=1, column=0, padx=5, pady=5, sticky=W)
entry_new_geschlecht = Entry(master=frame_add_student, width=20)
entry_new_geschlecht.grid(row=1, column=1, padx=5, pady=5, sticky=W)

Label(master=frame_add_student, text="Alter:", bg="light blue", foreground="orange").grid(row=2, column=0, padx=5, pady=5, sticky=W)
entry_new_alter = Entry(master=frame_add_student, width=20)
entry_new_alter.grid(row=2, column=1, padx=5, pady=5, sticky=W)

Label(master=frame_add_student, text="Fachrichtung:", bg="light blue", foreground="blue").grid(row=3, column=0, padx=5, pady=5, sticky=W)
entry_new_fachrichtung = Entry(master=frame_add_student, width=20)
entry_new_fachrichtung.grid(row=3, column=1, padx=5, pady=5, sticky=W)

# Erstellt eine Schaltfläche zum Hinzufügen eines neuen Studenten
btn_add_student = Button(master=frame_add_student, text="Student hinzufügen", command=add_student, bg="green", fg="white")
btn_add_student.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

# Erstellt ein Frame für die Eingabefelder zur Bearbeitung eines Studenten
frame_edit_student = Frame(master=tkFenster, bg="light blue")
frame_edit_student.pack(padx=10, pady=10, fill=X)

# Erstellt Eingabefelder und Labels für die Bearbeitung eines Studenten
Label(master=frame_edit_student, text="Vorname:", bg="light blue", foreground="green").grid(row=0, column=0, padx=5, pady=5, sticky=W)
entry_edit_vorname = Entry(master=frame_edit_student, width=20)
entry_edit_vorname.grid(row=0, column=1, padx=5, pady=5, sticky=W)

Label(master=frame_edit_student, text="Geschlecht:", bg="light blue", foreground="purple").grid(row=1, column=0, padx=5, pady=5, sticky=W)
entry_edit_geschlecht = Entry(master=frame_edit_student, width=20)
entry_edit_geschlecht.grid(row=1, column=1, padx=5, pady=5, sticky=W)

Label(master=frame_edit_student, text="Alter:", bg="light blue", foreground="orange").grid(row=2, column=0, padx=5, pady=5, sticky=W)
entry_edit_alter = Entry(master=frame_edit_student, width=20)
entry_edit_alter.grid(row=2, column=1, padx=5, pady=5, sticky=W)

Label(master=frame_edit_student, text="Fachrichtung:", bg="light blue", foreground="blue").grid(row=3, column=0, padx=5, pady=5, sticky=W)
entry_edit_fachrichtung = Entry(master=frame_edit_student, width=20)
entry_edit_fachrichtung.grid(row=3, column=1, padx=5, pady=5, sticky=W)

# Erstellt eine Schaltfläche zur Bearbeitung eines Studenten
btn_edit_student = Button(master=frame_edit_student, text="Student bearbeiten", command=edit_student, bg="orange", fg="white")
btn_edit_student.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

# Erstellt eine Schaltfläche zum Löschen eines Studenten
btn_delete_student = Button(master=frame_edit_student, text="Student löschen", command=delete_student, bg="red", fg="white")
btn_delete_student.grid(row=5, column=0, padx=5, pady=5, columnspan=2)

# Erstellt eine Schaltfläche zum Speichern und Schließen des Fensters
btn_save_close = Button(master=tkFenster, text="Speichern und Schließen", command=save_and_close, bg="purple", fg="white")
btn_save_close.pack(pady=10)

# Aktualisiert die Anzeige mit den aktuellen Studentendaten
aktualisiere_student_info()

# Startet die Haupt-Event-Schleife von Tkinter
tkFenster.mainloop()
