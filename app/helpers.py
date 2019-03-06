import openpyxl
from .models import EarlyWorksDoc 
from app import db
from datetime import datetime

wb = openpyxl.load_workbook('xlsx/midorewd.xlsx')
ws = wb.active
session = db.session
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
        print('row added', row[1].value)
    session.commit()
    print('session committed')