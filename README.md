# SAVI - Practical Assignment 1
Advanced Industrial Visualization Systems (Sistemas Avançados de Visualização Industrial) - Group 6 - University of Aveiro - 2023/24

## Table of Contents

- [Introduction](#introduction)
- [Libraries Used](#libraries-used)
- [Installation](#installation)
- [Code Explanation](#code-explanation)
- [Authors](#authors)

---
## Introduction

<p align="justify"> In this assignment, a program has been created capable of detecting and tracking faces of individuals approaching the camera, recognizing and greeting people already saved in the Database and questioning strangers about their names. Regarding additional options, the user has the possibility of changing the names of individuals previously registered in the Database.</p>

[SAVI - TP1 - Demo](https://github.com/RBastos36/SAVI-TP1/assets/145439743/68df23d6-3c08-4bec-b5fc-8decbdaa8c51)

<p align="center">
Demonstration of how the program works.
</p>


---
## Libraries Used

To run the program and scripts presented in this repository, some libraries need to be installed beforehand. These are the following:

- **OpenCV**
  - Description: this library allows for easy problem solving involving image processing and computer vision.
  - Installation:
    ```bash
    sudo apt-get install python3-opencv
    ```

- **Face-Recognition**
  - Description: library that provides functions to recognize and manipulate faces using models created through deep learning.
  - Installation:
    ```bash
    pip3 install face_recognition
    ```

- **PyTTSx3**
  - Description: library used to convert text to speech, with the ability to work offline. This library is compatible with Pyhton 2 and 3.
  - Installation:
    ```bash
    pip install pyttsx3
    ```

- **Threading**
  - Description: this library allows to introduce a sequence of instructions that can be executed independently from the rest of the process.
  - Installation: This library already comes available with Python 3.7 and above.


---
## Installation

The program can be installed by following the steps below:

1. Clone the repository:
```bash
git clone https://github.com/joaonogueiro/TP1_SAVI
```
2. Change into the project directory:
```bash
cd SAVI-TP1
```
3. Run the program:
```bash
./main.py
```

If the steps presented above are followed, the program should run with no problems.


---
## Code Explanation

<p align="justify"> The code begins to verify if there is any information inside the Database and, if it finds any, reads it. Afterwards, the camera is initialized and begins detecting faces using the commands below, based on the <b>Face-Recognition</b> library.</p>

```python
# Find all the faces and face encodings in the current frame of video
face_locations = face_recognition.face_locations(rgb_small_frame)
face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
```

<p align="justify">It is based on these commands, which rely on extremely efficient models trained with deep learning, that the program will mainly operate. Here, all face locations in the frame are identified and undergo an encoding for later comparison with the faces stored in the Database. If the program finds a high enough similarity level with any information in the Database, it will recognize and greet the person detected. Additionally, the program also tracks each individual.</p>

<p align="justify">At the same time, a menu in the Terminal will be running in parallel (using the <b>Threading</b> library), allowing the user to name each unknown individual and also change the name of any person present in the Database.</p>

---
## Authors

These are the contributors who made this project possible:

- **[Afonso Miranda](https://github.com/afonsosmiranda)**
  - Information:
    - Email: afonsoduartem@ua.pt
    - NMec: 100090

- **[João Nogueiro](https://github.com/joaonogueiro)**
  - Information:
    - Email: joao.nogueiro@ua.pt
    - NMec: 111807

- **[Ricardo Bastos](https://github.com/RBastos36)**
  - Information:
    - Email: r.bastos@ua.pt
    - NMec: 103983
