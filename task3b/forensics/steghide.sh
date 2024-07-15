#!/bin/bash

# Installing steghide
sudo apt-get install -y steghide 

# Check installation
steghide

# Create the text file to be embedded 
touch "flag.txt"
echo "Congrats! Here's your flag" > flag.txt

# Embed the file using steghide
steghide embed -ef flag.txt -ef mystery.png

# Check whether a file is embedded or not
steghide info mystery.png

# Extract the data
steghide extract -sf mystery.png
