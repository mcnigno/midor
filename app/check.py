import os
import openpyxl

def check_correspondence():
    wb = openpyxl.load_workbook('../xlsx/correspondence.xlsx')
    ws = wb.active
    for row in ws.iter_rows(min_row=10):
        document_code = row[4].value
        ext = check_extension(document_code)
        print(document_code,ext)

file_list = []
error_list = []

def create_file_list():
    directory = '../xlsx/TPIT/'
    for root, directories, files in os.walk(directory):
        for filename in files: 
            # join the two strings in order to form the full filepath.
            #  
            try:
                file_rad, extension = filename.split('.')
                file_list.append((file_rad,extension))
            except:
                error_list.append(filename)

def check_extension(document_code):
    file_dict = dict(file_list)
    try:
        return file_dict[document_code]
    except:
        print('Wrong', document_code)
        return None

create_file_list()
check_correspondence()
print(error_list)