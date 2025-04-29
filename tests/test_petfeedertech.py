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
