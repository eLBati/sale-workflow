# -*- coding: utf-8 -*-
#
#    Sale Fiscal Position Update module for OpenERP
#    Copyright (C) 2011-2014 Julius Network Solutions SARL <contact@julius.fr>
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
#    @author Mathieu Vatel <mathieu _at_ julius.fr>
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#    Copyright 2016 Lorenzo Battistini - Agile Business Group
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#

from openerp import models, api
from openerp.tools.translate import _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('fiscal_position')
    def fiscal_position_change(self):
        lines_without_product = []
        if self.fiscal_position and self.order_line:
            fp_model = self.env['account.fiscal.position']
            for line in self.order_line:
                if line.product_id:
                    taxes = fp_model.map_tax(line.product_id.taxes_id)
                    line.tax_id = taxes
                else:
                    lines_without_product.append(line.name)
        if lines_without_product:
            res = {}
            res['warning'] = {'title': _('Warning')}
            res['warning']['message'] = _(
                "The following Sale Order Lines were not updated "
                "to the new Fiscal Position because they don't have a "
                "Product:\n - %s\nYou should update the "
                "Taxes of these Sale Order Lines manually."
            ) % ('\n- '.join(lines_without_product))
            return res
