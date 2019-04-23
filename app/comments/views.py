from flask_appbuilder.baseviews import BaseView, expose
from flask_appbuilder import ModelView, action, MasterDetailView, MultipleView
from flask_appbuilder.models.sqla.interface import SQLAInterface
#from flask import render_template, request
from app.comments.models import Document, Revision, Commentsheet, Comment
from app import appbuilder, db
from .helpers import check_labels, get_data_from_cs
from flask import session, redirect, url_for, abort
from app.comments.customWidgets import commentListWidget, RevisionListCard
from flask_appbuilder.widgets import ListBlock
from .helpers import update_data_from_cs

   
 
class CommentView(ModelView):
    datamodel = SQLAInterface(Comment)
    list_columns = ['ownerCommentComment','contractorReplyComment','ownerCounterReplyComment']
    list_widget = commentListWidget
    label_columns = {
        'ownerCommentBy': 'Owner',
        'ownerCommentComment': 'Owner Comment',
        'contractorReplyComment': 'Contractor Reply',
        'ownerCounterReplyComment' : 'Owner Reply'
    }
   
    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())


class CommentSheetView(ModelView):
    datamodel = SQLAInterface(Commentsheet)
    add_columns = ['cs_file', 'current']
    list_columns = ['stage','filename', 'current', 'download'] 
    #related_views = [CommentView]
    #show_template = 'appbuilder/general/model/show_cascade.html'


    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())
    
    @action("setcurrent", "Set as Current", "Set all as Curent Really?", "fa-rocket", multiple=False)
    def setcurrent(self, items):
        item = items
         
        update_data_from_cs(item) 
 
        #return redirect(self.get_redirect())
        return redirect(url_for('DocumentView.show', pk=item.document_id))

    def pre_add(self, item):
        
        # Check File Requirements
        check_labels(item)
        data = get_data_from_cs(item) 

        if data == False:
            return abort(400, 'No revision found.')

    def pre_update(self, item):
        session['last_document'] = item.document_id
        
        
        # Find or Create Document
        # Find or Create Revision
    
    def post_edit_redirect(self):
        """Override this function to control the redirect after add endpoint is called."""
        
        doc = str(session['last_document'])

        return redirect(url_for('DocumentView.show', pk=doc))



class RevisionView(ModelView):
    datamodel = SQLAInterface(Revision)
    list_columns = ['document','stage_class','name', 'current_cs'] 
    related_views = [CommentSheetView, CommentView] 
    #default_view = 'show'
    list_widget = RevisionListCard
    show_template = 'appbuilder/general/model/show_cascade.html'

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())


 


class DocumentView(ModelView):
    datamodel = SQLAInterface(Document)
    related_views = [CommentSheetView, RevisionView, CommentView]
    show_template = 'appbuilder/general/model/show_cascade.html'

    list_columns = ['name','created_on','created_by']







'''
    DRAS Comment Sheet Section
'''

appbuilder.add_view(DocumentView, 'Document', icon="fa-folder-open-o",
                    category="DRAS", category_icon='fa-envelope')
appbuilder.add_view(RevisionView, 'Revision',
                    icon="fa-folder-open-o", category="DRAS")
appbuilder.add_view(CommentSheetView, 'CommentSheet',
                    icon="fa-folder-open-o", category="DRAS")
appbuilder.add_view(CommentView, 'Comment',
                    icon="fa-folder-open-o", category="DRAS")
