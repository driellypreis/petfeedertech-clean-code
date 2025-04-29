import unittest
from datetime import datetime, timedelta
from src import PetFeederTech

class TestPetFeederTech(unittest.TestCase):
  def setup(self):
    self.feeder = PetFeederTech()
  def test_ligar_sistema(self):
    self.feeder.ligar()
    self.assertTrue(self.feeder.sistema_ativo)
  def test_desligar_sistema(self):
    self.feeder.ligar()
    self.feeder.desligar()
    self.assertFalse(self.feeder.sistema_ativo)
  def test_alimentar_com_ração(self):
    self.feeder.ligar()
    peso_antes = self.feeder.sensor.medir.pesp()
    self.feeder.alimentar()
    peso_depois = self.feeder.sensor.medir_peso()
    self.assertLess(peso_depois, peso_antes)
  def test_não_alimentar_sem_ração(self):
    self.feeder.ligar()
    self.feeder.sensor.peso = 0
    self.feeder.alimentar()
    self.assertEqual(self.feeder.sensor.medir_peso(), 0)
  def test_agendar_alimentacao(self):
    self.feeder.ligar()
    horario = datetime.now() + timedelta(minutes=1)
    self.feeder.agendar_alimentacao(horario)
    self.assertEqual(len(self.feeder.agendamentos), 1)
  def test_conectar_wifi(self):
    self.feeder.conectar_wifi()
    self.assertTrue(self.feeder.wifi.conectado)
  def test_desconectar_wifi(self):
    self.feeder.conectar_wifi()
    self.feeder.desconectar_wifi()
    self.assertFalse(self.feeder.wifi.conectado)

if __name__ == '__main__':
    unittest.main() 
