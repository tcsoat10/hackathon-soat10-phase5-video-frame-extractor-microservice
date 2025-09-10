import datetime
from typing import TypeVar, Generic
from mongoengine import Document, DateTimeField, ObjectIdField
from bson import ObjectId

M = TypeVar("M", bound="BaseModel")

class BaseModel(Document, Generic[M]):

    meta = {'abstract': True}

    id = ObjectIdField(primary_key=True, default=ObjectId)

    created_at = DateTimeField(default=datetime.datetime.now, required=True)

    updated_at = DateTimeField(default=datetime.datetime.now, required=True)

    inactivated_at = DateTimeField(required=False)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now(datetime.UTC)
        return super().save(*args, **kwargs)

__all__ = ["BaseModel"]
