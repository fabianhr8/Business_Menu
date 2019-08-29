from tkinter import *
import csv

inventory = 'inventory.csv'


class businessMenu():

    def __init__(self, master):             # Define configurations

        self.master = master
        master.geometry('1000x500')
        master.title('Business Menu')           # Window title

        self.container = Frame(self.master)                  # Main layout
        self.container.pack(fill="both", expand=True)
        self.container.pack()
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frameUp = Frame(self.container)               # Upper frame
        self.frameUp.pack(side = TOP, fill="both", expand=YES)
        self.frameDown = Frame(self.container)          # Lower frame
        self.frameDown.pack(side=BOTTOM, fill="both", expand=YES)

        self.frame0 = Frame(self.frameUp, background='red') # Actual client's order
        self.frame0.pack(side=LEFT, fill=BOTH, expand=YES)

        self.frame1 = Frame(self.frameUp, background='blue') # Available items
        self.frame1.pack(side=RIGHT, fill=BOTH, expand=YES)

        self.frame2 = Frame(self.frameDown, backgroun='black')   # Available clients
        self.frame2.pack(side=LEFT, fill=BOTH, expand=YES)

        self.client1 = Button(self.frame1, text='Client 1', command= lambda: self.actual_client(1))     #Choose client
        self.client1.grid(row=1, column=0)
        self.client2 = Button(self.frame1, text='Client 2', command=lambda: self.actual_client(2))
        self.client2.grid(row=1, column=1)

    def actual_client(self, client_chosen):  

        self.client_chosen_text = 'client' + str(client_chosen)          # Get text and file of client
        self.client_chosen_file = 'client' + str(client_chosen) + '.csv'

        self.frame0.destroy()                                       # Erase and renew the frames so they remain empty
        self.frame0 = Frame(self.frameUp, background='red')
        self.frame0.pack(side=LEFT, fill=BOTH, expand=YES)

        self.frame2.destroy()               
        self.frame2 = Frame(self.frameDown, background='black')
        self.frame2.pack(side=LEFT, fill=BOTH, expand=YES)

        with open(self.client_chosen_file, 'r') as readCl:                    # Read csv file of current client

            self.readClient = csv.reader(readCl.readlines())
            line_num = 0
            readCl.close()

            for row in self.readClient:
                self.item_label = Label(self.frame0, text=row[1], anchor=E)   # Display list of bought items by client
                self.item_label.grid(row=line_num, column=0, sticky=W)
                self.blank_label = Label(self.frame0, text=' x ')
                self.blank_label.grid(row=line_num, column=1)
                self.quantity_label = Label(self.frame0, text=row[3], anchor=W)
                self.quantity_label.grid(row=line_num, column=2, sticky=E)
                line_num += 1

        self.clamato_boton = Button(self.frame2, text='Item #1', command= lambda: self.agregar_articulo(client_chosen, 100))      # 100 es el codigo del articulo
        self.clamato_boton.grid(row=1, column=0)
        self.cerveza_boton = Button(self.frame2, text='Item #2', command=lambda: self.agregar_articulo(client_chosen, 101))
        self.cerveza_boton.grid(row=1, column=1)

    def agregar_articulo(self, client_chosen, item_ordered):

        longFinal = 0                                           # Will be used to check if article exists in client's list
        item_exists = 0
        i = 0

        with open(self.client_chosen_file, 'r') as readCl:                      # Read client's csv file

            self.readClient = csv.reader(readCl.readlines())
            readClient_list = list(self.readClient)             
            longInitial = len(readClient_list)              # Will be used to check if article exists in client's list

            for row in readClient_list:

                if int(row[0]) == item_ordered:                    # If the product is new in client's list
                    item_exists = 1
                    item_ordered_text = row[1]
                    item_price = row[2]

        with open(inventory, 'r') as readInv:                      # Read inventory CSV	
            self.readInventory = csv.reader(readInv)

            for row in self.readInventory:

                if int(row[0]) == item_ordered and item_exists == 0:            # If item is new in client's list...

                    item_ordered_text = row[1]                                             # Item name
                    item_price = row[2]
                    final_ordered_row = row[0] + ',' + row[1] + ',' + row[2] + ',' + str('1')       # Row that will be saved in client's list

        with open(self.client_chosen_file, 'w', newline='') as writeCl:     # Write in Client's CSV file
            writeClient = csv.writer(writeCl)

            for row in readClient_list:

                if item_ordered_text == row[1]:                   # If client had already ordered that item
                
                    row[3] = str(int(row[3]) + 1)
                    rowModified = str(item_ordered) + ',' + item_ordered_text + ',' + str(item_price) + ',' + row[3]
                    readClient_list[i] = row
                    writeClient.writerows(readClient_list)
                    longFinal = longFinal - 1

                i = i + 1
                longFinal = longFinal + 1

            if longInitial == longFinal:                        # If client had not ordered the item

                writeClient.writerows(readClient_list)              # Add item to list
                writeClient.writerow(final_ordered_row.split(','))

            readCl.close()                            # close CSV files
            readInv.close()
            writeCl.close()



root = Tk()                                  # Create root window
root.bind("<Escape>", lambda e: root.quit())
cls = businessMenu(root)
root.mainloop()                             # Start mainloop











