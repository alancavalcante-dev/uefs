import google.generativeai as genai
from django.conf import settings

class GeminiService:
    def __init__(self):
        # Configure sua chave no settings.py ou .env
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        

    def analisar_impacto_solo(self, registro):
        """
        Envia os dados do RegistroAdubacao para o Gemini analisar.
        """
        prompt = f"""
        Como especialista em agronomia e sustentabilidade, analise os seguintes dados:
        - Local: {registro.area.nome_local} ({registro.area.tipo_solo})
        - Peso de Resíduos Aplicados: {registro.peso_residuos_kg} kg
        - pH Inicial: {registro.ph_pre_aplicacao}
        - pH Final: {registro.ph_pos_aplicacao}
        - Índice NDVI Final: {registro.ndvi_pos_aplicacao}

        Com base nesses dados das planilhas UEFS, forneça:
        1. O impacto estimado na neutralização da acidez.
        2. Uma estimativa da redução de CO2 baseada no volume de resíduos.
        3. Recomendações técnicas para a próxima safra.
        Resposta curta e técnica para dashboard.
        """
        
        response = self.model.generate_content(prompt)
        return response.text