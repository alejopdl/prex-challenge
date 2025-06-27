import unittest
import os
import sys
import json
import shutil
import tempfile
from unittest.mock import patch, MagicMock

# Añadir directorio padre a la ruta para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from api_server.app import app

class TestAPIApp(unittest.TestCase):
    
    def setUp(self):
        # Crear un cliente de prueba
        self.app = app.test_client()
        self.app.testing = True
        
        # Crear un directorio temporal para pruebas
        self.test_data_dir = tempfile.mkdtemp()
        # Parchear la instancia de almacenamiento en el módulo de la aplicación
        self.storage_mock = MagicMock()
        self.patcher = patch('api_server.app.storage', self.storage_mock)
        self.patcher.start()
        
        # Datos de prueba de ejemplo
        self.test_data = {
            'ip_address': '192.168.1.100',
            'hostname': 'test-host',
            'timestamp': '2025-06-27T10:00:00',
            'cpu': {'cores': 4, 'usage_percent': 25.0, 'frequency_mhz': 2500},
            'processes': [
                {'pid': 1, 'name': 'process1', 'username': 'user1', 'memory_percent': 5.2, 'cpu_percent': 10.5},
                {'pid': 2, 'name': 'process2', 'username': 'user2', 'memory_percent': 3.1, 'cpu_percent': 5.0}
            ],
            'logged_users': [
                {'name': 'user1', 'terminal': 'tty1', 'host': 'host1', 'started': '2025-06-27 12:00:00'}
            ],
            'os': {'name': 'Linux', 'release': '5.4.0', 'version': 'Ubuntu 20.04', 'architecture': 'x86_64'}
        }
    
    def tearDown(self):
        # Eliminar el directorio temporal después de las pruebas
        self.patcher.stop()
        shutil.rmtree(self.test_data_dir)
    
    def test_root_endpoint(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('name', data)
        self.assertIn('version', data)
        self.assertIn('endpoints', data)
    
    def test_health_endpoint(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
    
    def test_upload_endpoint_success(self):
        # Configurar mock de almacenamiento para devolver éxito
        self.storage_mock.store_data.return_value = {
            'success': True,
            'message': 'Data stored successfully',
            'file_path': os.path.join(self.test_data_dir, f"{self.test_data['ip_address']}_2025-06-27.json")
        }
        
        # Test POST to /upload
        response = self.app.post('/upload', 
                                json=self.test_data,
                                content_type='application/json')
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Verificar que el mock fue llamado con los datos correctos
        self.storage_mock.store_data.assert_called_once_with(self.test_data)
    
    def test_upload_endpoint_failure(self):
        # Configurar mock de almacenamiento para devolver fallo
        self.storage_mock.store_data.return_value = {
            'success': False,
            'message': 'Error storing data',
            'file_path': None
        }
        
        # Test POST to /upload
        response = self.app.post('/upload', 
                                json=self.test_data,
                                content_type='application/json')
        
        # Verify response
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_upload_endpoint_invalid_data(self):
        # Probar con datos inválidos (campos requeridos faltantes)
        invalid_data = {'ip_address': '192.168.1.1'}  # Faltan hostname y timestamp
        
        # Test POST to /upload
        response = self.app.post('/upload', 
                                json=invalid_data,
                                content_type='application/json')
        
        # Verify response
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_query_endpoint_with_ip(self):
        # Configurar mock para devolver datos de prueba
        self.storage_mock.query_data.return_value = {
            'success': True,
            'message': 'Data retrieved successfully',
            'data': [self.test_data]
        }
        
        # Probar GET a /query con parámetro IP
        response = self.app.get('/query?ip=192.168.1.100')
        
        # Verificar respuesta
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['ip_address'], '192.168.1.100')
        
        # Verificar que el mock fue llamado con los parámetros correctos
        self.storage_mock.query_data.assert_called_once_with('192.168.1.100', None)
    
    def test_query_endpoint_with_ip_and_date(self):
        # Configurar mock para devolver datos de prueba
        self.storage_mock.query_data.return_value = {
            'success': True,
            'message': 'Data retrieved successfully',
            'data': [self.test_data]
        }
        
        # Probar GET a /query con parámetros IP y fecha
        response = self.app.get('/query?ip=192.168.1.100&date=2025-06-27')
        
        self.storage_mock.query_data.assert_called_once_with('192.168.1.100', '2025-06-27')
    
    def test_query_endpoint_no_ip(self):
        # Probar GET a /query sin parámetro IP (debería devolver 400)
        response = self.app.get('/query')
        
        # Verify response
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
{{ ... }}
        self.assertIn('IP address is required', data['message'])
    
    def test_list_endpoint(self):
        # Configurar mock para devolver datos de prueba
        self.storage_mock.list_available_data.return_value = {
            'success': True,
            'message': 'Found 2 data files',
            'available_data': [
                {'ip_address': '192.168.1.100', 'date': '2025-06-27', 'filename': '192.168.1.100_2025-06-27.json'},
                {'ip_address': '10.0.0.1', 'date': '2025-06-27', 'filename': '10.0.0.1_2025-06-27.json'}
            ]
        }
        
        # Probar GET a /list
        response = self.app.get('/list')
        
        # Verificar respuesta
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['available_data']), 2)
        self.assertEqual(data['available_data'][0]['ip_address'], '192.168.1.100')
        
        # Verificar que el mock fue llamado
        self.storage_mock.list_available_data.assert_called_once()

if __name__ == '__main__':
    unittest.main()
