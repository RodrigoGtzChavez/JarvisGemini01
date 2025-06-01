from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Configuración de entorno y seguridad
env_path = Path(_file_).parent / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(_name_)
CORS(app)

# Configura el sistema de log para seguimiento de errores
logging.basicConfig(level=logging.ERROR)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logging.error("GEMINI_API_KEY no está configurada en el archivo .env")
    raise ValueError("La clave API de Gemini no está configurada.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def validar_entrada(data):
    """Valida que los valores sean correctos antes de enviarlos al modelo"""
    try:
        data['income'] = float(data.get('income', 0))
        data['expenses'] = float(data.get('expenses', 0))
        data['debts'] = float(data.get('debts', 0))
        data['goals'] = str(data.get('goals', ""))
        data['skills'] = str(data.get('skills', ""))
        return data
    except ValueError:
        return None

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    data = request.json
    data_validada = validar_entrada(data)

    if not data_validada:
        return jsonify({"error": "Datos de entrada inválidos. Verifica los valores numéricos."}), 400

    prompt = f"""
Actúa como Jarvis Financiero, un asesor personalizado.
Usuario:
- Ingresos mensuales: {data_validada['income']}
- Gastos mensuales: {data_validada['expenses']}
- Deudas: {data_validada['debts']}
- Metas: {data_validada['goals']}
- Habilidades e intereses: {data_validada['skills']}

Genera un plan financiero estratégico, claro, con pasos concretos para avanzar hacia la paz financiera.
"""

    try:
        response = model.generate_content(prompt)
        plan = response.text if response.candidates else "No se pudo generar el plan."
        return jsonify({"plan": plan})
    except Exception as e:
        logging.error(f"Error al generar el plan financiero: {str(e)}")
        return jsonify({"error": "Ocurrió un problema interno al generar el plan."}), 500

if _name_ == '_main_':
    app.run(debug=True, port=5000)
