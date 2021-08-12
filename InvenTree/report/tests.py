# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shutil

from django.urls import reverse
from django.conf import settings

from InvenTree.api_tester import InvenTreeAPITestCase

import report.models as report_models


class ReportTest(InvenTreeAPITestCase):

    fixtures = [
        'category',
        'part',
        'company',
        'location',
        'supplier_part',
        'stock',
        'stock_tests',
    ]

    model = None
    list_url = None
    detail_url = None
    print_url = None

    def setUp(self):
        super().setUp()

    def copyReportTemplate(self, filename, description):
        """
        Copy the provided report template into the required media directory
        """

        src_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'templates',
            'report'
        )

        template_dir = os.path.join(
            'report',
            'inventree',
            self.model.getSubdir(),
        )

        dst_dir = os.path.join(
            settings.MEDIA_ROOT,
            template_dir
        )

        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)

        src_file = os.path.join(src_dir, filename)
        dst_file = os.path.join(dst_dir, filename)

        if not os.path.exists(dst_file):
            shutil.copyfile(src_file, dst_file)

        # Convert to an "internal" filename
        db_filename = os.path.join(
            template_dir,
            filename
        )

        # Create a database entry for this report template!
        self.model.objects.create(
            name=os.path.splitext(filename)[0],
            description=description,
            template=db_filename,
            enabled=True
        )

    def test_list_endpoint(self):
        """
        Test that the LIST endpoint works for each report
        """

        if not self.list_url:
            return

        url = reverse(self.list_url)

        response = self.get(url)
        self.assertEqual(response.status_code, 200)

        reports = self.model.objects.all()

        n = len(reports)

        # API endpoint must return correct number of reports
        self.assertEqual(len(response.data), n)

        # Filter by "enabled" status
        response = self.get(url, {'enabled': True})
        self.assertEqual(len(response.data), n)
        
        response = self.get(url, {'enabled': False})
        self.assertEqual(len(response.data), 0)

        # Disable each report
        for report in reports:
            report.enabled = False
            report.save()

        # Filter by "enabled" status
        response = self.get(url, {'enabled': True})
        self.assertEqual(len(response.data), 0)
        
        response = self.get(url, {'enabled': False})
        self.assertEqual(len(response.data), n)


class TestReportTest(ReportTest):

    model = report_models.TestReport

    list_url = 'api-stockitem-testreport-list'
    detail_url = 'api-stockitem-testreport-detail'
    print_url = 'api-stockitem-testreport-print'

    def setUp(self):

        self.copyReportTemplate('inventree_test_report.html', 'stock item test report')

        return super().setUp()


class BuildReportTest(ReportTest):

    model = report_models.BuildReport

    list_url = 'api-build-report-list'
    detail_url = 'api-build-report-detail'
    print_url = 'api-build-report-print'

    def setUp(self):

        self.copyReportTemplate('inventree_build_order.html', 'build order template')

        return super().setUp()


class BOMReportTest(ReportTest):

    model = report_models.BillOfMaterialsReport

    list_url = 'api-bom-report-list'
    detail_url = 'api-bom-report-detail'
    print_url = 'api-bom-report-print'


class POReportTest(ReportTest):

    model = report_models.PurchaseOrderReport

    list_url = 'api-po-report-list'
    detail_url = 'api-po-report-detail'
    print_url = 'api-po-report-print'


class SOReportTest(ReportTest):

    model = report_models.SalesOrderReport

    list_url = 'api-so-report-list'
    detail_url = 'api-so-report-detail'
    print_url = 'api-so-report-print'
