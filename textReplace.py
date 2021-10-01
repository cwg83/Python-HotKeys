import keyboard
from tkinter import *
from tkinter import messagebox
import re


#  Create the options function
def options():
    #  Initialize the tk interpreter / create root window
    master = Tk()
    #  Set geometry variables
    window_height = 400
    window_width = 600
    #  Get screen size
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    #  Set X and Y coordinates for window in order for the window to be centered
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    #  set geometry using previous variables
    master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
    #  Set window title
    master.title("Options")
    #  Create the text_field widget and set it's arguments
    text_field = Entry(master)
    text_field.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
    #  Set focus on the text field widget
    text_field.focus_set()
    #  Configure weight of desired rows and columns (non-zero weight columns and rows grow if there is extra space)
    master.grid_rowconfigure(0, weight=1)
    master.grid_rowconfigure(1, weight=1)
    master.grid_rowconfigure(2, weight=1)
    master.grid_columnconfigure(0, weight=1)
    master.grid_columnconfigure(1, weight=1)
    master.grid_columnconfigure(2, weight=0)
    master.grid_columnconfigure(3, weight=1)

    #  Open text file as Readable add text from file to the Label widget

    with open("hotkeys.txt", "r+") as file:

        Label(master,
              text=file.read(),
              anchor='center',
              justify='center').grid(
                                row=1,
                                column=1,
                                padx=10,
                                pady=10,
                                columnspan=2)
    instructions = ("Instructions:\n" 
                    "Typing the text before the :: and pressing space will " 
                    "automatically replace what you typed with anything after the ::\n"     
                    "To add a hotkey: type the letters you want as the hotkey, " 
                    "then :: then the text you want to replace the hotkey with.")
    Label(master,
          text=instructions, wraplength=580, anchor='w', justify='left').grid(
                            row=0,
                            column=0,
                            padx=10,
                            pady=10,
                            columnspan=4, sticky=W)

    def remove():
        #  Set variable to the text_field input
        old_hotkey = text_field.get()
        #  Open text doc as Readable
        hot_text = open("hotkeys.txt", "r+")
        lines = hot_text.readlines()
        #  Loop through lines in the text file and split by ::, then add_abbreviation attribute from keyboard
        match = False
        for line in lines:
            hotkey = line.split('::', 1)
            if old_hotkey == hotkey[0]:
                match = True
        success_message = "Hotkey was found and will be removed."
        if match:
            messagebox.showinfo(title="Successful removal", message=success_message)
            hot_text.seek(0)
            for index, line in enumerate(lines):
                if line.split("::")[0] != old_hotkey:
                    hot_text.write(line)
            hot_text.truncate()
            #  Close the main window
            master.destroy()
            #  Get hotkeys
            get_hotkeys()
            #  Run options function again to re-open window
            options()
        else:
            messagebox.showerror(title="Not found", message="Apologies, no matching hotkey was found.")

    #  Create function for adding new hotkeys to the file
    def add_new():
        #  Open text file as readable+ (readable and writeable)
        hot_text_write = open("hotkeys.txt", "r+")
        #  Get lines from document
        lines = hot_text_write.readlines()
        #  Set variable to the text_field input
        new_hotkey = text_field.get()
        #  If input matches regex
        if re.match(r'[@\w]+::[\w@]+', new_hotkey) is not None:
            #  If lines is empty (if document is empty)
            if not lines:
                #  Add new_hotkey without newline character
                hot_text_write.write(new_hotkey)
            #  Else if document is not empty
            else:
                #  Add newline character and new_hotkey to the text file
                hot_text_write.write("\n" + new_hotkey.replace("\n", ""))
                with open('hotkeys.txt') as reader, open('hotkeys.txt', 'r+') as writer:
                    for line in reader:
                        if line.strip():
                            writer.write(line)
                    writer.truncate()
            #  Create success message variable
            success_message = new_hotkey + " has been added to your list."
            #  Display messagebox with success_message
            messagebox.showinfo(title="Successful addition", message=success_message)
            #  Close the text document
            hot_text_write.close()
            #  Close the main window
            master.destroy()
            #  Get hotkeys again so we can see the new addition
            get_hotkeys()
            #  Run options function again to re-open window
            options()
        #  If input does not match the format
        elif re.match(r'[\[@\w]+ \d]]+', new_hotkey) is not None:
            print(new_hotkey)
        else:
            #  Display messagebox with error message
            messagebox.showerror(title="Format Error", message="Please use the format of hotkey::hotkeytext")

    #  Add buttons
    add_button = Button(master, text="Add", width=10, command=add_new)
    remove_button = Button(master, text="Remove", width=10, command=remove)
    add_button.grid(row=2, column=0, padx=10, pady=10, sticky=W, columnspan=2)
    remove_button.grid(row=2, column=2, padx=10, pady=10, sticky=E, columnspan=2)
    #  Run event loop (listens for events))
    mainloop()


#  Function to get hotkeys from the document
def get_hotkeys():
    #  Open text doc as Readable
    hot_text = open("hotkeys.txt", "r")
    #  Loop through lines in the text file and split by ::
    for lines in hot_text.readlines():
        if lines == "\n":
            continue
        elif lines[0] == "[" and lines[-1] == "]":
            print(lines)
        else:
            hotkey = lines.split('::', 1)
            #  Add results keyboard.add_abbreviation for the text replace hotkeys
            keyboard.add_abbreviation(hotkey[0], hotkey[1].strip())


if __name__ == "__main__":
    options()
    get_hotkeys()
