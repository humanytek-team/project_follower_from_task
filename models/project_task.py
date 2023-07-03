from odoo import _, api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def create(self, vals):
        task = super(ProjectTask, self).create(vals)
        task.sudo().message_follower_ids.unlink()
        return task

    def message_subscribe(self, partner_ids=None, subtype_ids=None, project=True):
        res = super(ProjectTask, self).message_subscribe(partner_ids, subtype_ids)
        if not project:
            for r in self:
                r.project_id.message_subscribe(
                    partner_ids=r.message_partner_ids.ids, subtype_ids=[1]
                )
        return res
