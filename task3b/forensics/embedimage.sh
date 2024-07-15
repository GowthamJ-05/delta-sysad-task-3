#!/bin/bash


touch flag.txt
echo "Congrats! Here's your flag" > flag.txt

base64 < flag.txt > encoded_text.txt
convert mystery.png -set comment "$(cat encoded_text.txt)" mystery_with_text.png
exiftool -comment output_with_text.png
