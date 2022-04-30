import unittest
import kali_boots

kali = kali_boots.KALI('192.168.1.186', 'kali', 'kali')

class TestSSHConnection(unittest.TestCase):

	def test_ssh_commands(self):
		result = kali.ssh_command(command='df')
		self.assertIsNot(result, '')
		
		result = kali.ssh_command(command='whoami')
		self.assertIn('kali', result)

		result = kali.ssh_command(command='sudo whoami')
		self.assertIn('root', result)
		
if __name__ == '__main__':
	unittest.main()
		

