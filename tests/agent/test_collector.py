import unittest
import os
import sys
import json
from unittest.mock import patch, MagicMock

# Añadir directorio padre a la ruta para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from agent.collector import get_cpu_info, get_process_list, get_logged_users, get_os_info, collect_all

class TestCollector(unittest.TestCase):
    
    @patch('agent.collector.psutil.cpu_percent')
    @patch('agent.collector.psutil.cpu_count')
    def test_get_cpu_info(self, mock_cpu_count, mock_cpu_percent):
        # Configurar mocks
        mock_cpu_percent.side_effect = [[5.0, 6.0, 7.0, 8.0], 25.0]  # First call for per-cpu, second for avg
        mock_cpu_count.side_effect = [4, 8]  # Physical and logical
        
        # Llamar a la función
        result = get_cpu_info()
        
        # Verificar resultados
        self.assertEqual(result['physical_cores'], 4)
        self.assertEqual(result['logical_cores'], 8)
        self.assertEqual(result['avg_usage'], 25.0)
        self.assertEqual(len(result['usage_percent']), 4)
    
    @patch('agent.collector.psutil.process_iter')
    def test_get_process_list(self, mock_process_iter):
        # Crear diccionarios de procesos simulados
        process1 = {
            'pid': 1,
            'name': 'test_process1',
            'username': 'user1',
            'memory_percent': 5.2,
            'cpu_percent': 10.5
        }
        
        process2 = {
            'pid': 2,
            'name': 'test_process2',
            'username': 'user2',
            'memory_percent': None,  # Probar el manejo de valores None
            'cpu_percent': None
        }
        
        # Crear procesos simulados
        mock_proc1 = MagicMock()
        mock_proc1.as_dict.return_value = process1
        mock_proc1.__getitem__ = lambda self, key: process1[key]
        mock_proc1.get = lambda key, default=None: process1.get(key, default)
        
        mock_proc2 = MagicMock()
        mock_proc2.as_dict.return_value = process2
        mock_proc2.__getitem__ = lambda self, key: process2[key]
        mock_proc2.get = lambda key, default=None: process2.get(key, default)
        
        # Configurar mock para devolver nuestros procesos de prueba
        mock_process_iter.return_value = [mock_proc1, mock_proc2]
        
        # Llamar a la función
        result = get_process_list()
        
        # Verificar resultados
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['pid'], 1)
        self.assertEqual(result[0]['name'], 'test_process1')
        self.assertEqual(result[0]['username'], 'user1')
        self.assertEqual(result[0]['memory_percent'], 5.2)
        self.assertEqual(result[0]['cpu_percent'], 10.5)
        
        # Verificar que los valores None se manejen correctamente
        self.assertEqual(result[1]['memory_percent'], 0)
        self.assertEqual(result[1]['cpu_percent'], 0)
    
    @patch('agent.collector.psutil.users')
    @patch('agent.collector.datetime.datetime')
    def test_get_logged_users(self, mock_datetime, mock_users):
        # Configurar mock de datetime
        mock_date = MagicMock()
        mock_date.strftime.return_value = '2025-06-27 12:00:00'
        mock_datetime.fromtimestamp.return_value = mock_date
        
        # Configurar usuarios simulados
        mock_user1 = MagicMock()
        mock_user1.name = 'user1'
        mock_user1.terminal = 'tty1'
        mock_user1.host = 'host1'
        mock_user1.started = 1234567890
        
        mock_user2 = MagicMock()
        mock_user2.name = 'user2'
        mock_user2.terminal = 'pts/0'
        mock_user2.host = 'host2'
        mock_user2.started = 1234567891
        
        mock_users.return_value = [mock_user1, mock_user2]
        
        # Call function
        result = get_logged_users()
        
        # Verify results
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'user1')
        self.assertEqual(result[0]['terminal'], 'tty1')
        self.assertEqual(result[0]['host'], 'host1')
        self.assertEqual(result[0]['started'], '2025-06-27 12:00:00')
        self.assertEqual(result[1]['name'], 'user2')
    
    @patch('agent.collector.platform.system')
    @patch('agent.collector.platform.release')
    @patch('agent.collector.platform.version')
    @patch('agent.collector.platform.machine')
    @patch('agent.collector.platform.processor')
    def test_get_os_info(self, mock_processor, mock_machine, mock_version, mock_release, mock_system):
        # Configurar mocks
        mock_system.return_value = 'Linux'
        mock_release.return_value = '5.4.0'
        mock_version.return_value = 'Ubuntu 20.04.1'
        mock_machine.return_value = 'x86_64'
        mock_processor.return_value = 'Intel Core i7'
        
        # Llamar función
        result = get_os_info()
        
        # Verificar resultados
        self.assertEqual(result['name'], 'Linux')
        self.assertEqual(result['release'], '5.4.0')
        self.assertEqual(result['version'], 'Ubuntu 20.04.1')
        self.assertEqual(result['machine'], 'x86_64')
        self.assertEqual(result['processor'], 'Intel Core i7')
    
    @patch('agent.collector.get_cpu_info')
    @patch('agent.collector.get_process_list')
    @patch('agent.collector.get_logged_users')
    @patch('agent.collector.get_os_info')
    @patch('agent.collector.socket.gethostname')
    @patch('agent.collector.socket.gethostbyname')
    @patch('agent.collector.datetime.datetime')
    def test_collect_all(self, mock_datetime, mock_gethostbyname, mock_gethostname, 
                        mock_get_os_info, mock_get_logged_users, mock_get_process_list, 
                        mock_get_cpu_info):
        # Configurar mocks
        mock_datetime_now = MagicMock()
        mock_datetime_now.strftime.return_value = '2025-06-27 12:00:00'
        mock_datetime.now.return_value = mock_datetime_now
        
        mock_get_cpu_info.return_value = {'physical_cores': 4, 'logical_cores': 8, 'avg_usage': 25.0}
        mock_get_process_list.return_value = [{'pid': 1, 'name': 'test_process'}]
        mock_get_logged_users.return_value = [{'name': 'test_user'}]
        mock_get_os_info.return_value = {'name': 'Linux', 'version': '1.0'}
        mock_gethostname.return_value = 'test-host'
        mock_gethostbyname.return_value = '192.168.1.1'
        # Simular la conexión socket para obtener la IP local
        mock_socket = MagicMock()
        mock_socket.getsockname.return_value = ('192.168.1.1', 12345)
        mock_socket_patcher = patch('agent.collector.socket.socket', return_value=mock_socket)        
        mock_socket_patcher.start()
        self.addCleanup(mock_socket_patcher.stop)
        
        # Llamar función
        result = collect_all()
        
        # Verificar resultados
        self.assertEqual(result['ip_address'], '192.168.1.1')
        self.assertEqual(result['hostname'], 'test-host')
        self.assertEqual(result['cpu_info']['physical_cores'], 4)
        self.assertEqual(len(result['processes']), 1)
        self.assertEqual(len(result['logged_users']), 1)
        self.assertEqual(result['os_info']['name'], 'Linux')
        self.assertEqual(result['timestamp'], '2025-06-27 12:00:00')

if __name__ == '__main__':
    unittest.main()
