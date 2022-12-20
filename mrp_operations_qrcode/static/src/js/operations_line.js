odoo.define('mrp_operations_qrcode.OperationsLine', function(require) {
    'use strict';

    var field_utils = require('web.field_utils');
    var time = require('web.time');
    var Widget = require('web.Widget');

    var OperationsLine = Widget.extend({
        template: 'operations_line',

        events: {
            'click': '_on_click'
        },

        init: function(parent, order_id, line_index, is_new_line) {
            this._super.apply(this, arguments);
            this.order_id = order_id;
            this.is_new_line = is_new_line;
            this.line_index = line_index;
            this.mrp_order = {};
            this.states = parent.workorder_states;
            this.current_workorder;
            this.timer = null;

            // Valores de la operación actual de la orden que se muestran en la linea
            this.components = null;
            this.insole_size = null;
            this.operation_name = null;
            this.operation_state = null;
            this.operation_state_color = null;
            this.operation_duration_expected = null;
            this.operation_duration = null;
            this.observations;
        },


        willStart: function() {
            var defs = [this._super.apply(this, arguments)];
            defs.push(this._fetch_order());

            return Promise.all(defs);
        },

        start: function() {
            var self = this;

            return this._super.apply(this, arguments).then(function() {
                self._start_time_counter();
                self.put_in();
            });
        },


        // Cuando se hace clic en la línea, se muestra el registro de la orden
        _on_click: function(e) {
            //Evitamos abrir el formulario si se hace click en el enlace
            if (e.target && e.target.classList.value == "design_link") {
                return
            }
            this.do_action({
                type: 'ir.actions.act_window',
                name: this.mrp_order.name,
                res_model: 'mrp.production',
                res_id: this.order_id,
                views: [
                    [false, 'form']
                ],
                target: 'new',
                flags: {
                    mode: 'view'
                }
            });
        },


        _fetch_order: function() {
            var self = this;

            // Orden de fabricación
            return this._rpc({
                model: 'mrp.production',
                method: 'get_qrcode_line_data',
                args: [
                    [this.order_id]
                ]
            }).then(function(mrp_order) {
                self.mrp_order = mrp_order;
                self.current_workorder = self.mrp_order.workorder_ids[self.mrp_order.current_operation_index];
                self.operation_name = self.current_workorder.name;
                self.operation_state = self.states[self.current_workorder.state];
                self.operation_state_color = (self.current_workorder.state == 'done') ? 'bg-success-light' : 'bg-info-light';
                self.operation_duration_expected = field_utils.format.float_time(self.current_workorder.duration_expected);
                self.operation_duration = self.current_workorder.duration;
                self.insole_size = self.mrp_order.insole_size ? self.mrp_order.insole_size : '';
                self.observations = self.mrp_order.observations ? self.mrp_order.observations : '';

                self.components = '';

                for (let i = 0; i < self.mrp_order.move_raw_ids.length; i++) {
                    self.components += self.mrp_order.move_raw_ids[i].product_id.name;

                    if (i < (self.mrp_order.move_raw_ids.length - 1)) {
                        self.components += ', ';
                    }
                }

                // Productividad del centro de trabajo (para obtener el tiempo
                // que ha pasado en una operación)
                return self._rpc({
                    model: 'mrp.workcenter.productivity',
                    method: 'search_read',
                    domain: [
                        ['workorder_id', '=', self.current_workorder.id],
                        ['date_end', '=', false],
                    ]
                }).then(function(result) {
                    var now = new Date();
                    var duration = 0;

                    if (result.length > 0) {
                        duration += self._get_date_difference(time.auto_str_to_date(result[0].date_start), now);
                    }

                    var minutes = duration / 60 >> 0;
                    var seconds = duration % 60;
                    self.operation_duration += minutes + seconds / 60;
                });
            });
        },


        update_data: function(order_id) {
            var self = this;

            this.order_id = order_id;

            this._fetch_order().then(function() {
                self.$el.find('.order_name').text(self.mrp_order.name);
                self.$el.find('.product_name').text(self.mrp_order.product_id.name);
                self.$el.find('.product_components').text(self.components);
                self.$el.find('.insole_size').text(self.insole_size);
                self.$el.find('.operation_name').text(self.operation_name);
                //Se añade la liga de la plantilla
                self.$el.find('.design_link').text(self.mrp_order.p_design_link);
                self.$el.find('.order_count').text(self.mrp_order.order_count)

                var order_operation = self.$el.find('.order_operation');

                if (self.mrp_order.p_to_send) {
                    order_operation.html('<span class="badge badge-pill o_field_badge o_field_widget bg-success-light">Lista para envío</span>');
                } else {
                    var operation_name = '<span class="operation_name">' + self.operation_name + '</span>';
                    var operation_state = '<span class="operation_state badge badge-pill o_field_badge o_field_widget ' + self.operation_state_color + '">' + self.operation_state + '</span>';
                    order_operation.html(operation_name + ' ' + operation_state);
                }

                self.$el.find('.operation_duration_expected').text(self.operation_duration_expected);
                self._start_time_counter();
            });
        },


        // Agrega o mueve la línea a la parte superior
        put_in: function() {
            if (this.is_new_line) {
                this.$el.css({
                    opacity: 0
                }).animate({
                    opacity: 1
                }, 300);
            } else {
                if (this.line_index !== 0) {
                    this.$el.css({
                        zIndex: 90,
                        bottom: this.el.offsetHeight * -1,
                    }).animate({
                        bottom: 0,
                        zIndex: 100
                    }, 100);
                }
            }
        },


        // Elimina la línea
        take_out: function() {
            var self = this;

            return new Promise(function(resolve, reject) {
                self.$el.css({
                    zIndex: 90
                }).animate({
                    bottom: self.el.offsetHeight,
                }, 100, resolve);
            });
        },


        next_stage: function() {
            var self = this;

            return this._rpc({
                model: 'mrp.production',
                method: 'operations_next_stage',
                args: [this.order_id]
            }).then(function(result) {
                self.displayNotification({
                    type: result.status,
                    title: result.order,
                    message: result.message
                });

                return result.status;
            });
        },


        _get_date_difference: function(date_start, date_end) {
            return moment(date_end).diff(moment(date_start), 'seconds');
        },

        _start_time_counter: function() {
            var self = this;

            clearTimeout(this.timer);

            if (this.current_workorder.state == 'progress') {
                this.timer = setTimeout(function() {
                    self.operation_duration += 1 / 60;
                    self._start_time_counter();
                }, 1000);
            } else {
                clearTimeout(this.timer);
            }

            this.$el.find('.operation_duration').text(field_utils.format.float_time(this.operation_duration));
        },
    });


    return OperationsLine;

});