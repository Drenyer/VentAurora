import firebase_admin
from firebase_admin import credentials, db

class FirebaseDB:
    def __init__(self, credential_path, database_url):
        # Inicializar cuenta en firebase con certicaciones.
        cred = credentials.Certificate(credential_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })

    def write_record(self, path, data):
        """ Escribe datos en la base de datos en tiempo real en la ruta especificada.
        Args:
        - path (str): Ruta en la que se escribirán los datos.
        - data (dict): Datos a escribir.
        """
        ref = db.reference(path)
        ref.set(data)

    def read_record(self, path):
        """ Lee datos desde la base de datos en tiempo real en la ruta especificada.
        Args:
        - path (str): Ruta desde la que se leerán los datos.
        Returns:
        - dict: Datos leídos desde la base de datos.
        """
        ref = db.reference(path)
        return ref.get()

    def update_record(self, path, data):
        """ Actualiza datos en la base de datos en tiempo real en la ruta especificada.
        Args:
        - path (str): Ruta en la que se actualizarán los datos.
        - data (dict): Datos actualizados.
        """
        ref = db.reference(path)
        ref.update(data)

    def delete_record(self, path):
        """ Elimina datos de la base de datos en tiempo real en la ruta especificada.
        Args:
        - path (str): Ruta de la que se eliminarán los datos.
        """
        ref = db.reference(path)
        ref.delete()

