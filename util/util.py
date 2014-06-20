import re
import datetime
import time
import string
import random
from django.core.urlresolvers import reverse



def file_url(category):
    def inner(instance, filename):
        r = re.compile(r'[^\S]')
        filename = r.sub('', filename)
        now = datetime.datetime.now()
        timestamp = int(time.time())
        return 'uploads/{0}/{1.year:04}/{1.month:02}/{1.day:02}/{2}/{3}'.format( \
                category, now, timestamp, filename)
    return inner

def random_string(length):
    alphanumeric = string.letters + string.digits
    return "".join(random.choice(alphanumeric) for i in range(length))

def list_button(self, meta, page, button_display, obj_id=None, query=None): 
    info = self.admin_site.name, meta.app_label, meta.module_name, page 
    string = '{0}:{1}_{2}_{3}'.format(*info)
    if obj_id:
        url = reverse(string, args=(obj_id,)) 
    else:
        url = reverse(string)
    if query:
        url += query
    return "<a href='{0}'>{1}</a>".format(url, button_display) 
