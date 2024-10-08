Projeto para IOT na faculdade.

Este projeto utiliza MycroPython para programação de uma placa ESP32. Este projeto foi feito em parceria com uma barbearia, para coletar os dados e transforma-los.

Utilizando Dois sensores HC-SR04 para detectar a entrada de pessoas dentro da barbearia, um para captar a entrada e outro para captar a saída.

Usando um botao apertado pelo proprio barbeiro em teoria, ele contabiliza os cortes feitos pelo barbeiro, assim contabilizando as entradas as saídas e os cortes feitos.

Após isso ele envia esses dados para um servidor linux dedicado, que exibe os dados em formato de gráfico, quantas entradas foram feitas, e quantas dessas entradas foram convertidas em cortes.
