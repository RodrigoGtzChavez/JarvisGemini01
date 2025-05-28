from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
CORS(app)

# Configura la API de Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY no está configurada en el archivo .env")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    data = request.json
    income = data.get('income')
    expenses = data.get('expenses')
    debts = data.get('debts')
    goals = data.get('goals')
    skills = data.get('skills')

    prompt = f"""
Actúa como Jarvis Financiero, un asesor personalizado.
Usuario:
- Ingresos mensuales: {income}
- Gastos mensuales: {expenses}
- Deudas: {debts}
- Metas: {goals}
- Habilidades e intereses: {skills}

Genera un plan financiero estratégico, claro, con pasos concretos para avanzar hacia la paz financiera.
"""

    try:
        response = model.generate_content(prompt)
        plan = response.text if response.candidates else "No se pudo generar el plan."
        return jsonify({"plan": plan})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
