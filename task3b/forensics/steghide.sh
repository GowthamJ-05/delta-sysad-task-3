#!/bin/bash

base64 < your_text_file.txt > encoded_text.txt
convert mystery.png -set comment "$(cat encoded_text.txt)" mystery_with_text.png
exiftool -comment output_with_text.png
