
from util.util import list_button

class EditButtonMixin(object):
    def edit(self, obj):
        return list_button(self,obj._meta, "change","Edit", obj.id)
    edit.allow_tags = True

class NoteButtonMixin(object):
    def note(self, obj):
        return "note"

class DeleteButtonMixin(object):
    def delete(self, obj):
        return list_button(self, obj._meta, "delete", "Delete", obj.id)
    delete.allow_tags = True
