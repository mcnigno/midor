
'''
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean
from sqlalchemy.orm import relationship
from flask import Markup, url_for
from flask_appbuilder.filemanager import get_file_original_name
from app import db
'''




'''

class Moc(Model, AuditMixin):
    id = Column(Integer, primary_key=True)

    name = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class Discipline(Model, AuditMixin):
    id = Column(Integer, primary_key=True)

    name = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class Dedoc(Model, AuditMixin):
    id = Column(Integer, primary_key=True)

    name = Column(String(100), unique=True, nullable=False)

    moc_id = Column(Integer, ForeignKey('moc.id'))
    moc = relationship(Moc)

    def __repr__(self):
        return self.name



class Unit(Model, AuditMixin):
    id = Column(Integer, primary_key=True)

    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)

    moc_id = Column(Integer, ForeignKey('moc.id'))
    moc = relationship(Moc)

    dedoc_id = Column(Integer, ForeignKey('dedoc.id'))
    dedoc = relationship(Dedoc)

    def __repr__(self):
        return self.name

class SplitOfWorks(Model, AuditMixin):
    id = Column(Integer, primary_key=True)

    unit_id = Column(Integer, ForeignKey('unit.id'))
    unit = relationship(Unit)

    discipline_id = Column(Integer, ForeignKey('discipline.id'))
    discipline = relationship(Discipline)

    oc_id = Column(Integer, ForeignKey('dedoc.id'))
    oc = relationship(Dedoc) 


    def __repr__(self):
        return self.id


class Document(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)

    moc_id = Column(Integer, ForeignKey('moc.id'))
    moc = relationship(Moc)

    dedoc_id = Column(Integer, ForeignKey('dedoc.id'))
    dedoc = relationship(Dedoc)
    
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
                'Y2': 'Y2 - Commented',
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
                return Markup('<small class="Superseeded">Superseeded</small>')
            return Markup('<small class="Current">current</small>') + current_cs.download() 
        except:
            pass 

class Actionrequired(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(50))

    def __repr__(self):
        return self.name


class Issuetype(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(50))

    def __repr__(self):
        return self.name


class Commentsheet(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
  
    revision_id = Column(                       Integer, ForeignKey('revision.id'))
    revision = relationship(Revision)

    document_id = Column(                       Integer, ForeignKey('document.id'))
    document = relationship(Document)

    stage = Column(                             String(5), nullable=False) 

    ownerTransmittalReference =Column(          String(50))
    ownerTransmittalDate = Column(              Date)

    response_status = Column(                   String(50))

    contractorTransmittalReference = Column(    String(50))
    contractorTransmittalDate = Column(         Date)
    contractorTransmittalMr = Column(           String(50))
    contractorTransmittalVendor = Column(       String(50))

    documentReferenceDoc = Column(              String(50))
    documentReferenceRev = Column(              String(50))
    documentReferenceDesc = Column(             Text)
    documentReferenceBy = Column(               String(50))
    
    # Set manual INPUT

    cs_file = Column(FileColumn, nullable = False)
    current = Column(Boolean, default=True)
    
    documentClientCode = Column(String(50))

    issuetype_id = Column(Integer, ForeignKey('issuetype.id'))
    issuetype = relationship(Issuetype)

    actionrequired_id = Column(Integer, ForeignKey('actionrequired.id'))
    actionrequired = relationship(Actionrequired)

    notificationItem = Column(String(50))
    actualDate = Column(Date)
    expectedDate = Column(Date)
    plannedDate = Column(Date)

    note = Column(Text)


    def __repr__(self):
        return self.filename()
    
    def filename(self):
        return get_file_original_name(self.cs_file)
     
    def download(self):
        return Markup('<a href="' + url_for('CommentSheetView.download', filename=str(self.cs_file)) + '" download>'+'<img border="0" src="/static/img/excel.png" alt="W3Schools" width="24" height="24">'+'</a>')

    def stage_icon(self):
        if self.stage == 'Y' or self.stage == 'Y2':
            return Markup('<i class="fa fa-arrow-circle-left" aria-hidden="true"></i>'+'<span>'+ self.stage + '</span>')
        if self.stage == 'YF':
            return Markup('<i class="fa fa-check-circle" aria-hidden="true"></i> '+'<span>' + self.stage + '</span>')
        
        return Markup('<i class="fa fa-arrow-circle-right" aria-hidden="true"></i>'+'<span>'+ self.stage + '</span>')
    
    def is_current(self):
        if self.current:
            return Markup('<small class="Current">current</small>')
        return Markup('<small class="Superseeded">Superseeded</small>')
        


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

    def finalComment(self):
        if self.finalAgreementComment:
            return self.finalAgreementComment 
        return ' | Without Final Comments.'
'''


