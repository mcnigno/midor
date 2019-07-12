from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean
from flask import Markup, url_for
from flask_appbuilder.filemanager import get_file_original_name
from app import db

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who

Progressive
"""
#from app.comments.models import *

class EarlyWorksDoc(Model):
    id = Column(Integer, primary_key=True)
    discipline = Column(String(50))
    contractor_code = Column(String(50), unique=True, nullable=False)
    unit = Column(String(5))
    client_code = Column(String(250))
    description = Column(String(250))
    revision = Column(String(5))
    issue_type = Column(String(50))
    doc_date = Column(Date)
    doc_type = Column(String(5))
    engineering_code = Column(String(50))
    progressive = Column(String(5))

    def short_desc(self):
        return self.description[:80]


    def file(self):
        return Markup("<a href='https://report.quasarpm.com/static/assets/midor/ewd/FILES/" + self.contractor_code + '_' + self.revision + ".pdf'" + "download>" + '<i class="fa fa-file-pdf-o" aria-hidden="true"></i>' + "<a/>")



class Correspondence(Model):
    id = Column(Integer, primary_key=True)
    type_correspondence = Column(String(50))
    company = Column(String(255))
    unit = Column(String(50))
    discipline = Column(String(255))
    document_code = Column(String(50))
    document_date = Column(String(50))
    doc_description = Column(String(255))
    note = Column(String(255))
    action = Column(String(50))
    expected_date = Column(String(50))
    response = Column(String(255))
    response_date = Column(String(50))
    file_ext = Column(String(20), default='ND')

    def file(self):
        return Markup("<a href='https://midor.quasarpm.com/static/assets/midor/midor_crs/" + self.document_code + '.' + str(self.file_ext) + "'" + "download>"+ str(self.icon()) + "<a/>")

    def icon(self):
        try:
            if self.file_ext.lower() == 'zip' or self.file_ext.lower() == 'rar':
                return '<i class="fa fa-file-archive-o" aria-hidden="true"></i>'
            if self.file_ext[:3].lower() == 'doc':
                return '<i class="fa fa-file-word-o" aria-hidden="true"></i>' 
            if self.file_ext.lower() == 'pdf': 
                return '<i class="fa fa-file-pdf-o" aria-hidden="true"></i>'
        except:
            return 'ND'



class Uop_Bpd(Model):
    id = Column(Integer, primary_key=True)
    document_code = Column(String(50))
    unit = Column(String(50))
    refinery_unit = Column(String(50))
    uop_section = Column(String(50))
    doc_description = Column(String(255))
    rev = Column(String(50))
    file_ext = Column(String(20), default='ND')

    def file(self):
        return Markup("<a href='https://midor.quasarpm.com/static/assets/midor/UOP/" + self.document_code + '.' + str(self.file_ext) + "'" + "download>"+ str(self.icon()) + "<a/>")

    def icon(self):
        try:
            if self.file_ext.lower() == 'zip' or self.file_ext.lower() == 'rar':
                return '<i class="fa fa-file-archive-o" aria-hidden="true"></i>'
            if self.file_ext[:3].lower() == 'doc':
                return '<i class="fa fa-file-word-o" aria-hidden="true"></i>' 
            if self.file_ext.lower() == 'pdf': 
                return '<i class="fa fa-file-pdf-o" aria-hidden="true"></i>'
        except:
            return 'ND'


class Uop_spec(Model):
    id = Column(Integer, primary_key=True)
    document_code = Column(String(50))
    document_type = Column(String(50))
    doc_description = Column(String(255))
    revision = Column(String(50))
    file_ext = Column(String(20), default='ND')

    def file(self):
        return Markup("<a href='https://midor.quasarpm.com/static/assets/midor/UOP/" + self.document_code + '.' + str(self.file_ext) + "'" + "download>"+ str(self.icon()) + "<a/>")

    def icon(self):
        try:
            if self.file_ext.lower() == 'zip' or self.file_ext.lower() == 'rar':
                return '<i class="fa fa-file-archive-o" aria-hidden="true"></i>'
            if self.file_ext[:3].lower() == 'doc':
                return '<i class="fa fa-file-word-o" aria-hidden="true"></i>' 
            if self.file_ext.lower() == 'pdf': 
                return '<i class="fa fa-file-pdf-o" aria-hidden="true"></i>'
        except:
            return 'ND'



class Tagdiscipline(Model,AuditMixin):
    id = Column(Integer, primary_key=True)

    name = Column(String(100), unique=True, nullable=False)
    start = Column(Integer, nullable=False)
    finish = Column(Integer, nullable=False) 

    def __repr__(self):
        return self.name


class Disciplinedras(Model, AuditMixin):
    id = Column(Integer, primary_key=True)

    name = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return self.name



class Mocmodel(Model, AuditMixin):
    id = Column(Integer, primary_key=True)

    name = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class Dedocmodel(Model, AuditMixin):
    id = Column(Integer, primary_key=True)

    name = Column(String(100), unique=True, nullable=False)

    moc_id = Column(Integer, ForeignKey('mocmodel.id'))
    moc = relationship(Mocmodel)

    def __repr__(self):
        return self.name


class Unitmodel(Model, AuditMixin):
    id = Column(Integer, primary_key=True)

    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)

    moc_id = Column(Integer, ForeignKey('mocmodel.id'))
    moc = relationship(Mocmodel)

    dedoc_id = Column(Integer, ForeignKey('dedocmodel.id'))
    dedoc = relationship(Dedocmodel)

    def __repr__(self):
        return self.name


 
class Splitofworks(Model, AuditMixin):
    id = Column(Integer, primary_key=True)

    unit_id = Column(Integer, ForeignKey('unitmodel.id'))
    unitmodel = relationship(Unitmodel) 

    discipline_id = Column(Integer, ForeignKey('disciplinedras.id'))
    disciplinedras = relationship(Disciplinedras)

    oc_id = Column(Integer, ForeignKey('dedocmodel.id'))
    oc = relationship(Dedocmodel) 


    def __repr__(self):
        return self.id


class Drasdocument(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)

    moc_id = Column(Integer, ForeignKey('mocmodel.id'))
    moc = relationship(Mocmodel)

    dedoc_id = Column(Integer, ForeignKey('dedocmodel.id'))
    dedoc = relationship(Dedocmodel)
    
    def __repr__(self):
        return self.name

    def open_comm(self):
        session = db.session
        open_comm = session.query(Drascomment).filter(Drascomment.drasdocument_id == self.id,
                                            Drascomment.commentStatus == 'Open').all()
        return len(open_comm)

    def title_name(self):
        return Markup('<span class="document_title">' + self.name + '</span>')

    def current_rev(self):
        session = db.session
        cs = session.query(Drascommentsheet).filter(Drascommentsheet.drasdocument_id == self.id,
                                            Drascommentsheet.current == True).first()
        if cs:
            return cs.drasrevision
        return "Not Found"
    
    def description(self):
        session = db.session
        cs = session.query(Drascommentsheet).filter(Drascommentsheet.drasdocument_id == self.id,
                                            Drascommentsheet.current == True).first()
        if cs:
            return cs.documentReferenceDesc
        return "Not Found"

    def current_stage(self):
        session = db.session
        cs = session.query(Drascommentsheet).filter(Drascommentsheet.drasdocument_id == self.id,
                                            Drascommentsheet.current == True).first()
        if cs:
            return cs.stage
        return "Stage Not Found"
class Drasrevision(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(5), nullable=False)
    pos = Column(Integer, default=0)
    
    stage = Column(String(5))
    

    drasdocument_id = Column(Integer, ForeignKey('drasdocument.id'))
    drasdocument = relationship(Drasdocument)

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
            current_cs = db.session.query(Drascommentsheet).filter(
                Drascommentsheet.drasrevision_id == self.id,
                Drascommentsheet.current == True).first()
            if current_cs is None:
                return Markup('<small class="Superseeded">Superseeded</small>')
            return Markup('<small class="Current">current</small>') + current_cs.download() 
        except:
            pass 

class Drasactionrequired(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(50))

    def __repr__(self):
        return self.name


class Drasissuetype(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(50))

    def __repr__(self):
        return self.name

class Drascommentsheet(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
  
    drasrevision_id = Column(                       Integer, ForeignKey('drasrevision.id'))
    drasrevision = relationship(Drasrevision)

    drasdocument_id = Column(                       Integer, ForeignKey('drasdocument.id'))
    drasdocument = relationship(Drasdocument)

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

    issuetype_id = Column(Integer, ForeignKey('drasissuetype.id'))
    issuetype = relationship(Drasissuetype)

    actionrequired_id = Column(Integer, ForeignKey('drasactionrequired.id'))
    actionrequired = relationship(Drasactionrequired)

    notificationItem = Column(String(50))
    actualDate = Column(Date)
    expectedDate = Column(Date)
    plannedDate = Column(Date)

    note = Column(Text)


    def __repr__(self):
        return str(self.id)
    
    def filename(self):
        return get_file_original_name(self.cs_file)
     
    def download(self):
        return Markup('<a href="' + url_for('CommentSheetView.download', filename=str(self.cs_file)) + '" download>'+'<img border="0" src="/static/img/excel.png" alt="W3Schools" width="24" height="24">'+'</a>')

    def stage_icon(self):
        if self.stage == 'Y' or self.stage == 'Y2':
            return Markup('<i class="fa fa-arrow-circle-left" aria-hidden="true"></i>'+'<span>'+ self.stage + '</span>')
        if self.stage == 'YF':
            return Markup('<i class="fa fa-check-circle" aria-hidden="true"></i> '+'<span>' + self.stage + '</span>')
        if self.stage == 'S':
            return Markup('<i class="fa fa-arrow-circle-right" aria-hidden="true"></i>'+'<span>'+ self.stage + '</span>')

        return Markup('<i class="fa fa-arrow-circle-right" aria-hidden="true"></i>'+'<span>'+ self.stage + '</span>')
    
    def is_current(self):
        if self.current:
            return Markup('<small class="Current">current</small>')
        return Markup('<small class="Superseeded">Superseeded</small>')

class Drascomment(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    
    drasrevision_id = Column(Integer, ForeignKey('drasrevision.id'))
    drasrevision = relationship(Drasrevision)

    drasdocument_id = Column(Integer, ForeignKey('drasdocument.id'))
    drasdocument = relationship(Drasdocument)

    drascommentsheet_id = Column(Integer, ForeignKey('drascommentsheet.id'))
    drascommentsheet = relationship(Drascommentsheet)

    tagdiscipline_id = Column(Integer, ForeignKey('tagdiscipline.id'))
    tagdiscipline = relationship(Tagdiscipline)
    
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









    
 

     
    
    








