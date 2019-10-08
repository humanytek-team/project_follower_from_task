from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'
   
    @api.model
    def create(self, vals):
        task = super(ProjectTask, self).create(vals)
        task.sudo().message_follower_ids.unlink()
        return task

    @api.multi
    def message_subscribe(self, partner_ids=None, channel_ids=None, subtype_ids=None):
        res = super(ProjectTask, self).message_subscribe(partner_ids, channel_ids, subtype_ids)
        for r in self:
            r.project_id.message_subscribe(partner_ids=r.message_partner_ids.ids, subtype_ids=[1])
        return res
