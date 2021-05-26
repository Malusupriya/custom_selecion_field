# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

""" High-level objects for fields. """
from odoo.fields import Selection
from collections import defaultdict
from functools import partial
from odoo import api, fields, models, _

class Selection(Selection):
    selection = None
    has_color = False

    def _description_selection(self, env):
        """ return the selection list (pairs (value, label)); labels are
            translated according to context language
        """
        selection = self.selection
        if isinstance(selection, str):
            return getattr(env[self.model_name], selection)()
        if callable(selection):
            return selection(env[self.model_name])

        # translate selection labels
        if env.lang:
            # return env['ir.translation'].get_field_selection(self.model_name, self.name)
            translate = partial(
                env['ir.translation']._get_source, self.name, 'selection', env.lang)
            if self.has_color:
                return [(value, translate(label) if label else label, color or '#000000') for value, label, color in selection]
            else:
                return [(value, translate(label) if label else label) for value, label in selection]
        else:
            return selection

    def get_values(self, env):
        """Return a list of the possible values."""
        selection = self.selection
        if isinstance(selection, str):
            selection = getattr(env[self.model_name], selection)()
        elif callable(selection):
            selection = selection(env[self.model_name])
        if self.has_color:
            return [value for value, _, _ in selection]
        else:
            return [value for value, _ in selection]

    def _selection_modules(self, model):
        """ Return a mapping from selection values to modules defining each value. """
        if not isinstance(self.selection, list):
            return {}
        value_modules = defaultdict(set)
        for field in reversed(resolve_mro(model, self.name, self._can_setup_from)):
            module = field.args.get('_module')
            if not module:
                continue
            if 'selection' in field.args:
                value_modules.clear()
                if isinstance(field.args['selection'], list):
                    if self.has_color:
                        for value, label, color in field.args['selection']:
                            value_modules[value].add(module)
                    else:
                        for value, label in field.args['selection']:
                            value_modules[value].add(module)
            if 'selection_add' in field.args:
                for value_label in field.args['selection_add']:
                    if len(value_label) > 1:
                        value_modules[value_label[0]].add(module)
        return value_modules

    def _setup_regular_base(self, model):
        assert self.selection is not None, "Field %s without selection" % self
        if isinstance(self.selection, list):
            if self.has_color:
                assert all(isinstance(v, str) for v, _,_ in self.selection), \
                    "Field %s with non-str value in selection" % self
            else:
                super(Selection, self)._setup_regular_base(model)

    """ Need to replace this below function inside the 'class Selection(Field)' in Field """
    # def _setup_attrs(self, model, name):
    #     super(Selection, self)._setup_attrs(model, name)
    #
    #     # determine selection (applying 'selection_add' extensions)
    #     values = None
    #     labels = {}
    #     has_label = False
    #     selection = []
    #     for field in reversed(resolve_mro(model, name, self._can_setup_from)):
    #         # We cannot use field.selection or field.selection_add here
    #         # because those attributes are overridden by ``_setup_attrs``.
    #         if 'selection' in field.args:
    #             if self.related:
    #                 _logger.warning("%s: selection attribute will be ignored as the field is related", self)
    #             selection = field.args['selection']
    #             if isinstance(selection, list):
    #                 if values is not None and values != [kv[0] for kv in selection]:
    #                     _logger.warning("%s: selection=%r overrides existing selection; use selection_add instead", self, selection)
    #                 values = [kv[0] for kv in selection]
    #
    #                 if 'has_color' in field.args:
    #                     has_label = field.args['has_color']
    #                     custom_selection = [(kv[0], kv[1]) for kv in selection]
    #                     labels = dict(custom_selection)
    #                 else:
    #                     labels = dict(selection)
    #                     self.ondelete = {}
    #             else:
    #                 values = None
    #                 labels = {}
    #                 self.selection = selection
    #                 self.ondelete = None
    #
    #         if 'selection_add' in field.args:
    #             if self.related:
    #                 _logger.warning("%s: selection_add attribute will be ignored as the field is related", self)
    #             selection_add = field.args['selection_add']
    #             assert isinstance(selection_add, list), \
    #                 "%s: selection_add=%r must be a list" % (self, selection_add)
    #             assert values is not None, \
    #                 "%s: selection_add=%r on non-list selection %r" % (self, selection_add, self.selection)
    #
    #             ondelete = field.args.get('ondelete') or {}
    #             new_values = [kv[0] for kv in selection_add if kv[0] not in values]
    #             for key in new_values:
    #                 ondelete.setdefault(key, 'set null')
    #             if self.required and new_values and 'set null' in ondelete.values():
    #                 raise ValueError(
    #                     "%r: required selection fields must define an ondelete policy that "
    #                     "implements the proper cleanup of the corresponding records upon "
    #                     "module uninstallation. Please use one or more of the following "
    #                     "policies: 'set default' (if the field has a default defined), 'cascade', "
    #                     "or a single-argument callable where the argument is the recordset "
    #                     "containing the specified option." % self
    #                 )
    #
    #             # check ondelete values
    #             for key, val in ondelete.items():
    #                 if callable(val) or val in ('set null', 'cascade'):
    #                     continue
    #                 if val == 'set default':
    #                     assert self.default is not None, (
    #                         "%r: ondelete policy of type 'set default' is invalid for this field "
    #                         "as it does not define a default! Either define one in the base "
    #                         "field, or change the chosen ondelete policy" % self
    #                     )
    #                     continue
    #                 raise ValueError(
    #                     "%r: ondelete policy %r for selection value %r is not a valid ondelete "
    #                     "policy, please choose one of 'set null', 'set default', 'cascade' or "
    #                     "a callable" % (self, val, key)
    #                 )
    #
    #             values = merge_sequences(values, [kv[0] for kv in selection_add])
    #             labels.update(kv for kv in selection_add if len(kv) == 2)
    #             self.ondelete.update(ondelete)
    #
    #     if values is not None:
    #         if has_label:
    #             self.selection = [(value, label, color) for value, label, color in selection]
    #         else:
    #             self.selection = [(value, labels[value]) for value in values]


