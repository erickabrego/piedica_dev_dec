odoo.define('theme_scita.wishlist_products', function (require) {
"use strict";
    var ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');
    publicWidget.registry.toggle_wishlist = publicWidget.Widget.extend({
        selector: '#my_wish',
        events: {
            'click #wishlish_collapse': '_onClickShowMyWish',
            'click .wishlist-section .o_wish_rm': '_onClickWishProRemove',
        },
        _onClickShowMyWish: function (e) {
            var self = this;
            ajax.jsonRpc('/theme_scita/get_current_wishlist', 'call').then(function(data) {
                $('#show-wishlist').html(data);
            });
        },
        _onClickWishProRemove: function (e) {
            var tr = $(e.currentTarget).parents('tr');
            var $tbody = $(e.currentTarget).parents('tbody');
            var wish = tr.data('wish-id');
            var product = tr.data('product-id');
            var self = this;
            this._rpc({
                route: '/shop/wishlist/remove/' + wish,
            }).then(function () {
                location.reload(true);
            });

        },
    });
});