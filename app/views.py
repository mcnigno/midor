from flask import render_template, request
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, BaseView, expose
from app import appbuilder, db
from .helpers import upload_ewd
from .models import EarlyWorksDoc


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
    list_columns = ['discipline', 'contractor_code','short_desc','file_pdf']
    #show_template = 'custom/showdoc.html'               
 
"""    
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404



appbuilder.add_view(MidorewdDashboardView, "Early Works Document", icon="fa-folder-open-o", category="Dashboard", category_icon='fa-envelope')
appbuilder.add_view(EarlyWorksDocView, "EWD Document List", icon="fa-folder-open-o", category="Early Works", category_icon='fa-envelope')
db.create_all()
#upload_ewd()