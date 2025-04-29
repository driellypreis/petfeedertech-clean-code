import tkinter as tk
from datetime import datetime
import random

# -------------------- COMPONENTES AUXILIARES --------------------

class Display:
    def __init__(self, update_status_callback=None):
        self.update_status_callback = update_status_callback

    def show_message(self, message: str) -> None:
        if self.update_status_callback:
            self.update_status_callback(message)
        else:
            print(f"[Display]: {message}")

class SensorDePeso:
    def __init__(self):
        self.peso = 1000  # gramas iniciais

    def medir_peso(self) -> int:
        return self.peso

    def consumir_peso(self, quantidade):
        self.peso = max(self.peso - quantidade, 0)

class Motor:
    def liberar_racao(self) -> None:
        print("[Motor]: Ração liberada!")

class RTC:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RTC, cls).__new__(cls)
        return cls._instance

    def agora(self) -> datetime:
        return datetime.now()

class Buzzer:
    def alertar(self) -> None:
        print("[Buzzer]: BEEP BEEP - Reabastecer ração!")

class ModuloWiFi:
    def __init__(self):
        self.conectado = False

    def conectar(self):
        self.conectado = True

    def desconectar(self):
        self.conectado = False

    def enviar_notificacao(self, mensagem: str) -> None:
        if self.conectado:
            print(f"[WiFi]: {mensagem}")

# -------------------- CLASSE PRINCIPAL --------------------

class PetFeederTech:
    def __init__(self, update_status_callback=None):
        self.display = Display(update_status_callback)
        self.sensor = SensorDePeso()
        self.motor = Motor()
        self.rtc = RTC()
        self.buzzer = Buzzer()
        self.wifi = ModuloWiFi()
        self.sistema_ativo = False
        self.agendamentos = []
        self.historico_alimentacao = []
        self.peso_pet = 0
        self.raca_pet = ""
        self.alerta_callback = None

    def ligar(self):
        self.sistema_ativo = True
        self.display.show_message("Sistema ligado!")

    def desligar(self):
        self.sistema_ativo = False
        self.display.show_message("Sistema desligado!")

    def alimentar(self):
        if self.sistema_ativo:
            peso_atual = self.sensor.medir_peso()
            if peso_atual > 50:
                self.motor.liberar_racao()
                self.sensor.consumir_peso(50)
                self.historico_alimentacao.append(f"{datetime.now().strftime('%d/%m %H:%M:%S')} - Ração liberada")
                self.display.show_message("Ração liberada!")
            else:
                self.buzzer.alertar()
                if self.wifi.conectado and self.alerta_callback:
                    self.alerta_callback("Nível de ração crítico!")
                self.display.show_message("Sem ração suficiente para alimentar!")
        else:
            self.display.show_message("Sistema desligado. Não é possível alimentar.")

    def verificar_peso(self):
        if not self.sistema_ativo:
            return
        peso = self.sensor.medir_peso()
        self.display.show_message(f"Peso atual: {peso}g")
        if peso < 200:
            self.buzzer.alertar()
            if self.wifi.conectado and self.alerta_callback:
                self.alerta_callback("Nível de ração baixo!")

    def agendar_alimentacao(self, horario, diario=False):
        if not self.sistema_ativo:
            return
        self.agendamentos.append((horario, diario))
        freq = "Todos os Dias" if diario else "Hoje"
        self.display.show_message(f"Agendado para {horario.strftime('%H:%M')} | Frequência: {freq}")

    def checar_agendamentos(self):
        if not self.sistema_ativo:
            return
        agora = self.rtc.agora()
        for agendamento in self.agendamentos.copy():
            horario, diario = agendamento
            if agora.hour == horario.hour and agora.minute == horario.minute and agora.second == 0:
                self.alimentar()
                if not diario:
                    self.agendamentos.remove(agendamento)

    def configurar_pet(self, peso, raca):
        self.peso_pet = peso
        self.raca_pet = raca
        self.display.show_message(f"Pet configurado: {raca} com {peso}kg")

    def conectar_wifi(self):
        self.wifi.conectar()
        self.display.show_message("Wi-Fi conectado!")

    def desconectar_wifi(self):
        self.wifi.desconectar()
        self.display.show_message("Wi-Fi desconectado!")

    def set_alerta_callback(self, callback):
        self.alerta_callback = callback
# -------------------- INTERFACE DO CELULAR --------------------

