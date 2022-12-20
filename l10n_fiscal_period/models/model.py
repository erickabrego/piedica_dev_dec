# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError

import datetime
import calendar


class AccountingYear(models.Model):
    _name = "accounting.year"
    _description = "Accounting year period"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def _validate_duplicity_exercise(self):
        fiscal_accountings = self.search([])
        if fiscal_accountings:
            duplicity_year = fiscal_accountings.filtered(
                lambda f: f.start_date < self.end_date and self.start_date < f.end_date
            )

            if duplicity_year and len(duplicity_year) > 1:
                raise UserError(
                    _("There is an accounting year that coincides on the date.")
                )

    name = fields.Char(string="Code", copy=False)
    user_id = fields.Many2one(
        "res.users", string="Create by user", default=lambda self: self.env.user.id
    )
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.company
    )
    start_date = fields.Date(string="Start date", default=fields.Date.today)
    end_date = fields.Date(string="End date", default=fields.Date.today)

    accounting_period_ids = fields.One2many(
        "accounting.period", "accounting_year_id", string="Periods"
    )
    note = fields.Text(string="Note")
    state = fields.Selection(
        [("draft", "Draft"), ("in_progress", "In progress"), ("closed", "Closed")],
        string="State",
        default="draft",
        tracking=True,
    )
    periods_generated = fields.Boolean()

    @api.model
    def create(self, vals_list):
        record = super(AccountingYear, self).create(vals_list)
        record._validate_duplicity_exercise()
        return record

    def set_in_progress(self):
        self._validate_duplicity_exercise()
        self.write({"state": "in_progress"})

    def set_closed(self):
        periods = self.env["accounting.period"].search(
            [("accounting_year_id", "=", self.id), ("state", "=", "in_progress")]
        )
        if periods:
            raise UserError(
                _("You cannot close the fiscal year with periods in progress status.")
            )

        self.write({"state": "closed"})

    def generate_monthly_periods(self):
        if self.accounting_period_ids:
            raise UserError(
                _(u"Thid accounting year already has all monthly periods. You can't generate more by this action."))

        current_year = self.start_date.year
        periods = []

        month = 1
        while month <= 12:
            start_day_month = datetime.date(year=current_year, month=month, day=1)
            end_day_month = datetime.date(year=current_year, month=month,
                                          day=calendar.monthrange(year=current_year, month=month)[1])
            month += 1

            period = self.env['accounting.period'].create({
                'start_date': start_day_month,
                'end_date': end_day_month,
                'name': datetime.datetime.strftime(start_day_month, "%b/%Y"),
                'accounting_year_id': self.id
            })

            periods.append(period.id)

        self.periods_generated = True
        self.accounting_period_ids = [(6, False, periods)]


class AccountingPeriod(models.Model):
    _name = "accounting.period"
    _description = "Accounting period"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def _validate_state(self):
        validate = True if self.accounting_year_id.state != "closed" else False
        return validate

    def _validate_duplicity_period(self):
        period_accountings = self.search([]).filtered(
            lambda p: p.accounting_year_id == self.accounting_year_id
        )
        if period_accountings:
            duplicity_period = period_accountings.filtered(
                lambda f: f.start_date < self.end_date and self.start_date < f.end_date
            )
            if duplicity_period and len(duplicity_period) > 1:
                raise UserError(
                    _("There is an accounting period that coincides on the date.")
                )

    name = fields.Char(string="Code", copy=False)
    start_date = fields.Date(string="Start date", default=fields.Date.today)
    end_date = fields.Date(string="end date", default=fields.Date.today)
    user_id = fields.Many2one(
        "res.users", string="Create by user", default=lambda self: self.env.user.id
    )
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.company
    )
    accounting_year_id = fields.Many2one("accounting.year", string="Accounting year")

    state = fields.Selection(
        [("draft", "Draft"), ("in_progress", "In progress"), ("closed", "Closed")],
        string="State",
        default="draft",
        tracking=True,
    )

    @api.model
    def create(self, vals_list):
        record = super(AccountingPeriod, self).create(vals_list)
        record._validate_duplicity_period()
        return record

    def set_in_progress(self):
        if self._validate_state():
            self.write({"state": "in_progress"})
        else:
            raise UserError(
                _("The accounting year corresponding to the period has been closed.")
            )

    def set_closed(self):
        if self._validate_state():
            self.write({"state": "closed"})
        else:
            raise UserError(
                _("The accounting year corresponding to the period has been closed.")
            )

    def set_reopen(self):
        if self._validate_state():
            self.write({"state": "in_progress"})
            self._create_msg()
        else:
            raise UserError(
                _("The accounting year corresponding to the period has been closed.")
            )

    def _create_msg(self):
        display_msg = """ El usuario """ + self.env.user.name + """,
                                                <br/>
                                                Reabrió el periodo con código:
                                                """ + self.name + """
                                                <br/>
                                                <br/>
                                            """
        self.accounting_year_id.message_post(body=display_msg)


class AccountMove(models.Model):
    _inherit = "account.move"

    def _check_period(self):
        accounting_year = (
            self.env["accounting.year"]
                .search([])
                .filtered(
                lambda y: y.state == "in_progress"
                          and y.start_date <= self.date
                          and y.end_date >= self.date
            )
        )
        if not accounting_year:
            raise UserError(
                _("There is no accounting year configured in progress for this period.")
            )
        accounting_period = (
            self.env["accounting.period"]
                .search([])
                .filtered(
                lambda p: p.state == "in_progress"
                          and p.start_date <= self.date
                          and p.end_date >= self.date
                          and p.accounting_year_id.id == accounting_year.id
            )
        )
        if not accounting_period:
            raise UserError(
                _(
                    "There is no accounting period configured in progress for this period."
                )
            )

    def write(self, vals):
        state = vals.get("state", False)
        for record in self:
            if state and state == "posted" and record.id:
                record._check_period()
        return super(AccountMove, self).write(vals)
