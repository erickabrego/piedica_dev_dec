odoo.define('theme_scita.scita_product_js', function(require) {
    "use strict";
// Multi image gallery
    var ajax = require('web.ajax');
    var VariantMixin = require('sale.VariantMixin');
    var sAnimations = require('website.content.snippets.animation');
    var api;
    function check()
    {   
        if (chkObject('gallery')==true)
       {    
        
        ajax.jsonRpc('/theme_scita/scita_multi_image_thumbnail_config', 'call', {})
                    .then(function(res) {
            var dynamic_data = {}

            dynamic_data['gallery_images_preload_type'] = 'all'
            dynamic_data['slider_enable_text_panel'] = false
            dynamic_data['gallery_skin'] = "alexis"
            dynamic_data['gallery_height'] = 850
            dynamic_data['slider_scale_mode']='fit'
            dynamic_data['slider_enable_arrows'] = true
            
            dynamic_data['strippanel_enable_handle'] = true
            if (res.theme_panel_position != false) {
                dynamic_data['theme_panel_position'] = res.theme_panel_position
            }
            else{
             dynamic_data['theme_panel_position'] = "left"   
            }
            if (res.color_opt_thumbnail != false && res.color_opt_thumbnail != 'default') {
                dynamic_data['thumb_image_overlay_effect'] = true
                if (res.color_opt_thumbnail == 'b_n_w') {}
                if (res.color_opt_thumbnail == 'blur') {
                    dynamic_data['thumb_image_overlay_type'] = "blur"
                }
                if (res.color_opt_thumbnail == 'sepia') {
                    dynamic_data['thumb_image_overlay_type'] = "sepia"
                }
            }
            if (res.enable_disable_text == true) {
                dynamic_data['slider_enable_text_panel'] = true
            }
            if (res.change_thumbnail_size == true) {
                dynamic_data['thumb_height'] = res.thumb_height
                dynamic_data['thumb_width'] = res.thumb_width
            }
            else{
                dynamic_data['thumb_width'] = 66          
                dynamic_data['thumb_height'] = 86

            }
            if (res.interval_play != false) {
                dynamic_data['gallery_play_interval'] = res.interval_play
            }
            if (res.no_extra_options == false) {
                dynamic_data['slider_enable_progress_indicator'] = false
                dynamic_data['slider_enable_play_button'] = false
                dynamic_data['slider_enable_fullscreen_button'] = false
                dynamic_data['slider_enable_zoom_panel'] = false
                dynamic_data['slider_enable_text_panel'] = false
                dynamic_data['gridpanel_enable_handle'] = false
                dynamic_data['theme_panel_position'] = 'left'
                dynamic_data['thumb_image_overlay_effect'] = false
            }
            api = $('#gallery').unitegallery(dynamic_data);
            api.on("item_change", function(num, data) {
            if (data['index'] == 0) {
                    update_gallery_product_image();
                }
            });
            if (api != undefined && $('#gallery').length != 0) {
                setTimeout(function() {
                    update_gallery_product_image()
                }, 200);
            }
            });
            int=window.clearInterval(int);

       }
       else{

       }
    }
    var int=setInterval(check, 100);
    function chkObject(elemClass)
    {  
       return ($('#'+elemClass).length==1)? true : false;
    }
    // multi image for product id get and vraint image change start
    VariantMixin._onChangeCombinationProd = function (ev, $parent, combination) {
        var product_id = 0;

        // needed for list view of variants
        if ($parent.find('input.product_id:checked').length) {
            product_id = $parent.find('input.product_id:checked').val();
        } else {
            product_id = $parent.find('.product_id').val();
        }
        update_gallery_product_variant_image($parent, product_id);
        // default code as per varaint wise start 
        ajax.jsonRpc("/shop/variant_change", 'call', {
            'pro_id':product_id
        }).then(function (data){

            if (data.is_default_code_disp && data.default_code) {
                var code = $('.sct-default-code').html();
                if (code){
                    $('.sct-default-code').html(data.default_code)
                }
                else {
                    $('.sct-sku-display-div').append('<p class="sct-sku-display">SKU: <span class="sct-default-code">'+data.default_code+'</span> </p>')
                }
            }
            else {
                $('.sct-sku-display-div').empty()
            }
        });
        // default code as per varaint wise end 
        
    };
    
    function update_gallery_product_variant_image(event_source, product_id) {
        var $imgs = $(event_source).closest('.oe_website_sale').find('.ug-slide-wrapper');
        var $img = $imgs.find('img');
        if (api!= undefined)
        {
            var total_img = api.getNumItems()
            if (total_img != undefined) {
                api.selectItem(0);
            }
            var $stay;
            $img.each(function(e) {
                if ($(this).attr("src").startsWith('/web/image/scita.product.images/') == false) {
                    
                    $(this).attr("src", "/web/image/product.product/" + product_id + "/image_1920");
                    $("img.js_variant_img_small").attr("src", "/web/image/product.product/" + product_id + "/image_1920");
                    $stay = $(this).parent().parent();
                    $(this).css({
                        'width': 'initial',
                        'height': 'initial'
                    });
                    api.resetZoom();
                    api.zoomIn();
                    
                }
            });    
        }
        
    }

    function update_gallery_product_image() {
        var $container = $('.oe_website_sale').find('.ug-slide-wrapper');
        var $img = $container.find('img');
        var $product_container = $('.oe_website_sale').find('.js_product').first();
        var p_id = parseInt($product_container.find('input.product_id').first().val());

        if (p_id > 0) {
            $img.each(function(e_img) {
                if ($(this).attr("src").startsWith('/web/image/scita.product.images/') == false) {
                    
                    $(this).attr("src", "/web/image/product.product/" + p_id + "/image_1920");
                    
                }
            });
        } else {
            var spare_link = api.getItem(0).urlThumb;
            $img.each(function(e_img) {
                if ($(this).attr("src").startsWith('/web/image/scita.product.images/') == false) {
                    
                    $(this).attr("src", spare_link);
                    
                }
            });
        }
    }
    sAnimations.registry.WebsiteSale.include({
        _onChangeCombination: function (){
            this._super.apply(this, arguments);
            VariantMixin._onChangeCombinationProd.apply(this, arguments);
        }
    });
    // multi image for product id get and vraint image change end

    
    $(document).ready(function () {
        //product detail page cart fix
        if ($('div').hasClass("sct-add-to-cart-mob")){
            $('#wrapwrap').addClass("sct-mobile-pro-detail-list");
        }
        if ($('#product_detail').length != 0) {
            $('body').addClass('sct-cst-pro-page');
        }
        // Product delivery location available checking start
        $('.checker').on('click', function(){
            var zip =  $('input.value-zip').val();
            ajax.jsonRpc("/shop/zipcode", 'call', {
                'zip_code':zip
            }).then(function (data){
                if (data.status == true){
                    $('.get_status').removeClass("fail");
                    $('.get_status').addClass("success");
                    $('#fail_msg').addClass("o_hidden");
                    $('#success_msg').removeClass("o_hidden");
                    $('#blank_msg').addClass("o_hidden");
                    $('input.value-zip').val(zip);
                }
                if (data.status == false) {
                    $('input.value-zip').val(zip);
                    $('.get_status').removeClass("success");
                    $('.get_status').addClass("fail");
                    $('#fail_msg').removeClass("o_hidden");
                    $('#success_msg').addClass("o_hidden");
                    $('#blank_msg').addClass("o_hidden");
                }
                if(data.zip == "notavailable"){
                    $('input.value-zip').val(zip);
                    $('.get_status').removeClass("success");
                    $('.get_status').addClass("fail");
                    $('#fail_msg').addClass("o_hidden");
                    $('#success_msg').addClass("o_hidden");
                    $('#blank_msg').removeClass("o_hidden");
                }
             });
        });
        // Product delivery location available checking end
    });
});
// ajax cart start
odoo.define('theme_scita.ajax_cart', function(require) {
    "use strict";
    var ajax = require('web.ajax');
    var core = require('web.core');
    var publicWidget = require('web.public.widget');
    require('website_sale.website_sale');
    var timeout;
    var _t = core._t;

    publicWidget.registry.WebsiteSale.include({
        _onClickSubmit: function (ev, forceSubmit) {
            if ($(ev.currentTarget).is('#add_to_cart,.o_wsale_product_btn .a-submit') && !forceSubmit) {
                return;
            }
            var $aSubmit = $(ev.currentTarget);

            if (!ev.isDefaultPrevented() && !$aSubmit.is(".disabled")) {
                ev.preventDefault();
                if ($aSubmit.parents('.ajax_cart_template').length) {
                    var frm = $aSubmit.closest('form');
                    var product_product = frm.find('input[name="product_id"]').val();
                    var quantity = frm.find('.quantity').val();
                    if(!quantity) {
                       quantity = 1;
                    }
                    ajax.jsonRpc('/shop/cart/update_custom', 'call',{'product_id':product_product,'add_qty':quantity}).then(function(data) {
                        if(data) {
                            var $quantity = $(".my_cart_quantity");
                            var old_quantity = $quantity.html();
                            $quantity.parent().parent().removeClass('d-none');
                            $quantity.html(parseInt(quantity) + parseInt(old_quantity)).hide().fadeIn(600);
                        }
                    });
                } else {
                    $aSubmit.closest('form').submit();
                }
            }
            if ($aSubmit.hasClass('a-submit-disable')){
                $aSubmit.addClass("disabled");
            }
            if ($aSubmit.hasClass('a-submit-loading')){
                var loading = '<span class="fa fa-cog fa-spin"/>';
                var fa_span = $aSubmit.find('span[class*="fa"]');
                if (fa_span.length){
                    fa_span.replaceWith(loading);
                } else {
                    $aSubmit.append(loading);
                }
            }
        },
    });

    publicWidget.registry.CustomSaleCartHover = publicWidget.Widget.extend({
        selector: 'div.my-cart',
        events: {
            'mouseenter': '_onMouseEnter',
            'click': '_onClick',
        },
        init: function () {
            this._super.apply(this, arguments);
            this._popoverRPC = null;
        },
        start: function () {
            return this._super.apply(this, arguments);
        },
        _onMouseEnter: function (ev) {
            var self = this;
            waitForElementToAppendCartData("div#header-cart",100);
            function waitForElementToAppendCartData(selector, time) {
                if(document.querySelector(selector)!=null) {
                    self._popoverRPC = $.get("/shop/cart/hover_update", {
                    }).then(function (data) {
                        $('div#header-cart').empty().append(data);
                    });
                    return;
                }
                else {
                    setTimeout(function() {
                        waitForElementToAppendCartData(selector, time);
                    }, time);
                }
            }
        },
        _onClick: function (ev) {
            clearTimeout(timeout);
            if (this._popoverRPC && this._popoverRPC.state() === 'pending') {
                ev.preventDefault();
                var href = ev.currentTarget.href;
                this._popoverRPC.then(function () {
                    if(href != undefined){
                        window.location.href = href;
                    }
                });
            }
        },
    });
});
// ajax cart end

