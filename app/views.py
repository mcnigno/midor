from flask import render_template, request
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, BaseView, expose
from app import appbuilder, db
from .helpers import upload_ewd, upload_correspondence,create_file_list
from .models import EarlyWorksDoc, Correspondence, Uop_Bpd, Uop_spec
from flask_appbuilder.models.sqla.filters import FilterStartsWith, FilterEqualFunction, FilterEqual, FilterNotContains


"""
    DRASS Comments View Section
"""
from flask_appbuilder.baseviews import BaseView, expose
from flask_appbuilder import ModelView, action, MasterDetailView, MultipleView
from flask_appbuilder.models.sqla.interface import SQLAInterface
#from flask import render_template, request
#from app.models import Document, Revision, Commentsheet, Comment, Dedoc, Moc,Discipline, Unit, SplitOfWorks, Actionrequired, Issuetype
from app.models import (Disciplinedras, Mocmodel, Dedocmodel, Unitmodel, 
                        Splitofworks, Drasdocument, Drasrevision, Drasissuetype,
                        Drasactionrequired, Drascommentsheet, Drascomment,
                        Tagdiscipline)


#from app import appbuilder, db
from app.comments.helpers import check_labels, get_data_from_cs
from flask import session, redirect, url_for, abort
from app.comments.customWidgets import commentListWidget, RevisionListCard
from flask_appbuilder.widgets import ListBlock
from app.comments.helpers import update_data_from_cs
#from app.comments.ListeXLSX.helpers import add_moc, add_unit
#import app.comments.ListeXLSX.helpers
from flask_babel import lazy_gettext


#from app.init_helpers import fakeItem3

'''
from app.comments.views import (DocumentView, RevisionView, CommentSheetView, 
                                CommentView, DrasUploadView, DEDOperatingCenterView,
                                MainOperatingCenterView, DEDOperatingCenterView, UnitView,
                                SowView, IssueTypeView, ActionRequiredView)
'''

"""
    Early Works View Section 
"""
class MidorewdDashboardView(BaseView):
    default_view = 'midorewd'
    @expose('/midorewd', methods=['POST', 'GET'])
    def midorewd(self): 
        return self.render_template('midorewd.html')

class MidorDrasDashboardView(BaseView):
    default_view = 'dash_dras'
    @expose('/dash_dras', methods=['POST', 'GET'])
    def dash_dras(self): 
        return self.render_template('dash_dras.html')

class MidorDras2DashboardView(BaseView):
    default_view = 'dash_dras'
    @expose('/dash_dras', methods=['POST', 'GET'])
    def dash_dras(self): 
        return self.render_template('dash_dras2.html')


class EarlyWorksDocView(ModelView):
    datamodel = SQLAInterface(EarlyWorksDoc)
    list_columns = ['discipline', 'contractor_code', 'revision', 'short_desc','file']
    #list_columns = ['contractor_code', 'short_desc','file']
    #
    #show_template = 'custom/showdoc.html'
    list_template = 'listEwd.html'              

class EarlyWorksDocViewRestricted(ModelView):
    datamodel = SQLAInterface(EarlyWorksDoc)
    list_columns = ['discipline', 'contractor_code','short_desc','file']
    base_filters = [['unit',FilterNotContains,'11']]
    list_template = 'listEwd.html'

class CorrespondenceView(ModelView):
    datamodel = SQLAInterface(Correspondence)
    list_columns = ['document_code','doc_description','file']
    list_template = 'listCrs.html'

class Uop_BpdView(ModelView):
    datamodel = SQLAInterface(Uop_Bpd)
    list_columns = ['document_code', 'rev', 'doc_description', 'file']
    list_template = 'listUop_bdp.html'

class Uop_SpecView(ModelView):
    datamodel = SQLAInterface(Uop_spec)
    label_columns = {
        'revision':'Rev'
    }
    list_columns = ['document_code', 'revision', 'doc_description', 'file']
    list_template = 'listUop_spec.html' 

