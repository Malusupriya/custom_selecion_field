odoo.define('custom_selecion_field.relational_fields', function (require) {
    "use strict";

    const FieldSelection = require('web.relational_fields').FieldSelection;
    const core = require('web.core');
    const _t = core._t;

    FieldSelection.include({

        /**
         * Inherited
         */
        init: function () {
            this._super.apply(this, arguments);
            this.hasColor = this.field.selection && this.field.selection.length && this.field.selection[0].length > 2;
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * Inherited function to add color inside selection field based on the value defined in python
         * @private
         */
        _renderEdit: function () {
            if (this.hasColor) {
                this.$el.addClass('o_color_selection');
                this.$el.empty();
                var found = _.find(this.values, function (el) {
                    return el[0] === this.value;
                }, this);
                if (this.value && found) {
                    this.$el.attr({'style': 'color: ' + found[2] + ';'});
                }
                for (var i = 0 ; i < this.values.length ; i++) {
                    this.$el.append($('<option/>', {
                        value: JSON.stringify(this.values[i][0]),
                        text: this.values[i][1],
                        style: this.values[i][2] ? 'color: ' + this.values[i][2] + ';' : '',
                    }));
                }
                this.$el.val(JSON.stringify(this._getRawValue()));
            }
            else {
                this._super.apply(this, arguments);
            }
        },

        /**
         * To show color in readonly mode also
         * @private
         */
        _renderReadonly: function () {
            this._super.apply(this, arguments);
            if (this.hasColor) {
                this.$el.addClass('o_color_selection');
                var found = _.find(this.values, function (el) {
                    return el[0] === this.value;
                }, this);
                this.$el.attr('raw-value', this._getRawValue());
                if (this.value && found) {
                    this.$el.attr({'style': 'color: ' + found[2] + ';'});
                }
            }
        },

    });

    // bootstrapselect

});