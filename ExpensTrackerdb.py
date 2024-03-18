from tkinter import *
import sqlite3
from tkcalendar import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox

root = Tk()
root.geometry("500x500")
root.title("Expense Tracker")

try:
    #Connecting to Database
    dbconn = sqlite3.connect('Expense_Tracker.db')
    dbcursor = dbconn.cursor()

    dbcursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses_new (
            SNo INTEGER PRIMARY KEY AUTOINCREMENT,
            Date DATETIME,
            Payee VARCHAR(255),
            Description VARCHAR(255),
            Amount FLOAT,
            Mode_Of_Payment VARCHAR(255)
        )
    """)

    dbcursor.execute("""
        INSERT INTO expenses_new (SNo, Date, Payee, Description, Amount, Mode_Of_Payment)
        SELECT SNo, Date, Payee, Description, Amount, "Mode Of Payment"
        FROM expenses
    """)

    dbcursor.execute("DROP TABLE IF EXISTS expenses")
    dbcursor.execute("ALTER TABLE expenses_new RENAME TO expenses")


    #creating table named expenses...
   # dbcursor.execute("""
          #              CREATE TABLE IF NOT EXISTS expenses(
   #                           SNo INTEGER PRIMARY KEY AUTOINCREMENT ,
    #                          Date DATETIME,
     #                         Payee VARCHAR(255),
      #                        Description VARCHAR(255),
       #                       Amount FLOAT,
        #                      "Mode Of Payment" VARCHAR(255)
         #               )
               #     """)


    dbconn.commit()

except sqlite3.Error as e:
    print("Error while working with SQLite", e)

finally:
        if dbconn:
            dbconn.close()




frame1 = Frame(root,width=600,height=900)
frame1.pack(side="left",expand=1,fill="both")
#frame1.grid(row=0,column=0)

frame2 = Frame(root,width=500,height=900,bg="black")
frame2.pack(side="right",expand=1,fill="both")
#frame2.grid(row=0,column=1)


#added left image..on frame1
my_pic1 = Image.open("expense_img/main.png")
resized = my_pic1.resize((950, 700))
img_1 = ImageTk.PhotoImage(resized)
img = Label(frame1, image=img_1)
img.pack(fill="both",expand=1)


#added top right image.. on frame2..
my_pic2 = ImageTk.PhotoImage(Image.open("expense_img/main2.png"))
img2 = Label(frame2, image=my_pic2)
img2.pack(pady=20)
#img2.grid(row=0,column=0,sticky="n",pady=3)

def submit(_list):
    check = 0        #check if list does not contain any empty string..(if user has not entered any data)
    for i in _list:
        if i.get() == "":
            pass
        else:
            check += 1

    try:
        if check == 5:
            dbconn = sqlite3.connect('Expense_Tracker.db')
            dbcursor = dbconn.cursor()
            dbcursor.execute("""INSERT INTO expenses (Date, Payee, Description, Amount, Mode_Of_Payment)\
                             VALUES (:Date, :Payee, :Description, :Amount, :Mode_Of_Payment)""",
                             {
                                 'Date': (_list[0]).get(),
                                 'Payee': (_list[3]).get(),
                                 'Description': (_list[1]).get(),
                                 'Amount': float((_list[2].get())),
                                 'Mode_Of_Payment': (_list[4]).get()
                                        }
                            )
            dbconn.commit()
            dbconn.close()

            messagebox.showinfo("Success", "Successfully added the record to the database")
            for i in _list:
                i.delete(0,END)

        else:
            messagebox.showwarning("WARNING!", "One or more than one fields are empty\nPlease Check Again")
            pass

    except(ValueError):
        messagebox.showwarning("WARNING!", "Amount Paid must be integer number\nPlease Check Again")
    exp.destroy()


def remove():
    pass






def view_expenses(view_record_frame):
    global ltt
    ltt = []
    dbconn = sqlite3.connect('Expense_Tracker.db')
    dbcursor = dbconn.cursor()
    dbcursor.execute("SELECT * FROM  expenses ")
    records = dbcursor.fetchall()        #fetched data stored in rec

    dbcursor.execute("SELECT oid from expenses")
    rec = dbcursor.fetchall()

    for r in rec:
        ltt.append(rec[0])

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="white", foreground="black", rowheight=45, fieldbackground="white")
    style.map('Treeview', background=[('selected', 'green')])

    tree_scroll = Scrollbar(view_record_frame,orient=VERTICAL)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(view_record_frame,yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=my_tree.yview,activerelief=GROOVE)

    my_tree.tag_configure("oddrow", background="WHITE")
    my_tree.tag_configure("evenrow", background="grey")

    my_tree['columns'] = ('Date Of Payment', 'Payee', 'Description', 'Amount Paid(In Rupees)', 'Mode_Of_Payment')
    my_tree.column("#0", width=0, anchor=W, minwidth=0, stretch=NO)
    my_tree.column("Date Of Payment", width=200, anchor=W, minwidth=25)
    my_tree.column("Payee", width=200, anchor=W, minwidth=25)
    my_tree.column("Description", width=200, anchor=W, minwidth=50)
    my_tree.column("Amount Paid(In Rupees)", width=200, anchor=W, minwidth=25)
    my_tree.column("Mode_Of_Payment", width=200, anchor=W, minwidth=25)

    my_tree.heading("#0", text="Label", anchor=W)
    #my_tree.heading("SNo", text="SNo", anchor=W)
    my_tree.heading("Date Of Payment", text="Date Of Payment (MM/DD/YY)", anchor=W)
    my_tree.heading("Payee", text="Paid To", anchor=W)
    my_tree.heading("Description", text="Description", anchor=W)
    my_tree.heading("Amount Paid(In Rupees)", text="Amount Paid(In Rs)", anchor=W)
    my_tree.heading("Mode_Of_Payment", text="Mode Of Payment", anchor=W)

    p, q = 1, 0
    for record in records:
        if p % 2 == 0:
            my_tree.insert(parent='', index='end', iid=p, text='Parent', values=record, tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=p, text='Parent', values=record, tags=('oddrow',))

        p += 1

    my_tree.pack(padx=10, ipadx=50, ipady=20)

    del_button = Button(view_record_frame,text="DELETE THE SELECTED RECORD",bg="black",font=("BOLD", 15),command=remove,foreground="white")
    del_button.pack(padx=10,pady=20)


    dbconn.commit()
    dbconn.close()