class UnitView(ModelView):
    datamodel = SQLAInterface(Unitmodel)
    #related_views = [CommentSheetView, RevisionView, CommentView]
    #show_template = 'appbuilder/general/model/show_cascade.html'

    list_columns = ['name','code','moc', 'dedoc']
    label_columns = {
        'moc':'Main OC',
        'dedoc':'DED OC', 
        'name': 'Title',
        'code': 'Unit'
    }

class DEDOperatingCenterView(ModelView):
    datamodel = SQLAInterface(Dedocmodel)
    #related_views = [CommentSheetView, RevisionView, CommentView]
    #show_template = 'appbuilder/general/model/show_cascade.html'

    list_columns = ['name','moc']
    label_columns = {
        'moc':'MOC',
        'name': 'Name'
    }

class MainOperatingCenterView(ModelView):
    datamodel = SQLAInterface(Mocmodel)
    #related_views = [DEDOperatingCenterView]
    show_template = 'appbuilder/general/model/show_cascade.html'

    list_columns = ['name','created_on','created_by']

class DisciplineView(ModelView):
    datamodel = SQLAInterface(Disciplinedras)
    #related_views = [CommentSheetView, RevisionView, CommentView]
    #show_template = 'appbuilder/general/model/show_cascade.html'

    list_columns = ['name','created_on','created_by']

class SowView(ModelView):
    datamodel = SQLAInterface(Splitofworks)
    #related_views = [CommentSheetView, RevisionView, CommentView]
    #show_template = 'appbuilder/general/model/show_cascade.html'


    list_columns = ['unitmodel.code','unitmodel.name','disciplinedras.name','oc.moc','oc']
    show_columns = list_columns = ['unitmodel.code','unitmodel.name','disciplinedras.name','oc.moc','oc']
    label_columns = {
        'unitmodel.name':'Unit Title',
        'unitmodel.code':'Unit',
        'disciplinedras.name': 'Discipline',
        'oc': 'DED OC',
        'oc.moc': 'MAIN OC'
    }

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())

  
class IssueTypeView(ModelView):
    datamodel = SQLAInterface(Drasissuetype)
    list_columns = ['name']

class ActionRequiredView(ModelView):
    datamodel = SQLAInterface(Drasactionrequired)
    list_columns = ['name']

