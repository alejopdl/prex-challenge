import unittest
import os
import sys
import json
import shutil
import tempfile
from datetime import datetime

# Añadir directorio padre a la ruta para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from api_server.storage import JSONStorage

class TestJSONStorage(unittest.TestCase):
    
    def setUp(self):
        # Crear un directorio temporal para pruebas
        self.test_data_dir = tempfile.mkdtemp()
        self.storage = JSONStorage(self.test_data_dir)
        
        # Datos de prueba de ejemplo
        self.test_ip = '192.168.1.100'
        self.test_date = datetime.now().strftime('%Y-%m-%d')
        self.test_data = {
            'ip_address': self.test_ip,
            'timestamp': datetime.now().isoformat(),
            'cpu': {'cores': 4, 'usage_percent': 25.0, 'frequency_mhz': 2500},
            'processes': [
                {'pid': 1, 'name': 'process1', 'username': 'user1', 'memory_percent': 5.2, 'cpu_percent': 10.5},
                {'pid': 2, 'name': 'process2', 'username': 'user2', 'memory_percent': 3.1, 'cpu_percent': 5.0}
            ],
            'users': [
                {'username': 'user1', 'terminal': 'tty1', 'host': 'host1', 'login_time': 1234567890}
            ],
            'os': {'name': 'Linux', 'release': '5.4.0', 'version': 'Ubuntu 20.04', 'architecture': 'x86_64'}
        }
    
    def tearDown(self):
        # Eliminar el directorio temporal después de las pruebas
        shutil.rmtree(self.test_data_dir)
    
    def test_store_data(self):
        # Almacenar datos de prueba
        result = self.storage.store_data(self.test_data)
        
        # Verificar resultado
        self.assertTrue(result['success'])
        
        # Verificar que el archivo fue creado
        expected_filename = f"{self.test_ip}_{self.test_date}.json"
        expected_path = os.path.join(self.test_data_dir, expected_filename)
        self.assertTrue(os.path.exists(expected_path))
        
        # Verificar contenido del archivo
        with open(expected_path, 'r') as f:
            stored_data = json.load(f)
            self.assertEqual(stored_data[0]['ip_address'], self.test_ip)
            self.assertEqual(len(stored_data[0]['processes']), 2)
            self.assertEqual(stored_data[0]['cpu']['cores'], 4)
    
    def test_query_data_by_ip(self):
        # Primero almacenar datos de prueba
        self.storage.store_data(self.test_data)
        
        # Consultar datos para la IP
        result = self.storage.query_data(self.test_ip)
        
        # Verificar resultado
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['data'])
        self.assertEqual(len(result['data']), 1)  # Debería tener una entrada
        self.assertEqual(result['data'][0]['ip_address'], self.test_ip)
        self.assertEqual(result['data'][0]['cpu']['cores'], 4)
    
    def test_query_data_by_ip_and_date(self):
        # Primero almacenar datos de prueba
        self.storage.store_data(self.test_data)
        
        # Consultar datos para la IP y fecha
        result = self.storage.query_data(self.test_ip, self.test_date)
        
        # Verificar resultado
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['data'])
        self.assertEqual(len(result['data']), 1)  # Debería tener una entrada
        self.assertEqual(result['data'][0]['ip_address'], self.test_ip)
    
    def test_query_nonexistent_ip(self):
        # Consultar datos para una IP inexistente
        result = self.storage.query_data('10.0.0.1')
        
        # Verify result indicates failure
        self.assertFalse(result['success'])
        self.assertIsNone(result['data'])
    
    def test_query_nonexistent_date(self):
        # Primero almacenar datos de prueba
        self.storage.store_data(self.test_data)
        
        # Consultar datos para una fecha inexistente
        result = self.storage.query_data(self.test_ip, '2000-01-01')
        
        # Verify result indicates failure
        self.assertFalse(result['success'])
        self.assertIsNone(result['data'])
    
    def test_list_available_data(self):
        # Primero almacenar datos de prueba
        self.storage.store_data(self.test_data)
        
        # Almacenar otro conjunto de datos con una IP diferente
        test_data2 = self.test_data.copy()
        test_data2['ip_address'] = '10.0.0.1'
        self.storage.store_data(test_data2)
        
        # Listar datos disponibles
        result = self.storage.list_available_data()
        
        # Verificar resultado
        self.assertTrue(result['success'])
        self.assertEqual(len(result['available_data']), 2)  # Debería tener dos entradas
        filenames = [item['filename'] for item in result['available_data']]
        self.assertIn(f"{self.test_ip}_{self.test_date}.json", filenames)
        self.assertIn(f"10.0.0.1_{self.test_date}.json", filenames)

if __name__ == '__main__':
    unittest.main()
