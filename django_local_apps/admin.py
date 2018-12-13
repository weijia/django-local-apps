from djangoautoconf.auto_conf_admin_tools.admin_features.foreign_key_sort import ForeignKeySortFeature
from djangoautoconf.auto_conf_admin_tools.admin_register import AdminRegister
from djangoautoconf.auto_conf_admin_tools.foreign_key_auto_complete import ForeignKeyAutoCompleteFeature
from obj_sys.models_ufs_obj import UfsObj
import models


r = AdminRegister()

# s = ForeignKeySortFeature()
# s.sort_attribute = "content_type"
# s.sort_field_of_foreign_key = "model"
# r.add_feature(s)
# r.register(models.DbCleanConfig)


r = AdminRegister()
f = ForeignKeyAutoCompleteFeature()
f.set_search_field_by_model({UfsObj: ("uuid", "ufs_url", "full_path")})
r.add_feature(f)
s = ForeignKeySortFeature()
r.register_all_models(models)