class CommentSheetView(ModelView):
    datamodel = SQLAInterface(Drascommentsheet)
    add_title = 'View DRAS'
    edit_title = 'Edit DRAS'
    edit_exclude_columns = ['cs_file']
    list_title = 'List DRAS History'
    show_title = 'Show DRAS' 
    add_columns = ['cs_file', 'current'] 
    order_columns = ['actualDate']
    base_order = ('actualDate','asc') 
    list_columns = ['drasrevision','stage_icon','actualDate','expectedDate','notificationItem','response_status', 'is_current', 'download'] 
    label_columns = {
        'documentReferenceDoc':     'Document',
        'documentReferenceRev':     'Revision', 
        'documentReferenceDesc':    'Description',
        'documentReferenceBy':      'Discipline',

        'ownerTransmittalReference':'ID', 
        'ownerTransmittalDate':     'Date', 
        'response_status':          'Status',

        'contractorTransmittalReference':   'ID', 
        'contractorTransmittalDate':        'Date', 
        'contractorTransmittalMr':          'MR',
        'contractorTransmittalVendor':      'Vendor',
        'stage_icon':'Stage',

        'issuetype':                'Issue Type', 
        'actionrequired':           'Action Required', 
        'notificationItem':         'Notification Item',
        'actualDate':               'Actual Date', 
        'expectedDate':             'Expected Date',
        'plannedDate':              'Planned Date',
        'drasdocument':             'Document',
        'drasrevision':             'Revision'
    }
    
    show_fieldsets = [
        (lazy_gettext('DRAS Info'),

         {'fields': ['drasdocument', 'drasrevision', 'stage_icon']}),
        
        (lazy_gettext('Document Reference'),

         {'fields': ['documentReferenceDoc', 
                    'documentReferenceRev', 
                    'documentReferenceDesc',
                    'documentReferenceBy',
                    'issuetype'], 'expanded': True}),
        
        (lazy_gettext('Owner Status'),

         {'fields': [ 
                    'response_status'], 
                    'expanded': True}),
        
        (lazy_gettext('Contractor Trasmittal Reference'), 

         {'fields': [
                    'contractorTransmittalDate',
                    'contractorTransmittalReference', 
                    'contractorTransmittalMr',
                    'contractorTransmittalVendor',
                    'actionrequired'], 
                    'expanded': True}),
        
        (lazy_gettext('DRAS Notification'),

         {'fields': ['notificationItem',
                    'actualDate', 
                    'expectedDate'], 'expanded': True}),
        
        (lazy_gettext('DRAS Internal Info'),

         {'fields': ['note'], 
                    'expanded': False}),
    ]

    edit_fieldsets = [
        (lazy_gettext('DRAS Info'),

         {'fields': ['drasdocument', 'drasrevision']}),
        
        (lazy_gettext('Document Reference'),

         {'fields': ['documentReferenceDoc', 
                    'documentReferenceRev', 
                    'documentReferenceDesc',
                    'documentReferenceBy',
                    'issuetype'], 'expanded': True}),
        
        (lazy_gettext('Owner Transmittal Reference'),

         {'fields': [ 
                    'response_status'], 
                    'expanded': True}),
        
        (lazy_gettext('Contractor Trasmittal Reference'), 

         {'fields': [ 
                    'contractorTransmittalMr',
                    'contractorTransmittalVendor',
                    'actionrequired'], 
                    'expanded': True}),
        
        (lazy_gettext('DRAS Notification'),

         {'fields': ['notificationItem',
                    'actualDate', 
                    'expectedDate'], 'expanded': True}),
        
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
        print(session)
 
        #return redirect(self.get_redirect())
        return redirect(url_for('DrasdocumentView.show', pk=item.drasdocument_id))

    

    def pre_add(self, item):
        
        
        # Check File Requirements
        check_labels(item)
        doc = get_data_from_cs(item) 

        #session['last_document'] = doc
        #print('PRE ADD FUNCTION ************ ',session['last_document'] )

        if doc == False:
            return abort(400, 'Pre Add Function Error.')



    def pre_update(self, item):
        if session['last_document']:
            session['last_document'] = item.drasdocument_id
        
        
        # Find or Create Document
        # Find or Create Revision
    
    def post_add_redirect(self):
        """Override this function to control the redirect after add endpoint is called."""
        if session['last_document']:
            doc = str(session['last_document'])
            print('POST EDIT FUNCTION ************ ',session['last_document'] )

            return redirect(url_for('DrasdocumentView.show', pk=doc))

class CommentView(ModelView):
    datamodel = SQLAInterface(Drascomment)
    list_columns = ['tag','ownerCommentComment','contractorReplyStatus','contractorReplyComment','ownerCounterReplyComment','finalComment', 'commentStatus', 'pos']
    show_title = 'Show Comment'
    list_title = 'List Comments'
    add_title = 'Add Comment'
    edit_title = 'Edit Comment' 
    search_columns = ['commentStatus']
    list_widget = commentListWidget 
    label_columns = {
        'ownerCommentBy': 'by',
        'ownerCommentDate': 'Date',
        'ownerCommentComment': 'Owner:',

        'contractorReplyDate': 'Date',
        'contractorReplyStatus': 'Status',
        'contractorReplyComment': 'Contractor:',

        'ownerCounterReplyDate': 'Date',
        'ownerCounterReplyComment' : 'Owner:',

        'finalAgreementDate': 'Agreement Date', 
        'finalAgreemntCommentDate':'Comment Date', 
        'finalAgreementComment': 'Agreement:',
        'commentStatus': 'Status'
        
    }

    show_fieldsets = [
        (lazy_gettext('DRAS Comment'),

         {'fields': ['pos', 'tag', 'info']}),
        
        (lazy_gettext('Owner Comment'),

         {'fields': ['ownerCommentBy', 
                    'ownerCommentDate', 
                    'ownerCommentComment'], 'expanded': True}),
        
        (lazy_gettext('Contractor Reply'),

         {'fields': ['contractorReplyDate', 
                    'contractorReplyStatus', 
                    'contractorReplyComment'], 
                    'expanded': False}),
        
        (lazy_gettext('Owner Counter Reply'), 

         {'fields': ['ownerCounterReplyDate', 
                    'ownerCounterReplyComment',], 
                    'expanded': False}),
        
        (lazy_gettext('Final Agreement'),

         {'fields': ['finalAgreementDate', 
                    'finalAgreemntCommentDate', 
                    'finalAgreementComment',
                    'commentStatus'], 'expanded': False}),
        
        
    ]
   
    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())

