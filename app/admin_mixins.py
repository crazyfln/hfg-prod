from django.core.urlresolvers import reverse
from util.util import list_button

class EditButtonMixin(object):
    def edit(self, obj):
        return list_button(self,obj._meta, "change","Edit", obj.id)
    edit.allow_tags = True

class NoteButtonMixin(object):
    def note(self, obj):
        if obj._meta.model_name == 'facility':
            url_name = 'edit_manager_note_facility'
        elif obj._meta.model_name == 'invoice':
            url_name = 'edit_manager_note_invoice'
        url = reverse(url_name, args=(obj.pk,))
        display = "Note"
        jsurl = "javascript:window.open('" + url + "','editNoteWindow',width=100,height=100)"
        return "<a href={0}>{1}</a>".format(jsurl,display)
    note.allow_tags = True


class DeleteButtonMixin(object):
    def delete(self, obj):
        return list_button(self, obj._meta, "delete", "Delete", obj.id)
    delete.allow_tags = True
