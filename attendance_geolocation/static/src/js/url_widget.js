odoo.define('web_widget_url_advanced', function (require) {
    "use strict";

    var basic_fields = require('web.basic_fields');

    basic_fields.UrlWidget.include({
        init: function () {
            this._super.apply(this, arguments);
            if (this.nodeOptions['button_name']){ 
                this.button_name = this.nodeOptions['button_name'];
            }
            else{
                this.button_name = this.value;
            }
            if(this.button_name){
                this.attrs.text = this.button_name;
            }
        },
    });

});