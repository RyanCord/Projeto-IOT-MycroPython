from machine import Pin, time_pulse_us
import urequests
import time
import network
import uasyncio as asyncio  

# Definição dos pinos
trigger_entrada = Pin(15, Pin.OUT)
echo_entrada = Pin(2, Pin.IN)
trigger_saida = Pin(13, Pin.OUT)
echo_saida = Pin(12, Pin.IN)
botao_corte = Pin(4, Pin.IN, Pin.PULL_UP)  

#Função para conectar no Wi-Fi
def conecta_wifi():
    ssid = 'Wokwi-GUEST'
    senha = ""
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Conectando à rede Wi-Fi...')
        sta_if.active(True)
        sta_if.connect(ssid, senha)
        while not sta_if.isconnected():
            time.sleep(1)
    print('Conectado ao Wi-Fi:', sta_if.ifconfig())

#Função que mede a distancia dos sensores
def medir_distancia(trigger, echo):
    trigger.value(0)
    time.sleep_us(2)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)
    
    duracao = time_pulse_us(echo, 1, 1000000)
    distancia = (duracao / 2) / 29.1
    return distancia

# Função para enviar os dados para o servidor
def enviar_dados(num_entradas, num_saidas, num_cortes):
    url = "http://18.220.174.45/update"
    dados = {'entradas': num_entradas, 'saidas': num_saidas, 'cortes': num_cortes}
    try:
        response = urequests.post(url, json=dados)
        print('Dados enviados:', response.text)
    except Exception as e:
        print('Erro ao enviar dados:', e)


num_entradas = 0
num_saidas = 0
num_cortes = 0

conecta_wifi()

#Função usando a biblioteca ASYNCIO que permite com que eu rode duas verificações de loops ao mesmo tempo
#essa abaixo verifica os sensores
async def monitorar_sensores():
    global num_entradas, num_saidas
    while True:
        #Verifica a distancia de entradas
        distancia_entrada = medir_distancia(trigger_entrada, echo_entrada)
        if distancia_entrada < 50:
            num_entradas += 1
            enviar_dados(num_entradas, num_saidas, num_cortes)
            await asyncio.sleep(2)  # Pausa para evitar leituras duplicadas

        # Verifica a distância de saídas
        distancia_saida = medir_distancia(trigger_saida, echo_saida)
        if distancia_saida < 50:
            num_saidas += 1
            enviar_dados(num_entradas, num_saidas, num_cortes)
            await asyncio.sleep(2) 
        
        await asyncio.sleep(0.1) 

#Função que monitora o botao
async def monitorar_botao():
    global num_cortes
    estado_anterior_botao = botao_corte.value()
    while True:
        if botao_corte.value() == 0 and estado_anterior_botao == 1:  
            
            if botao_corte.value() == 0: 
                num_cortes += 1
                enviar_dados(num_entradas, num_saidas, num_cortes)
                print(f'Botão pressionado: Cortes = {num_cortes}')
                await asyncio.sleep(2)  

        estado_anterior_botao = botao_corte.value()
        await asyncio.sleep(0.1)  

#Função main que roda as duas funções
async def main():
    tarefa_sensores = asyncio.create_task(monitorar_sensores())
    tarefa_botao = asyncio.create_task(monitorar_botao())
    await tarefa_sensores
    await tarefa_botao


asyncio.run(main())
