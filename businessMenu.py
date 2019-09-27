from tkinter import *
import csv
import datetime
import os

inventory = 'inventory.csv'
day_log = 'daily_log.csv'

class businessMenu():

    def __init__(self, master):             # Define configurations

        global client1_name, client2_name       #Global variables for names of Clients
        global client_final_name
        client1_name = StringVar()
        client2_name = StringVar()
        client1_name.set('Client 1')
        client2_name.set('Client 2')
        client_final_name = ['', 'Client 1', 'Client 2']                     # Array for final name of clients

        self.master = master
        master.geometry('1000x500')
        master.title('Business Menu')           # Window title

        self.container = Frame(self.master)                  # Main layout
        self.container.pack(fill="both", expand=True)
        self.container.pack()
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frameUp = Frame(self.container)                       # Upper frame
        self.frameUp.pack(side = TOP, fill="both", expand=YES)
        self.frameDown = Frame(self.container)                # Lower frame
        self.frameDown.pack(side=BOTTOM, fill="both", expand=YES)

        self.frame0 = Frame(self.frameUp, background='red')          # Actual client's order
        self.frame0.pack(side=LEFT, fill=BOTH, expand=YES)

        self.frame1 = Frame(self.frameUp, background='blue')         #Available clients
        self.frame1.pack(side=RIGHT, fill=BOTH, expand=YES)

        self.frame2 = Frame(self.frameDown, backgroun='black')    # Available items
        self.frame2.pack(side=LEFT, fill=BOTH, expand=YES)

        self.frameList = Frame(self.frame0, background='red')  # Frame for actual client
        self.frameList.pack(side=BOTTOM, fill=BOTH, expand=YES)

        self.frameTotal = Frame(self.frame0, backgroun='green')                     # Frame for client's total debt
        self.frameTotal.pack(side=BOTTOM, fill=BOTH, expand=YES)

        self.client1 = Button(self.frame1, textvariable=client1_name, command= lambda: self.actual_client(1))     #Choose client
        self.client1.grid(row=1, column=0)
        self.client2 = Button(self.frame1, textvariable=client2_name, command=lambda: self.actual_client(2))
        self.client2.grid(row=1, column=1)

    def actual_client(self, client_chosen):  

        global client_num                   # To change the client's name
        client_num = client_chosen
        button_num = 0                                 # Used to know which client is on

        self.client_chosen_text = 'client' + str(client_chosen)          # Get text and file of client
        self.client_chosen_file = 'client' + str(client_chosen) + '.csv'

        if os.stat(self.client_chosen_file).st_size == 0:        # If the client's file is empty

            self.Change_the_name(client_chosen)                       # Go to the function to change the client's name

        for button_num in range(1,3):                   # Stop sinking all the buttons so that we can sink the chosen one

            not_used_button = 'self.client' + str(button_num) + '.config(relief=RAISED)'
            exec(not_used_button)                           # Raise buttons

            button_num = button_num + 1

        used_button = 'self.client' + str(client_chosen) + '.config(relief=SUNKEN)'      # Sink chosen client's button
        exec(used_button)

        item_cost_by_quantity = 0                 # Item's price x items ordered
        total_charge = 0                                    # Total the client owes

        self.frameTotal.destroy()  # Erase and renew the frames so they remain empty
        self.frameTotal = Frame(self.frame0, backgroun='green')   
        self.frameTotal.pack(side=BOTTOM, fill=BOTH, expand=YES)

        self.frameList.destroy() 
        self.frameList = Frame(self.frame0, backgroun='red') 
        self.frameList.pack(side=BOTTOM, fill=BOTH, expand=YES)

        self.frame2.destroy()               
        self.frame2 = Frame(self.frameDown, background='black')
        self.frame2.pack(side=LEFT, fill=BOTH, expand=YES)

        with open(self.client_chosen_file, 'r') as readCl:                    # Read csv file of current client

            self.readClient = csv.reader(readCl.readlines())
            line_num = 0
            readCl.close()

            for row in self.readClient:
                self.item_label = Label(self.frameList, text=row[1], anchor=E)   # Display list of bought items by client
                self.item_label.grid(row=line_num, column=0, sticky=W)
                self.blank_label = Label(self.frameList, text=' x ')
                self.blank_label.grid(row=line_num, column=1)
                self.quantity_label = Label(self.frameList, text=row[3], anchor=W)
                self.quantity_label.grid(row=line_num, column=2, sticky=E)

                item_cost_by_quantity = int(row[2])*int(row[3])
                total_charge = str(int(total_charge) + item_cost_by_quantity)

                line_num += 1

        self.separation_label = Label(self.frameTotal, text='------------------------')           # For client's total debt
        self.separation_label.grid(row=0, columnspan=3, sticky=W)
        self.total_label = Label(self.frameTotal, text='total ', anchor=E)
        self.total_label.grid(row=1, column=0, sticky=W)
        self.equal_label = Label(self.frameTotal, text=' = ')
        self.equal_label.grid(row=1, column=1)
        self.total_qty_label = Label(self.frameTotal, text=total_charge, anchor=W)
        self.total_qty_label.grid(row=1, column=2, sticky=E)

        self.space_label = Label(self.frameTotal, text='   ')
        self.space_label.grid(row=1, column=3)
        self.pay_button = Button(self.frameTotal, text='Pay', command=lambda: self.pay_account(total_charge))       # To pay bill
        self.pay_button.grid(row=1, column=4, sticky=E)

        self.item1_button = Button(self.frame2, text='Item 1', command= lambda: self.add_item(client_chosen, 100))      # 100 is item's code
        self.item1_button.grid(row=1, column=0)
        self.item2_button = Button(self.frame2, text='Item 2', command=lambda: self.add_item(client_chosen, 101))
        self.item2_button.grid(row=1, column=1)

    def add_item(self, client_chosen, item_ordered):

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

    def pay_account(self,tot_charge):

        print('final')
        print(client_final_name)    

        time_and_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")           # Get date and hour
        button_num = 0                  

        with open(self.client_chosen_file, 'w', newline='') as client_w:               # Erease client's CSV file for a new client
            client_writer = csv.writer(client_w)
            client_w.close()

        for button_num in range(1,3):            # Stop sinking all the buttons so that we can sink the chosen one

            not_used_button = 'self.client' + str(button_num) + '.config(relief=RAISED)'       # Stop sinking the button
            exec(not_used_button) 

            if client_num == button_num:               

                with open(day_log, 'a', newline='') as log_w:                   # Send order info to CSV daily log                    
                    log_writer = csv.writer(log_w)

                    row_to_log = tot_charge + ',' + client_final_name[button_num] + ',' + time_and_date  
                    log_writer.writerow(row_to_log.split(','))           # Send info to daily log CSV

                    log_w.close()

                original_name = 'client' + str(button_num) + '_name.set(\'Client ' + str(button_num) + '\')'        # The \ is used so that we can print the '
                exec(original_name)

            button_num = button_num + 1

    def Change_the_name(self, client_chosen):                    # Go to the window that changes the client's name

        newWindow = Toplevel(self.master)
        app = Name_changer(newWindow, client_chosen)


