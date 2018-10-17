"""Reformat parameter string values (Super handy for renaming elements)"""
#pylint: disable=E0401,W0703,W0613
from pyrevit import coreutils
from pyrevit import revit, DB
from pyrevit import forms


__author__ = "{{author}}"
__context__ = "selection"


class ReValueItem(object):
    def __init__(self, eid, oldvalue, final=False):
        self.eid = eid
        self.oldvalue = oldvalue
        self.newvalue = ''
        self.final = final
        self.tooltip = ''

    def format_value(self, old_format, new_format):
        try:
            if old_format and new_format:
                self.newvalue = coreutils.reformat_string(self.oldvalue,
                                                          old_format,
                                                          new_format)
                self.tooltip = '{} --> {}'.format(old_format, new_format)
            else:
                self.tooltip = 'No Conversion Specified'
        except Exception:
            self.newvalue = ''


class ReValueWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        # create pattern maker window and process options
        forms.WPFWindow.__init__(self, xaml_file_name)
        self._target_elements = revit.get_selection().elements
        self._reset_preview()
        self._setup_params()

    @property
    def selected_param(self):
        return self.params_cb.SelectedItem

    @property
    def preview_items(self):
        return self.preview_dg.ItemsSource

    @property
    def selected_preview_items(self):
        return self.preview_dg.SelectedItems

    def _setup_params(self):
        unique_params = set()
        for element in self._target_elements:
            for param in element.Parameters:
                if not param.IsReadOnly \
                        and param.StorageType == DB.StorageType.String:
                    unique_params.add(param.Definition.Name)

        all_params = ['Name']
        all_params.extend(sorted(list(unique_params)))
        self.params_cb.ItemsSource = all_params
        self.params_cb.SelectedIndex = 0

    def _reset_preview(self):
        self._revalue_items = []
        self.preview_dg.ItemsSource = self._revalue_items

    def _refresh_preview(self):
        self.preview_dg.Items.Refresh()

    def on_param_change(self, sender, args):
        self._reset_preview()
        for element in self._target_elements:
            if self.selected_param == 'Name':
                old_value = revit.ElementWrapper(element).name
            else:
                param = element.LookupParameter(self.selected_param)
                if param:
                    old_value = param.AsString()

            newitem = ReValueItem(eid=element.Id, oldvalue=old_value)
            newitem.format_value(self.orig_format_tb.Text,
                                 self.new_format_tb.Text)
            self._revalue_items.append(newitem)
        self._refresh_preview()

    def on_format_change(self, sender, args):
        for item in self._revalue_items:
            if not item.final:
                item.format_value(self.orig_format_tb.Text,
                                  self.new_format_tb.Text)
        self._refresh_preview()

    def mark_as_final(self, sender, args):
        selected_names = [x.eid for x in self.selected_preview_items]
        for item in self._revalue_items:
            if item.eid in selected_names:
                item.final = True
        self._refresh_preview()

    def apply_new_values(self, sender, args):
        self.Close()
        try:
            with revit.Transaction('ReValue {}'.format(self.selected_param),
                                   log_errors=False):
                for item in self._revalue_items:
                    if item.newvalue:
                        element = revit.doc.GetElement(item.eid)
                        if self.selected_param == 'Name':
                            element.Name = item.newvalue
                        else:
                            param = element.LookupParameter(self.selected_param)
                            if param:
                                param.Set(item.newvalue)
        except Exception as ex:
            forms.alert(str(ex), title='Error')


ReValueWindow('ReValueWindow.xaml').show(modal=True)