class AppCelular:
    def __init__(self, parent, feeder: PetFeederTech):
        self.feeder = feeder
        self.window = tk.Toplevel(parent)
        self.window.title("PetFeeder App")
        self.window.geometry("320x600")
        self.window.configure(bg="white")

        tk.Label(self.window, text="PetFeeder App", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        self.label_status = tk.Label(self.window, text="Wi-Fi: Desconectado", font=("Arial", 12), bg="white")
        self.label_status.pack(pady=5)

        self.alerta_text = tk.Text(self.window, height=10, width=30)
        self.alerta_text.pack(pady=5)

        self.botao_wifi = tk.Button(self.window, text="Conectar Wi-Fi", command=self.toggle_wifi, font=("Arial", 12))
        self.botao_wifi.pack(pady=5)

        self.btn_alimentar = tk.Button(self.window, text="Alimentar Agora", command=self.feeder.alimentar, font=("Arial", 12))
        self.btn_verificar = tk.Button(self.window, text="Verificar Peso", command=self.feeder.verificar_peso, font=("Arial", 12))

    def toggle_wifi(self):
        if self.feeder.wifi.conectado:
            self.feeder.desconectar_wifi()
            self.label_status.config(text="Wi-Fi: Desconectado")
            self.botao_wifi.config(text="Conectar Wi-Fi")
            self.btn_alimentar.pack_forget()
            self.btn_verificar.pack_forget()
        else:
            self.feeder.conectar_wifi()
            self.label_status.config(text="Wi-Fi: Conectado")
            self.botao_wifi.config(text="Desconectar Wi-Fi")
            self.btn_alimentar.pack(pady=5)
            self.btn_verificar.pack(pady=5)

    def receber_alerta(self, mensagem):
        self.alerta_text.insert(tk.END, f"{mensagem}\n")
        self.alerta_text.see(tk.END)

# -------------------- INTERFACE DO DISPOSITIVO --------------------

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("PetFeederTech")
        self.feeder = PetFeederTech(self.update_status)

        self.root.geometry("400x650")
        self.frame_display = tk.Frame(root, bg="#e0e0e0", bd=2, relief="groove")
        self.frame_display.pack(pady=10, padx=10, fill="both", expand=True)

        self.label_titulo = tk.Label(self.frame_display, text="PetFeederTech", font=("Arial", 20, "bold"), bg="#e0e0e0")
        self.label_titulo.pack(pady=(10, 5))

        self.frame_relogio = tk.Frame(self.frame_display, bg="black", width=200, height=40)
        self.frame_relogio.pack(pady=5)

        self.label_hora = tk.Label(self.frame_relogio, text="", font=("Arial", 14), fg="lime", bg="black")
        self.label_hora.pack()

        self.status_text = tk.Label(self.frame_display, text="Status: Sistema desligado", font=("Arial", 12), bg="#e0e0e0")
        self.status_text.pack(pady=10)

        self.btn_ligar = tk.Button(self.frame_display, text="Ligar/Desligar", command=self.pressionar_botao, font=("Arial", 14, "bold"), bg="red", fg="white")
        self.btn_ligar.pack(pady=5)

        self.btn_alimentar = tk.Button(self.frame_display, text="Alimentar Agora", command=self.feeder.alimentar, font=("Arial", 12))
        self.btn_alimentar.pack(pady=5)

        self.btn_verificar = tk.Button(self.frame_display, text="Verificar Peso", command=self.feeder.verificar_peso, font=("Arial", 12))
        self.btn_verificar.pack(pady=5)

        self.frame_agendamento = tk.Frame(self.frame_display, bg="#e0e0e0")
        self.frame_agendamento.pack(pady=10)

        self.entry_agendar = tk.Entry(self.frame_agendamento, font=("Arial", 14), width=10, justify="center")
        self.entry_agendar.pack()
        self.entry_agendar.bind("<KeyRelease>", self.formatar_horario_em_tempo_real)

        self.freq_var = tk.StringVar(value="Hoje")
        tk.Radiobutton(self.frame_agendamento, text="Hoje", variable=self.freq_var, value="Hoje", bg="#e0e0e0").pack(side="left")
        tk.Radiobutton(self.frame_agendamento, text="Todos os Dias", variable=self.freq_var, value="Todos os Dias", bg="#e0e0e0").pack(side="left")

        self.btn_agendar = tk.Button(self.frame_display, text="Agendar Alimentação", command=self.agendar, font=("Arial", 12))
        self.btn_agendar.pack(pady=5)

        self.btn_configurar = tk.Button(self.frame_display, text="Configurar Pet", command=self.abrir_configuracao, font=("Arial", 12))
        self.btn_configurar.pack(pady=5)

        self.btn_sincronizar = tk.Button(self.frame_display, text="Sincronizar Celular", command=self.abrir_celular, font=("Arial", 12))
        self.btn_sincronizar.pack(pady=5)

        self.frame_teclado = tk.Frame(self.frame_display)
        self.frame_teclado.pack(pady=5)

        self.criar_teclado()

        self.app_celular = None
        self.feeder.set_alerta_callback(self.alertar_no_celular)

        self.atualizar_hora()
        self.atualizar()

    def formatar_horario_em_tempo_real(self, event):
        texto = self.entry_agendar.get().replace(":", "")
        if len(texto) > 4:
            texto = texto[:4]
        if len(texto) > 2:
            texto = texto[:2] + ":" + texto[2:]
        self.entry_agendar.delete(0, tk.END)
        self.entry_agendar.insert(0, texto)

    def criar_teclado(self):
        botoes = [ ('1',), ('2',), ('3',), ('4',), ('5',), ('6',), ('7',), ('8',), ('9',), ('0',), ('Apagar',) ]
        row, col = 0, 0
        for (texto,) in botoes:
            action = lambda x=texto: self.adicionar_tecla(x)
            b = tk.Button(self.frame_teclado, text=texto, width=5, height=2, command=action)
            b.grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 2:
                col = 0
                row += 1

    def adicionar_tecla(self, valor):
        if valor == "Apagar":
            self.entry_agendar.delete(0, tk.END)
        else:
            self.entry_agendar.insert(tk.END, valor)

    def update_status(self, mensagem):
        self.status_text.config(text=mensagem)

    def pressionar_botao(self):
        if self.feeder.sistema_ativo:
            self.feeder.desligar()
        else:
            self.feeder.ligar()
        status = "Sistema ligado" if self.feeder.sistema_ativo else "Sistema desligado"
        self.status_text.config(text=status)

    def agendar(self):
        horario_str = self.entry_agendar.get()
        if not horario_str or len(horario_str) != 5 or horario_str[2] != ":":
            self.update_status("Formato inválido. Use HH:MM.")
            return
        try:
            horario = datetime.strptime(horario_str, "%H:%M").time()
        except ValueError:
            self.update_status("Horário inválido.")
            return
        diario = True if self.freq_var.get() == "Todos os Dias" else False
        self.feeder.agendar_alimentacao(horario, diario)

    def abrir_configuracao(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("Configurar Pet")
        config_window.geometry("300x300")

        tk.Label(config_window, text="Peso do Pet (kg)", font=("Arial", 12)).pack(pady=5)
        peso_entry = tk.Entry(config_window, font=("Arial", 12))
        peso_entry.pack()

        tk.Label(config_window, text="Raça do Pet", font=("Arial", 12)).pack(pady=5)
        raca_entry = tk.Entry(config_window, font=("Arial", 12))
        raca_entry.pack()

        def salvar():
            try:
                peso = float(peso_entry.get())
                raca = raca_entry.get()
                self.feeder.configurar_pet(peso, raca)
                config_window.destroy()
            except ValueError:
                self.update_status("Peso inválido!")

        def abrir_historico():
            historico_window = tk.Toplevel(config_window)
            historico_window.title("Histórico de Alimentações")
            historico_window.geometry("300x400")
            text = tk.Text(historico_window, font=("Arial", 10))
            text.pack()
            for registro in self.feeder.historico_alimentacao:
                text.insert(tk.END, f"{registro}\n")

        tk.Button(config_window, text="Salvar Configurações", command=salvar, font=("Arial", 12)).pack(pady=5)
        tk.Button(config_window, text="Ver Histórico de Alimentações", command=abrir_historico, font=("Arial", 12)).pack(pady=5)

    def abrir_celular(self):
        if not self.app_celular or not tk.Toplevel.winfo_exists(self.app_celular.window):
            self.app_celular = AppCelular(self.root, self.feeder)

    def alertar_no_celular(self, mensagem):
        if self.app_celular:
            self.app_celular.receber_alerta(mensagem)

    def atualizar_hora(self):
        agora = datetime.now().strftime("%H:%M:%S")
        self.label_hora.config(text=agora)
        self.root.after(1000, self.atualizar_hora)

    def atualizar(self):
        self.feeder.checar_agendamentos()
        self.root.after(1000, self.atualizar)

# -------------------- EXECUÇÃO --------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
