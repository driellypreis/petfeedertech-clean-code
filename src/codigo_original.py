import time

def ligar_motor():
    print("Motor ligado para liberar ração")

def desligar_motor():
    print("Motor desligado")

def mostrar_mensagem(msg):
    print("Mensagem: ", msg)

def checar_horario():
    agora = time.localtime()
    if agora.tm_hour == 8 or agora.tm_hour == 18:
        return True
    return False

def liberar_racao():
    ligar_motor()
    time.sleep(2)
    desligar_motor()
    mostrar_mensagem("Ração liberada!")

def main():
    while True:
        if checar_horario():
            liberar_racao()
            time.sleep(3600)  # espera 1 hora
        else:
            print("Ainda não é hora de alimentar")
            time.sleep(60)

main()
