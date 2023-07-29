from flask import Blueprint

admin = Blueprint(
    name="admin",
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)

import FoodyAdmin.views
import FoodyAdmin.model

@admin.app_context_processor
def admin_context():
    func = {
        "GetAdminObject":""
    }
    return func

# apps:
import FoodyAdmin.api
import FoodyAdmin.Apps.ManageUsers.views
import FoodyAdmin.Apps.ManageFoods.views
import FoodyAdmin.Apps.Accounting.views