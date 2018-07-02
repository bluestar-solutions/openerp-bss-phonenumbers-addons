/**
 * Part of Phone Numbers.
 * See LICENSE file for full copyright and licensing details.
 */

goog.require('i18n.phonenumbers.PhoneNumberFormat');
goog.require('i18n.phonenumbers.PhoneNumberUtil');

odoo.define('bss_phonenumbers.phone_widget', function (require) {
    "use strict";

    var core = require('web.core');
    var session = require('web.session');
    var form_widgets = require('web.form_widgets');
    var tree_widgets = require('web.ListView');
    var PNF = i18n.phonenumbers.PhoneNumberFormat;
    var pnu = i18n.phonenumbers.PhoneNumberUtil.getInstance();

    var FieldPhone = form_widgets.FieldEmail.extend({
        template: 'FieldPhone',
        init: function (field_manager, node) {
            this._super(field_manager, node);
            var self = this;
            this.rpc_country_code().done(function(r) {
                self._country_code = r;
            });
        },
        store_dom_value: async function () {
            if (this.$input && this.is_syntax_valid()) {
                if (this.$input.val()) {
                    var number = pnu.parse(this.$input.val(), this._country_code);
                    var value = pnu.format(number, PNF.INTERNATIONAL);
                    this.$input.val(value);
                    this.internal_set_value(value);
                } else {
                    this.internal_set_value(false);
                }
            }
        },
        render_value: function() {
            this._super();
            if (this.get("effective_readonly") && this.clickable) {
                var data = this.get('value');
                if (data) {
                    var number = pnu.parse(this.get('value'));
                    this.$el.attr('href', pnu.format(number, PNF.RFC3966));
                }
            }
        },
        is_syntax_valid: function() {
            if (this.$input && this.$input.val()) {
                try {
                    if (this._country_code) {
                        var number = pnu.parse(
                                this.$input.val(), this._country_code);
                    } else {
                        var number = pnu.parse(this.$input.val());
                    }
                    // Disable validation (only formatting)
                    //return pnu.isPossibleNumber(number) &&
                    //        pnu.isValidNumber(number);
                    return true
                } catch (e) {
                    return false;
                }
            }
            return true;
        },
        rpc_country_code: function() {
            return this.rpc('/bss_phonenumbers/country_code', {});
        },
    });

    if (!core.form_widget_registry.get('phone')) {
        core.form_widget_registry.add('phone', FieldPhone);
    }

    var ColumnPhone = tree_widgets.Column.extend({
        _format: function(row_data, options) {
            var value = row_data[this.id].value;
            if (value) {
                var number = pnu.parse(value);
                return _.template("<a href='<%-href%>'><%-text%></a>")({
                    href: pnu.format(number, PNF.RFC3966),
                    text: value
                });
            }
            return this._super(row_data, options);
        }
    });


    if (!core.list_widget_registry.get('phone')) {
        core.list_widget_registry.add('field.phone', ColumnPhone);
    }
});
