import time
from machine import Pin, ADC, Timer
from math import pow

# Inicialização de pinos e timer
ldr_sensor = ADC(Pin(34))
ldr_sensor.atten(ADC.ATTN_11DB)
botao = Pin(14, Pin.IN, Pin.PULL_UP)
timer = Timer(0)

# Inicialização de constantes
GAMMA = 0.7
RL10 = 50
LIMIAR_PARADA = 5000 # em ms
LUX_ESTEIRA_LIVRE = 500
LUX_ESTEIRA_BLOQUEADA = 100

# Inicialização de variáveis globais
obj_no_sensor = False
tempo_estouro = False
contador_itens = 0
botao_foi_pressionado = False
tempo_atual = 0
tempo_passado = 0

print("Contador de Producao Inicializado\n")

def read_lux():
    # Fórmula para extração do valor do Lux retirada da documentação oficial do sensor LDR
    valor_lido = ldr_sensor.read()
    tensao = valor_lido / 4096 * 5
    resistencia = 2000 * tensao / (1 - tensao / 5)
    lux = pow(RL10 * 1e3 * pow(10, GAMMA) / resistencia, (1 / GAMMA))

    return lux

def timer_acabado(timer_obj):
    global tempo_estouro

    if obj_no_sensor:
        tempo_estouro = True

def turno_reset(pino):
    global contador_itens, tempo_atual, tempo_passado, obj_no_sensor, tempo_estouro, botao_foi_pressionado

    if pino.value() == 0:
        if not botao_foi_pressionado and time.ticks_diff(tempo_atual, tempo_passado) > 300:
            botao_foi_pressionado = True
            tempo_passado = tempo_atual

    elif pino.value() == 1:
        if botao_foi_pressionado:
            botao_foi_pressionado = False
            contador_itens = 0
            obj_no_sensor = False
            tempo_passado = tempo_atual
            tempo_estouro = False
            timer.deinit() 
            print("Turno resetado com sucesso. Contadores zerados.")

while True:
    tempo_atual = time.ticks_ms()

    lux = read_lux()

    if lux < LUX_ESTEIRA_BLOQUEADA:
        if not obj_no_sensor:
            # Inicia um timer em modo One Shot para acabar em LIMIAR_PARADA milissegundos
            # caso o objeto não avance na esteira
            timer.init(period=LIMIAR_PARADA,            
                       mode=Timer.ONE_SHOT,         
                       callback=timer_acabado)  
            obj_no_sensor = True

        if tempo_estouro:
            print("Micro-parada detectada!")
            tempo_estouro = False
            
    if lux >= LUX_ESTEIRA_LIVRE and obj_no_sensor:
        # Desinicializa o timer se o objeto passar pelo sensor antes do tempo
        timer.deinit()
        obj_no_sensor = False
        tempo_estouro = False
        contador_itens += 1
        print(f"Peca detectada! Total: {contador_itens}")

    turno_reset(botao)

    # Pequeno delay para aliviar o micro
    time.sleep_ms(10)
