odoo.define('theme_scita.editor_js',function(require) {
'use strict';
    var ajax = require('web.ajax');
    var core = require('web.core');
    var weContext = require('web_editor.context');
    var web_editor = require('web_editor.editor');
    var options = require('web_editor.snippets.options');
    var wUtils = require('website.utils');
    var qweb = core.qweb;
    var _t = core._t;
    ajax.loadXML('/theme_scita/static/src/xml/theme_scita.xml', qweb);
    var set_timer = options.Class.extend({
        popup_template_id: "editor_new_product_slider_template",
        popup_title: _t("Modify Time"),
        date_configure: function(type,value) {
            var self = this;
            
            $('#datetimepicker1').datetimepicker({ 
            });
            let today = new Date(),
            day = today.getDate(),
            month = today.getMonth()+1, //January is 0
            year = today.getFullYear();
                 if(day<10){
                        day='0'+day
                    } 
                if(month<10){
                    month='0'+month
                }
                today = year+'-'+month+'-'+day;
            self.$modal = $(qweb.render("theme_scita.model_dialog_commingsoon"));
            self.$modal.find("input#date").min=today;
            
            self.$modal.appendTo('body');
            self.$modal.modal();
            var $sub_data = self.$modal.find("#biztech_coumtdown_btn");
            var $can = self.$modal.find("#biz_cancle");
            $sub_data.on('click', function() {
                
                  var date = new Date(self.$modal.find("input#date").val());
                  var day = date.getDate();
                  var month = date.getMonth();
                  var year = date.getFullYear();
                 
                var $mins_ret = self.$modal.find("input[name='minutes']")
                
               
                $mins_ret.val($('div.js_counter_timer #minutes').html());
                
                var count_hours = parseInt(self.$modal.find("input#hours").val());
                var count_min = parseInt(self.$modal.find("input#minutes").val());
                var count_sec = parseInt(self.$modal.find("input#second").val());
                var monthShortNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
                                        ];

                var formated_date = monthShortNames[month] + ' ' + day + ',' + year + ' ' + count_hours + ':' + count_min + ':' + count_sec;
                

                if(date == 'Invalid Date')
                {
                    alert("Invalid Time Format. Please enter correct format of Time")
                    self.$target.attr("data-date","nan");
                    self.$target.attr("data-msg", self.$modal.find("input#sale_over").val());
                    self.$modal.modal('hide');
                    self.date_configure('click')
                }
                else
                {
                    self.$target.attr("data-date", formated_date);
                    self.$target.attr("data-msg", self.$modal.find("input#sale_over").val());
                    self.$modal.modal('hide');
                }
            });
            $can.on('click', function() {
                self.getParent()._onRemoveClick($.Event("click"))
            })
           
        },
        onBuilt: function () {
            var self = this;
            this._super();
            this.date_configure('click');
        }
    });
    options.registry.js_counter_timer = set_timer.extend({        
        cleanForSave: function(){
        this.$target.empty();
        }
    });

});
    
