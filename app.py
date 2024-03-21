from flask import Flask, request, render_template
import os
import subprocess

app = Flask(__name__)

# Define la carpeta de carga de archivos
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define las extensiones de archivo permitidas
ALLOWED_EXTENSIONS = {'stl'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Verifica si la solicitud POST tiene la parte del archivo
        if 'file' not in request.files:
            return 'No se ha seleccionado ningún archivo'
        file = request.files['file']
        # Si el usuario no selecciona un archivo, el navegador también
        # envía una parte vacía sin nombre de archivo
        if file.filename == '':
            return 'No se ha seleccionado ningún archivo'
        if file and allowed_file(file.filename):
            # Guarda el archivo subido
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            # Ejecuta el código de Python para calcular el área
            try:
                result = subprocess.check_output(['python', 'volume_calculator.py', filename, 'area'])
                return f'El área de {file.filename} es {result.decode("utf-8")}'
            except subprocess.CalledProcessError:
                return 'Error al ejecutar el código de Python'
    return render_template('upload.html')  # Crea una plantilla HTML para el formulario de carga

if __name__ == '__main__':
    app.run(debug=True)