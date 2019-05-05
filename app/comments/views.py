'''
from flask_appbuilder.baseviews import BaseView, expose
from flask_appbuilder import ModelView, action, MasterDetailView, MultipleView
from flask_appbuilder.models.sqla.interface import SQLAInterface
#from flask import render_template, request
from app.comments.models import Document, Revision, Commentsheet, Comment, Dedoc, Moc, Discipline, Unit, SplitOfWorks, Actionrequired, Issuetype
from app import appbuilder, db
from .helpers import check_labels, get_data_from_cs
from flask import session, redirect, url_for, abort
from app.comments.customWidgets import commentListWidget, RevisionListCard
from flask_appbuilder.widgets import ListBlock
from .helpers import update_data_from_cs
from app.comments.ListeXLSX.helpers import add_moc, add_unit
#import app.comments.ListeXLSX.helpers
from flask_babel import lazy_gettext
   
   
class CommentView(ModelView):
    datamodel = SQLAInterface(Comment)
    list_columns = ['ownerCommentComment','contractorReplyComment','ownerCounterReplyComment','finalComment', 'commentStatus', 'pos']
    
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
    add_title = 'DRAS View'
    edit_title = 'DRAS Edit'
    list_title = 'DRAS List'
    show_title = 'DRAS Show'
    add_columns = ['cs_file', 'current'] 
    list_columns = ['created_on','stage_icon','documentReferenceRev','filename', 'is_current', 'download'] 
    label_columns = {
        'documentReferenceDoc': 'Document',
        'documentReferenceRev': 'Revision', 
        'documentReferenceDesc': 'Description',
        'documentReferenceBy': 'By',

        'ownerTransmittalReference': 'ID', 
        'ownerTransmittalDate':'Date', 
        'response_status': 'Status',

        'contractorTransmittalReference': 'ID', 
        'contractorTransmittalDate': 'Date', 
        'contractorTransmittalMr': 'MR',
        'contractorTransmittalVendor':'Vendor',
        'stage_icon':'Stage',

        'issuetype':'Issue Type', 
        'actionrequired':'Action Required', 
        'notificationItem':'Notification Item',
        'actualDate': 'Actual Date', 
        'expectedDate': 'Expected Date',
        'plannedDate': 'Planned Date'
    }
    show_fieldsets = [
        (lazy_gettext('DRAS Info'),

         {'fields': ['id', 'document', 'revision', 'stage_icon']}),
        
        (lazy_gettext('Document Reference'),

         {'fields': ['documentReferenceDoc', 
                    'documentReferenceRev', 
                    'documentReferenceDesc',
                    'documentReferenceBy'], 'expanded': True}),
        
        (lazy_gettext('Owner Transmittal Reference'),

         {'fields': ['ownerTransmittalReference', 
                    'ownerTransmittalDate', 
                    'response_status'], 
                    'expanded': False}),
        
        (lazy_gettext('Contractor Trasmittal Reference'), 

         {'fields': ['contractorTransmittalReference', 
                    'contractorTransmittalDate', 
                    'contractorTransmittalMr',
                    'contractorTransmittalVendor'], 
                    'expanded': False}),
        
        (lazy_gettext('DRAS Notification'),

         {'fields': ['issuetype', 
                    'actionrequired', 
                    'notificationItem',
                    'actualDate', 
                    'expectedDate',
                    'plannedDate'], 'expanded': False}),
        
        (lazy_gettext('DRAS Internal Info'),

         {'fields': ['note'], 
                    'expanded': False}),
    ]
    add_fieldsets = [
        (lazy_gettext('DRAS File'),
         {'fields': ['cs_file','current']}),
        
        (lazy_gettext('DRAS Notification'),
         {'fields': ['issuetype', 
                    'actionrequired', 
                    'notificationItem',
                    'actualDate', 
                    'expectedDate',
                    'plannedDate'], 'expanded': True}),
        
        (lazy_gettext('DRAS Internal Info'),
         {'fields': ['note'], 
                    'expanded': False}),
        
    ]
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
        doc = get_data_from_cs(item) 

        session['last_document'] = doc
        print('PRE ADD FUNCTION ************ ',session['last_document'] )

        if doc == False:
            return abort(400, 'Pre Add Function Error.')



    def pre_update(self, item):
        session['last_document'] = item.document_id
        
        
        # Find or Create Document
        # Find or Create Revision
    
    def post_add_redirect(self):
        """Override this function to control the redirect after add endpoint is called."""
        
        doc = str(session['last_document'])
        print('POST EDIT FUNCTION ************ ',session['last_document'] )

        return redirect(url_for('DocumentView.show', pk=doc))

class DrasUploadView(ModelView):
    datamodel = SQLAInterface(Commentsheet)
    add_title = 'DRAS Upload'
    default_view = 'add'
    base_permissions = ['can_add'] 
    label_columns = {
        'documentReferenceDoc': 'Document',
        'documentReferenceRev': 'Revision', 
        'documentReferenceDesc': 'Description',
        'documentReferenceBy': 'By',

        'ownerTransmittalReference': 'ID', 
        'ownerTransmittalDate':'Date', 
        'response_status': 'Status',

        'contractorTransmittalReference': 'ID', 
        'contractorTransmittalDate': 'Date', 
        'contractorTransmittalMr': 'MR',
        'contractorTransmittalVendor':'Vendor',
        'stage_icon':'Stage',

        'issuetype':'Issue Type', 
        'actionrequired':'Action Required', 
        'notificationItem':'Notification Item',
        'actualDate': 'Actual Date', 
        'expectedDate': 'Expected Date',
        'plannedDate': 'Planned Date'
    }
    
    add_fieldsets = [
        (lazy_gettext('DRAS File'),
         {'fields': ['cs_file','current']}),
        
        (lazy_gettext('DRAS Notification'),
         {'fields': ['issuetype', 
                    'actionrequired', 
                    'notificationItem',
                    'actualDate', 
                    'expectedDate',
                    'plannedDate'], 'expanded': True}),
        
        (lazy_gettext('DRAS Internal Info'),
         {'fields': ['note'], 
                    'expanded': False}),
        
    ]
    #related_views = [CommentView]
    #show_template = 'appbuilder/general/model/show_cascade.html'


    
    def pre_add(self, item):
        
        
        # Check File Requirements
        check_labels(item)
        doc = get_data_from_cs(item) 

        session['last_document'] = doc
        print('PRE ADD FUNCTION ************ ',session['last_document'] )

        if doc == False:
            return abort(400, 'Pre Add Function Error.')



    def pre_update(self, item):
        session['last_document'] = item.document_id
        
        
        # Find or Create Document
        # Find or Create Revision
    
    def post_add_redirect(self):
        """Override this function to control the redirect after add endpoint is called."""
        
        doc = str(session['last_document'])
        print('POST EDIT FUNCTION ************ ',session['last_document'] )

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
    show_columns = ['name','moc','dedoc']

    label_columns = {
        
        'moc':'Main Operating Center',
        'dedoc':'DED Operating Center'
    }








class DEDOperatingCenterView(ModelView):
    datamodel = SQLAInterface(Dedoc)
    #related_views = [CommentSheetView, RevisionView, CommentView]
    #show_template = 'appbuilder/general/model/show_cascade.html'

    list_columns = ['name','moc','created_on','created_by']

class MainOperatingCenterView(ModelView):
    datamodel = SQLAInterface(Moc)
    related_views = [DEDOperatingCenterView]
    show_template = 'appbuilder/general/model/show_cascade.html'

    list_columns = ['name','created_on','created_by']

class DisciplineView(ModelView):
    datamodel = SQLAInterface(Discipline)
    #related_views = [CommentSheetView, RevisionView, CommentView]
    #show_template = 'appbuilder/general/model/show_cascade.html'

    list_columns = ['name','created_on','created_by']

class UnitView(ModelView):
    datamodel = SQLAInterface(Unit)
    #related_views = [CommentSheetView, RevisionView, CommentView]
    #show_template = 'appbuilder/general/model/show_cascade.html'

    list_columns = ['name','code','moc', 'dedoc', 'created_on','created_by']

class SowView(ModelView):
    datamodel = SQLAInterface(SplitOfWorks)
    #related_views = [CommentSheetView, RevisionView, CommentView]
    #show_template = 'appbuilder/general/model/show_cascade.html'

    list_columns = ['id','unit.name','unit.code','discipline.name', 'oc','oc.moc']

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())

class IssueTypeView(ModelView):
    datamodel = SQLAInterface(Issuetype)

class ActionRequiredView(ModelView):
    datamodel = SQLAInterface(Actionrequired)





appbuilder.add_view(DocumentView, 'Document', icon="fa-folder-open-o",
                    category="DRAS", category_icon='fa-envelope')

appbuilder.add_view(RevisionView, 'Revision',
                    icon="fa-folder-open-o", category="DRAS")

appbuilder.add_view(CommentSheetView, 'Dras List',
                    icon="fa-folder-open-o", category="DRAS")

appbuilder.add_view(CommentView, 'Comment',
                    icon="fa-folder-open-o", category="DRAS")

 
appbuilder.add_separator(category="DRAS")

appbuilder.add_view(DrasUploadView, 'Dras Upload',
                    icon="fa-folder-open-o", category="DRAS")


appbuilder.add_view(IssueTypeView, 'Issue Type',
                    icon="fa-folder-open-o", category="DRAS Components")

appbuilder.add_view(ActionRequiredView, 'Action Required',
                    icon="fa-folder-open-o", category="DRAS Components")

appbuilder.add_separator(category="DRAS Components")

appbuilder.add_view(UnitView, 'Unit',
                    icon="fa-folder-open-o", category="DRAS Components")

appbuilder.add_view(DisciplineView, 'Discipline',
                    icon="fa-folder-open-o", category="DRAS Components")

appbuilder.add_separator(category="DRAS Components")

appbuilder.add_view(MainOperatingCenterView, 'Main Operating Centers',
                    icon="fa-folder-open-o", category="DRAS Components")

appbuilder.add_view(DEDOperatingCenterView, 'DED Operating Centers',
                    icon="fa-folder-open-o", category="DRAS Components")

appbuilder.add_view(SowView, 'Split of Works',
                    icon="fa-folder-open-o", category="DRAS Components")



db.create_all()

#add_moc()
'''