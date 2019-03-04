from flask import render_template, request
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, BaseView, expose
from app import appbuilder, db

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

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()

appbuilder.add_view(MidorewdDashboardView, "Early Works Document", icon="fa-folder-open-o", category="Dashboard", category_icon='fa-envelope')

