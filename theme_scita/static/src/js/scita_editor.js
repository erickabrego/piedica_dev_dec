odoo.define('theme_scita.scita_editor_js', function(require) {
    'use strict';
    var options = require('web_editor.snippets.options');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t;

    ajax.loadXML('/theme_scita/static/src/xml/theme_scita.xml', qweb);

    options.registry.oe_cat_slider = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find(".oe_cat_slider").empty();
            if (!editMode) {
                self.$el.find(".oe_cat_slider").on("click", _.bind(self.cat_slider, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.cat_slider()) {
                this.cat_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },

        cleanForSave: function() {
            $('.oe_cat_slider').empty();
        },

        cat_slider: function(type, value) {
            var self = this;
            
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_dynamic_category_slider"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#slider_type"),
                    $category_slider_delete = self.$modal.find("#cancel"),
                    $pro_cat_sub_data = self.$modal.find("#cat_sub_data");
                ajax.jsonRpc('/theme_scita/category_get_options', 'call', {}).then(function(res) {
                    $('#slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });

                $pro_cat_sub_data.on('click', function() {
                    var type = '';
                    // self.$target.attr('data-cat-slider-type', $slider_type.val());
                    self.$target.attr('data-cat-slider-id', $slider_type.val());
                    if ($('select#slider_type').find(":selected").text()) {
                        type = _t($('select#slider_type').find(":selected").text());
                    } else {
                        type = _t("Category Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $category_slider_delete.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });

    
    options.registry.second_cat_slider = options.Class.extend({
        start: function(editMode) {
            var self = this;

            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find(".second_cat_slider").empty();
            if (!editMode) {
                self.$el.find(".second_cat_slider").on("click", _.bind(self.cat_slider, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.cat_slider()) {
                this.cat_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },

        cleanForSave: function() {
            $('.second_cat_slider').empty();
        },

        cat_slider: function(type, value) {
            var self = this;
            
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_dynamic_category_slider"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#slider_type"),
                    $category_slider_delete = self.$modal.find("#cancel"),
                    $pro_cat_sub_data = self.$modal.find("#cat_sub_data");
                ajax.jsonRpc('/theme_scita/category_get_options', 'call', {}).then(function(res) {
                    $('#slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });

                $pro_cat_sub_data.on('click', function() {
                    var type = '';
                    // self.$target.attr('data-cat-slider-type', $slider_type.val());
                    self.$target.attr('data-cat-slider-id', $slider_type.val());
                    if ($('select#slider_type').find(":selected").text()) {
                        type = _t($('select#slider_type').find(":selected").text());
                    } else {
                        type = _t("Category Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $category_slider_delete.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    options.registry.theme_scita_product_slider = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("hidden");
            this.$target.find(".oe_prod_slider").empty();
            if (!editMode) {
                self.$el.find(".oe_prod_slider").on("click", _.bind(self.prod_slider, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.prod_slider()) {
                this.prod_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },

        cleanForSave: function() {
            $('.oe_prod_slider').empty();
        },

        prod_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                
                self.$modal = $(qweb.render("theme_scita.scita_dynamic_product_slider"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#slider_type"),
                    $product_slider_cancel = self.$modal.find("#cancel"),
                    $pro_sub_data = self.$modal.find("#prod_sub_data");

                ajax.jsonRpc('/theme_scita/product_get_options', 'call', {}).then(function(res) {
                    $('#slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });

                $pro_sub_data.on('click', function() {
                    var type = '';
                    // self.$target.attr('data-cat-slider-type', $slider_type.val());
                    self.$target.attr('data-prod-slider-id', $slider_type.val());
                    if ($('select#slider_type').find(":selected").text()) {
                        type = _t($('select#slider_type').find(":selected").text());
                    } else {
                        type = _t("Product Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $product_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                });
            } else {
                return;
            }
        },
    });
    options.registry.scita_multi_cat_custom_snippet = options.Class.extend({

        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("hidden");
            this.$target.find('.oe_multi_category_slider .owl-carousel').empty();
            if (!editMode) {
                self.$el.find(".oe_multi_category_slider").on("click", _.bind(self.multi_category_slider, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.multi_category_slider()) {
                this.multi_category_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },

        cleanForSave: function() {
            $('.oe_multi_category_slider .owl-carousel').empty();
        },

        multi_category_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.multi_product_custom_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#slider_type"),
                    $cancel = self.$modal.find("#cancel"),
                    $snippnet_submit = self.$modal.find("#snippnet_submit");

                ajax.jsonRpc('/theme_scita/product_multi_get_options', 'call', {}).then(function(res) {
                    $("select[id='slider_type'] option").remove();
                    _.each(res, function(y) {
                        $("select[id='slider_type']").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });

                $snippnet_submit.on('click', function() {
                    // var type = '';
                    self.$target.attr('data-multi-cat-slider-type', $slider_type.val());
                    self.$target.attr('data-multi-cat-slider-id', 'multi-cat-myowl' + $slider_type.val());
                    if ($('select#slider_type').find(":selected").text()) {
                        var type = '';
                        type = _t($('select#slider_type').find(":selected").text());
                    } else {
                        var type = '';
                        type = _t("Multi Product Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="row our-categories">\
                                                        <div class="col-md-12">\
                                                            <div class="title-block">\
                                                                <h4 class="section-title style1">\
                                                                    <span>' + type + '</span>\
                                                                </h4>\
                                                            </div>\
                                                        </div>\
                                                    </div>\
                                                </div>');
                });
            } else {
                return;
            }
        },
    });
    options.registry.fashion_multi_cat_custom_snippet = options.Class.extend({

        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("hidden");
            this.$target.find('.fashion_multi_category_slider .owl-carousel').empty();
            if (!editMode) {
                self.$el.find(".fashion_multi_category_slider").on("click", _.bind(self.multi_category_slider, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.multi_category_slider()) {
                this.multi_category_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },

        cleanForSave: function() {
            $('.fashion_multi_category_slider .owl-carousel').empty();
        },

        multi_category_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.multi_product_custom_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#slider_type"),
                    $cancel = self.$modal.find("#cancel"),
                    $snippnet_submit = self.$modal.find("#snippnet_submit");

                ajax.jsonRpc('/theme_scita/product_multi_get_options', 'call', {}).then(function(res) {
                    $("select[id='slider_type'] option").remove();
                    _.each(res, function(y) {
                        $("select[id='slider_type']").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });

                $snippnet_submit.on('click', function() {
                    // var type = '';
                    self.$target.attr('data-multi-cat-slider-type', $slider_type.val());
                    self.$target.attr('data-multi-cat-slider-id', 'multi-cat-myowl' + $slider_type.val());
                    if ($('select#slider_type').find(":selected").text()) {
                        var type = '';
                        type = _t($('select#slider_type').find(":selected").text());
                    } else {
                        var type = '';
                        type = _t("Multi Product Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="row our-categories">\
                                                        <div class="col-md-12">\
                                                            <div class="title-block">\
                                                                <h4 class="section-title style1">\
                                                                    <span>' + type + '</span>\
                                                                </h4>\
                                                            </div>\
                                                        </div>\
                                                    </div>\
                                                </div>');
                });
            } else {
                return;
            }
        },
    });
    options.registry.prod_brands = options.Class.extend({

        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("hidden");
            this.$target.find(".oe_brand_slider .owl-carousel").empty();

             if (!editMode) {
                self.$el.find(".oe_brand_slider").on("click", _.bind(self.scita_brand_slider, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.scita_brand_slider()) {
                this.scita_brand_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },

        cleanForSave: function() {
            $('.oe_brand_slider .owl-carousel').empty();
        },

        scita_brand_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_brand_configration"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#slider_type"),
                    $cancel = self.$modal.find("#cancel"),
                    $brand_sub_data = self.$modal.find("#pro_brand_sub_data");

                ajax.jsonRpc('/theme_scita/brand_get_options', 'call', {}).then(function(res) {
                    $('#slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });

                $brand_sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-brand-config-type', $slider_type.val());
                    self.$target.attr('data-brand-config-id', $slider_type.val());
                    if ($('select#slider_type').find(":selected").text()) {
                        type = _t($('select#slider_type').find(":selected").text());
                    } else {
                        type = _t("Our Brands");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="row oe_our_slider">\
                                                        <div class="col-md-12">\
                                                            <div class="title-block">\
                                                                <h4 class="section-title style1">\
                                                                    <span>' + type + '</span>\
                                                                </h4>\
                                                            </div>\
                                                        </div>\
                                                    </div>\
                                                </div>');
                });
            } else {
                return;
            }
        },
    });
    // html builder
    var Dialog = require('web.Dialog');
    var QWeb = core.qweb;
    options.registry.html_builder_snippet = options.Class.extend({

        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("hidden");
            this.$target.find('.html_builder_new .owl-carousel').empty();
            if (!editMode) {
                self.$el.find(".html_builder_new").on("click", _.bind(self.html_content_builder, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            this.html_content_builder("click", "true");
        },

        cleanForSave: function() {
            $('.html_builder_new .owl-carousel').empty();
        },
        html_content_builder: function(type, value) {
            var new_qty , content;
            var emp_str = ''
            var self = this;
            this.id = this.$target.attr("id");
            var modification = this.$target.html().split("<style>");
            if(type == false || type == 'click'){
                var val =  this.$target.text().trim();
                if (val == 'HTML Snippet Builder') {
                    var emp_str = ''
                }
                else {
                    setTimeout(function(){
                        if (modification[0]) {
                            $('#get_content_html').html(modification[0])
                        }
                        if (modification[1]) {
                            var mod = modification[1].replace("</style>", "");
                            $('#get_content_css').val(mod)
                        }
                    },400);
                }
                var dialog =new Dialog(self, {
                    size: 'medium',
                    title: _t('HTML Snippet Builder'),
                    buttons: [{text: _t('Save'), classes: 'sct-save', close: true, click: function () {
                    new_qty = $('#get_content_html').val();
                    var cont =  $('#get_content_css').val();
                    content = '<style>'+ cont +'</style>';
                    var data = new_qty + content;
                    var data = self.$target.empty().append(data);
                }}, {text: _t('Discard'), classes: 'sct-discard', close: true,click: function () {

                    if (val == 'HTML Snippet Builder') {
                        var data = self.$target.empty()
                    }
                 }}],
                $content: QWeb.render("theme_scita.html_build",{'data': emp_str}),
            });
            waitForElementToAddClass(".sct_html_snippet_builder",100);
            function waitForElementToAddClass(selector, time) {
                    if(document.querySelector(selector)!=null) {
                        $('.sct_html_snippet_builder').parent().addClass('sct_content_builder');
                        return;
                    }
                    else {
                        setTimeout(function() {
                            waitForElementToAddClass(selector, time);
                        }, time);
                    }
                }
            dialog.open();
            return self;
          }
        },
    });

    // box Brand 
    options.registry.brands_box_slider_4 = options.Class.extend({

        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("hidden");
            this.$target.find(".box_brand_slider .owl-carousel").empty();

            if (!editMode) {
                self.$el.find(".box_brand_slider").on("click", _.bind(self.box_brand_slider, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.box_brand_slider()) {
                this.box_brand_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },

        cleanForSave: function() {
            $('.box_brand_slider .owl-carousel').empty();
        },

        box_brand_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_brand_configration"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#slider_type"),
                    $cancel = self.$modal.find("#cancel"),
                    $brand_sub_data = self.$modal.find("#pro_brand_sub_data");

                ajax.jsonRpc('/theme_scita/brand_get_options', 'call', {}).then(function(res) {
                    $('#slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });

                $brand_sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-brand-config-type', $slider_type.val());
                    self.$target.attr('data-brand-config-id', $slider_type.val());
                    if ($('select#slider_type').find(":selected").text()) {
                        type = _t($('select#slider_type').find(":selected").text());
                    } else {
                        type = _t("Brand snippet");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="row oe_our_slider">\
                                                        <div class="col-md-12">\
                                                            <div class="title-block">\
                                                                <h4 class="section-title style1">\
                                                                    <span>' + type + '</span>\
                                                                </h4>\
                                                            </div>\
                                                        </div>\
                                                    </div>\
                                                </div>');
                });
            } else {
                return;
            }
        },
    });
    // for brand slider
    options.registry.it_prod_brands = options.Class.extend({

        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find(".it_brand_slider").empty();
            if (!editMode) {
                self.$el.find(".it_brand_slider").on("click", _.bind(self.brand_it_slider, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.brand_it_slider()) {
                this.brand_it_slider().fail(function() {
                    self.getParent()._removeSnippet();

                });
            }
        },
        cleanForSave: function() {
            $('.it_brand_slider .owl-carousel').empty();
        },

        brand_it_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_brand_configration"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#slider_type"),
                    $cancel = self.$modal.find("#cancel"),
                    $brand_sub_data = self.$modal.find("#pro_brand_sub_data");

                ajax.jsonRpc('/theme_scita/brand_get_options', 'call', {}).then(function(res) {
                    $('#slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });

                $brand_sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-brand-config-type', $slider_type.val());
                    self.$target.attr('data-brand-config-id', $slider_type.val());
                    if ($('select#slider_type').find(":selected").text()) {
                        type = _t($('select#slider_type').find(":selected").text());
                    } else {
                        type = _t("Our Brands");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="row oe_our_slider">\
                                                        <div class="col-md-12">\
                                                            <div class="title-block">\
                                                                <h4 class="section-title style1">\
                                                                    <span>' + type + '</span>\
                                                                </h4>\
                                                            </div>\
                                                        </div>\
                                                    </div>\
                                                </div>');
                });
            } else {
                return;
            }
        },

    });
    options.registry.health_blog_custom_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.health_blog_slider').empty();
            
            if (!editMode) {
                self.$el.find(".health_blog_slider").on("click", _.bind(self.theme_scita_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.theme_scita_blog_slider()) {
                this.theme_scita_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.health_blog_slider').empty();
        },
        theme_scita_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#blog_slider_type"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/theme_scita/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_type.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_type.val());
                    if ($('select#blog_slider_type').find(":selected").text()) {
                        type = _t($('select#blog_slider_type').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    options.registry.theme_scita_blog_custom_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.scita_blog_slider').empty();
           
            if (!editMode) {
                self.$el.find(".scita_blog_slider").on("click", _.bind(self.theme_scita_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.theme_scita_blog_slider()) {
                this.theme_scita_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.scita_blog_slider').empty();
        },
        theme_scita_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#blog_slider_type"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/theme_scita/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_type.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_type.val());
                    if ($('select#blog_slider_type').find(":selected").text()) {
                        type = _t($('select#blog_slider_type').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    options.registry.blog_2_custom_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.blog_2_custom').empty();
            
            if (!editMode) {
                self.$el.find(".blog_2_custom").on("click", _.bind(self.theme_scita_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.theme_scita_blog_slider()) {
                this.theme_scita_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.blog_2_custom').empty();
        },
        theme_scita_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#blog_slider_type"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/theme_scita/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_type.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_type.val());
                    if ($('select#blog_slider_type').find(":selected").text()) {
                        type = _t($('select#blog_slider_type').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    options.registry.blog_3_custom_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.blog_3_custom').empty();
            
            if (!editMode) {
                self.$el.find(".blog_3_custom").on("click", _.bind(self.theme_scita_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.theme_scita_blog_slider()) {
                this.theme_scita_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.blog_3_custom').empty();
        },
        theme_scita_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#blog_slider_type"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/theme_scita/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_type.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_type.val());
                    if ($('select#blog_slider_type').find(":selected").text()) {
                        type = _t($('select#blog_slider_type').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    
    options.registry.blog_4_custom_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.blog_4_custom').empty();
           
            if (!editMode) {
                self.$el.find(".blog_4_custom").on("click", _.bind(self.theme_scita_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.theme_scita_blog_slider()) {
                this.theme_scita_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.blog_4_custom').empty();
        },
        theme_scita_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#blog_slider_type"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/theme_scita/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_type.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_type.val());
                    if ($('select#blog_slider_type').find(":selected").text()) {
                        type = _t($('select#blog_slider_type').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    options.registry.blog_6_custom_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.blog_6_custom').empty();
           
            if (!editMode) {
                self.$el.find(".blog_6_custom").on("click", _.bind(self.theme_scita_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.theme_scita_blog_slider()) {
                this.theme_scita_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.blog_6_custom').empty();
        },
        theme_scita_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#blog_slider_type"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/theme_scita/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_type.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_type.val());
                    if ($('select#blog_slider_type').find(":selected").text()) {
                        type = _t($('select#blog_slider_type').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    options.registry.blog_5_custom_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.blog_5_custom').empty();
            if (!editMode) {
                self.$el.find(".blog_5_custom").on("click", _.bind(self.theme_scita_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.theme_scita_blog_slider()) {
                this.theme_scita_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.blog_5_custom').empty();
        },
        theme_scita_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#blog_slider_type"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/theme_scita/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_type.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_type.val());
                    if ($('select#blog_slider_type').find(":selected").text()) {
                        type = _t($('select#blog_slider_type').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    options.registry.blog_8_custom_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.blog_8_custom').empty();
            if (!editMode) {
                self.$el.find(".blog_8_custom").on("click", _.bind(self.theme_scita_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.theme_scita_blog_slider()) {
                this.theme_scita_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.blog_8_custom').empty();
        },
        theme_scita_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#blog_slider_type"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/theme_scita/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_type.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_type.val());
                    if ($('select#blog_slider_type').find(":selected").text()) {
                        type = _t($('select#blog_slider_type').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    options.registry.cat_slider_3 = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find(".cat_slider_3").empty();
            if (!editMode) {
                self.$el.find(".cat_slider_3").on("click", _.bind(self.cat_slider, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.cat_slider()) {
                this.cat_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },

        cleanForSave: function() {
            $('.cat_slider_3').empty();
        },

        cat_slider: function(type, value) {
            var self = this;
            
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_dynamic_category_slider"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#slider_type"),
                    $category_slider_delete = self.$modal.find("#cancel"),
                    $pro_cat_sub_data = self.$modal.find("#cat_sub_data");
                ajax.jsonRpc('/theme_scita/category_get_options', 'call', {}).then(function(res) {
                    $('#slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });

                $pro_cat_sub_data.on('click', function() {
                    var type = '';
                    // self.$target.attr('data-cat-slider-type', $slider_type.val());
                    self.$target.attr('data-cat-slider-id', $slider_type.val());
                    if ($('select#slider_type').find(":selected").text()) {
                        type = _t($('select#slider_type').find(":selected").text());
                    } else {
                        type = _t("Category Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $category_slider_delete.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    options.registry.cat_slider_4 = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find(".cat_slider_4").empty();
            if (!editMode) {
                self.$el.find(".cat_slider_4").on("click", _.bind(self.cat_slider, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.cat_slider()) {
                this.cat_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },

        cleanForSave: function() {
            $('.cat_slider_4').empty();
        },

        cat_slider: function(type, value) {
            var self = this;
            
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_dynamic_category_slider"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#slider_type"),
                    $category_slider_delete = self.$modal.find("#cancel"),
                    $pro_cat_sub_data = self.$modal.find("#cat_sub_data");
                ajax.jsonRpc('/theme_scita/category_get_options', 'call', {}).then(function(res) {
                    $('#slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });

                $pro_cat_sub_data.on('click', function() {
                    var type = '';
                    // self.$target.attr('data-cat-slider-type', $slider_type.val());
                    self.$target.attr('data-cat-slider-id', $slider_type.val());
                    if ($('select#slider_type').find(":selected").text()) {
                        type = _t($('select#slider_type').find(":selected").text());
                    } else {
                        type = _t("Category Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $category_slider_delete.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    // new brand and product/category snippet
    options.registry.custom_scita_product_category_slider = options.Class.extend({

        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find(".custom_oe_pro_cat_slider").empty();
            if (!editMode) {
                self.$el.find(".custom_oe_pro_cat_slider").on("click", _.bind(self.custom_pro_cat_slider, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.custom_pro_cat_slider()) {
                this.custom_pro_cat_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },

        cleanForSave: function() {
            $('.oe_pro_cat_slider').empty();
        },

        custom_pro_cat_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_dynamic_product_slider"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#slider_type"),
                    $cancel = self.$modal.find("#cancel"),
                    $pro_cat_sub_data = self.$modal.find("#prod_sub_data");

                ajax.jsonRpc('/theme_scita/pro_get_options', 'call', {}).then(function(res) {
                    $('#slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $pro_cat_sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-prod-cat-slider-type', $slider_type.val());
                    self.$target.attr('data-prod-cat-slider-id', 'prod-cat-myowl' + $slider_type.val());
                    if ($('select#slider_type').find(":selected").text()) {
                        type = _t($('select#slider_type').find(":selected").text());
                    } else {
                        type = _t("Product/Category Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="row oe_our_slider">\
                                                        <div class="col-md-12">\
                                                            <div class="title-block">\
                                                                <h4 class="section-title style1">\
                                                                    <span>' + type + '</span>\
                                                                </h4>\
                                                            </div>\
                                                        </div>\
                                                    </div>\
                                                </div>');
                });
            } else {
                return;
            }
        },
    });
    options.registry.custom_scita_brand_custom_slider = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find(".custom_scita_pro_brand_slider").empty();
            if (!editMode) {
                self.$el.find(".custom_scita_pro_brand_slider").on("click", _.bind(self.custom_scita_brand_slider, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.custom_scita_brand_slider()) {
                this.custom_scita_brand_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },

        cleanForSave: function() {
            $('.custom_scita_pro_brand_slider').empty();
        },

        custom_scita_brand_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_brand_configration"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#slider_type"),
                    $cancel = self.$modal.find("#cancel"),
                    $brand_sub_data = self.$modal.find("#pro_brand_sub_data");

                ajax.jsonRpc('/theme_scita/brand_get_options', 'call', {}).then(function(res) {
                    $('#slider_type option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='slider_type'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });

                $brand_sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-brand-config-type', $slider_type.val());
                    self.$target.attr('data-brand-config-id', $slider_type.val());
                    if ($('select#slider_type').find(":selected").text()) {
                        type = _t($('select#slider_type').find(":selected").text());
                    } else {
                        type = _t("Brand snippet");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="row oe_our_slider">\
                                                        <div class="col-md-12">\
                                                            <div class="title-block">\
                                                                <h4 class="section-title style1">\
                                                                    <span>' + type + '</span>\
                                                                </h4>\
                                                            </div>\
                                                        </div>\
                                                    </div>\
                                                </div>');
                });
            } else {
                return;
            }
        },
    });
    //  brand and product/category snippet end
    options.registry.product_category_img_slider_config = options.Class.extend({

        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("hidden");
            this.$target.find('.multi_product_and_category_slider .owl-carousel').empty();
            if (!editMode) {
                self.$el.find(".multi_product_and_category_slider").on("click", _.bind(self.multi_category_slider, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.multi_category_slider()) {
                this.multi_category_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },

        cleanForSave: function() {
            $('.multi_product_and_category_slider .owl-carousel').empty();
        },

        multi_category_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_product_category_img_slider_config"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#slider_type"),
                    $cancel = self.$modal.find("#cancel"),
                    $snippnet_submit = self.$modal.find("#snippnet_submit");
                ajax.jsonRpc('/theme_scita/product_category_slider', 'call', {}).then(function(res) {
                    $("select[id='slider_type'] option").remove();
                    _.each(res, function(y) {
                        $("select[id='slider_type']").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });

                $snippnet_submit.on('click', function() {
                    self.$target.attr('data-multi-cat-slider-type', $slider_type.val());
                    self.$target.attr('data-multi-cat-slider-id', 'multi-cat-myowl' + $slider_type.val());
                    if ($('select#slider_type').find(":selected").text()) {
                        var type = '';
                        type = _t($('select#slider_type').find(":selected").text());
                    } else {
                        var type = '';
                        type = _t("Image Product/Category Snippet");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="row our-categories">\
                                                        <div class="col-md-12">\
                                                            <div class="title-block">\
                                                                <h4 class="section-title style1">\
                                                                    <span>' + type + '</span>\
                                                                </h4>\
                                                            </div>\
                                                        </div>\
                                                    </div>\
                                                </div>');
                });
            } else {
                return;
            }
        },
    });
    options.registry.sct_product_snippet_1 = options.Class.extend({

        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("hidden");
            this.$target.find('.sct_product_snippet_1 .owl-carousel').empty();
            if (!editMode) {
                self.$el.find(".sct_product_snippet_1").on("click", _.bind(self.multi_category_slider, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.multi_category_slider()) {
                this.multi_category_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },

        cleanForSave: function() {
            $('.sct_product_snippet_1 .owl-carousel').empty();
        },

        multi_category_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_dynamic_product_snippet_configuration"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#slider_type"),
                    $cancel = self.$modal.find("#cancel"),
                    $snippnet_submit = self.$modal.find("#snippnet_submit");
                ajax.jsonRpc('/theme_scita/product_configuration', 'call', {}).then(function(res) {
                    $("select[id='slider_type'] option").remove();
                    _.each(res, function(y) {
                        $("select[id='slider_type']").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });

                $snippnet_submit.on('click', function() {
                    self.$target.attr('data-multi-cat-slider-type', $slider_type.val());
                    self.$target.attr('data-multi-cat-slider-id', 'multi-cat-myowl' + $slider_type.val());
                    if ($('select#slider_type').find(":selected").text()) {
                        var type = '';
                        type = _t($('select#slider_type').find(":selected").text());
                    } else {
                        var type = '';
                        type = _t("Multi Product Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="row our-categories">\
                                                        <div class="col-md-12">\
                                                            <div class="title-block">\
                                                                <h4 class="section-title style1">\
                                                                    <span>' + type + '</span>\
                                                                </h4>\
                                                            </div>\
                                                        </div>\
                                                    </div>\
                                                </div>');
                });
            } else {
                return;
            }
        },
    });
    options.registry.sct_product_snippet_2 = options.Class.extend({

        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("hidden");
            this.$target.find('.sct_product_snippet_2 .owl-carousel').empty();
            if (!editMode) {
                self.$el.find(".sct_product_snippet_2").on("click", _.bind(self.multi_category_slider, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.multi_category_slider()) {
                this.multi_category_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },

        cleanForSave: function() {
            $('.sct_product_snippet_2 .owl-carousel').empty();
        },

        multi_category_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.scita_dynamic_product_snippet_configuration"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_type = self.$modal.find("#slider_type"),
                    $cancel = self.$modal.find("#cancel"),
                    $snippnet_submit = self.$modal.find("#snippnet_submit");
                ajax.jsonRpc('/theme_scita/product_configuration', 'call', {}).then(function(res) {
                    $("select[id='slider_type'] option").remove();
                    _.each(res, function(y) {
                        $("select[id='slider_type']").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });

                $snippnet_submit.on('click', function() {
                    self.$target.attr('data-multi-cat-slider-type', $slider_type.val());
                    self.$target.attr('data-multi-cat-slider-id', 'multi-cat-myowl' + $slider_type.val());
                    if ($('select#slider_type').find(":selected").text()) {
                        var type = '';
                        type = _t($('select#slider_type').find(":selected").text());
                    } else {
                        var type = '';
                        type = _t("Multi Product Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="row our-categories">\
                                                        <div class="col-md-12">\
                                                            <div class="title-block">\
                                                                <h4 class="section-title style1">\
                                                                    <span>' + type + '</span>\
                                                                </h4>\
                                                            </div>\
                                                        </div>\
                                                    </div>\
                                                </div>');
                });
            } else {
                return;
            }
        },
    });
    // Dynamic Video banner js start
    options.registry.dynamic_video_banner = options.Class.extend({

        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("hidden");
            this.$target.find(".dynamic_video_banner").empty();

            if (!editMode) {
                self.$el.find(".dynamic_video_banner").on("click", _.bind(self.dynamic_video_banner, self));
            }
        },

        onBuilt: function() {
            var self = this;
            this._super();
            if (this.dynamic_video_banner()) {
                this.dynamic_video_banner().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },

        cleanForSave: function() {
            $('.dynamic_video_banner').empty();
        },

        dynamic_video_banner: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("theme_scita.video_banner_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var modification = this.$target.html()
                var $video_url = self.$modal.find("#video-url"),
                    $cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#video_sub_data");
                $video_url.val(self.$target.attr('data-video-url'));
                $sub_data.on('click', function() {
                    var type = _t("Video Banner");

                    self.$target.attr("data-video-url", $video_url.val());

                    self.$target.empty().append('<div class="container">\
                                                    <div class="row our-brands">\
                                                        <div class="col-md-12">\
                                                            <div class="title-block">\
                                                                <h4 class="section-title style1">\
                                                                    <span>' + type + '</span>\
                                                                </h4>\
                                                            </div>\
                                                        </div>\
                                                    </div>\
                                                </div>');
                });
            } else {
                return;
            }
        },
    });
    // Dynamic Video banner js End
    // Animation effects for Theme js start
    // options.registry.animaion_effect = options.Class.extend({
    //     start: function () {
    //         var self = this;
    //         if(this.$target.parent().attr('class') != undefined)
    //         {
    //             var parentclassName = this.$target.parent().attr('class').match("sct_img_effect(.)")
    //             if(parentclassName){
    //                 this.$target.addClass(parentclassName[0]);
    //             }    
    //         }
    //         return this._super.apply(this, arguments);
    //     },
    //     _setActive: function () {
    //         this._super.apply(this, arguments);
    //         this.$target.parent().removeClass('sct_img_effect1 sct_img_effect2 sct_img_effect3 sct_img_effect4 sct_img_effect5')
    //         if(this.$target.attr('class') != undefined)
    //         {
    //             var newclassName = this.$target.attr('class').match("sct_img_effect(.)");
    //             if(newclassName){
    //                 this.$target.parent().addClass(newclassName[0])
    //                 this.$target.removeClass(newclassName[0])
    //             }    
    //         }
    //     },
    // });
    options.registry.animaion_effect = options.Class.extend({
        start: function () {
            var self = this;
            if(this.$target.parent().attr('class') != undefined)
            {
                var parentclassName = this.$target.parent().attr('class').match("sct_img_effect(.)")
                if(parentclassName){
                    this.$target.addClass(parentclassName[0]);
                }    
            }
            return this._super.apply(this, arguments);
        },
        _computeWidgetState(methodName, params) {
            this.$target.parent().removeClass('sct_img_effect1 sct_img_effect2 sct_img_effect3 sct_img_effect4 sct_img_effect5')
            if(this.$target.attr('class') != undefined)
            {
                var newclassName = this.$target.attr('class').match("sct_img_effect(.)");
                if(newclassName){
                    this.$target.parent().addClass(newclassName[0])
                    this.$target.addClass(newclassName[0])
                }    
            }
            return this._super(...arguments);
        },
    });
    // Animation effects for Theme js End
});