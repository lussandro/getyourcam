#!/bin/bash


ssh -R 80:localhost:5000 serveo.net > serveo.log 2>&1 &

# Aguardar alguns segundos para garantir que o Serveo tenha iniciado
sleep 5


url=$(grep -o 'Forwarding.*' serveo.log | sed 's/Forwarding //;s/ ->.*//')

echo "*"
echo "*"
echo "*****************************************************"
echo "** Acesse a aplicação em: $url"
echo "*****************************************************"
echo "*"
echo "*"
python3 app.py
