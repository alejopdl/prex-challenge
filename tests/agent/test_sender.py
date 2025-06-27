import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock

# Añadir directorio padre a la ruta para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from agent.sender import APISender

class TestSender(unittest.TestCase):
    
    @patch('agent.sender.requests.post')
    def test_send_data_success(self, mock_post):
        # Configurar respuesta simulada para caso de éxito
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'ok'}
        mock_post.return_value = mock_response
        
        # Datos de prueba
        test_data = {'cpu_info': {'physical_cores': 4}, 'ip_address': '192.168.1.1'}
        test_url = 'http://test-api.com'
        
        # Crear instancia del sender
        sender = APISender(test_url)
        
        # Llamar al método
        result = sender.send_data(test_data)
        
        # Verificar resultados
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Data sent successfully')
        mock_post.assert_called_once_with(f'{test_url}/upload', data=json.dumps(test_data), headers={'Content-Type': 'application/json'})
    
    @patch('agent.sender.requests.post')
    def test_send_data_failure(self, mock_post):
        # Configurar respuesta simulada para caso de fallo
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = 'Internal Server Error'
        mock_post.return_value = mock_response
        
        # Datos de prueba
        test_data = {'cpu_info': {'physical_cores': 4}, 'ip_address': '192.168.1.1'}
        test_url = 'http://test-api.com'
        
        # Crear instancia del sender
        sender = APISender(test_url)
        
        # Llamar al método
        result = sender.send_data(test_data)
        
        # Verificar resultados
        self.assertFalse(result['success'])
        self.assertIn('HTTP 500', result['message'])
    
    @patch('agent.sender.requests.post')
    def test_send_data_exception(self, mock_post):
        # Configurar mock para lanzar una excepción
        mock_post.side_effect = Exception("Connection error")
        
        # Datos de prueba
        test_data = {'cpu_info': {'physical_cores': 4}, 'ip_address': '192.168.1.1'}
        test_url = 'http://test-api.com'
        
        # Crear instancia del sender
        sender = APISender(test_url)
        
        # Llamar al método
        result = sender.send_data(test_data)
        
        # Verificar resultados  
        self.assertFalse(result['success'])
        self.assertIn('Error', result['message'])
        self.assertIsNone(result['response'])

if __name__ == '__main__':
    unittest.main()
