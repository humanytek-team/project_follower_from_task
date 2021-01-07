from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def create(self, vals):
        task = super(ProjectTask, self).create(vals)
        task.sudo().message_follower_ids.unlink()
        return task

    def message_subscribe(self, partner_ids=None, channel_ids=None, subtype_ids=None):
        res = super(ProjectTask, self).message_subscribe(partner_ids, channel_ids, subtype_ids)
        for r in self:
            current_followers = (
                self.env["mail.followers"]
                .sudo()
                .search(
                    [
                        ("res_model", "=", r.project_id._name),
                        ("res_id", "in", r.project_id.id),
                        "|",
                        ("partner_id", "in", partner_ids or []),
                        ("channel_id", "in", channel_ids or []),
                    ]
                )
            )
            partners_to_suscribe = r.message_partner_ids - current_followers
            if partners_to_suscribe:
                r.project_id.message_subscribe(
                    partner_ids=partners_to_suscribe.ids, subtype_ids=[1]
                )
        return res
