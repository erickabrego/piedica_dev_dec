from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict
from odoo.http import request


class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        SaleOrder = request.env['sale.order'].sudo()
        partner = request.env.user.partner_id
        start_date = datetime.now() - relativedelta(years=2)
        domain = ['&', '&', ('partner_id', '=', partner.id), ('date_order', '>', start_date), ('state', 'not in', ['draft', 'cancel'])]

        if 'insole_count' in counters:
            insole_count = SaleOrder.sudo().search_count(domain) if SaleOrder.check_access_rights('read', raise_exception=False) else 0
            values['insole_count'] = insole_count

        return values


    def _insole_get_page_view_values(self, mrp_order, access_token, **kwargs):
        values = {
            'page_name': 'insole',
            'sale_order': sale_order,
        }

        return self._get_page_view_values(sale_order, access_token, values, 'my_insoles_history', False, **kwargs)


    @http.route(['/my/insoles', '/my/insoles/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_insoles(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        SaleOrder = request.env['sale.order'].sudo()
        partner = request.env.user.partner_id
        start_date = datetime.now() - relativedelta(years=2)
        domain = ['&', '&', ('partner_id', '=', partner.id), ('date_order', '>', start_date), ('state', 'not in', ['draft', 'cancel'])]

        searchbar_sortings = {
            'date': {'label': 'Fecha', 'order': 'date_order desc'}
        }

        # default sort by order
        if not sortby:
            sortby = 'date'

        order = searchbar_sortings[sortby]['order']

        searchbar_filters = {
            'all': {'label': 'Todos', 'domain': []},
        }

        # default filter by value
        if not filterby:
            filterby = 'all'

        domain += searchbar_filters[filterby]['domain']

        if date_begin and date_end:
            domain += [('date_order', '>', date_begin), ('date_order', '<=', date_end)]

        # count for pager
        insole_count = SaleOrder.search_count(domain)

        # pager
        pager = portal_pager(
            url="/my/insoles",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=insole_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        sale_orders = SaleOrder.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_insoles_history'] = sale_orders.ids[:100]

        values.update({
            'date': date_begin,
            'sale_orders': sale_orders,
            'page_name': 'insole',
            'pager': pager,
            'default_url': '/my/insoles',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby':filterby,
        })

        return request.render("crm_sync_orders.portal_my_insoles", values)
