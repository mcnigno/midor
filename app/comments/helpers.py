
from config import UPLOAD_FOLDER
import openpyxl
from .models import Document, Revision, Commentsheet, Comment
from datetime import datetime
from flask import flash, abort
from app import db


def date_parse(field):
    if isinstance(field, datetime):
        #print('We got a valid Date!')
        return field
    try:
        return datetime.strptime(field,'%d/%m/%y')
    except:
        #print('Date Parse ERROR --------------- GOT:', field)
        return None

def check_labels(item):
    # 
    # Check File Labels
    # 
    #  
    item = item.cs_file
    csFile = openpyxl.load_workbook(UPLOAD_FOLDER+item)
    csSheet = csFile.active
    
    # Duplicate key (label in excel) for check purpose
    header_labels_dict = {
        'Reference' : csSheet['C8'].value,
        'Date' : csSheet['D8'].value,

        'Reference' : csSheet['G8'].value,
        'Date' : csSheet['G9'].value,
        'Material requisition': csSheet['G10'].value,
        'Vendor Name' : csSheet['G11'].value,

        'Rev.' : csSheet['J9'].value,
        'Description': csSheet['J10'].value,
        'Issued by (Contractor Discipline)': csSheet['J11'].value
    }

    for key, value in header_labels_dict.items():
        #print(key, value)
        if key != value:
            #flash(('Header Label ' + key + ' Not Found, Check your DRAS Template!'), category='warning')
            abort(400,('Header Label ' + key + ' Not Found, Check your DRAS Template!'))
    
    table_label_dict = {
        'Pos.' : csSheet['B14'].value,
        
        'Status' : csSheet['G16'].value,

        'Date' : csSheet['K15'].value,

    }

    for key, value in table_label_dict.items():
        #print(key, value)
        if key != value:
            flash(('Table Label ' + key + ' Not Found, Check your DRAS Template!'), category='warning')
            print(('Table Label ' + key + ' Not Found, Check your DRAS Template!'))
            return False
    
    print('-------------------- CHECK FUNCTION TRUE')
    return True

def update_data_from_cs(item):
    session = db.session   
    csFile = openpyxl.load_workbook(UPLOAD_FOLDER+item.cs_file, data_only=True)
    csSheet = csFile.active
 
    print('--------       Query -|')
    '''
    # Check If a revision for this document already exist
    DRAS_2544-17-DW-0510-04_CY.xlsx
    '''
    try:
        document = item.cs_file.split('_sep_DRAS_')[1].split('_')[0]
        
    except:
        return abort(400, 'Error in your File Name.')
    #doc = session.query(Document).filter(Document.id == item.document_id).first()

    rev = session.query(Revision).filter(Revision.id == item.revision_id).first()
    
        
    rev.stage = item.stage
    
    print(rev.id)
    #print(doc.id)
    session.flush()
    print(rev.id)
    #print(doc.id)

    '''
        HEADER - UPDATE THE COMMENT SHEET
    '''

    
    print(csSheet['C9'].value)
    
    try:
        print('before maybe here')
        #item.revision_id = rev.id
        #item.document_id = item.document_id
        
        
        item.ownerTransmittalReference = csSheet['C9'].value
        
        item.ownerTransmittalDate = date_parse(csSheet['D9'].value)
        print(csSheet['C12'].value)
        item.response_status = csSheet['C12'].value
        
        
        item.contractorTransmittalReference = csSheet['H8'].value
        item.contractorTransmittalDate = date_parse(csSheet['H9'].value)
        

        item.contractorTransmittalMr = csSheet['H10'].value
        item.contractorTransmittalVendor = csSheet['H11'].value
        
        item.documentReferenceDoc = csSheet['K8'].value
        item.documentReferenceRev = csSheet['K9'].value
        item.documentReferenceDesc = csSheet['K10'].value
        item.documentReferenceBy = csSheet['K11'].value
        
        '''
        BODY - CREATE NEW COMMENTS FOR THIS CS
        '''
        
        

        doc = session.query(Document).filter(Document.name == document).first()
        session.query(Comment).filter(Comment.document_id == doc.id).delete()
        
        cs = session.query(Commentsheet).filter( 
                                    Document.id == doc.id,
                                    Commentsheet.current == True).first()
        #item.stage = rev_stage
          
        cs.current = False
        print('cs', cs.current, cs.id, 'item',item.current, item.id)
        item.current = True
        print('cs', cs.current, cs.id, 'item',item.current, item.id)

        for row in csSheet.iter_rows(min_row=17,min_col=2):
            
            
            

            if row[0].value is not None:
                #print(row[0].value) 
                comment = Comment(

                    revision_id = rev.id,
                    commentsheet = item,

                    pos = row[0].value,
                    tag = row[1].value,
                    info = row[2].value,
                    ownerCommentBy = row[3].value,
                    ownerCommentDate = date_parse(csSheet['F15'].value),
                    ownerCommentComment = row[4].value,

                    contractorReplyDate = date_parse(csSheet['H15'].value),
                    contractorReplyStatus = row[5].value,
                    contractorReplyComment = row[6].value,
                    
                    ownerCounterReplyDate = date_parse(csSheet['J15'].value),
                    ownerCounterReplyComment = row[7].value,

                    finalAgreementDate = date_parse(csSheet['L15'].value),
                    finalAgreemntCommentDate = date_parse(row[8].value),
                    finalAgreementComment = row[9].value,

                    commentStatus = row[10].value,
                )
                print('-----         ************       --------')
                print(item.current)
                if item.current == True:
                    
                    comment.document_id = doc.id
                    
                    print(comment.document_id, doc.id)
                    

                
                session.add(comment)
        #session.query(Comment).filter(Comment.document_id == doc.id).delete()
        
        print('maybe here')
        session.commit()
        return True
    except:
        abort(400,'Error - Data in Table badly formatted :( - check your file !')



