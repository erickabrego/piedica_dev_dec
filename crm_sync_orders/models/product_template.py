from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Productos
    prod_production_type_id = fields.Many2one('prod.production.type', string='Production type')
    prod_shape_list_ids = fields.Many2many('prod.shape.list', string='Shape list')
    prod_prod_use_list_ids = fields.Many2many('prod.prod.use.list', string='Prod use list')
    prod_design_type = fields.Many2many('prod.design.type', string='Design Type')
    prod34 = fields.Boolean(string='3/4')
    prod_material_subtype_id = fields.Many2one('prod.material.subtype', string='Prod Material SubType')
    is_custom = fields.Boolean(string='¿Es custom?')

    # Materiales
    matSupplierName = fields.Char(string='Supplier Name')
    matSupplier = fields.Char(string='Supplier')
    matAlias = fields.Char(string='Alias')
    matName = fields.Char(string='Material Name')
    matMaterialType = fields.Many2one('mat.material.type', string='Material Type')
    matMaterialSubType = fields.Many2one('mat.material.subtype', string='Material SubType')
    matShoreA = fields.Many2one('mat.shore.a', string='Shore A')
    matHardness = fields.Many2one('mat.hardness', string='Hardness')
    matColor = fields.Many2many('mat.color', string='Color')
    matThickness = fields.Float(string='Thickness')
    matTopLayer = fields.Boolean(string='Top Layer')
    matMainLayer = fields.Boolean(string='Main Layer')
    matMidLayer = fields.Boolean(string='Mid Layer')
    is_material = fields.Boolean(string="¿Es material?")
