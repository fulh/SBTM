import xadmin
from .models import Project,TestCase,Module
from xadmin.layout import Fieldset

class ProjectAdmin(object):
    list_display = ("id", "name", "proj_owner", "test_owner", "dev_owner", "desc", "create_time", "update_time")


class ModuleAdmin(object):
    list_display = ("id", "name", "belong_project", "test_owner", "desc", "create_time", "update_time")


class TestCaseAdmin(object):
    list_display = (
        "id", "case_name", "belong_project", "request_data", "uri", "assert_key", "maintainer",
        "extract_var", "request_method", "status", "created_time", "updated_time",'user')
    form_layout = (
        Fieldset(None,
                 'case_name', 'belong_project', 'request_data', 'uri'
                 ),
        Fieldset(None,
                 'pc_parent', **{"style": "display:None"}
                 ),
    )


xadmin.site.register(Project,ProjectAdmin)
xadmin.site.register(Module,ModuleAdmin)
xadmin.site.register(TestCase, TestCaseAdmin)