class IrModelSelection(models.Model):
    _inherit = 'ir.model.fields.selection'

    # Override to check the condition for color
    def _reflect_selections(self, model_names):
        """ Reflect the selections of the fields of the given models. """
        fields = [
            field
            for model_name in model_names
            for field_name, field in self.env[model_name]._fields.items()
            if field.type in ('selection', 'reference')
            if isinstance(field.selection, list)
        ]
        if not fields:
            return

        # determine expected and existing rows
        IMF = self.env['ir.model.fields']
        # Commented by supriya
        # expected = {
        #     (field_id, value): (label, index)
        #     for field in fields
        #     for field_id in [IMF._get_ids(field.model_name)[field.name]]
        #     for index, (value, label), color in enumerate(field.selection) if len(self.selection[0]) > 2
        #     for index, (value, label) in enumerate(field.selection) if len(self.selection[0]) < 3
        # }
        # end of comment

        # added by supriya
        expected = {}
        for field in fields:
            for field_id in [IMF._get_ids(field.model_name)[field.name]]:
                if len(field.selection[0]) == 3:
                    count = 0
                    for value, label, color in field.selection:
                        count += 1
                        expected[(field_id, value)] = (label, count)
                if len(field.selection[0]) == 2:
                    for index, (value, label) in enumerate(field.selection):
                        expected[(field_id, value)] = (label, index)
        # end of comment

        cr = self.env.cr
        query = """
            SELECT s.field_id, s.value, s.name, s.sequence
            FROM ir_model_fields_selection s, ir_model_fields f
            WHERE s.field_id = f.id AND f.model IN %s
        """
        cr.execute(query, [tuple(model_names)])
        existing = {row[:2]: row[2:] for row in cr.fetchall()}

        # create or update rows
        cols = ['field_id', 'value', 'name', 'sequence']
        rows = [key + val for key, val in expected.items() if existing.get(key) != val]
        if rows:
            ids = upsert(cr, self._table, cols, rows, ['field_id', 'value'])
            self.pool.post_init(mark_modified, self.browse(ids), cols[2:])

        # update their XML ids
        module = self._context.get('module')
        if not module:
            return

        query = """
            SELECT f.model, f.name, s.value, s.id
            FROM ir_model_fields_selection s, ir_model_fields f
            WHERE s.field_id = f.id AND f.model IN %s
        """
        cr.execute(query, [tuple(model_names)])
        selection_ids = {row[:3]: row[3] for row in cr.fetchall()}

        data_list = []
        for field in fields:
            model = self.env[field.model_name]
            for value, modules in field._selection_modules(model).items():
                if module in modules:
                    xml_id = selection_xmlid(module, field.model_name, field.name, value)
                    record = self.browse(selection_ids[field.model_name, field.name, value])
                    data_list.append({'xml_id': xml_id, 'record': record})
        self.env['ir.model.data']._update_xmlids(data_list)

