import os
from pathlib import Path
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from xml.dom import minidom
import shutil


def check_or_create_folders():
    Path("files").mkdir(exist_ok=True)
    Path("converted_files").mkdir(exist_ok=True)


def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def clicked():
    for selected in convert_list_box.curselection():
        convert_content(convert_list_box.get(selected))


def popup(error):
    messagebox.showwarning("Error message", error)


def convert_content(file_to_convert: str):
    filename = "files/" + file_to_convert
    people = ET.Element("people")
    with open(filename, "r") as file:
        lines = file.readlines()
        top = ""
        for line in lines:
            elem = line.strip().split("|")
            if elem[0] == "P" and len(elem) == 3:
                top = "P"
                person = ET.SubElement(people, "person")
                first_name = ET.SubElement(person, "firstname")
                first_name.text = elem[1]
                last_name = ET.SubElement(person, "lastname")
                last_name.text = elem[2]
            elif elem[0] == "T" and len(elem) == 3:
                if top == "P":
                    phone = ET.SubElement(person, "phone")
                else:
                    phone = ET.SubElement(family, "phone")
                mobile = ET.SubElement(phone, "mobile")
                mobile.text = elem[1]
                landline = ET.SubElement(phone, "landline")
                landline.text = elem[2]
            elif elem[0] == "A" and len(elem) == 4:
                if top == "P":
                    address = ET.SubElement(person, "address")
                else:
                    address = ET.SubElement(family, "address")
                street = ET.SubElement(address, "street")
                street.text = elem[1]
                city = ET.SubElement(address, "city")
                city.text = elem[2]
                zip = ET.SubElement(address, "zip")
                zip.text = elem[3]
            elif elem[0] == "F" and len(elem) == 3:
                top = "F"
                family = ET.SubElement(person, "family")
                name = ET.SubElement(family, "name")
                name.text = elem[1]
                born = ET.SubElement(family, "born")
                born.text = elem[2]
            else:
                error = "Got invalid format for: (" + str(
                    elem) + ")\n" + "See README for correct format.\n" + "XML file will be missing this information."
                popup(error)

    name = file_to_convert.split(".")[0]
    output_file = open("converted_files/" + name + ".xml", "w")
    output_file.write(prettify(people))
    update_list("converted_files", converted_list_box)


def update_list(folder: str, list_box: Listbox):
    files = os.listdir(folder)
    list_box.delete("0", END)
    for file in files:
        list_box.insert(END, file)


def display_xml(event):
    selection = event.widget.curselection()
    xml_file = event.widget.get(selection)
    xml = ET.parse("converted_files/" + xml_file)
    xml_str = ElementTree.tostring(xml.getroot(), 'utf-8')
    xml_file_text.config(state="normal")
    xml_file_text.delete("1.0", END)
    xml_file_text.insert(END, xml_str)
    xml_file_text.config(state="disabled")


def add_files():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    file_path = filedialog.askopenfilename(initialdir="/", title="Select file to add to convert directory", filetypes=filetypes)
    dest_path = os.path.dirname(__file__) + "/files/" + file_path.split("/")[-1]
    print("Path: " + dest_path)
    shutil.copyfile(file_path, dest_path)
    update_list("files", convert_list_box)


# Start of program
check_or_create_folders()

window = Tk()
window.title("Text to XML")
window.geometry("800x1000")

my_notebook = ttk.Notebook(window)

frame1 = Frame(my_notebook)
convert_list_box = Listbox(frame1, selectmode=MULTIPLE)
update_list("files", convert_list_box)
convert_selected_btn = Button(frame1, text="Convert selected document", command=clicked)
add_files_btn = Button(frame1, text="Add text files to convert", command=add_files)

frame2 = Frame(my_notebook)
converted_list_box = Listbox(frame2)
converted_list_box.bind("<<ListboxSelect>>", display_xml)
update_list("converted_files", converted_list_box)
xml_file_text = Text(frame2, width=80, height=55)
xml_file_text.config(state="disabled")

# Pack things and align in grids
my_notebook.grid(row=0, column=0, pady=15)

# Tab 1
frame1.grid(row=0, column=0)
convert_list_box.grid(row=0, column=0)
convert_selected_btn.grid(row=1, column=0)
add_files_btn.grid(row=2, column=0)

# Tab 2
frame2.grid(row=0, column=0)
converted_list_box.grid(row=0, column=0)
xml_file_text.grid(row=0, column=1)

my_notebook.add(frame1, text="Convert files")
my_notebook.add(frame2, text="Converted files")

window.mainloop()
