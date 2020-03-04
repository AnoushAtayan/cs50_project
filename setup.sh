#!/bin/bash

#install the  Python 3.6 distribution
sudo apt-get update
sudo apt-get install python3.6

#install pip for Python 3.6 version
sudo apt-get install -y python3-pip
sudo apt-get install build-essential libssl-dev libffi-dev python-dev

#install virtual environment
sudo apt-get install -y python3-venv

#create virtual environment
python3 -m venv venv

#install make
sudo apt install make
sudo apt install make-guile

#install default java
sudo apt-get install default-jre
sudo apt-get install default-jdk

#install tesseract
sudo apt-get install tesseract-ocr libtesseract-dev libleptonica-dev pkg-config
sudo apt-get install tesseract-ocr-eng

#activate virtual environment
source venv/bin/activate