#function get called on clicking track expense image on root window..
def open_expense():
    global exp
    exp = Tk()          #new window opens
    exp.geometry("500x500")
    exp.title("Track Expense")

    #creating a notebook containing different tabs..
    my_nb = ttk.Notebook(exp)
    my_nb.pack(expand=True, fill="both")

    new_record_frame = Frame(my_nb)
    my_nb.add(new_record_frame, text="Add New Expense")

    global view_record_frame
    view_record_frame = Frame(my_nb)
    my_nb.add(view_record_frame, text="View Expenses")
    view_expenses(view_record_frame)

    Amount_Paid = DoubleVar()
    #extracting data from user for a new record(expense)...
    #entry boxes...
    date_of_payment_entry = DateEntry(new_record_frame, width=12, background="black", foreground="white", borderwidth=2)
    date_of_payment_entry.grid(row=0, column=1, padx=20)
    Description_Entry = Entry(new_record_frame, width=25)
    Description_Entry.grid(row=1, column=1,pady=3,padx=15)
    Amount_Paid_Entry = Entry(new_record_frame, width=25, textvariable=Amount_Paid)
    Amount_Paid_Entry.grid(row=2, column=1,pady=10,padx=15)
    Paid_To_Entry = Entry(new_record_frame, width=25)
    Paid_To_Entry.grid(row=3, column=1,padx=15,pady=7)
    global mode_of_payment
    mode_of_payment = ttk.Combobox(new_record_frame, values=["CASH","CARD","PAYTM","CHEQUE","ONLINE TRANSACTION"])
    mode_of_payment.current(0)
    mode_of_payment.grid(row=4, column=1,padx=14,pady=12)


    #label corresponding to each entry box...
    date_of_payment_label = Label(new_record_frame,text="Date of Payment\n(MM\DD\YY)", font=("Times New Roman",11))
    date_of_payment_label.grid(row=0,column=0,pady=40,padx=10)
    description_label = Label(new_record_frame, text="Description",font=("Times New Roman",11))
    description_label.grid(row=1, column=0,pady=10)
    amount_paid_label = Label(new_record_frame, text="Amount Paid(In Rs)", font=("Times New Roman",11))
    amount_paid_label.grid(row=2, column=0,pady=10)
    paid_to_label = Label(new_record_frame, text="Payee",font=("Times New Roman",11))
    paid_to_label.grid(row=3, column=0,pady=10)
    mode_of_payment_label = Label(new_record_frame, text="Mode Of Payment\n",font=("Times New Roman",11))
    mode_of_payment_label.grid(row=4, column=0,pady=21)

    _list = [date_of_payment_entry, Description_Entry, Amount_Paid_Entry, Paid_To_Entry,mode_of_payment]
    #creating button to add data to database..and calls function submit()...
    submit_btn = Button(new_record_frame, text="Add Expense", command=lambda: submit(_list),bg="light blue",relief=RAISED)
    submit_btn.grid(row=5, column=0,columnspan=2,pady=10, padx=10,ipadx=100)

    exp.mainloop()





my_pic3 = Image.open("expense_img/main3.png")
track_img = ImageTk.PhotoImage(my_pic3.resize((250, 100)))
#my_pic3 = ImageTk.PhotoImage(Image.open("expense_img/main3.png"))
track_lbl_img = Label(frame2, image=track_img, relief="sunken", borderwidth=5)
track_lbl_img.pack(pady=50)
track_lbl_img.bind("<Button-1>", lambda event: open_expense())      #click on left mouse button..
text_lbl = Label(frame2, text="Click on above image..")
text_lbl.pack()


#bt = Button(frame2, text="Track Expense", width=20, command=open_expense)
#bt.grid(row=1, column=0, pady=20,sticky="s")
root.grid_rowconfigure(0, weight=2)
root.grid_columnconfigure(0, weight=2)
root.mainloop()