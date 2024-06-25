import sqlparse
from sqlparse.sql import Statement
from sqlparse.tokens import Keyword

class SQLValidator:
    @staticmethod
    def validate_sql(query):
        """Valida la sintaxis SQL y retorna el tipo de comando y argumentos si es válido."""
        # Remover espacios en blanco y punto y coma final
        query = query.strip().rstrip(';')
        parsed = sqlparse.parse(query)
        if not parsed or not isinstance(parsed[0], Statement):
            raise SyntaxError(f"Error de sintaxis en el comando SQL: '{query}'.")

        statement = parsed[0]
        command_type = None
        command_args = []

        for token in statement.tokens:
            if token.ttype == Keyword.DDL:
                command_type = token.value.upper()
            elif token.ttype is None and token.value.strip().upper() == "DATABASE":
                # Asegura que "DATABASE" es parte del comando
                continue
            elif token.ttype is None and not token.is_whitespace:
                # Argumentos del comando
                command_args.append(token.value)

        if command_type not in ("CREATE", "DROP"):
            raise SyntaxError(f"Comando '{command_type}' no soportado en el comando: '{query}'.")

        if len(command_args) != 1:
            raise SyntaxError(f"Error de sintaxis en el uso de '{command_type}'. Uso esperado: {command_type} DATABASE {{nombre}}. Comando: '{query}'.")

        db_name = command_args[0]
        return command_type, db_name
