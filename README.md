# Automated Color Identification System Using Computer Vision

## Project Overview

This project develops an assistive system that identifies colors in real time using computer vision and embedded electronics. Designed to support people with color blindness, it combines image processing with microcontroller communication to provide accessible, multisensory feedback.

The system captures images through a webcam, detects the color at a selected point, and displays the identified color on an LCD screen while activating the corresponding RGB LED.

## Key Features

- **Real-Time Color Detection:** Identifies 12 basic colors using Python and OpenCV.
- **Computer Vision:** Processes webcam images and analyzes pixel values in HSV color space.
- **Embedded Systems Integration:** Connects computer vision software with microcontrollers.
- **LCD Display:** Shows the detected color name.
- **RGB LED Feedback:** Visually represents the identified color.
- **Serial Communication:** Transfers color data between the computer and Arduino using UART and between microcontrollers using I2C.
- **Assistive Technology:** Explores an affordable solution to make color identification more accessible.

## System Architecture

The project consists of three main modules:

1. **Python and OpenCV:** Captures webcam images, analyzes a selected region, classifies the detected color, and transmits the results through a serial connection.
2. **Arduino:** Receives color data from the computer and forwards the information to the PIC microcontroller.
3. **PIC16F877A:** Processes the received data and controls the RGB LEDs to provide visual feedback.

The identified color is also displayed on a 16×2 LCD connected directly to the Arduino.

## Technologies and Tools

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![Arduino](https://img.shields.io/badge/Arduino-00979D?style=flat-square&logo=arduino&logoColor=white)
![C](https://img.shields.io/badge/C-A8B9CC?style=flat-square&logo=c&logoColor=black)
![Serial Communication](https://img.shields.io/badge/UART%20%7C%20I2C-555555?style=flat-square)
![Embedded Systems](https://img.shields.io/badge/Embedded%20Systems-006699?style=flat-square)

**Software and development tools**
- Python 3.x
- OpenCV 4.5
- PySerial 3.5
- Arduino IDE
- CCS C Compiler

**Hardware components**
- Arduino development board
- PIC16F877A microcontroller
- Webcam
- 16×2 LCD display
- Red, green, and blue LEDs
- Electronic components and connecting wires

## Communication Protocols

- **UART:** Serial communication between the computer and Arduino.
- **I2C:** Communication between the Arduino and PIC16F877A microcontroller.

## Results

Functional testing demonstrated successful integration of image processing, serial communication, microcontroller control, and visual output. The report describes response times below 500 milliseconds and identifies opportunities for future improvements, including object detection and a custom printed circuit board (PCB).

## Future Improvements

- Extend detection beyond individual colors to objects and their surroundings.
- Improve robustness under different lighting conditions.
- Design a custom PCB to reduce electrical noise.
- Further optimize processing latency and system reliability.

## Authors

- Natalia Ochoa
- Samuel López
- Nicolás Clavijo

La Sabana University
