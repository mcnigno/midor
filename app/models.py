from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from flask import Markup

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who

Progressive
"""

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


    def file_pdf(self):
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



