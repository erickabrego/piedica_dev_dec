odoo.define('mrp_operations_qrcode.OperationsLines', function (require) {
'use strict';

var concurrency = require('web.concurrency');
var core = require('web.core');
var Widget = require('web.Widget');

var OperationsLine = require('mrp_operations_qrcode.OperationsLine');


var OperationsLines = Widget.extend({
    template: 'operations_lines',


    init: function (parent) {
        this._super.apply(this, arguments);

        this.lines = [];
        this.mutex = new concurrency.Mutex();
        this.workorder_states = {};
    },


    willStart: function () {
        return Promise.all([
            this._super.apply(this, arguments),
            this._get_workorder_states()
        ]);
    },


    start: function () {
        var self = this;

        return this._super.apply(this, arguments).then(function () {
            core.bus.on('barcode_scanned', self, self._on_barcode_scanned_handler);
        });
    },


    destroy: function () {
        core.bus.off('barcode_scanned', this, this._on_barcode_scanned_handler);
        this._super();
    },


    _on_barcode_scanned_handler: function (barcode) {
        var self = this;

        this.mutex.exec(function () {
            return self._on_barcode_scanned(barcode);
        });
    },


    _get_workorder_states: function () {
        var self = this;

        return this._rpc({
            model: 'mrp.workorder',
            method: 'get_states_selection',
            args: [[]],

        }).then(function (states) {
            self.workorder_states = states;
        });
    },


    // Cada que se escanee una orden, por lo general se agregará una nueva línea
    // de operación en la pantalla
    _on_barcode_scanned: async function (barcode) {
        var self = this;

        var order_id = parseInt(barcode.split(',')[1]);

        if (this._order_exists(order_id)) {


            var is_new_line = false;
            var line;
            var line_index = this._get_line_index(order_id);

            if (line_index !== false) {
                line = this.lines[line_index];
            } else {
                // Si es una orden que no está en las líneas en pantalla, se
                // creará una nueva línea
                is_new_line = true;
                line = new OperationsLine(this, order_id, line_index, is_new_line);
            }

            line.next_stage().then(async function (status) {
                if (!is_new_line) {
                    // En caso de que no se haya pasado a la siguiente fase de
                    // operación (ya sea porque aún no ha pasado el tiempo mínimo
                    // para completar la operación o porque ya no hay más operaciones
                    // pendientes), la línea se dejará donde está
                    if (status == 'warning') {
                        return;
                    }

                    // Si el QR escaneado pertenece a la primer linea, solo se
                    // actualizará la información de la linea
                    if (line_index === 0) {
                        line.update_data(order_id);
                    } else {
                        // Si la línea existente cambió de fase, se eliminará para
                        // volver a insertarla en la parte superior de las lineas
                        var old_line = line;
                        line = new OperationsLine(self, order_id, line_index, is_new_line);
                        var body = self.$el.find('.qr_lines');

                        if (line_index != 0) {
                            await old_line.take_out();
                        }

                        self.lines.splice(line_index, 1);
                        self.lines.unshift(line);
                        line.prependTo(body);
                        old_line.destroy();
                    }
                } else {
                    var body = self.$el.find('.qr_lines');
                    line.prependTo(body);
                    self.lines.unshift(line);
                }
            });
        } else {
            this.displayNotification({
                type: 'warning',
                message: 'No se encontró la orden escaneada'
            });
        }
    },


    _order_exists: function (order_id) {
        return this._rpc({
            model: 'mrp.production',
            method: 'search',
            args: [[['id', '=', order_id]]]
        }).then(function (order) {
            if (order.length != 0) {
                return true;
            } else {
                return false;
            }
        });
    },


    _get_line_index: function (order_id) {
        for (let i = 0; i < this.lines.length; i++) {
            if (this.lines[i].order_id == order_id) {
                return i;
            }
        }

        return false;
    }
});


return OperationsLines;

});
