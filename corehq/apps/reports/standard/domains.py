from django.utils.translation import ugettext_noop
import time
from corehq.apps.domain.calculations import CALC_FNS
from corehq.apps.domain.models import Domain
from corehq.apps.hqadmin.views import _all_domain_stats, domain_list
from corehq.apps.orgs.models import Organization
from corehq.apps.reports.datatables import DataTablesHeader, DataTablesColumn, DTSortType
from corehq.apps.reports.dispatcher import BasicReportDispatcher, AdminReportDispatcher
from corehq.apps.reports.generic import GenericTabularReport
from django.utils.translation import ugettext as _
import json
from dimagi.utils.couch.database import get_db


class DomainStatsReport(GenericTabularReport):
    dispatcher = BasicReportDispatcher
    asynchronous = True
    ajax_pagination = True
    section_name = 'DOMSTATS'
    base_template = "reports/async/default.html"
    custom_params = []
    # fields = ['corehq.apps.reports.fields.FilterUsersField',
    #           'corehq.apps.reports.fields.SelectMobileWorkerField']

    name = ugettext_noop('Domain Statistics')
    slug = 'dom_stats'

    def get_domains(self):
        return getattr(self, 'domains', [])

    @property
    def headers(self):
        headers = DataTablesHeader(
            DataTablesColumn("Project"),
            DataTablesColumn("# Web Users", sort_type=DTSortType.NUMERIC),
            # DataTablesColumn(_("# Active Mobile Workers"), sort_type=DTSortType.NUMERIC),
            DataTablesColumn(_("# Mobile Workers"), sort_type=DTSortType.NUMERIC),
            DataTablesColumn(_("# Active Cases"), sort_type=DTSortType.NUMERIC),
            DataTablesColumn(_("# Cases"), sort_type=DTSortType.NUMERIC),
            DataTablesColumn(_("# Form Submissions"), sort_type=DTSortType.NUMERIC),
            DataTablesColumn(_("First Form Submission")),
            DataTablesColumn(_("Last Form Submission")),
            # DataTablesColumn(_("Admins"))
        )
        # headers.no_sort = True
        return headers

    @property
    def rows(self):
        rows = []
        all_stats = _all_domain_stats()
        for dom in self.get_domains():
            rows.append([
                dom,
                int(all_stats["web_users"][dom]),
                # CALC_FNS["mobile_users"](dom, 'active'),
                int(all_stats["commcare_users"][dom]),
                CALC_FNS["cases_in_last"](dom, 30),
                int(all_stats["cases"][dom]),
                int(all_stats["forms"][dom]),
                CALC_FNS["first_form_submission"](dom),
                CALC_FNS["last_form_submission"](dom),
                # [row["doc"]["email"] for row in get_db().view("users/admins_by_domain",
                #                                               key=dom, reduce=False, include_docs=True).all()],
            ])
        return rows

    @property
    def shared_pagination_GET_params(self):
        ret = super(DomainStatsReport, self).shared_pagination_GET_params
        for k, v in self.request.GET.items():
            if k in self.custom_params:
                ret.append(dict(name=k, value=v))
        return ret

class OrgDomainStatsReport(DomainStatsReport):
    custom_params = ['org']

    def get_domains(self):
        org = self.request.GET.get('org', None)
        organization = Organization.get_by_name(org, strict=True)
        if organization and \
                (self.request.couch_user.is_superuser or self.request.couch_user.is_member_of_org(org)):
            return [d.name for d in Domain.get_by_organization(organization.name).all()]
        return []

class AdminDomainStatsReport(DomainStatsReport):
    dispatcher = AdminReportDispatcher
    custom_params = ['domains']

    def get_domains(self):
        domains = self.request.GET.get("domains", "").split('|')
        if not domains:
            domains = [d.name for d in Domain.get_all()]
        return domains
