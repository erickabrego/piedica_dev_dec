odoo.define('theme_scita.rating_state_js', function(require) {
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var qweb = core.qweb;

    ajax.loadXML('/portal_rating/static/src/xml/portal_chatter.xml', qweb);
    var PortalChatter = require('portal.chatter').PortalChatter;
 
    PortalChatter.include({
        start: function(){
            var res = this._super.apply(this);
            var rating_val = this.options['rating_val'];

            var only_rating = this.options['only_rating'];
            if (only_rating == 1){
                if (this.__getterSetterInternalMap.rating_card_values['avg'] && this.__getterSetterInternalMap.rating_card_values['avg'] < 6){
                    this.$el.closest('.o_portal_chatter').empty().html(qweb.render("portal_rating.rating_stars_static", {'val': this.__getterSetterInternalMap.rating_card_values['avg']}));
                }
                else if(rating_val == 6){
                    this.$el.closest('.o_portal_chatter').empty().html(qweb.render("portal_rating.rating_stars_static", {'val': 0.0}));
                }
            }
            return res
        }
    });
});
