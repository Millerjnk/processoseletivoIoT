# Processo Seletivo – Intensivo Maker | IoT

## Etapa Prática – Sistemas Embarcados

Bem-vindo(a) à **etapa prática do processo seletivo para o Intensivo Maker | IoT**.

Esta atividade tem como objetivo avaliar suas competências em **Sistemas Embarcados**, com foco em **organização de projeto, lógica de firmware e simulação de hardware**, a partir da aplicação prática dos conhecimentos adquiridos nos cursos EAD da etapa anterior.

> **Objetivo principal**  
> Avaliar sua capacidade de **planejar, estruturar e desenvolver** uma solução funcional de sistemas embarcados, seguindo boas práticas de engenharia.

---

## Antes de Tudo

Se você **nunca utilizou Git ou GitHub**, não se preocupe.  
Siga atentamente os passos abaixo.

---

### 1 - Criação de Conta no GitHub

1. Acesse: <https://github.com>
2. Clique em **Sign up**
3. Crie sua conta gratuita seguindo as instruções da plataforma

> O GitHub será utilizado para:
>
> - Envio do seu projeto
> - Versionamento do código
> - Correção e validação automática via GitHub Actions

---

### 2 - Instalação do Git

O **Git** é a ferramenta responsável pelo controle de versões do seu código.

### Windows

Baixe e instale o **Git Bash**:  
<https://git-scm.com/downloads>

### Linux / macOS

Verifique se o Git já está instalado:

```bash
git --version
```

> Caso não esteja, instale pelo gerenciador de pacotes do seu sistema.

## Preparando o Ambiente

Para desenvolver o desafio, você deverá criar uma cópia deste repositório no seu GitHub.

### 1 - Fork do Repositório

No canto superior direito desta página, clique em Fork

<img width="219" height="45" alt="image" src="https://github.com/user-attachments/assets/5d629626-513a-445c-ba0f-e5bb3e225187" />

Uma cópia do repositório será criada no seu perfil do GitHub

> O Fork permite que você trabalhe de forma independente, sem alterar o repositório original do processo seletivo.

### 2 - Clone do Repositório

No repositório do seu Fork, clique em **<> Code**

<img width="149" height="52" alt="image" src="https://github.com/user-attachments/assets/abbd331b-a005-4633-89c6-afd16acbe828" />

Copie a URL e execute no terminal:

```bash
git clone https://github.com/SEU_USUARIO/nome-do-repositorio.git
cd nome-do-repositorio
```

> O comando git clone cria uma cópia local do repositório para desenvolvimento.

### 3 - Preparação do Ambiente de Execução

Você pode executar o projeto de duas formas. Escolha apenas uma.

#### Opção A – Ambiente Python Local

**Requisitos:**

- Python 3.10 ou 3.11
- pip

**Instale as dependências:**

```bash
pip install -r requirements.txt
```

#### Opção B – Dev Container (Recomendado)

Este repositório inclui um Dev Container, garantindo um ambiente padronizado.

**Requisitos:**

- VS Code
- Docker instalado
- Extensão Dev Containers

**Passos:**

1. Abra o repositório no VS Code
2. Clique em “Reopen in Container”
3. Aguarde a criação automática do ambiente

> Todas as dependências serão instaladas automaticamente.

## Criando sua API Key do Wokwi

A simulação do projeto será executada automaticamente via GitHub Actions, utilizando o Wokwi CLI.

Para isso, você precisa gerar uma API Key.

1. Acesse: <https://wokwi.com/dashboard/ci>
2. Faça login (Google ou GitHub)
3. Clique em Generate API Token
4. Copie a chave gerada (exemplo: wokwi-xxxxxxxx)

> Importante

- Nunca faça commit dessa chave
- Ela deve ser armazenada apenas como secret no GitHub

## Configurando a API Key no GitHub (Secrets)

**No repositório do seu Fork:**

1. Vá em Settings
2. Acesse Secrets and variables → Actions
3. Clique em New repository secret
4. Nome: WOKWI_API_KEY
5. Valor: sua chave gerada
6. Salve

