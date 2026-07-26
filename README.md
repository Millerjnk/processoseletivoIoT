# Processo Seletivo – Intensivo Maker | IoT

## Etapa Prática – Sistemas Embarcados

---
### Identificação do Candidato

- **Nome completo:** Guilherme Miller Gama Cardoso
- **GitHub:** https://github.com/Millerjnk

---

## Visão Geral da Solução

O objetivo do projeto é criar uma solução de baixo custo voltada para indústrias e linhas de montagem manuais ou semiautomáticas que operam sem Controladores Lógicos Programáveis (CLPs), eliminando a necessidade de anotações manuais e fornecendo métricas de produtividade em tempo real.

O sistema realiza a contagem de itens em uma linha de montagem a partir da detecção do objeto pelo sensor óptico e mostra em um display OLED a quantidade de peças detectadas, apontando também se houve micro-paradas que possam estar atrasando a linha de produção.  

Ademais, o usuário/operador também pode interagir com o sistema por meio de um botão, que reinicia a aplicação, zerando a contagem de peças e exibindo no display que a reinicialização foi executada.

## Arquitetura do Sistema Embarcado

### Fluxo principal 

O fluxo do programa pode ser dividido em 2 grandes blocos:
- **Inicialização**:

Aqui são inicializados os pinos, o timer e o barramento I2C, além do start-up do display e da declaração das variáveis e constantes globais utilizadas durante a execução do código, como `GAMMA` e `RL10`, para a extração dos valores de lux, e `obj_no_sensor` para o controle do fluxo da esteira.

- **Loop principal**: 

No loop principal, temos 5 ações sendo realizadas:

1. **Leitura do sensor óptico e do tempo atual:** o programa lê o valor presente no pino ADC e o converte em um valor de lux, de acordo com a documentação, além de coletar o tempo atual da execução do código.

```python
tempo_atual = time.ticks_ms()
lux = read_lux()
```

```python
def read_lux():
    # Fórmula para extração do valor do Lux retirada da documentação oficial do sensor LDR
    valor_lido = ldr_sensor.read()
    tensao = valor_lido / 4096 * 5
    resistencia = 2000 * tensao / (1 - tensao / 5)
    lux = pow(RL10 * 1e3 * pow(10, GAMMA) / resistencia, (1 / GAMMA))
    return lux
```

2. **Verificação de objeto no sensor:** Uma estrutura condicional _if_ presente no loop verifica se há algum objeto passando pelo sensor. Se o lux for menor que `LUX_ESTEIRA_BLOQUEADA` (uma constante utilizada para determinar o limiar de lux que indica a passagem de um item), o código executa as seguintes linhas:

```python
if lux < LUX_ESTEIRA_BLOQUEADA:
        if not obj_no_sensor:
            # Inicia um timer em modo One-Shot para acabar em LIMIAR_PARADA milissegundos
            # caso o objeto não avance na esteira
            timer.init(period=LIMIAR_PARADA, mode=Timer.ONE_SHOT, callback=timer_acabado)  
            obj_no_sensor = True
```
Um timer no modo _One-shot_ é ativado para `LIMIAR_PARADA` milissegundos, e a flag `obj_no_sensor` recebe _True_.

3. **Verificação do estouro do timer:** Assim que o timer acaba, uma flag é ativada e o loop principal a verifica ativamente por meio do código:

```python
if tempo_estouro:
        print("Alerta: Micro-parada detectada!")
        
        oled.fill(0)
        oled.text("ALERTA:", 30, 10)
        oled.text("Micro-parada", 15, 25)
        oled.text("detectada!", 20, 40)
        oled.show()

        tempo_estouro = False
```
Um _print_ com a mensagem "Alerta: Micro-parada detectada!" é enviado para o terminal serial e uma mensagem no display indicando a micro-parada é exibida; em seguida, a flag `tempo_estouro` é redefinida.

4. **Verificação da saída do objeto do sensor óptico:** neste passo, uma outra estrutura condicional _if_ é executada, validando se o lux lido pelo sensor voltou aos padrões normais por meio do limiar `LUX_ESTEIRA_LIVRE` e da flag `obj_no_sensor`.

