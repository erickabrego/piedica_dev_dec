from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict
from odoo.http import request


class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        PatientExam = request.env['patient.exam']
        partner = request.env.user.partner_id
        domain = [('patient_id', '=', partner.id)]

        if 'exam_count' in counters:
            exam_count = PatientExam.search_count(domain) if PatientExam.check_access_rights('read', raise_exception=False) else 0
            values['exam_count'] = exam_count

        return values


    def _exam_get_page_view_values(self, exam, access_token, **kwargs):
        values = {
            'page_name': 'exam',
            'exam': exam,
        }

        return self._get_page_view_values(exam, access_token, values, 'my_exams_history', False, **kwargs)


    @http.route(['/my/exams', '/my/exams/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_exams(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        PatientExam = request.env['patient.exam']
        ExamStatus = request.env['exam.status']
        partner = request.env.user.partner_id
        domain = [('patient_id', '=', partner.id)]

        searchbar_sortings = {
            'date': {'label': 'Fecha', 'order': 'date desc'},
            'status': {'label': 'Estatus', 'order': 'exam_status_id'},
        }

        # default sort by order
        if not sortby:
            sortby = 'date'

        order = searchbar_sortings[sortby]['order']

        no_solicitado = ExamStatus.search([('code', '=', 'no_solicitado')])
        solicitado = ExamStatus.search([('code', '=', 'solicitado')])
        generado = ExamStatus.search([('code', '=', 'generado')])

        searchbar_filters = {
            'all': {'label': 'Todos', 'domain': []},
            'no_solicitado': {'label': 'No solicitado', 'domain': [('exam_status_id', '=', no_solicitado.id)]},
            'solicitado': {'label': 'Solicitado', 'domain': [('exam_status_id', '=', solicitado.id)]},
            'generado': {'label': 'Generado', 'domain': [('exam_status_id', '=', generado.id)]}
        }

        # default filter by value
        if not filterby:
            filterby = 'all'

        domain += searchbar_filters[filterby]['domain']

        if date_begin and date_end:
            domain += [('date', '>', date_begin), ('date', '<=', date_end)]

        # count for pager
        exam_count = PatientExam.search_count(domain)

        # pager
        pager = portal_pager(
            url="/my/exams",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=exam_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        exams = PatientExam.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_exams_history'] = exams.ids[:100]

        values.update({
            'date': date_begin,
            'exams': exams,
            'page_name': 'exam',
            'pager': pager,
            'default_url': '/my/exams',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby':filterby,
        })

        # Verifica si se redireccionó desde "/my/exams/<id>/request"
        requested_redirect = request.session.pop('requested_redirect', None)

        if requested_redirect:
            values.update({'requested_redirect': requested_redirect})

        return request.render("crm_sync_exams.portal_my_exams", values)


    @http.route('/my/exams/<id>/request', type='http', auth="user", website=True)
    def request_exam(self, id):
        PatientExam = request.env['patient.exam'].sudo()
        partner = request.env.user.partner_id
        domain = [('patient_id', '=', partner.id), ('id', '=', id)]
        exam = PatientExam.search(domain)

        if exam:
            exam.to_requested()
            request.session.update({'requested_redirect': True})

        return request.redirect('/my/exams')
