odoo.define('portal_account_custom_fields.portal', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var portalDetails = publicWidget.registry.portalDetails;
    var _events = portalDetails.prototype.events;

    _events['change input[name="p_physical_activity"]'] = '_on_physical_activity_change';
    _events['change select[name="p_hear_about_us"]'] = '_on_p_hear_about_us_change';

    portalDetails.include({
        start: function () {
            var def = this._super.apply(this, arguments);

            this._show_physical_activity_field();
            this._show_p_hear_about_us_field();

            return def;
        },


        _on_physical_activity_change: function () {
            this._show_physical_activity_field();
        },


        _on_p_hear_about_us_change: function () {
            this._show_p_hear_about_us_field();
        },


        _show_physical_activity_field: function () {
            var physical_activity_si_input = this.$('#p_physical_activity_si');
            var physical_activity_true_div = this.$('#p_physical_activity_true_div');
            var physical_activity_true_input = this.$('input[name="p_physical_activity_true"]');

            if (physical_activity_si_input.prop('checked')) {
                physical_activity_true_div.show();
                physical_activity_true_input.prop('disabled', false);
            } else {
                physical_activity_true_div.hide();
                physical_activity_true_input.prop('disabled', true);
            }
        },


        _show_p_hear_about_us_field: function () {
            var p_hear_about_us_input = this.$('select[name="p_hear_about_us"]');
            var p_hear_about_us_other_div = this.$('#p_hear_about_us_other_div');
            var p_hear_about_us_other_input = this.$('input[name="p_hear_about_us_other"]');

            if (p_hear_about_us_input.val() == 'otro') {
                p_hear_about_us_other_div.show();
                p_hear_about_us_other_input.prop('disabled', false);
            } else {
                p_hear_about_us_other_div.hide();
                p_hear_about_us_other_input.prop('disabled', true);
            }
        }
    });
});
