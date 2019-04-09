from flask import render_template, request
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, BaseView, expose
from app import appbuilder, db
from .helpers import upload_ewd, upload_correspondence,create_file_list
from .models import EarlyWorksDoc, Correspondence, Uop_Bpd, Uop_spec
from flask_appbuilder.models.sqla.filters import FilterStartsWith, FilterEqualFunction, FilterEqual, FilterNotContains

"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""
class MidorewdDashboardView(BaseView):
    default_view = 'midorewd'
    @expose('/midorewd', methods=['POST', 'GET'])
    def midorewd(self): 
        return self.render_template('midorewd.html')

class EarlyWorksDocView(ModelView):
    datamodel = SQLAInterface(EarlyWorksDoc)
    list_columns = ['discipline', 'contractor_code','short_desc','file']
    #show_template = 'custom/showdoc.html'               

class EarlyWorksDocViewRestricted(ModelView):
    datamodel = SQLAInterface(EarlyWorksDoc)
    list_columns = ['discipline', 'contractor_code','short_desc','file']
    base_filters = [['unit',FilterNotContains,'11']]

class CorrespondenceView(ModelView):
    datamodel = SQLAInterface(Correspondence)
    list_columns = ['document_code','doc_description','file']

class Uop_BpdView(ModelView):
    datamodel = SQLAInterface(Uop_Bpd)
    list_columns = ['document_code', 'rev', 'doc_description', 'file']

class Uop_SpecView(ModelView):
    datamodel = SQLAInterface(Uop_spec)
    label_columns = {
        'revision':'Rev'
    }
    list_columns = ['document_code', 'revision', 'doc_description', 'file']
    
"""    
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404



appbuilder.add_view(MidorewdDashboardView, "Early Works Documentation", icon="fa-folder-open-o", category="Dashboard", category_icon='fa-envelope')
appbuilder.add_view(EarlyWorksDocView, "Engineering Documents", icon="fa-folder-open-o", category="Early Works", category_icon='fa-envelope')
appbuilder.add_view(EarlyWorksDocViewRestricted, "Engineering Document PMC", icon="fa-folder-open-o", category="Early Works", category_icon='fa-envelope')
appbuilder.add_view(CorrespondenceView, "UOP Correspondence", icon="fa-folder-open-o", category="Early Works", category_icon='fa-envelope')
appbuilder.add_view(Uop_BpdView, "UOP BDP List", icon="fa-folder-open-o", category="Early Works", category_icon='fa-envelope')
appbuilder.add_view(Uop_SpecView, "UOP Std. Specification", icon="fa-folder-open-o", category="Early Works", category_icon='fa-envelope')

db.create_all() 
#upload_ewd()
#create_file_list()
#upload_correspondence()