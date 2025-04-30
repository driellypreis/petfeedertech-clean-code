import unittest
from datetime import datetime, timedelta
from src.main import PetFeederTech

class TestPetFeederTech(unittest.TestCase):
    def setUp(self):
        self.feeder = PetFeederTech()

    def test_ligar_e_desligar_sistema(self):
        self.feeder.ligar()
        self.assertTrue(self.feeder.sistema_ativo)
        self.feeder.desligar()
        self.assertFalse(self.feeder.sistema_ativo)

    def test_alimentar_com_racao_suficiente(self):
        self.feeder.ligar()
        peso_inicial = self.feeder.sensor.medir_peso()
        self.feeder.alimentar()
        peso_final = self.feeder.sensor.medir_peso()
        self.assertEqual(peso_final, peso_inicial - 50)

    def test_nao_alimentar_com_pouca_racao(self):
        self.feeder.ligar()
        self.feeder.sensor.peso = 10  # Força pouca ração
        self.feeder.alimentar()
        self.assertEqual(self.feeder.sensor.medir_peso(), 10)  # Não deve liberar ração

    def test_agendar_alimentacao(self):
        self.feeder.ligar()
        horario = (datetime.now() + timedelta(minutes=1)).time()
        self.feeder.agendar_alimentacao(horario, diario=False)
        self.assertEqual(len(self.feeder.agendamentos), 1)

    def test_configurar_pet(self):
        self.feeder.configurar_pet(12.5, "Golden Retriever")
        self.assertEqual(self.feeder.peso_pet, 12.5)
        self.assertEqual(self.feeder.raca_pet, "Golden Retriever")

    def test_wifi_conectar_desconectar(self):
        self.feeder.conectar_wifi()
        self.assertTrue(self.feeder.wifi.conectado)
        self.feeder.desconectar_wifi()
        self.assertFalse(self.feeder.wifi.conectado)

    def test_verificar_peso(self):
        self.feeder.ligar()
        self.feeder.sensor.peso = 150
        self.feeder.verificar_peso()
        self.assertLess(self.feeder.sensor.medir_peso(), 200)  # Deve ativar alerta

if __name__ == "__main__":
    unittest.main()
