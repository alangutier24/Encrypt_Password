import pandas as pd
from tkinter import *
from tkinter import ttk
import random

__init__ = ['Store', 'Search']

# Storing passwords
def Store():
    new_index = pd.MultiIndex.from_tuples([(app.get(), user.get())], names=['App', 'Account'])

    new_frame = pd.DataFrame([password.get()], index=new_index, columns = ['Password'])

    app.delete(0, END)
    user.delete(0, END)
    password.delete(0, END)

    existing_frame = pd.read_csv('../Storage/records.csv', index_col=['App', 'Account'])

    existing_frame = existing_frame.append(new_frame)

    existing_frame.to_csv('../Storage/records.csv', index_label=['App', 'Account'])

# Creates a password based on the users criteria
def Create():
    args = []
    args.append(alp.get())
    args.append(upper_alp.get())
    args.append(spec_alp.get())

    c = 0
    for i in args:
        if i == 1:
            args[c] = c
        else:
            args[c] = 3
        c += 1

    base = {0:"abcdefghijklmnopqrstuvwxyz", 1:"ABCDEFGHIJKLMNOPQRSTUVWXYZ", 2:"!@#$%^&*()-_=+/?\[]{}|", 3:""}
    char = base[args[0]] + base[args[1]] + base[args[2]]

    password = random.choices(char, k=24)

    created_password = ''
    for i in password:
        created_password += i

    #Show the password
    Label(create, text=created_password).grid(column=1, row=2, columnspan=1, padx=15, pady=15, ipadx=15, ipady=15)

# Retrieving passwords
def Search():
    #Gathering the data
    app = s_app.get()
    user = s_user.get()
    existing_frame = pd.read_csv('../Storage/records.csv', index_col=['App', 'Account'])

    #Cases only user, only app, both
    data = ''

    #Case only app, either dataframe or series
    if app == '':
        data = existing_frame.loc[existing_frame.index.isin([user], level=1)]
        ind = data.index

        apps = list(set([i for i, c in ind]))

        win = Toplevel(search)
        Label(win, text="App").grid(column=0, row=3)
        Label(win, text="Password").grid(column=0, row=3)

        at = 4
        for i, c in ind:
            Label(win, text=i).grid(column=0, row=at, ipadx=15, ipady=15)
            Label(win, text=data.loc[i, c].values[0]).grid(column=1, row=at, ipadx=15, ipady=15)
            at += 1

    #Case only user, either dataframe or series
    elif user == '':
        data = existing_frame.loc[app]
        ind = data.index

        win = Toplevel(search)

        Label(win, text="User").grid(column=1, row=3)
        Label(win, text="Password").grid(column=2, row=3)

        at = 4
        for i in ind:
            Label(win, text=i).grid(column=1, row=at, ipadx=15, ipady=15)
            Label(win, text=data.loc[i].values[0]).grid(column=2, row=at, ipadx=15, ipady=15)
            at += 1
    #Case both, Series
    else:

        win = Toplevel(search)

        data = existing_frame.loc[app, user]
        Label(win, text="Password").grid(column=0, row=2)
        Label(win, text=data.values[0]).grid(column=1, row=2, ipadx=15, ipady=15)

#Start GUI interface
root = Tk()
root.title("Password Manager")
root.resizable(False, False)

#Start GUI Notebook
notebook = ttk.Notebook(root)
notebook.pack()

# Creating the password searching mechanism
search = ttk.Frame(notebook, padding="3 3 12 12")
notebook.add(search, text='Search')

s_app = ttk.Entry(search, width=19)
s_user = ttk.Entry(search, width=19)

s_app.grid(column=2, row=0, sticky=(W, E))
s_user.grid(column=2, row=1, sticky=(W, E))

ttk.Label(search, text="App").grid(column=1, row=0, sticky=(W, E))
ttk.Label(search, text="User").grid(column=1, row=1, sticky=(W, E))

Button(search, text="Search", command=Search).grid(column=2, row=2, sticky=(W, E))

#Creating the storing password mechanism
store = ttk.Frame(notebook, padding="3 3 12 12")
notebook.add(store, text='Store')

empty = ttk.Frame(store, width=75, height=2)
empty.grid(column=0, row=0, columnspan=1, rowspan=1)

app = ttk.Entry(store, width=19)
user = ttk.Entry(store, width=19)
password = ttk.Entry(store, width=19, show="*")

app.grid(column=2, row=0, sticky=(W, E))
user.grid(column=2, row=1, sticky=(W, E))
password.grid(column=2, row=2, sticky=(W, E))

ttk.Label(store, text="App").grid(column=1, row=0, sticky=(W, E))
ttk.Label(store, text="User").grid(column=1, row=1, sticky=(W, E))
ttk.Label(store, text="Password").grid(column=1, row=2, sticky=(W, E))

ttk.Button(store, text="Save", command=Store).grid(column=2, row=3, sticky=(W, E))

store.bind("<Return>", Store)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

for child in store.winfo_children():
    child.grid_configure(padx=5, pady=5)

# Creating the password creator interface
create = ttk.Frame(notebook, padding="3 3 12 12")
notebook.add(create, text='Create')

alp = IntVar()
upper_alp = IntVar()
spec_alp = IntVar()

Checkbutton(create, text='Lower case alphabet', variable=alp).grid(column=0, row=1)
Checkbutton(create, text='Upper case alphabet', variable=upper_alp).grid(column=1, row=1)
Checkbutton(create, text='Special characters', variable=spec_alp).grid(column=2, row=1)
ttk.Button(create, text="Generate Password", command=Create).grid(column=1, row=3, sticky=W+E)

root.mainloop()
