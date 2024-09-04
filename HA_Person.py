import json
from tkinter import *
import os

class Person:
    def __init__(self, vorname, name, geburtsdatum, wohnort):
        self.__vorname = vorname
        self.__name = name
        self.__geburtsdatum = geburtsdatum
        self.__wohnort = wohnort
    
    def name_aendern(self, neuer_vorname, neuer_name):
        self.__vorname = neuer_vorname
        self.__name = neuer_name
    
    def umziehen(self, neuer_wohnort):
        self.__wohnort = neuer_wohnort
    
    def geburtsdatum_aendern(self, neues_geburtsdatum):
        self.__geburtsdatum = neues_geburtsdatum
    
    @property
    def vorname(self):
        return self.__vorname
    
    @vorname.setter
    def vorname(self, value):
        self.__vorname = value

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def geburtsdatum(self):
        return self.__geburtsdatum
    
    @geburtsdatum.setter
    def geburtsdatum(self, value):
        self.__geburtsdatum = value

    @property
    def wohnort(self):
        return self.__wohnort
    
    @wohnort.setter
    def wohnort(self, value):
        self.__wohnort = value
    
    def __str__(self):
        return (f"Person: {self.__vorname} {self.__name}, "
                f"geboren am {self.__geburtsdatum}, wohnt in {self.__wohnort}")

    def to_dict(self):
        return {
            "vorname": self.__vorname,
            "name": self.__name,
            "geburtsdatum": self.__geburtsdatum,
            "wohnort": self.__wohnort
        }

    def from_dict(self, data):
        self.__vorname = data["vorname"]
        self.__name = data["name"]
        self.__geburtsdatum = data["geburtsdatum"]
        self.__wohnort = data["wohnort"]

class PersonManager:
    def __init__(self):
        self.persons = []
        self.current_index = 0
        self.current_person = None

    def load_from_file(self):
        if os.path.exists("person_data.json"):
            with open("person_data.json", "r") as file:
                data = json.load(file)
                self.persons = [Person(**item) for item in data]
                self.current_person = self.persons[0] if self.persons else None

    def save_to_file(self):
        with open("person_data.json", "w") as file:
            json.dump([person.to_dict() for person in self.persons], file)

    def add_person(self, person):
        self.persons.append(person)
        self.current_index = len(self.persons) - 1
        self.current_person = self.persons[self.current_index]

    def get_current_person(self):
        return self.current_person

    def get_next_person(self):
        if self.persons:
            self.current_index = (self.current_index + 1) % len(self.persons)
            self.current_person = self.persons[self.current_index]
            return self.current_person

    def get_prev_person(self):
        if self.persons:
            self.current_index = (self.current_index - 1) % len(self.persons)
            self.current_person = self.persons[self.current_index]
            return self.current_person

person_manager = PersonManager()
person_manager.load_from_file()

def aktualisiere_person_info():
    if person_manager.get_current_person():
        current_person = person_manager.get_current_person()
        text_widget.delete(1.0, END)  # Clear previous content
        text_widget.insert(INSERT, f"Person: ", "title")
        text_widget.insert(INSERT, f"{current_person.vorname} {current_person.name}\n", "name")
        text_widget.insert(INSERT, f"Geboren am ", "label")
        text_widget.insert(INSERT, f"{current_person.geburtsdatum}\n", "geburtsdatum")
        text_widget.insert(INSERT, f"wohnt in ", "label")
        text_widget.insert(INSERT, f"{current_person.wohnort}", "wohnort")

def name_aendern():
    neuer_vorname = entry_vorname.get()
    neuer_name = entry_nachname.get()
    current_person = person_manager.get_current_person()
    if current_person:
        current_person.name_aendern(neuer_vorname, neuer_name)
        aktualisiere_person_info()

def wohnort_aendern():
    neuer_wohnort = entry_wohnort.get()
    current_person = person_manager.get_current_person()
    if current_person:
        current_person.umziehen(neuer_wohnort)
        aktualisiere_person_info()

def geburtsdatum_aendern():
    neues_geburtsdatum = entry_geburtsdatum.get()
    current_person = person_manager.get_current_person()
    if current_person:
        current_person.geburtsdatum_aendern(neues_geburtsdatum)
        aktualisiere_person_info()

def add_person():
    vorname = entry_new_vorname.get()
    name = entry_new_nachname.get()
    geburtsdatum = entry_new_geburtsdatum.get()
    wohnort = entry_new_wohnort.get()
    
    if vorname and name and geburtsdatum and wohnort:
        new_person = Person(vorname, name, geburtsdatum, wohnort)
        person_manager.add_person(new_person)
        aktualisiere_person_info()
    else:
        print("Bitte füllen Sie alle Felder aus.")

def save_and_close():
    person_manager.save_to_file()
    tkFenster.destroy()

def next_person():
    person_manager.get_next_person()
    aktualisiere_person_info()

