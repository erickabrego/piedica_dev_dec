odoo.define('mrp_operations_qrcode.OperationsScanAction', function (require) {
'use strict';

var core = require('web.core');

var AbstractAction = require('web.AbstractAction');

var OperationsLines = require('mrp_operations_qrcode.OperationsLines');


var OperationsScanAction = AbstractAction.extend({
    template: 'operations_scan',


    init: function (parent, action) {
        this._super.apply(this, arguments);
    },


    start: function () {
        var self = this;

        this.operations_lines = new OperationsLines(this);
        this.operations_lines.appendTo(self.$el);

        return this._super.apply(this, arguments);
    }
});


core.action_registry.add('operations_scan_action', OperationsScanAction);


return OperationsScanAction;

});
