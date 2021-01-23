
# Recomendador de Pesquisa Bovespa

Este projeto destina se a auxiliar investidores da bolsa de valores a fazerem melhores escolhas, utilizando tanto dados fundamentalista quando dados de swing trade. Sendo possível configurar a plataforma para enviar e-mail para um conjunto de usuários.
#### Exemplo do resultado dos dados fundamentalistas
![Exemplo do resultado dos dados fundamentalistas](https://raw.githubusercontent.com/LeandroBruscato/RecomendadorDePesquisaBovespa/master/Docs/fundamentus.png)
#### Exemplo do resultado dos indicadores
![Exemplo do resultado dos indicadores](https://raw.githubusercontent.com/LeandroBruscato/RecomendadorDePesquisaBovespa/master/Docs/indicadores.png)
## Índices Utilizados
### Fundamentalista
- Valor atual
- Graham
- Valor Alvo
- Valor máximo em um ano
- Valor mínimo em um ano
- Valor máximo nos últimos 15 dias
- Valor mínimo nos últimos 15 dias
- PL
- PVP
- EV EBITDA
- Dividendos
### Swing trade
- MACD
- Momentum
- OBV
- Índice de força relativa (RSI)
- Estocástico

# Configurações
Para este programa funcionar é preciso criar 2 programas que serão usados para os envio dos e-mail. 
## Criar o conf.ini
Este arquivo é responsável em acessar o a conta de e-mail que enviar para os clientes.
Para isso basta criar um arquivo com as sequiantes características:

    [EMAIL]
    password = XXXXXXXX
    login = email@email.com

## Criar o Clients.xml
Este arquivo é a relação dos clientes.
Para isso basta criar um arquivo com as sequiantes características:

    <?xml version="1.0"?>
    <Clients>
    <Client name="client1">
    <Name>"Name 1"</Name>
    <Email>"email1@gmail.com"</Email>
    </Client>
    <Client name="client2">
    <Name>"Name 2"</Name>
    <Email>"email2@hotmail.com"</Email>
    </Client>
    </Clients>
