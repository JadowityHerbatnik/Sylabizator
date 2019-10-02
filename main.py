from tkinter import *
import Sylabizator


class App:

    def __init__(self, mastter):
        mastter.title("Sylabizator")
        frame = Frame(mastter)
        frame.pack(expand=TRUE, fill=BOTH)
        self.field = Text(frame, height=10, wrap=WORD, font="arial")
        self.field.pack(expand=TRUE, side=TOP, fill=BOTH)
        self.field2 = Text(frame, height=10, state=DISABLED, wrap=WORD, font="arial")
        self.field2.pack(expand=TRUE, side=TOP, fill=BOTH)

        self.button = Button(frame, text="Wyjdz", fg="red", command=frame.quit)
        self.button.pack(side=BOTTOM, fill=X)

        self.hi_there = Button(frame, text="Sylabizuj", command=self.sylabizuj)
        self.hi_there.pack(side=BOTTOM, fill=X)

    def sylabizuj(self):
        var = self.field.get("1.0", END)
        try:
            indslow, indreszty = Sylabizator.zdania(var)
            druk = Sylabizator.wywolaj(indslow, indreszty, var)
            self.field2.configure(state=NORMAL)
            self.field2.delete("1.0", END)
            self.field2.insert(END, druk)
            self.field2.configure(state=DISABLED)
        except:
            brak = Sylabizator.zdania(var)
            self.field2.configure(state=NORMAL)
            self.field2.delete("1.0", END)
            self.field2.insert(END, brak)
            self.field2.configure(state=DISABLED)


root = Tk()
app = App(root)

root.mainloop()
root.destroy()
