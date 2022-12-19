odoo.define('pragmatic_odoo_whatsapp_integration.pos', function (require) {
    'use strict';

    const { Printer } = require('point_of_sale.Printer');
    const { is_email } = require('web.utils');
    const { useRef, useContext } = owl.hooks;
    const { useErrorHandlers, onChangeOrder } = require('point_of_sale.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const AbstractReceiptScreen = require('point_of_sale.AbstractReceiptScreen');

    const ReceiptScreen = (AbstractReceiptScreen) => {
        class ReceiptScreen extends AbstractReceiptScreen {
            constructor() {
                super(...arguments);
                useErrorHandlers();
                onChangeOrder(null, (newOrder) => newOrder && this.render());
                this.orderReceipt = useRef('order-receipt');
                const order = this.currentOrder;
                const client = order.get_client();
                this.orderUiState = useContext(order.uiState.ReceiptScreen);
                this.orderUiState.inputEmail = this.orderUiState.inputEmail || (client && client.email) || '';
                this.is_email = is_email;
            }
            mounted() {
                // Here, we send a task to the event loop that handles
                // the printing of the receipt when the component is mounted.
                // We are doing this because we want the receipt screen to be
                // displayed regardless of what happen to the handleAutoPrint
                // call.
                setTimeout(async () => await this.handleAutoPrint(), 0);
            }
            async onSendEmail() {
                if (!is_email(this.orderUiState.inputEmail)) {
                    this.orderUiState.emailSuccessful = false;
                    this.orderUiState.emailNotice = 'Invalid email.';
                    return;
                }
                try {
                    await this._sendReceiptToCustomer();
                    this.orderUiState.emailSuccessful = true;
                    this.orderUiState.emailNotice = 'Email sent.'
                } catch (error) {
                    this.orderUiState.emailSuccessful = false;
                    this.orderUiState.emailNotice = 'Sending email failed. Please try again.'
                }
            }
            get orderAmountPlusTip() {
                const order = this.currentOrder;
                const orderTotalAmount = order.get_total_with_tax();
                const tip_product_id = this.env.pos.config.tip_product_id && this.env.pos.config.tip_product_id[0];
                const tipLine = order
                    .get_orderlines()
                    .find((line) => tip_product_id && line.product.id === tip_product_id);
                const tipAmount = tipLine ? tipLine.get_all_prices().priceWithTax : 0;
                const orderAmountStr = this.env.pos.format_currency(orderTotalAmount - tipAmount);
                if (!tipAmount) return orderAmountStr;
                const tipAmountStr = this.env.pos.format_currency(tipAmount);
                return `${orderAmountStr} + ${tipAmountStr} tip`;
            }
            get currentOrder() {
                return this.env.pos.get_order();
            }
            get nextScreen() {
                return { name: 'ProductScreen' };
            }
            /**
             * This function is called outside the rendering call stack. This way,
             * we don't block the displaying of ReceiptScreen when it is mounted; additionally,
             * any error that can happen during the printing does not affect the rendering.
             */
            async handleAutoPrint() {
                if (this._shouldAutoPrint()) {
                    await this.printReceipt();
                                        await this.js_custom_print();

                    if (this.currentOrder._printed && this._shouldCloseImmediately()) {
                        this.orderDone();
                    }
                }
            }
            orderDone() {
                this.currentOrder.finalize();
                const { name, props } = this.nextScreen;
                this.showScreen(name, props);
            }
            async printReceipt() {
                const isPrinted = await this._printReceipt();
                if (isPrinted) {
                    this.currentOrder._printed = true;
                }
            }

            async js_custom_print() {
                const isPrinted = await this._js_custom_print();
                if (isPrinted) {
                    this.currentOrder._printed = true;
                }
            }
            _shouldAutoPrint() {
                return this.env.pos.config.iface_print_auto && !this.currentOrder._printed;
            }
            _shouldCloseImmediately() {
                var invoiced_finalized = this.currentOrder.is_to_invoice() ? this.currentOrder.finalized : true;
                return this.env.pos.proxy.printer && this.env.pos.config.iface_print_skip_screen && invoiced_finalized;
            }
            async _sendReceiptToCustomer() {
                const printer = new Printer();
                const receiptString = this.orderReceipt.comp.el.outerHTML;
                const ticketImage = await printer.htmlToImg(receiptString);
                const order = this.currentOrder;
                const client = order.get_client();
                const orderName = order.get_name();
                const orderClient = { email: this.orderUiState.inputEmail, name: client ? client.name : this.orderUiState.inputEmail };
                const order_server_id = this.env.pos.validated_orders_name_server_id_map[orderName];
                await this.rpc({
                    model: 'pos.order',
                    method: 'action_receipt_to_customer',
                    args: [[order_server_id], orderName, orderClient, ticketImage],
                });
            }

                    async _js_custom_print() {
                    var order = this.env.pos.get_order();
        var order_list = this.env.pos.get_order_list();

        // Render receipt screen and can print function
        var value = {
            'order': order.name,
            'formatted_validation_date': order.formatted_validation_date,
            'company_name': this.env.pos.company.name,
            'company_phone': this.env.pos.company.phone,
            'user_name': this.env.pos.user.name,
//            'order_lines': order_list[0].orderlines.models

            }
             $.ajax({
            url : '/whatsapp/send/message',
            data : value,
            type: "POST",

            success: function (data) {
            alert("Whatsapp Message Send Sucessfully");
            }
            });
            }





//            if (this.env.pos.proxy.printer) {
//                const printResult = await this.env.pos.proxy.printer.print_receipt(this.orderReceipt.el.outerHTML);
//                if (printResult.successful) {
//                    return true;
//                } else {
//                    const { confirmed } = await this.showPopup('ConfirmPopup', {
//                        title: printResult.message.title,
//                        body: 'Do you want to print using the web printer?',
//                    });
//                    if (confirmed) {
//                        // We want to call the _printWeb when the popup is fully gone
//                        // from the screen which happens after the next animation frame.
//                        await nextFrame();
//                        return await this._printWeb();
//                    }
//                    return false;
//                }
//            } else {
//                return await this._printWeb();
//            }
        }


        ReceiptScreen.template = 'ReceiptScreen';
        return ReceiptScreen;
    };

    Registries.Component.addByExtending(ReceiptScreen, AbstractReceiptScreen);

    return ReceiptScreen;
});
