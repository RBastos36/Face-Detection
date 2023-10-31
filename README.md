# TP1 - Detetor de Caras
Sistemas Avançados de Visualização Industrial (SAVI) - Grupo 6 - Universidade de Aveiro - 2023/24

## Índice

- [Introdução](#introduction)
- [Bibliotecas Usadas](#libraries-used)
- [Instalação](#installation)
- [Explicação do Código](#code-explanation)
- [Autores](#authors)

---
## Introdução

<p align="justify"> No âmbito da Unidade Curricular de SAVI, foi criado um programa capaz de detetar e seguir as caras das pessoas que se aproximem da câmera, reconhecendo e cumprimentando as pessoas que já tem guardadas na <i>Database</i> e questionando os desconhecidos sobre os seus nomes. <br> Relativamente às opções adicionais, o utilizador tem a possibilidade alterar os nomes das pessoas, registadas previamente na base de dados. </p>

[Video.webm](https://github.com/joaonogueiro/TP1_SAVI/assets/114345550/8f64f7c6-c3a3-4698-b44e-39805258fb01)

<p align="center">
Vídeo ilustrativo do funcionamento do programa 
</p>


---
## Bibliotecas Usadas

Para a criação deste programa, recorreu-se à utilização de algumas bibliotecas. Estas serão brevemente explicadas abaixo.

- **OpenCV**
  - Descrição: OpenCV é uma biblioteca que existe em Python desenhada para resolver problemas de _computer vision_. 
  - Instalação:
    ```bash
    sudo apt-get install python3-opencv
    ```

- **Face-Recognition**
  - Descrição: Biblioteca de Python com comandos para reconhecer e manipular caras criada com modelos baseados em _deep learning_. 
  - Instalação:
    ```bash
    pip3 install face_recognition
    ```

- **PyTTSx3**
  - Descrição: Esta é uma biblioteca de Python para fazer conversão de texto para voz, funcionando _offline_ e sendo compatível com Python 2 e 3.
  - Instalação:
    ```bash
    pip install pyttsx3
    ```

- **Threading**
  - Descrição: Esta bibioteca permite introduzir uma sequência de intruções num programa que podem ser executadas independentemente do restante processo.
  - Instalação: Esta já vem disponível com a versão do Python 3.7.


---
## Instalação

O programa pode ser instalado seguindo os seguintes passos:

1. Clonar o repositório:
```bash
git clone https://github.com/joaonogueiro/TP1_SAVI
```
2. Alterar a diretória do projeto:
```bash
cd TP1_SAVI
```
3. Correr o programa:
```bash
./main.py
```

Se os passos acima foram seguidos, o programa deve correr sem problemas.


---
## Explicação do Código 

<p align="justify"> O código começa por verificar se existe alguma informação na base de dados, e se assim se verificar, lê a mesma. De seguida, inicializa a câmera e começa a tentar encontrar deteções de caras com os comandos abaixo, baseados na biblioteca <b>Face-Recognition</b>.</p>

```python
# Find all the faces and face encodings in the current frame of video
face_locations = face_recognition.face_locations(rgb_small_frame)
face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
```
<p align="justify">É na base destes comandos, que se baseiam em modelos extreamemte eficientes treinados com deep learning, que o programa irá funcionar. Aqui são encontradas todas as localizações de caras no _frame_ e sofrem um _encoding_ para posteriormente serem comparadas com as caras guardadas na <i>Database</i>. Se o programa encontrar um nível de parecença elevado com alguma das informações da base de dados, irá reconhecer e cumprimentar a pessoa detetada. Além disto, o programa ainda faz o seguimento de cada pessoa.</p>
<p align="justify">Ao mesmo tempo, um menu no Terminal estará a correr em pararelo (usando a biblioteca <b>Threading</b>) onde se poderá dar nome às pessoas detetadas como desconhecidas e ainda alterar o nome de qualquer pessoa presente na <i>Database</i>.</p>

---
## Autores

Estes foram os contribuidores para este projeto:

- **[Afonso Miranda](https://github.com/afonsosmiranda)**
  - Informação:
    - Email: afonsoduartem@ua.pt
    - Número Mecanográfico: 100090

- **[João Nogueiro](https://github.com/joaonogueiro)**
  - Informação:
    - Email: joao.nogueiro@ua.pt
    - Número Mecanográfico: 111807

- **[Ricardo Bastos](https://github.com/RBastos36)**
  - Informação:
    - Email: r.bastos@ua.pt
    - Número Mecanográfico: 103983
