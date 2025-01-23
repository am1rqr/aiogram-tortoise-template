from tortoise import Model, fields

from database.enums import UserStatus


class TimedModel(Model):
    updated_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Users(TimedModel):
    user_id = fields.BigIntField(primary_key=True)
    username = fields.CharField(max_length=32, null=True)
    first_name = fields.CharField(max_length=64)
    note = fields.TextField(null=True)
    language_code = fields.CharField(max_length=8)
    last_activity = fields.DatetimeField(null=True)
    status = fields.CharField(max_length=6, default=UserStatus.ACTIVE.value)