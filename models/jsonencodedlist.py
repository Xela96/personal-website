from sqlalchemy.types import Text
from sqlalchemy import TypeDecorator
import json

class JSONEncodedList(TypeDecorator):
    impl = Text
    def process_bind_param(self, value, dialect):
        return json.dumps(value) if value is not None else None
    def process_result_value(self, value, dialect):
        return json.loads(value) if value is not None else None