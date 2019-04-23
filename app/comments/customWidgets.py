from flask_appbuilder.widgets import ListWidget, ListBlock

class commentListWidget(ListWidget):
    template = 'widgets/commentList.html' 

class RevisionListCard(ListBlock):
    template = 'widgets/revisionListCard.html'
   