```python
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
```
Se a verificação for validada, ou seja, se o objeto passou pelo sensor, o timer é desinicializado, o contador de itens incrementado, a flag `tempo_estouro` redefinida, e a mensagem "Peca detectada! Total `contador_itens`" é impressa na saída serial e no display OLED.

5. **Chamada da função `turno_reset`:** por fim, uma função é chamada ao final de cada iteração do loop, com o objetivo de realizar a verificação do acionamento do botão.

### Estrutura de estados, loops ou temporizações

O código utiliza o _timer0_ para cronometrar o tempo necessário para detectar uma micro-parada, ativando a flag `tempo_estouro`, como já apontado anteriormente:

```python
def timer_acabado(timer_obj):
    global tempo_estouro
    if obj_no_sensor:
        tempo_estouro = True
```
Outro ponto pertinente de se comentar: o código é orientado a flags, ou seja, ao invés de executar funções que tomam muito tempo — como o _print_ — dentro de ISRs (como a do _timer0_), opta-se por utilizar flags globais que são ativadas ou redefinidas, e posteriormente tratadas no loop principal. Isso permite que as interrupções sejam pontuais e eficientes.

```python
# Inicialização de variáveis globais
obj_no_sensor = False
tempo_estouro = False
contador_itens = 0
botao_foi_pressionado = False
tempo_atual = tempo_passado = 0
```

### Como os componentes interagem entre si

Todos os componentes estão conectados ao cérebro do sistema, o ESP32. O sensor óptico capta os dados físicos de iluminação e transmite essa informação para o pino ADC do microcontrolador. O microcontrolador, então, é responsável por enviar mensagens via porta serial e também ao display, que funciona como um indicativo visual ao usuário. 

O LED vermelho é outro indicativo visual, apontando quando o nível de lux está abaixo de 100, um forte indício de que há um objeto no sensor. Já o LED verde apenas mostra que o sistema está energizado. O botão reinicia toda a contagem realizada via software, que também é atualizada no display. A caixa abaixo ilustra as conexões realizadas:

```text
ESP32
├── 3V3 ──► LED Verde (1k Ω)
├── GPIO 34 ◄── AO (Analog Output do sensor)
├── GPIO 14 ◄── Botão
├── GPIO 21 ──► SDA (OLED SSD1306)
├── GPIO 22 ──► SCL (OLED SSD1306)
├── 3V3 ──────► VCC (Sensor óptico e OLED)
└── GND ──────► GND (LEDs, Sensor óptico, Botão e OLED)
```

```text
Sensor Óptico
├── DO (Digital Output) ──► LED Vermelho (1k Ω)
├── AO (Analog Output do sensor) ──► LED Vermelho (1k Ω)
├── VCC (Sensor óptico e OLED) ◄─────── 3V3
└── GND ◄─────── GND (ESP32)
```
---

## Componentes Utilizados na Simulação

- **ESP32**: é o 'cérebro' do sistema. Responsável por interligar os componentes e executar a lógica do sistema da linha de montagem.

<br>

<div align="center">
  <img width="300" height="537" alt="Placa ESP32" src="https://github.com/user-attachments/assets/081a1560-fc95-4fb3-afa1-25f8a7c8c026" />
  <br>
  <em>Placa ESP32</em>
</div>

<br>

- **Sensor óptico**: tem a função de indicar que há um objeto na esteira, por meio da transdução de um fenômeno físico — a luz — em sinais digitais e analógicos que o microcontrolador entende.

<br>

<div align="center">
  <img width="340" height="166" alt="Sensor Óptico LDR" src="https://github.com/user-attachments/assets/3e155172-fe79-44f9-bff3-fcb4aece6e00" />
  <br>
  <em>Sensor Óptico LDR</em>
</div>

<br>
  
- **Display OLED**: serve como indicativo visual do sistema para o usuário/operador.

<br>

<div align="center">
  <img width="205" height="176" alt="Display OLED" src="https://github.com/user-attachments/assets/8b8a9b32-9654-494d-bb8c-5271eaf0ede2" />
  <br>
  <em>Display OLED SSD1306</em>
</div>

<br>
 
- **Botão**: responsável pelo _reset_ do sistema, zerando a contagem de itens.

<br>

<div align="center">
  <img width="148" height="119" alt="Botão Push Button" src="https://github.com/user-attachments/assets/e9bca7da-f5b1-4ac7-9a9b-1b3a62aa2236" />
  <br>
  <em>Botão (Push Button)</em>