def get_data_from_cs(item):
    #item ='4def885a-604b-11e9-bffd-ac87a32187da_sep_DRAS_2544-17-DW-0510-04_CY.xlsx'
    session = db.session
    
    
    csFile = openpyxl.load_workbook(UPLOAD_FOLDER+item.cs_file, data_only=True)
    csSheet = csFile.active
 
    print('--------       Query -|')
    '''
    # Check If a revision for this document already exist
    DRAS_2544-17-DW-0510-04_CY.xlsx
    '''
    try:
        document = item.cs_file.split('_sep_DRAS_')[1].split('_')[0]
        full_revision = item.cs_file.split('_sep_DRAS_')[1].split('_')[1].split('.')[0]
        revision = full_revision[:full_revision.index('Y')]
        rev_stage = full_revision[full_revision.index('Y'):]

    except:
        abort(400, 'Error in file name. Check Your File!')

    doc = session.query(Document).filter(Document.name == document).first()
    if doc is None:
        doc = Document(name=document)
        session.add(doc)
        print('Document',doc.name)

    rev = session.query(Revision).filter(Revision.name == revision, Document.name == document).first()
    if rev is None:
        print(rev)
        print('    ----------     Rev is None: ', revision, rev_stage, document)
        rev = Revision(name=revision, document=doc)
        
    rev.stage = rev_stage
    session.add(rev)
    print(rev.id)
    print(doc.id)
    session.flush()
    print(rev.id)
    print(doc.id)

    '''
        HEADER - UPDATE THE COMMENT SHEET
    '''

    print('***********************')
    print(csSheet['C9'].value)
    
    
    print('before maybe here')
    item.revision_id = rev.id
    item.document_id = doc.id
    

    item.ownerTransmittalReference = csSheet['C9'].value
    print('*********************** BEFORE DATE PARSE')
    item.ownerTransmittalDate = date_parse(csSheet['D9'].value)
    print('*********************** DATE PARSE')
    item.response_status = csSheet['C12'].value

    item.contractorTransmittalReference = csSheet['H8'].value
    item.contractorTransmittalDate = date_parse(csSheet['H9'].value)
    item.contractorTransmittalMr = csSheet['H10'].value
    item.contractorTransmittalVendor = csSheet['H11'].value

    item.documentReferenceDoc = csSheet['K8'].value
    item.documentReferenceRev = csSheet['K9'].value
    item.documentReferenceDesc = csSheet['K10'].value
    item.documentReferenceBy = csSheet['K11'].value
    
    
    '''
    BODY - CREATE NEW COMMENTS FOR THIS CS
    '''
    
    if item.current:
        session.query(Comment).filter(Comment.document_id == doc.id).delete()
        
        commentSheets = session.query(Commentsheet).filter(Revision.name == revision).all()
        item.stage = rev_stage

        for cs in commentSheets:
            cs.current = False

    
    for row in csSheet.iter_rows(min_row=17,min_col=2):

    
        if row[0].value is not None:
            #print(row[0].value) 
            comment = Comment(

                revision_id = rev.id,
                commentsheet = item,

                pos = row[0].value,
                tag = row[1].value,
                info = row[2].value,
                ownerCommentBy = row[3].value,
                ownerCommentDate = date_parse(csSheet['F15'].value),
                ownerCommentComment = row[4].value,

                contractorReplyDate = date_parse(csSheet['H15'].value),
                contractorReplyStatus = row[5].value,
                contractorReplyComment = row[6].value,
                
                ownerCounterReplyDate = date_parse(csSheet['J15'].value),
                ownerCounterReplyComment = row[7].value,

                finalAgreementDate = date_parse(csSheet['L15'].value),
                finalAgreemntCommentDate = date_parse(row[8].value),
                finalAgreementComment = row[9].value,

                commentStatus = row[10].value,
            )
            if item.current:
                
                comment.document_id = doc.id
                

            print('Contractor Status:',len(contractorReplyStatus),contractorReplyStatus)
            session.add(comment)
    #session.query(Comment).filter(Comment.document_id == doc.id).delete()
    
    print('maybe here')
    session.commit()
    print('after commit')
    #return True
    '''
    except:
        abort(400,'Error - Data in Table badly formatted :( - check your file !')
    '''
        
            

def find_rev():
    session = db.session
    document = '2544-17-DW-0510-04'
    revision = 'CYF'

    rev = session.query(Revision).filter(Revision.name == revision, Document.name == document).first()
    if rev is None:
        print('     ----- Rev is NONE')
    print('    ------  RR rev: ',rev.id, rev.name, rev.document)
    
    return

#find_rev()