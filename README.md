getyourcam 📸

Capture imagens e localizações diretamente do navegador de seus visitantes com getyourcam. Uma ferramenta poderosa e discreta para coletar informações visuais e geográficas.


🌟 Recursos

    Captura de Imagem: Acesse a câmera do dispositivo e capture imagens em tempo real.
    Geolocalização: Obtenha a localização precisa do dispositivo.
    Visualização de Dados: Acesse a rota /consulta para visualizar todas as imagens e localizações capturadas em uma interface amigável.
    Segurança: Proteção por senha para acessar os dados coletados.
    Link Externo: Com o script start.sh, obtenha um link externo via Serveo para acessar sua aplicação de qualquer lugar.

🚀 Começando
Pré-requisitos

    Python 3.x
    Flask
    geoip2

Instalação

    Clone o repositório:

    bash

git clone https://github.com/seuusername/getyourcam.git

Entre no diretório do projeto:

bash

cd getyourcam

Instale as dependências:

bash

pip install -r requirements.txt

Execute o script para iniciar a aplicação e obter o link externo:

bash

    ./start.sh

    Acesse o link fornecido pelo Serveo ou, localmente, vá para http://localhost:5000.

🛠️ Consultar capturas:

    Acesso: Acesse a url gerada pelo serveo que apareceu para você na tela ex: https:/aj1249241iurqw.serveo.net/consulta.
    usuario: admin
    senha: secret (vc pode mudar no app.py o usuario e senha)
    Geolocalização: Utilize a base de dados GeoLite2 para obter informações detalhadas sobre os IPs coletados.
 
 Geolite2
 O módulo `geoip2` utiliza um banco de dados gratuito da Maxmind chamado "GeoLite2-City.mmdb
    Como o nosso sistema usa o Geolite2, você precisa acessar o site https://www.maxmind.com/
    E baixar o arquivo de licença gratuita "GeoLite2-City.mmdb" e coloca na raiz do projeto.

📜 Licença

    Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

🤝 Contribuições

    Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.