class Name_changer(Frame):                          # To change client's name if their file is empty

    def __init__(self, master, client_chosen_num):
 
        Frame.__init__(self, master)
        self.master = master
        self.master.title('Client\'s name')
        self.master.geometry('%dx%d+%d+%d' % (150, 100, 200, 80))

        self.choose_name_label = Label(self.master, text='Choose client\'s name:', anchor=E)
        self.choose_name_label.grid(row=0, column=0, sticky=W)
        self.choose_name = Entry(self.master)
        self.choose_name.grid(row=1, column=0)
        self.choose_name_button = Button(self.master, text='Choose', command = self.change_name)
        self.choose_name_button.grid(row=2, column=0)

    def change_name(self):           # Get chosen name

        new_clients_name = self.choose_name.get()

        for i in range(1,3):
            
            if new_clients_name == '':                       # If nothing's chosen, keep the same name

                self.after(1000, self.master.destroy())
                client_final_name[i] = 'Clientt ' + str(client_num)

            else:
            
                if i == client_num:                 # Check client's number 

                    print(client_num)
                    client_final_name[i] = new_clients_name
                    change_name_instruction = 'client'  + str(i) + '_name.set(client_final_name[i])'
                    exec(change_name_instruction)

                self.after(1000, self.master.destroy())             # Close window


root = Tk()                                  # Create root window
root.bind("<Escape>", lambda e: root.quit())
cls = businessMenu(root)
root.mainloop()                             # Start mainloop
