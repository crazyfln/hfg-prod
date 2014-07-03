"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'hfg.manager_dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        self.children.append(modules.ModelList(
            title="Administration",
            column=1,
            collapsible=False,
            models=('app.models.Facility','app.models.FacilityMessage','app.models.Invoice','account.models.User')
        ))
        
        self.children.append(modules.ModelList(
            title="Options",
            column=1,
            collapsible=True,
            models=('account.models.HoldingGroup', 'app.models.Amenity', 'app.models.Condition', 'app.models.Fee', 'app.models.RoomType', 'app.models.FacilityType', 'app.models.Language')
        ))
        
        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=2,
        ))


