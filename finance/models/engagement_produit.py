from odoo import fields, models, api


class EngagementProduit(models.Model):
    _name = 'finance.engagement_produit'
    # _description = 'Description'
    _sql_constraints = [
        ('unique_BC_Prod', 'unique (bon_com_id,produit_id)',
         'vous ne pouvez pas réutiliser le même produit dans le même engagement')
    ]

    id = fields.Id('ID')
    # -------------------------------------Relations------------------------------------------------
    bon_com_id = fields.Many2one('finance.bon.commande', string='Engagement')
    produit_id = fields.Many2one('finance.produit', string='Product')
    # ----------------------------------------------------------------------------------------------

    quantity = fields.Integer(string='Quantite Acheter', default=1)

    # -------------------------------------Computed------------------------------------------------
    product_uni_price = fields.Float(compute="_get_product_price", store=False)
    product_total_price = fields.Float(compute="_get_total_price", store=False)
    product_fournisseur = fields.Char(compute="_get_prod_fourni", store=False)
    product_designation = fields.Char(compute="_get_product_name", store=False)
    product_code = fields.Integer(compute="_get_product_code", store=False)
    freeze_qte = fields.Boolean(compute='_freeze_qte')
    type = fields.Char(string="Type", compute="_get_type")

    # ---------------------------------------------------------------------------------------------

    @api.depends('produit_id.prix')
    def _get_product_price(self):
        for o in self:
            o.product_uni_price = o.produit_id.prix if o.produit_id else 0.0

    @api.depends('produit_id.type')
    def _get_type(self):
        for o in self:
            o.type = o.produit_id.type if o.produit_id else ''

    @api.depends('produit_id.fournisseur_id.name')
    def _get_prod_fourni(self):
        for o in self:
            o.product_fournisseur = o.produit_id.fournisseur_id.name if o.produit_id.fournisseur_id else ""

    @api.depends('produit_id.prix', 'quantity')
    def _get_total_price(self):
        for o in self:
            o.product_total_price = (o.produit_id.prix * o.quantity) if o.produit_id and o.quantity else 0.0

    @api.depends('produit_id')
    def _get_product_name(self):
        for o in self:
            o.product_designation = o.produit_id.name

    @api.depends('produit_id')
    def _get_product_code(self):
        for o in self:
            o.produit_id = o.produit_id.id

    @api.depends('produit_id.type')
    def _freeze_qte(self):
        for obj in self:
            if obj.produit_id.type == 'produit':
                obj.freeze_qte = False
            else:
                obj.quantity = 1
                obj.freeze_qte = True