def prev_person():
    person_manager.get_prev_person()
    aktualisiere_person_info()

tkFenster = Tk()
tkFenster.title("Personenverwaltung")
tkFenster.configure(bg="light blue")

text_widget = Text(tkFenster, wrap=WORD, height=6, width=80, bg="light blue", fg="black", font=("Helvetica", 16))
text_widget.pack(padx=10, pady=10)
text_widget.tag_configure("title", font=("Helvetica", 16, "bold"))
text_widget.tag_configure("name", foreground="green")
text_widget.tag_configure("label", foreground="black")
text_widget.tag_configure("geburtsdatum", foreground="orange")
text_widget.tag_configure("wohnort", foreground="yellow")

aktualisiere_person_info()

frame = Frame(master=tkFenster, bg="light blue")
frame.pack(padx=10, pady=10, fill=X)

Label(master=frame, text="Vorname:", bg="light blue", foreground="green").grid(row=0, column=0, padx=5, pady=5, sticky=W)
entry_vorname = Entry(master=frame, width=20)
entry_vorname.grid(row=0, column=1, padx=5, pady=5, sticky=W)

Label(master=frame, text="Nachname:", bg="light blue", foreground="green").grid(row=1, column=0, padx=5, pady=5, sticky=W)
entry_nachname = Entry(master=frame, width=20)
entry_nachname.grid(row=1, column=1, padx=5, pady=5, sticky=W)

btn_name_aendern = Button(master=frame, text="Name ändern", command=name_aendern, bg="red")
btn_name_aendern.grid(row=1, column=2, padx=5, pady=5, columnspan=2, sticky=W)

Label(master=frame, text="Neuer Wohnort:", bg="light blue", foreground="yellow").grid(row=2, column=0, padx=5, pady=5, sticky=W)
entry_wohnort = Entry(master=frame, width=20)
entry_wohnort.grid(row=2, column=1, padx=5, pady=5, sticky=W)

btn_wohnort_aendern = Button(master=frame, text="Wohnort ändern", command=wohnort_aendern, bg="red")
btn_wohnort_aendern.grid(row=2, column=2, padx=5, pady=5, columnspan=2, sticky=W)

Label(master=frame, text="Neues Geburtsdatum:", bg="light blue", foreground="orange").grid(row=3, column=0, padx=5, pady=5, sticky=W)
entry_geburtsdatum = Entry(master=frame, width=20)
entry_geburtsdatum.grid(row=3, column=1, padx=5, pady=5, sticky=W)

btn_geburtsdatum_aendern = Button(master=frame, text="Geburtsdatum ändern", command=geburtsdatum_aendern, bg="red")
btn_geburtsdatum_aendern.grid(row=3, column=2, padx=5, pady=5, columnspan=2, sticky=W)

btn_prev = Button(master=frame, text="< Vorherige", command=prev_person, bg="blue", fg="white")
btn_prev.grid(row=4, column=0, padx=5, pady=5, sticky=W)

btn_next = Button(master=frame, text="Nächste >", command=next_person, bg="blue", fg="white")
btn_next.grid(row=4, column=1, padx=5, pady=5, sticky=W)

frame_add_person = Frame(master=tkFenster, bg="light blue")
frame_add_person.pack(padx=10, pady=10, fill=X)

Label(master=frame_add_person, text="Neuer Vorname:", bg="light blue", foreground="green").grid(row=0, column=0, padx=5, pady=5, sticky=W)
entry_new_vorname = Entry(master=frame_add_person, width=20)
entry_new_vorname.grid(row=0, column=1, padx=5, pady=5, sticky=W)

Label(master=frame_add_person, text="Neuer Nachname:", bg="light blue", foreground="green").grid(row=1, column=0, padx=5, pady=5, sticky=W)
entry_new_nachname = Entry(master=frame_add_person, width=20)
entry_new_nachname.grid(row=1, column=1, padx=5, pady=5, sticky=W)

Label(master=frame_add_person, text="Neues Geburtsdatum:", bg="light blue", foreground="orange").grid(row=2, column=0, padx=5, pady=5, sticky=W)
entry_new_geburtsdatum = Entry(master=frame_add_person, width=20)
entry_new_geburtsdatum.grid(row=2, column=1, padx=5, pady=5, sticky=W)

Label(master=frame_add_person, text="Neuer Wohnort:", bg="light blue", foreground="yellow").grid(row=3, column=0, padx=5, pady=5, sticky=W)
entry_new_wohnort = Entry(master=frame_add_person, width=20)
entry_new_wohnort.grid(row=3, column=1, padx=5, pady=5, sticky=W)

btn_add_person = Button(master=frame_add_person, text="Person hinzufügen", command=add_person, bg="green", fg="white")
btn_add_person.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

btn_save_close = Button(master=tkFenster, text="Speichern und Schließen", command=save_and_close, bg="purple", fg="white")
btn_save_close.pack(pady=10)

tkFenster.mainloop()
