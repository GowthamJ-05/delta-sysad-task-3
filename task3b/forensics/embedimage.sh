#!/bin/bash

sudo apt install imagemagick exiftool -y


touch flag.txt
echo "Congrats! Here's your flag" > flag.txt

base64 < flag.txt > encoded_text.txt
convert mystery.png -set comment "$(cat encoded_text.txt)" mystery_with_text.png
exiftool -comment mystery_with_text.png
