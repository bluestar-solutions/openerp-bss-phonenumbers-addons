/**
 * Part of Phone Numbers.
 * See LICENSE file for full copyright and licensing details.
 */

odoo.define('bss_phonenumbers.phone_widget', function (require) {
    "use strict";

    var core = require('web.core');
    var session = require('web.session');
    var form_widgets = require('web.form_widgets');
    var tree_widgets = require('web.ListView');

    var FieldPhone = form_widgets.FieldEmail.extend({
        template: 'FieldPhone',
        init: function (field_manager, node) {
            this._super(field_manager, node);
            this._is_value_valid = true;
            this._is_value_false = true;
            this._tmp_value = [null, null];
        },
        initialize_content: function() {
            this._super();
            if(!this.get('effective_readonly') && this.$input) {
                this.$input.off('input');
                var self = this;
                this.$input.on('input', function() {
                    self.store_tmp_value();
                });
                this.$input.on('focus', function() {
                    self.store_tmp_value();
                });
            }
        },
        destroy_content: function() {
            this._super();
            this._is_value_valid = true;
        },
        rpc_format: function(phone_num) {
            var arg = {'number': phone_num};
            return this.rpc('/bss_phonenumbers/format', arg)
        },
        store_tmp_value : function() {
            var val = this.$input.val();
            if (val) {
                var self = this;
                this.rpc_format(val).done(function(r) {
                    self._is_value_valid = r.valid;
                    self._is_value_false = !val;
                    if (r.valid) {
                        self._tmp_value = r.value;
                    }
                });
            }
        },
        store_dom_value: function () {
            if (this.$input && this.is_syntax_valid() && this._tmp_value) {
                this.$input.val(this._tmp_value[0]);
                this.internal_set_value(this._tmp_value);
            }
            this._check_css_flags();
        },
        format_value: function(val, def) {
            if (Object.prototype.toString.call(val) === '[object Array]') {
                val = val[0];
            }
            return this._super(val, def)
        },
        render_value: function() {
            this._super();
            if (this.get("effective_readonly") && this.clickable) {
                var data = this.get('value');
                if (data) {
                    this.$el.attr('href', data[1]);
                }
            }
        },
        is_false: function() {
            return this._is_value_false;
        },
        is_syntax_valid: function() {
            return this._is_value_valid;
        }
    });

    if (!core.form_widget_registry.get('phone')) {
        core.form_widget_registry.add('phone', FieldPhone);
    }

    var ColumnPhone = tree_widgets.Column.extend({
        _format: function(row_data, options) {
            var data = row_data[this.id].value;
            if (data) {
                return _.template("<a href='<%-href%>'><%-text%></a>")({
                    href: data[1],
                    text: data[0]
                });
            }
            return this._super(row_data, options);
        }
    });


    if (!core.list_widget_registry.get('phone')) {
        core.list_widget_registry.add('field.phone', ColumnPhone);
    }
});
