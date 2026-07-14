from . import checklist, checklist_as_list, full, nuggets, single_nugget

METHODS = {
    full.NAME: full,
    checklist.NAME: checklist,
    checklist_as_list.NAME: checklist_as_list,
    nuggets.NAME: nuggets,
    single_nugget.NAME: single_nugget,
}
