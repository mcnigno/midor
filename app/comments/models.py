from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean
from sqlalchemy.orm import relationship
from flask import Markup, url_for
from flask_appbuilder.filemanager import get_file_original_name
from app import db


class Document(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)

    def __repr__(self):
        return self.name
 
class Revision(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(5), nullable=False)
    pos = Column(Integer, default=0)
    
    stage = Column(String(5))
    

    document_id = Column(Integer, ForeignKey('document.id'))
    document = relationship(Document)

    def __repr__(self):
        return self.name
    
    
    def stage_class(self):
        try:
            stage = {
                'Y': 'Y - Commented',
                'Y1': 'Y1 - Replied',
                'Y2': 'Y2 - Commented (2)',
                'YF': 'YF - Final'
            }
            return stage[self.stage]
        except:
            return 'N/D'

    def current_cs(self):
        try:
            current_cs = db.session.query(Commentsheet).filter(
                Commentsheet.revision_id == self.id,
                Commentsheet.current == True).first()
            if current_cs is None:
                return 'Superseeded'
            return 'by DRAS: ' + current_cs.download()
        except:
            pass 



class Commentsheet(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    stage = Column(String(5), nullable=False)
    
    cs_file = Column(FileColumn, nullable = False)
    
    revision_id = Column(Integer, ForeignKey('revision.id'))
    revision = relationship(Revision)

    document_id = Column(Integer, ForeignKey('document.id'))
    document = relationship(Document) 

    ownerTransmittalReference = Column(String(50))
    ownerTransmittalDate = Column(Date)

    response_status = Column(String(50))

    contractorTransmittalReference = Column(String(50))
    contractorTransmittalDate = Column(Date)
    contractorTransmittalMr = Column(String(50))
    contractorTransmittalVendor = Column(String(50))

    documentReferenceDoc = Column(String(50))
    documentReferenceRev = Column(String(50))
    documentReferenceDesc = Column(Text)
    documentReferenceBy = Column(String(50))

    current = Column(Boolean, default=True)

    def __repr__(self):
        return self.filename()
    
    def filename(self):
        return get_file_original_name(self.cs_file)
     
    def download(self):
        return Markup('<a href="' + url_for('CommentSheetView.download', filename=str(self.cs_file)) + '" download>'+'<img border="0" src="/static/img/excel.png" alt="W3Schools" width="24" height="24">'+'</a>')


class Comment(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    
    revision_id = Column(Integer, ForeignKey('revision.id'))
    revision = relationship(Revision)

    document_id = Column(Integer, ForeignKey('document.id'))
    document = relationship(Document)

    commentsheet_id = Column(Integer, ForeignKey('commentsheet.id'))
    commentsheet = relationship(Commentsheet)
    
    pos = Column(String(5))
    tag = Column(String(20))
    info = Column(String(255))
    ownerCommentBy = Column(String(50))
    ownerCommentDate = Column(String(50))
    ownerCommentComment = Column(Text)

    contractorReplyDate = Column(Date)
    contractorReplyStatus = Column(String(100))
    contractorReplyComment = Column(Text)
    
    ownerCounterReplyDate = Column(Date)
    ownerCounterReplyComment = Column(Text)

    finalAgreementDate = Column(Date)
    finalAgreemntCommentDate = Column(Date)
    finalAgreementComment = Column(Text)

    commentStatus = Column(String(20))

    def __repr__(self):
        return self.id