</div>

<br>

- **LED vermelho**: outro indicativo visual que aponta se o sensor está registrando níveis abaixo de 100 lux.

<br>

<div align="center">
  <img width="74" height="89" alt="LED Vermelho" src="https://github.com/user-attachments/assets/698573f3-a21f-44c6-9be4-fd41f4799304" />
  <br>
  <em>LED Vermelho</em>
</div>

<br>
 
- **LED verde**: indicativo visual que acusa se o sistema está energizado.

<br>

<div align="center">
  <img width="74" height="84" alt="LED Verde" src="https://github.com/user-attachments/assets/98a467c8-9489-4c1c-b69b-bdce5e878ac9" />
  <br>
  <em>LED Verde</em>
</div>

---

## Decisões Técnicas Relevantes

O código foi estruturado para utilizar majoritariamente flags, a fim de torná-lo mais responsivo e eficiente, como dito anteriormente. Um ponto relevante a ser destacado foi a escolha de acionar a ação do botão na segunda borda de subida, ou seja, quando o botão é solto. Isso é uma tentativa de mitigar um cenário em que o usuário pressiona o botão por muito tempo. Outro ponto é o descarte do uso de interrupção (ISR) de hardware para o botão, o que foi necessário para facilitar a implementação da lógica baseada na sua soltura. A função do botão é a que segue:

```python
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
```
Essa função é chamada por último no loop principal.

Ademais, foi utilizado um timer de hardware para realizar a cronometragem da micro-parada. A função de callback que trata esse timer está exibida abaixo:

```python
def timer_acabado(timer_obj):
    global tempo_estouro
    if obj_no_sensor:
        tempo_estouro = True
```

Por fim, foi implementado um pequeno delay no final do loop principal para aliviar a carga da CPU do microcontrolador:

```python
    # Pequeno delay para aliviar o micro
    time.sleep_ms(10)
```
---

## Resultados Obtidos

O sistema funciona corretamente na simulação do Wokwi, atendendo aos requisitos de _reset_ por meio do botão e a detecção de micro-paradas caso algum item fique retido no sensor. Somado a isso, a integração do display OLED e dos LEDs agregou muito à solução, fornecendo indicativos visuais claros para o usuário/operador em tempo real.

---

## Comentários Adicionais

Uma dificuldade que enfrentei foi implementar a lógica do botão na borda de soltura, ou seja, validando a ação apenas quando ele fosse solto. Inicialmente, programei o botão para ser tratado por uma ISR convencional, com o _reset_ sendo disparado imediatamente no momento do aperto. Entretanto, por mera coincidência, segurei o botão por tempo demais e percebi os diversos _resets_ consecutivos que ocorriam, gerando o famoso *bouncing* comportamental. Procurei referências de como resolver isso e encontrei um material que aplicava a lógica de estado desejada; fiz as adaptações necessárias e consegui fazer funcionar de maneira estável.

Em relação a possíveis melhorias, no futuro eu implementaria uma conexão MQTT integrada a um *dashboard* para o monitoramento remoto dos indicadores do sistema, resolvendo a necessidade do acompanhamento físico na linha de produção.

---

> Este relatório faz parte da avaliação técnica.  
> Clareza, objetividade e organização são tão importantes quanto o funcionamento do código.

---

## Especificação dos Testes Automatizados (Wokwi CI)

Para que o projeto seja validado com sucesso na esteira de integração contínua (CI), o firmware escrito em MicroPython deve interagir corretamente com as leituras dos sensores descritos em cada cenário e enviar as mensagens de status exatas.

### Requisitos Críticos de Implementação

1. **Casamento Exato de Strings:** O Wokwi CI faz uma verificação estrita caractere por caractere. Se houver divergência em maiúsculas/minúsculas, acentuação ou falta de pontuação, o teste irá falhar.
2. **Arquitetura Não-Bloqueante:** Evite o uso de funções bloqueantes. Elas podem fazer com que o firmware perca a janela de tempo em que o simulador altera o peso, quebrando a sincronia do teste automatizado.

---

## Suporte

Em caso de dúvidas:

- Consulte o material dos cursos EAD
- Leia atentamente este README
- Analise os logs das GitHub Actions
- Utilize os canais oficiais para contato com os instrutores
