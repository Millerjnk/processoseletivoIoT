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
tempo_atual = tempo_passado = 0

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

    if(obj_no_sensor):
        tempo_estouro = True

def ISR_botao(botao):
    global botao_foi_pressionado, tempo_atual, tempo_passado  

    if botao_foi_pressionado == False:
        tempo_atual = time.ticks_ms()
        if (time.ticks_diff(tempo_atual, tempo_passado)) > 500:
            botao_foi_pressionado = True
            tempo_passado = tempo_atual

botao.irq(trigger=Pin.IRQ_FALLING, handler=ISR_botao)

while True:

    lux = read_lux()

    if lux < LUX_ESTEIRA_BLOQUEADA:
        if not obj_no_sensor:
            # Inicia um timer em modo One Shot para acabar em LIMAR_PARADA milissegundos
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

    if botao_foi_pressionado:
        print("Turno resetado com sucesso. Contadores zerados.")
        contador_itens = 0
        botao_foi_pressionado = False