odoo.define('theme_scita.cart_hover', function (require) {
'use strict';

    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var wSaleUtils = require('website_sale.utils');
    var sAnimations = require('website.content.snippets.animation');
    var timeout;

    publicWidget.registry.scita_cart_popup = publicWidget.Widget.extend({
        selector: '#wrapwrap',
        init: function () {
            this._super.apply(this, arguments);
        },
        _onClickRemoveItem: function(ev) {
            $(ev.currentTarget).parent().siblings().find('.js_quantity').val(0).trigger('change');
        },
        _onUpdateQuantity: function(ev){
            /* Update the cart quantity and price while change the product quantity from input */
            ev.preventDefault();
            var $link = $(ev.currentTarget);
            var $input = $link.closest('.input-group').find("input");
            var min = parseFloat($input.data("min") || 0);
            var max = parseFloat($input.data("max") || Infinity);
            var previousQty = parseFloat($input.val() || 0, 10);
            var quantity = ($link.has(".fa-minus").length ? -1 : 1) + previousQty;
            var newQty = quantity > min ? (quantity < max ? quantity : max) : min;

            if (newQty !== previousQty) {
                $input.val(newQty).trigger('change');
            }
            return false;
        },
        _onChangeQuantity: function (ev){
            /* Get the updated data while change the cart quantity from cart. */
            var $input = $(ev.currentTarget);
            var self = this;
            $input.data('update_change', false);
            var value = parseInt($input.val() || 0, 10);
            if (isNaN(value)) {
                value = 1;
            }
            var line_id = parseInt($input.data('line-id'), 10);
            rpc.query({
                route: "/shop/cart/update_json",
                params: {
                    line_id: line_id,
                    product_id: parseInt($input.data('product-id'), 10),
                    set_qty: value
                },
            }).then(function (data) {
                $input.data('update_change', false);
                var check_value = parseInt($input.val() || 0, 10);
                if (isNaN(check_value)) {
                    check_value = 1;
                }
                if (value !== check_value) {
                    $input.trigger('change');
                    return;
                }
                if (!data.cart_quantity) {
                    return window.location = '/shop/cart';
                }
                wSaleUtils.updateCartNavBar(data);
                $input.val(data.quantity);
                $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);
                $(".popover-header").html(data.quantity);
                $.get("/shop/cart", {
                    type: 'popover',
                }).then(function(data) {
                    $(".mycart-popover .popover-body").html(data);
                    $('.mycart-popover .js_add_cart_json').off('click').on('click',function(ev) {
                        ev.preventDefault();
                        self._onUpdateQuantity(ev)
                    });
                    $(".mycart-popover .js_quantity[data-product-id]").off('change').on('change',function(ev) {
                        ev.preventDefault();
                        self._onChangeQuantity(ev)
                    });
                    $(".mycart-popover .scita_cart_popup_remove").off('click').on('click',function(ev) {
                        ev.preventDefault();
                        self._onClickRemoveItem(ev)
                    });
                });
            });
        }
    });
    publicWidget.registry.websiteSaleCartLink.include({
        selector: '.o_wsale_my_cart a[href$="/shop/cart"]',
        _onMouseEnter: function (ev) {
            var self = this;
            clearTimeout(timeout);
            $(this.selector).not(ev.currentTarget).popover('hide');
            timeout = setTimeout(function () {
                if (!self.$el.is(':hover') || $('.mycart-popover:visible').length) {
                    return;
                }
                self._popoverRPC = $.get("/shop/cart", {
                    type: 'popover',
                }).then(function (data) {
                    var cartPopup = new publicWidget.registry.scita_cart_popup();
                    self.$el.data("bs.popover").config.content = data;
                    self.$el.popover("show");
                    $(".mycart-popover .popover-body").html(data);
                    $('.popover').on('mouseleave', function () {
                        self.$el.trigger('mouseleave');
                    });
                    $('.mycart-popover .js_add_cart_json').off('click').on('click',function(ev) {
                        ev.preventDefault();
                        cartPopup._onUpdateQuantity(ev)
                    });
                    $(".mycart-popover .js_quantity[data-product-id]").off('change').on('change',function(ev) {
                        ev.preventDefault();

                        cartPopup._onChangeQuantity(ev)
                    });
                    $(".mycart-popover .scita_cart_popup_remove").off('click').on('click',function(ev) {
                        ev.preventDefault();
                        cartPopup._onClickRemoveItem(ev)
                    });
                });
            }, 300);
        }
    });
    // For quickview Start
    publicWidget.registry.quickView = publicWidget.Widget.extend({
        selector: "div#wrapwrap",
        events: {
            'click .quick_view_sct_btn': 'quickViewData',
            'click .cart_view_sct_btn': 'cartViewData',
        },
        quickViewData: function(ev) {
            var element = ev.currentTarget;
            var product_id = $(element).attr('data-id');
            ajax.jsonRpc('/theme_scita/shop/quick_view', 'call',{'product_id':product_id}).then(function(data) {
                var sale = new publicWidget.registry.WebsiteSale();

                    $("#shop_quick_view_modal").html(data);
                    $("#shop_quick_view_modal").modal();
                    sale.init();
                    $(".quick_cover").css("display", "block");
                    $("[data-attribute_exclusions]").on("change", function(ev) {
                        sale.onChangeVariant(ev);
                    });
                    $("[data-attribute_exclusions]").trigger("change");
                    $(".css_attribute_color input").click(function(ev){
                        sale._changeColorAttribute(ev);
                    });
                    $(".a-submit").on("click", function(ev) {
                        sale._onClickAdd(ev);
                    });
                    $("a.js_add_cart_json").on("click", function(ev) {
                        sale._onClickAddCartJSON(ev);
                    });
                    $("input[name='add_qty']").on("change", function(ev) {
                        sale._onChangeAddQuantity(ev);
                    });
            });
        },
        cartViewData: function(ev) {
            var element = ev.currentTarget;
            var product_id = $(element).attr('data-id');
            ajax.jsonRpc('/theme_scita/shop/cart_view', 'call',{'product_id':product_id}).then(function(data) {
                $("#shop_cart_view_modal").html(data);
                $("#shop_cart_view_modal").modal();
            });
        }
    });
    // For quickview End
    // For hoverableDropdown extend start
    publicWidget.registry.hoverableDropdown = publicWidget.registry.hoverableDropdown.extend({
        events: _.extend({}, publicWidget.RootWidget.prototype.events || {}, {
            'mouseenter .li-mega-menu': '_onMouseEnter',
            'mouseleave .li-mega-menu': '_onMouseLeave',
        }),
    });
    // For hoverableDropdown extend End
});
