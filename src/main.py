import time
from machine import Pin, ADC, Timer
from math import pow

#Inicializando variáveis do sistema

ldr_sensor = ADC(Pin(34))
botao = Pin(14, Pin.IN, Pin.PULL_UP)
# Configura a atenuação para ler a faixa completa de 0-3.3V
# ATTN_11DB é a configuração padrão para isso
ldr_sensor.atten(ADC.ATTN_11DB)
GAMMA = 0.7
RL10 = 50
timer = Timer(0)
obj_no_sensor = False
tempo_estouro = False
contador_itens = 0
botao_foi_pressionado = False
tempo_atual = tempo_passado = 0
print("Contador de Producao Inicializado\n")

def timer_acabado(timer_obj):
    global tempo_estouro
    if(obj_no_sensor):
        tempo_estouro = True

def ISR_botao(botao):
    global botao_foi_pressionado, tempo_atual, tempo_passado  # Avisa que vamos usar a variável global

    if botao_foi_pressionado == False:
        tempo_atual = time.ticks_ms()
        if (time.ticks_diff(tempo_atual, tempo_passado)) > 500:
            botao_foi_pressionado = True
            tempo_passado = tempo_atual

botao.irq(trigger=Pin.IRQ_FALLING, handler=ISR_botao)

while True:
    valor_lido = ldr_sensor.read()
    tensao = valor_lido / 4096 * 5
    resistencia = 2000 * tensao / (1 - tensao / 5)
    lux = pow(RL10 * 1e3 * pow(10, GAMMA) / resistencia, (1 / GAMMA))
    #print(lux)

    if lux < 100:
        if not obj_no_sensor:
            timer.init(period=3000,            # Período em milissegundos (200ms = 5 vezes por segundo)
                mode=Timer.ONE_SHOT,         # Modo: PERIODIC (repete) ou ONE_SHOT (uma vez)
                callback=timer_acabado)      # A função a ser chamada quando o timer estourar
            obj_no_sensor = True
        if tempo_estouro:
            print("Micro-parada detectada!")
            tempo_estouro = False
        
    if lux >= 500 and obj_no_sensor:
        timer.deinit()
        obj_no_sensor = False
        tempo_estouro = False
        contador_itens += 1
        print(f"Peca detectada! Total: {contador_itens}")

    if botao_foi_pressionado:
        print("Turno resetado com sucesso. Contadores zerados.")
        contador_itens = 0
        botao_foi_pressionado = False