> As GitHub Actions do template já estão preparadas para usar essa variável automaticamente.

## Desafio Técnico

Você deverá desenvolver um projeto de sistemas embarcados simulados, utilizando Python e Wokwi.

### Estrutura mínima esperada

```text
/project
 ├── src/
 │   └── main.py        # Código principal do projeto
 ├── wokwi.toml         # Configuração da simulação
 ├── diagram.json       # Circuito no Wokwi
 └── README.md          # Explicação do seu projeto
```

> Você pode expandir essa estrutura se desejar, desde que mantenha os arquivos essenciais.

### Escolha do cenário

No diretório "scenarios" existem arquivos .md e pastas referentes a diferentes desafios. Selecione apenas um deles e mantenha apenas a pasta e .md referente ao desafio a ser desenvolvido, deletando os demais. Isso fará com o que o fluxo de testes automáticos selecione o fluxo de acordo com o desafio escolhido.

### Como Desenvolver seu Projeto

O desenvolvimento acontece principalmente nos arquivos abaixo:

#### src/main.py

- Código Python executado na simulação
- Implementa a lógica do sistema embarcado
- Exemplos: controle de LEDs, leitura de sensores, estados, temporizações, etc.

#### diagram.json

- Define o hardware virtual do projeto
- Componentes como:
  - LEDs
  - Botões
  - Sensores
  - Placa microcontroladora

#### wokwi.toml

- Configura a simulação:
  - Tipo de placa
  - Framework
  - Dependências adicionais
 
#### Rodando localmente

Para executar o seu projeto locamente, é necesário preparar a imagem docker local, e após isso
utiliza-la para gerar o arquivo que conterá o seu código para o projeto, para isso, execute os 
seguintes códigos:

1. Prepara a imagem docker (Necessário rodar apenas 1 vez)

```bash
docker build -t esp32-builder -f Dockerfile .
```

2. Prepara o arquivo de memória fs.bin (Necessário a cada iteração)

```bash
docker run --rm -v "$(pwd)/src:/mnt/src" -v "$(pwd):/mnt/out" esp32-builder bash -c "mkdir -p /tmp/fs && cp -r /mnt/src/* /tmp/fs/ && /mklittlefs/mklittlefs -c /tmp/fs -b 4096 -p 256 -s 0x200000 /mnt/out/fs.bin"
```

#### Commit e Push

Após suas alterações:

```bash
git add .
git commit -m "Descrição clara do que foi feito"
git push
```

### Execução Automática (GitHub Actions)

A cada push, o GitHub Actions irá automaticamente:

- Executar o pipeline de build
- Rodar a simulação via Wokwi CLI
- Validar que o projeto executa sem erros

### Caso algo falhe

- Vá até a aba Actions
- Analise os logs da execução
- Corrija e envie novamente

## Critérios de Avaliação

Esta etapa será avaliada considerando:

- Funcionamento correto da simulação
- Código organizado e legível
- Estrutura de arquivos correta
- Uso adequado do Wokwi
- Commits claros e bem descritos
- Projeto executando sem falhas nas Actions

---

## Submissão Final

Após concluir o desenvolvimento:

1. Verifique se o projeto **executa sem erros** nas GitHub Actions
2. Confirme que todos os arquivos obrigatórios estão presentes
3. Copie o link do **seu repositório no GitHub**

Envie o link conforme as orientações do processo seletivo na plataforma do **PNAAT**.

---

## Relatório do Candidato

O arquivo **`README.md` do seu repositório** deve ser utilizado como o  
**relatório final do desafio técnico**.

Preencha todas as seções abaixo de forma **clara, objetiva e técnica**.

> **Dica importante**  
> Não é necessário um relatório extenso.  
> O principal critério é demonstrar **clareza nas decisões técnicas**, organização e entendimento do sistema embarcado desenvolvido.
> Não mantenha os demais conteúdos escritos nesse arquivo README, aqui devem ser concentradas apenas informações referentes ao projeto desenvolvido.

