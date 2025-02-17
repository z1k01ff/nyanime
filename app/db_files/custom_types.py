from sqlalchemy.types import UserDefinedType


def get_col_spec():
    return "XMLTYPE"


class XMLType(UserDefinedType):
    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value

        return process
