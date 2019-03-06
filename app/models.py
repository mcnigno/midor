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
        return Markup("<a href='https://report.quasarpm.com/static/assets/midor/ewd/FILES/" + self.contractor_code + '_' + self.revision + ".pdf'" + "download>PDF<a/>")







