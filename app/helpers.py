import openpyxl
from .models import EarlyWorksDoc, Correspondence, Uop_Bpd, Uop_spec
from app import db
from datetime import datetime
import os

wb = openpyxl.load_workbook('./xlsx/midorewd.xlsx')
ws = wb.active
session = db.session
file_list = []
error_list = []
file_dict = {}

def date_parse(date):
    if isinstance(date, int): return datetime.utcfromtimestamp(date)
    if isinstance(date, datetime): return date

    if date == '' or date is None: return None

    return datetime.strptime(date,'%d/%m/%y')


def upload_ewd():
    for row in ws.iter_rows(min_row=2):
        ewd = EarlyWorksDoc(
            discipline = row[0].value,
            contractor_code = row[1].value,
            unit = row[2].value,
            client_code = row[3].value,
            description = row[4].value,
            revision = row[5].value,
            issue_type = row[6].value,
            doc_date = date_parse(row[7].value),
            doc_type = row[8].value,
            engineering_code = row[9].value,
            progressive = row[10].value
        )
        session.add(ewd)
        #print('row added', row[1].value)
    session.commit()
    #print('session committed')

 
def upload_correspondence():
    file_dict = create_file_list()
    print('File Dict Len:',len(file_dict))
    
    wb = openpyxl.load_workbook('xlsx/correspondence.xlsx')
    ws = wb.active
    for row in ws.iter_rows(min_row=10):
        ext = ''
        try:
            ext = check_extension(row[4].value, file_dict)
        except: 
            print('Except', row[4].value)
        crs = Correspondence(
            type_correspondence = row[0].value,
            company = row[1].value,
            unit = row[2].value,
            discipline = row[3].value,
            document_code = row[4].value,
            document_date = row[5].value,
            doc_description = row[6].value,
            note = row[7].value,
            action = row[8].value,
            expected_date = row[9].value,
            response = row[10].value,
            response_date = row[11].value,
            file_ext = ext
            )
        session.add(crs)
    session.commit()


def upload_uop_bdp():
    file_dict = create_file_list()
    print('File Dict Len:',len(file_dict))
    
    wb = openpyxl.load_workbook('xlsx/uop_bdp.xlsx')
    ws = wb.active
    wrong_ext = []
    for row in ws.iter_rows(min_row=9):
        ext = ''
        try:
            ext = check_extension(row[0].value, file_dict) 
            if ext is None:
                wrong_ext.append(row[0].value)

        except: 
            print('Except', row[0].value)
            #wrong_ext.append(row[0].value)
        crs = Uop_Bpd(
            document_code = row[0].value,
            unit = row[1].value,
            refinery_unit = row[2].value,
            uop_section = row[3].value,
            doc_description = row[4].value,
            rev = row[5].value,
            file_ext = ext
            )
        session.add(crs)
    session.commit()
    print('Worng Extension List')
    print(wrong_ext)


def upload_uop_spec():
    file_dict = create_file_list()
    print('File Dict Len:',len(file_dict))
    
    wb = openpyxl.load_workbook('xlsx/uop_std_spec.xlsx')
    ws = wb.active
    wrong_ext = []
    for row in ws.iter_rows(min_row=10):
        ext = ''
        try:
            ext = check_extension(row[0].value, file_dict)
            if ext is None:
                wrong_ext.append(row[0].value)
        except: 
            print('Except', row[0].value)
        crs = Uop_spec(
            document_code = row[0].value,
            document_type = row[1].value,
            doc_description = row[2].value,
            revision = row[3].value,
            file_ext = ext
            )
        session.add(crs)
    session.commit()
    print('Worng Extension List')
    print(wrong_ext)


def create_file_list():
    file_list = []
    directory = 'app/static/assets/midor/UOP'
    for root, directories, files in os.walk(directory):
        for filename in files:
            try:
                file_rad, extension = filename.split('.')
                file_list.append((file_rad,extension))
            except:
                error_list.append(filename) 
    return dict(file_list)
    

def check_extension(document_code, file_dict):
    
    if file_dict:
        print('ok')
    try:
        return file_dict[document_code]
    except:
        print('Wrong Extension', document_code)
        return None

# 
#upload_correspondence()
#print(error_list)
#upload_uop_bdp()
#upload_uop_spec() 


from app.init_helpers import init_dras

#init_dras()