class RevisionView(ModelView):
    datamodel = SQLAInterface(Drasrevision)
    list_columns = ['drasdocument','stage_class','name', 'current_cs']
    show_columns = ['drasdocument','stage_class','name', 'current_cs']
    label_columns = {
        'drasdocument':'Document',
        'stage_class':'Stage',
        'name': 'Name',
        'current_cs': 'Status'
    }
    
    show_title = 'Show Revision'
    list_title = 'List Revision'
    add_title = 'Add Revision'
    edit_title = 'Edit Revision' 
    related_views = [CommentSheetView] 
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

class DrasdocumentView(ModelView):
    datamodel = SQLAInterface(Drasdocument)
    related_views = [CommentSheetView, RevisionView, CommentView]
    show_template = 'appbuilder/general/model/show_cascade.html'

    list_columns = ['name','moc','dedoc', 'open_comm' ] 
    show_columns = ['title_name','description', 'moc','dedoc','current_rev','current_stage']
    show_title = 'Show Document'
    list_title = 'List Document'
    add_title = 'Add Document'
    edit_title = 'Edit Document'


    label_columns = {
        
        'moc':'Main Operating Center',
        'dedoc':'DED Operating Center',
        'title_name': 'Document',
        'current_rev': 'Current Rev',
        'current_stage': 'Stage',
        'description' : 'Title' 

         
    }

class DrasUploadView(ModelView):
    datamodel = SQLAInterface(Drascommentsheet)
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
        'plannedDate': 'Planned Date',
        'cs_file': 'File'
    }
    
    add_fieldsets = [
        (lazy_gettext('DRAS File'),
         {'fields': ['cs_file','current']}),
        
        (lazy_gettext('DRAS Notification'),
         {'fields': ['issuetype', 
                    'actionrequired', 
                    'notificationItem',
                    'actualDate', 
                    'expectedDate'], 'expanded': True}),
        
        (lazy_gettext('DRAS Internal Info'),
         {'fields': ['note'], 
                    'expanded': True}),
        
    ]
    #related_views = [CommentView]
    #show_template = 'appbuilder/general/model/show_cascade.html'


    
    def pre_add(self, item):
        
        
        # Check File Requirements
        check_labels(item)
        doc = get_data_from_cs(item) 
        
        if session['last_document']:
            session['last_document'] = doc
            print('PRE ADD FUNCTION ************ ',session['last_document'] )
        

        if doc == False:
            return abort(400, 'Pre Add Function Error.')

        

    def pre_update(self, item):
        if session['last_document']:
            session['last_document'] = item.drasdocument_id
        
        
        # Find or Create Document
        # Find or Create Revision
    
    
    def post_add_redirect(self):
        # Override this function to control the redirect after add endpoint is called.
        try:
            if session['last_document']:
                doc = session['last_document']
                #print('POST EDIT FUNCTION ************ ',session['last_document'] )

                return redirect(url_for('DrasdocumentView.show', pk=doc))
        except:
            print('Something still does not work for session')
            return redirect(self.get_redirect())

