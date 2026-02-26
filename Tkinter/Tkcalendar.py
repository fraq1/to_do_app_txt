import tkinter as tk
from tkcalendar import Calendar

def pick_date():
    selected_date = None
    def on_date_select():
        nonlocal selected_date
        selected_date = cal.get_date()
        print(f"Chosen date: {selected_date}")
        root.destroy()

    root = tk.Tk()
    root.title("Chose date")
    cal = Calendar(root, selectmode='day', date_pattern='yyyy mm dd')
    cal.pack(pady=20)
    tk.Button(root, text="OK", command=on_date_select).pack(pady=10)
    root.mainloop()
    return selected_date