---

### Identificação do Candidato

- **Nome completo:** Guilherme Miller Gama Cardoso
- **GitHub:** https://github.com/Millerjnk

---

## Visão Geral da Solução

O objetivo do projeto é criar uma solução de baixo custo voltada para indústrias e linhas de montagem manuais ou semiautomáticas que operam sem Controladores
lógicos Programáveis (CLPs), eliminando a necessidade de anotações manuais e fornecendo métricas de produtividade em tempo real.

O sistema realiza a contagem de itens em uma linha de montagem a partir da detecção do objeto pelo sensor óptico e mostra em um display OLED a quantidade de peças que detectou, apontando também se houveram micro-paradas que estão atrasando a linha de produção.  

Ademais, o usuário/operador também pode interagir com o sistema através de um botão, que reinicia a aplicação, zerando a contagem de peças e exibindo no display que a reinicialização foi executada.

## Arquitetura do Sistema Embarcado

### Fluxo principal 

O fluxo do programa pode ser dividido em 2 grandes blocos:
- **Inicialização**:

Aqui são inicializados os pinos, timer e o barramento I2C, além do start-up do display e a declaração das variáveis e constantes globais utilizadas durante a execução do código, como `GAMMA`e `RL10`, para extração dos valores de lux, e `obj_no_sensor` para controle do fluxo da esteira.

- **Loop principal**: 

No loop principal, temos 5 ações sendo realizadas:

1. Leitura do sensor óptico e do tempo atual: o programa lê o valor presente no pino ADC e transforma em um valor de lux, de acordo com a documentação, além de coletar o tempo atual da execução do código.

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
2. Verificação de objeto no sensor: Um condicional _if_ presente no loop verifica se algum objeto passando no sensor. Se lux for menor que `LUX_ESTEIRA_BLOQUEADA`, uma variável para determinar o limiar de lux que indica quando um item está passando pelo sensor, o código executa as linhas:

```python
if lux < LUX_ESTEIRA_BLOQUEADA:
        if not obj_no_sensor:
            # Inicia um timer em modo One Shot para acabar em LIMIAR_PARADA milissegundos
            # caso o objeto não avance na esteira
            timer.init(period=LIMIAR_PARADA, mode=Timer.ONE_SHOT, callback=timer_acabado)  
            obj_no_sensor = True
```
Um timer _One_shot_ é ativado para `LIMIAR_PARADA` milissegundos, e a flag `obj_no_sensor` recebe _True_.

3. Verificação do estouro do timer: Assim que o timer acaba, uma flag é setada e o loop principal ativamente a verifica através do código:
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
Um _print_ com a mensagem "Alerta: Micro-parada detectada!" é enviado para a serial e uma mensagem no display acusando a micro-parada é exibida; a flag tempo estouro é resetada.

4. Verificação da saída do objeto do sensor óptico: neste passo, um outro condicional _if_ executa, validando se o lux lido pelo sensor voltou aos padrões normais, através do limiar `LUX_ESTEIRA_LIVRE` e da flag `obj_no_sensor`.

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
Se a verificação for validada, i.e., o objeto passou do sensor, o timer é desinicializado, o contador de itens incrementado, a flag `tempo_estouro` resetada e a mensagem "Peca detectada! Total `contador_itens`" é imprimida na saída serial e no display OLED.

5. Chamada da função `turno_reset`: por fim, uma função é chamada ao fim de todo loop, a fim de realizar a verificação do aperto do botão.

### Estrutura de estados, loops ou temporizações

O código utiliza o _timer0_ para fazer a cronometragem do tempo para acusar uma micro-parada, e levanta a flag `tempo_estouro`, como já apontado anteriormente:

