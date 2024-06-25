from database_manager import DatabaseManager
from sql_validator import SQLValidator
import re

def process_command(command, db_manager):
    """Procesa un comando SQL del usuario."""
    try:
        if command.upper().startswith("CREATE USER"):
            username, password = parse_create_user_command(command)
            db_manager.create_user(username, password)
        else:
            command_type, db_name = SQLValidator.validate_sql(command)
            if command_type == "CREATE":
                db_manager.create_database(db_name)
            elif command_type == "DROP":
                db_manager.delete_database(db_name)
            else:
                print("Comando no reconocido. Intenta con:")
                print("  CREATE DATABASE {nombre}")
                print("  DROP DATABASE {nombre}")
    except SyntaxError as e:
        print(f"Error de sintaxis: {e}")
        db_manager._log(f"Error de sintaxis: {e}", is_error=True)

def parse_create_user_command(command):
    """Extrae el nombre de usuario y la contraseña del comando CREATE USER."""
    match = re.match(r"CREATE USER\s+'([^']+)'\@'localhost'\s+IDENTIFIED BY\s+'([^']+)'", command, re.IGNORECASE)
    if not match:
        raise SyntaxError(f"Error de sintaxis en el comando SQL: '{command}'. Uso esperado: CREATE USER 'username'@'localhost' IDENTIFIED BY 'password'.")
    username, password = match.groups()
    return username, password

def main():
    # Instancia del manejador de base de datos
    db_manager = DatabaseManager()

    print("Bienvenido al manejador de bases de datos.")
    
    # Solicitar autenticación
    authenticated = False
    while not authenticated:
        username = input("Nombre de usuario: ")
        password = input("Contraseña: ")
        authenticated = db_manager.verify_user(username, password)
        if not authenticated:
            print("Error de autenticación. Por favor, inténtalo de nuevo.")
    
    print(f"Usuario '{username}' autenticado correctamente.")
    print("Escribe tu comando (CREATE DATABASE {nombre}, DROP DATABASE {nombre}, CREATE USER 'username'@'localhost' IDENTIFIED BY 'password', LIST):")

    while True:
        command = input(">>> ")
        if command.strip().lower() == 'exit':
            print("Saliendo del manejador de bases de datos.")
            break
        elif command.strip().lower() == 'list':
            databases = db_manager.list_databases()
            print("Bases de datos disponibles:", databases)
        else:
            db_manager._log(f"Recibido: {command}")  # Registrar comandos antes de procesar
            process_command(command, db_manager)

if __name__ == "__main__":
    main()