class TagdisciplineView(ModelView):
    datamodel = SQLAInterface(Tagdiscipline)
    list_columns = ['name','start','finish']

#appbuilder.add_view(RevisionView,'Revision',icon="fa-folder-open-o", category="DRAS", category_icon='fa-envelope')


"""    
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404


#appbuilder.add_view(MidorewdDashboardView, "Early Works Documentation", icon="fa-folder-open-o", category="Dashboard", category_icon='fa-envelope')
appbuilder.add_view(MidorDrasDashboardView, "Comments", icon="fa-folder-open-o", category="Dashboard", category_icon='fa-envelope')
appbuilder.add_view(MidorDras2DashboardView, "DRAS", icon="fa-folder-open-o", category="Dashboard", category_icon='fa-envelope')

appbuilder.add_view(EarlyWorksDocView, "Engineering Documents", icon="fa-folder-open-o", category="Early Works", category_icon='fa-envelope')
appbuilder.add_view(EarlyWorksDocViewRestricted, "Engineering Documents PMC", icon="fa-folder-open-o", category="Early Works", category_icon='fa-envelope')
appbuilder.add_view(CorrespondenceView, "Correspondence", icon="fa-folder-open-o", category="Early Works", category_icon='fa-envelope')
appbuilder.add_view(Uop_BpdView, "UOP BDP List", icon="fa-folder-open-o", category="Early Works", category_icon='fa-envelope')
appbuilder.add_view(Uop_SpecView, "UOP Std. Specification", icon="fa-folder-open-o", category="Early Works", category_icon='fa-envelope')


appbuilder.add_view(MainOperatingCenterView, 'Main Operating Centers',icon="fa-folder-open-o", category="DRAS Components")

appbuilder.add_view(DEDOperatingCenterView, 'DED Operating Centers', icon="fa-folder-open-o", category="DRAS Components")

appbuilder.add_view(UnitView, 'Unit',icon="fa-folder-open-o", category="DRAS Components")

appbuilder.add_view(DisciplineView, 'Discipline',icon="fa-folder-open-o", category="DRAS Components")
appbuilder.add_view(TagdisciplineView, 'Tags',icon="fa-folder-open-o", category="DRAS Components")


appbuilder.add_view(SowView, 'Split of Works',icon="fa-folder-open-o", category="DRAS Components")

appbuilder.add_view(DrasdocumentView, 'Document', icon="fa-folder-open-o",category="DRAS DCC", category_icon='fa-envelope')


appbuilder.add_view(RevisionView, 'Revision',
                    icon="fa-folder-open-o", category="DRAS DCC")

appbuilder.add_view(CommentSheetView, 'Dras List',
                    icon="fa-folder-open-o", category="DRAS DCC")

appbuilder.add_view(CommentView, 'Comment',
                    icon="fa-folder-open-o", category="DRAS DCC")

 
appbuilder.add_separator(category="DRAS DCC")

appbuilder.add_view(DrasUploadView, 'Dras Upload',
                    icon="fa-folder-open-o", category="DRAS DCC")




appbuilder.add_view(IssueTypeView, 'Issue Type',
                    icon="fa-folder-open-o", category="DRAS Components")

appbuilder.add_view(ActionRequiredView, 'Action Required',
                    icon="fa-folder-open-o", category="DRAS Components")

appbuilder.add_separator(category="DRAS Components")




appbuilder.add_separator(category="DRAS Components")





#db.create_all()

#add_moc()

db.create_all() 
#upload_ewd()
#create_file_list()
#upload_correspondence()
#fakeItem3(1)  