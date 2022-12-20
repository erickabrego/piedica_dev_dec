odoo.define('mrp_operations_qrcode.BasicModel', function (require) {
'use strict';

var BasicModel = require('web.BasicModel');


BasicModel.include({

    _generateChanges: function (record, options) {
        var changes = this._super(record, options);

        if (record.model == 'sale.order') {
            if (changes.order_line && changes.order_line.length) {
                this._split_products_qty_order_line(changes);
            }
        }

        return changes;
    },


    // Cuando se agregue un producto en las líneas de una orden de venta, si la
    // cantidad es > 1 y el producto es MTO, dicha línea se dividirá acorde a la
    // cantidad ingresada (ej: si se agrega una línea y el producto con cantidad
    // 5, en realidad se generarán 5 líneas con cantidad 1 de dicho producto).
    // Esto con la finalidad de que se genere una orden de fabricación por cada
    // producto individual
    _split_products_qty_order_line: function (changes) {
        var i;

        for (i = 0; i < changes.order_line.length; i++) {
            if (changes.order_line[i][2].product_uom_qty && changes.order_line[i][2].product_uom_qty > 1) {
                let line_data = _.findWhere(this.localData, {res_id: changes.order_line[i][1]});

                // Solo se dividirá la línea cuando sea un nuevo registro
                if (changes.order_line[i][0] === 0) {
                    if (line_data._changes.is_mto) {
                        let new_lines = [];

                        for (let j = 0; j < changes.order_line[i][2].product_uom_qty; j++) {
                            let new_line = {};
                            new_line = Object.assign(new_line, changes.order_line[i][2]);
                            new_line.product_uom_qty = 1;
                            new_lines.push([0, '', new_line]);
                        }

                        changes.order_line.splice(i, 1, ...new_lines);
                        break;
                    }
                // En el caso que se edita el registro, se mantendrá la
                // cantidad en 1
                } else if (changes.order_line[i][0] === 1) {
                    if (line_data.data.is_mto) {
                        changes.order_line[i][2].product_uom_qty = 1;
                        this.do_warn('Error al modificar',
                            'No puedes asignar una cantidad mayor a 1 al producto ' + line_data.data.name);
                    }
                }
            }
        }

        if (i < changes.order_line.length) {
            this._split_products_qty_order_line(changes);
        }
    }
});

});
