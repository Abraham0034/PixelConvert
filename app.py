from flask import Flask, render_template, request, send_file, jsonify
import os
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/convertir", methods=["POST"])
def convertir():
    if 'imagenes' not in request.files:
        return jsonify({'error': 'No se encontraron imágenes'}), 400
    
    archivos = request.files.getlist('imagenes')
    formato_destino = request.form.get('formato', 'JPEG').upper()
    
    if not archivos or archivos[0].filename == '':
        return jsonify({'error': 'No hay archivos seleccionados'}), 400
    
    archivos_convertidos = []

    for file in archivos:
        if file.filename:
            ruta_original = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(ruta_original)
            
            nombre_base, _ = os.path.splitext(file.filename)
            nombre_salida = f"{nombre_base}.{formato_destino.lower()}"
            ruta_salida = os.path.join(CONVERTED_FOLDER, nombre_salida)
            
            try:
                with Image.open(ruta_original) as img:
                    if formato_destino == 'JPEG' and img.mode in ('RGBA', 'LA'):
                        img = img.convert('RGB')
                    img.save(ruta_salida, formato_destino)
                archivos_convertidos.append(nombre_salida)
            except Exception as e:
                print(f"Error al procesar {file.filename}:", e)

    return jsonify({'convertidos': archivos_convertidos})

@app.route("/descargar/<filename>")
def descargar(filename):
    return send_file(os.path.join(CONVERTED_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)