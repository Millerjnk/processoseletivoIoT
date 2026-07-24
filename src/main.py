import time
from machine import Pin, ADC, Timer, I2C
from math import pow
from ssd1306 import SSD1306_I2C
from micropython import const

# Inicialização de pinos, timer e I2C
ldr_sensor = ADC(Pin(34))
ldr_sensor.atten(ADC.ATTN_11DB)
botao = Pin(14, Pin.IN, Pin.PULL_UP)
timer = Timer(0)

# Configuração do I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

time.sleep_ms(100)

# Inicialização do Display
largura_oled = 128
altura_oled = 64
oled = SSD1306_I2C(largura_oled, altura_oled, i2c)

# Inicialização de constantes
GAMMA = const(0.7)
RL10 = const(50)
LIMIAR_PARADA = const(5000) # em ms
LUX_ESTEIRA_LIVRE = const(500)
LUX_ESTEIRA_BLOQUEADA = const(100)

# Inicialização de variáveis globais
obj_no_sensor = False
tempo_estouro = False
contador_itens = 0
botao_foi_pressionado = False
tempo_atual = tempo_passado = 0

print("Contador de Producao Inicializado\n")

oled.fill(0)
oled.text("Contador", 20, 10)
oled.text("de Producao", 20, 25)
oled.text("Inicializado", 20, 40)
oled.show()

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
            
            oled.fill(0)
            oled.text("Turno Resetado!", 5, 20)
            oled.show()

while True:
    tempo_atual = time.ticks_ms()
    lux = read_lux()

    if lux < LUX_ESTEIRA_BLOQUEADA:
        if not obj_no_sensor:
            # Inicia um timer em modo One Shot para acabar em LIMIAR_PARADA milissegundos
            # caso o objeto não avance na esteira
            timer.init(period=LIMIAR_PARADA, mode=Timer.ONE_SHOT, callback=timer_acabado)  
            obj_no_sensor = True

    if tempo_estouro:
        print("Alerta: Micro-parada detectada!")
        
        oled.fill(0)
        oled.text("ALERTA:", 30, 10)
        oled.text("Micro-parada", 15, 25)
        oled.text("detectada!", 20, 40)
        oled.show()

        tempo_estouro = False
            
    if lux >= LUX_ESTEIRA_LIVRE and obj_no_sensor:
        # Desinicializa o timer se o objeto passar pelo sensor antes do tempo
        timer.deinit()
        obj_no_sensor = False
        tempo_estouro = False
        contador_itens += 1
        print(f"Peca detectada! Total: {contador_itens}")

        oled.fill(0) 
        oled.text("Peca detectada!", 5, 16)
        oled.text("Total: " + str(contador_itens), 30, 35)
        oled.show()

    turno_reset(botao)

    # Pequeno delay para aliviar o micro
    time.sleep_ms(10)