```python
def timer_acabado(timer_obj):
    global tempo_estouro
    if obj_no_sensor:
        tempo_estouro = True
```
Outro ponto pertinente de se comentar: o código é orientado a flags, ou seja, ao invés de executar funções que tomam muito tempo, por exemplo, _print_, dentro de ISR's como a do _timer0_, opta-se por utilizar flags globais, que são setadas ou resetadas e tratadas no loop principal, permitindo com que as interrupções sejam pontuais.

```python
# Inicialização de variáveis globais
obj_no_sensor = False
tempo_estouro = False
contador_itens = 0
botao_foi_pressionado = False
tempo_atual = tempo_passado = 0
```
### Como os componentes interagem entre si
Todos os componentes estão conectados ao cérebro do sistema, o ESP32. O sensor óptico capta os dados físicos de iluminação e transmite essa informação para o pino ADC do microcontrolador. O micro, então, é responsável por enviar mensagens na serial e também ao display, que funciona como um indicativo visual ao usuário. 

O LED vermelho é outro indicativo visual, apontando quando o nível de lux está abaixo de 100, um forte indício que há um objeto no sensor. Já o LED verde apenas mostra que o sistema está energizado. O botão reinicia toda a contagem realizada via software, que também é exibida no display. A caixa abaixo mostra as conexões realizadas:


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

Liste os principais componentes definidos no `diagram.json`, por exemplo:
- **ESP32**: é o 'cérebro' do sistema. Resposável por interligar os componentes e executar a lógica do sistema de linha de montagem.
- **Sensor óptico**: tem função de indicar que há um objeto na esteira, através da transdução de um fenôneno físico, a luz, em medidas digitais que o microcontrolador entende.
- **Display OLED**: serve como indicativo visual do sistema para o usuário/operador.
- **Botão**: responsável pelo _reset_ do sistema, zerando a contagem de itens.
- **LED vermelho**: outro indicativo visual que aponta se o sensor está lendo leituras abaixo de 100 lux.
---

## Decisões Técnicas Relevantes

Explique brevemente decisões importantes tomadas durante o desenvolvimento, como:
O código foi estruturado para utilizar majoritariamente flags, para tornar o código mais eficiente, como dito anteriormente. Um ponto relevante de ser tratado foi a escolha de acionar o botão na segunda borda de subida, ou seja, quando o botão for solto. Isso é uma tentativa de mitigar um cenário onde o usuário pressiona o botão por muito tempo. Outro ponto é o descarte do uso da interrupção do botão, que foi necessário para facilitar a implementação dessa lógica da soltura do mesmo. A função do botão é a que segue:

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

Ademais, foi utilizado um timer para realizar a cronometragem da micro-parada. A função que trata esse timer está exibida abaixo:

```python
def timer_acabado(timer_obj):
    global tempo_estouro
    if obj_no_sensor:
        tempo_estouro = True
```
Por fim, foi implementado um pequeno delay no fim do loop para aliviar a CPU do microcontrolador:

```python
# Pequeno delay para aliviar o micro
    time.sleep_ms(10)
```
---

## Resultados Obtidos

Descreva o comportamento final do sistema:

O sistema funciona corretamente na simulação do Wokwi, com os requesitos de _reset_ através do botão e a acusação de micro-paradas se algum item estiver preso no sensor. Somado a isto, a implementação do display OLED e os LED's acrescentaram à solução, dando indicativos visuais para o usuário/operador.
---

## Comentários Adicionais (Opcional)

Uma dificuldade que enfrentei foi implentar a lógica do botão na segunda borda de seu acionamento, i.e, quando ele fosse solto. Inicialmente, programei o botão para ser tratado por uma ISR, com o _reset_ sendo acionado no seu aperto. Entretanto, por mera coinciência, segurei o botão por tempo demais e percebi os diversos _resets_ que ocorriam. Procurei referências de como resolver isso e achei um vídeo realizando exatamente o que queria. Fiz as adaptações necessárias e consegui fazer funcionar.

Em relação a possíveis melhorias, eu implementaria uma conexão MQTT com um dashboard para monitoramento remoto do sistema, resolvendo a necessidade de estar presente fisicamente na linha de produção.

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
