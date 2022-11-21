from my_scrap import WebScrapper
from tkinter import *
from tkinter import ttk
import os

if __name__ == "__main__":

    def run_scrap():
        global entry
        # global label
        user_input = entry.get()
        label.configure(text=WebScrapper(user_input).google_scrap())


    # Creating necessary Files
    if not os.path.exists(os.path.join(os.getcwd(), "pdf_files")):
        os.mkdir(os.path.join(os.getcwd(), "pdf_files"))
    if not os.path.exists(os.path.join(os.getcwd(), "excel_files")):
        os.mkdir(os.path.join(os.getcwd(), "excel_files"))

    # Create an instance of Tkinter frame
    my_app = Tk()

    my_app.title("Scrap App Aravind")

    # Set the geometry of Tkinter frame
    my_app.geometry("750x250")

    Label(my_app, text="Scrap Anything", font=('Times', 24)).pack()
    # Create an Entry widget to accept User Input
    entry = Entry(my_app, width=40)
    entry.focus_set()
    entry.insert(0, "Enter Your Input to Scrap")
    entry.pack()

    # Initialize a Label to display the User Input
    label = Label(my_app, text="")
    label.pack()

    # Create a Button to validate Entry Widget
    ttk.Button(my_app, text="Scrap", width=20, command=run_scrap).pack(pady=20)

    my_app.mainloop()
