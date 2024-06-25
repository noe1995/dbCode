import os
import csv
import hashlib
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        # Definir rutas
        self.base_path = os.path.dirname(os.path.abspath(__file__))  # Ruta de `dbCode`
        self.databases_path = os.path.join(self.base_path, 'databases')
        self.binlog_path = os.path.join(self.base_path, 'logbin')
        self.binlog_file = os.path.join(self.binlog_path, 'logbin.txt')
        self.config_path = os.path.join(self.base_path, 'config')
        self.procedures_path = os.path.join(self.base_path, 'procedures')
        self.users_path = os.path.join(self.base_path, 'users')
        self.users_file = os.path.join(self.users_path, 'users.csv')
        self._setup_directories()

    def _setup_directories(self):
        """Configura las carpetas iniciales para bases de datos, log binario, configuración y procedimientos."""
        os.makedirs(self.databases_path, exist_ok=True)
        os.makedirs(self.binlog_path, exist_ok=True)
        os.makedirs(self.config_path, exist_ok=True)
        os.makedirs(self.procedures_path, exist_ok=True)
        os.makedirs(self.users_path, exist_ok=True)
        if not os.path.exists(self.binlog_file):
            with open(self.binlog_file, 'w') as f:
                f.write('')  # Crear archivo de log binario si no existe
        if not os.path.exists(self.users_file):
            # Crear el archivo CSV con encabezados
            with open(self.users_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['username', 'host', 'password'])  # Encabezados

    def _log(self, message, is_error=False):
        """Registra un mensaje en el archivo de log binario."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.binlog_file, 'a') as f:
            log_type = "ERROR" if is_error else "INFO"
            f.write(f"[{timestamp}] [{log_type}] {message}\n")

    def create_database(self, db_name):
        """Crea una nueva base de datos como una carpeta con subcarpetas internas."""
        db_path = os.path.join(self.databases_path, db_name)
        try:
            os.makedirs(db_path, exist_ok=False)
            # Crear subcarpetas internas
            os.makedirs(os.path.join(db_path, 'temp'))
            os.makedirs(os.path.join(db_path, 'cache'))
            os.makedirs(os.path.join(db_path, 'log'))
            self._log(f"CREATE DATABASE {db_name}")
            print(f"Base de datos '{db_name}' creada con subcarpetas en '{db_path}'")
        except FileExistsError:
            print(f"La base de datos '{db_name}' ya existe.")
            self._log(f"ERROR: La base de datos '{db_name}' ya existe.", is_error=True)

    def list_databases(self):
        """Lista todas las bases de datos existentes."""
        return [name for name in os.listdir(self.databases_path)
                if os.path.isdir(os.path.join(self.databases_path, name))]

    def delete_database(self, db_name):
        """Elimina una base de datos."""
        db_path = os.path.join(self.databases_path, db_name)
        try:
            for root, dirs, files in os.walk(db_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(db_path)
            self._log(f"DROP DATABASE {db_name}")
            print(f"Base de datos '{db_name}' eliminada.")
        except FileNotFoundError:
            print(f"La base de datos '{db_name}' no existe.")
            self._log(f"ERROR: La base de datos '{db_name}' no existe.", is_error=True)
        except OSError as e:
            print(f"Error al eliminar la base de datos '{db_name}': {e}")
            self._log(f"ERROR: {e}", is_error=True)

    def create_user(self, username, password):
        """Crea un nuevo usuario."""
        hashed_password = self._hash_password(password)
        user_info = [username, 'localhost', hashed_password]
        with open(self.users_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(user_info)
        self._log(f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}'")
        print(f"Usuario '{username}' creado con éxito.")

    def verify_user(self, username, password):
        """Verifica si el usuario y la contraseña son correctos."""
        hashed_password = self._hash_password(password)
        with open(self.users_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'username' in row and row['username'] == username:
                    if 'password' in row and row['password'] == hashed_password:
                        self._log(f"LOGIN SUCCESS: Usuario '{username}' ingresó correctamente.")
                        return True
                    else:
                        self._log(f"LOGIN ERROR: Contraseña incorrecta para el usuario '{username}'.", is_error=True)
                        return False
            self._log(f"LOGIN ERROR: Usuario '{username}' no definido.", is_error=True)
            return False

    def _hash_password(self, password):
        """Hashea la contraseña para almacenamiento."""
        return hashlib.sha256(password.encode()).hexdigest()
