from odoo import _, api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def create(self, vals):
        # Crear la tarea usando super y luego eliminar seguidores
        task = super(ProjectTask, self).create(vals)
        task.sudo().message_follower_ids.unlink()
        return task

    def message_subscribe(self, partner_ids=None, subtype_ids=None):
        # Revisar si estamos en una recursion infinita para evitar bucles
        prev_inf_recursion = self.env.context.get("inf_recursion", False)
        # Ejecutar la lógica original de suscripción a mensajes
        res = super(ProjectTask, self).message_subscribe(partner_ids, subtype_ids)
        if not prev_inf_recursion:
            self_ctx = self.with_context(inf_recursion=True)
            for r in self_ctx:
                r.project_id.message_subscribe(
                    partner_ids=r.message_partner_ids.ids, subtype_ids=[1]
                )
        return res
