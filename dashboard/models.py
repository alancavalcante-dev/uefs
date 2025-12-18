from django.db import models

from django.db import models


# 1. Comércios (Origem dos Resíduos) - Baseado na Tabela_Mercados_Residuos.xlsx
class FornecedorResiduo(models.Model):
    nome_mercado = models.CharField(max_length=255) # 
    cnpj = models.CharField(max_length=18, unique=True) # 
    compra_semanal_kg = models.DecimalField(max_digits=15, decimal_places=2) # 
    residuo_semanal_kg = models.DecimalField(max_digits=15, decimal_places=2) # 
    residuo_mensal_kg = models.DecimalField(max_digits=15, decimal_places=2) # 

    def __str__(self):
        return self.nome_mercado



# 2. Áreas de Estudo/Aplicação - Locais na UEFS
class AreaAplicacao(models.Model):
    nome_local = models.CharField(max_length=255) 
    tipo_solo = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome_local



# 3. Operação e Impacto - Baseado em Dados_Sistema_Aplicabilidade_Adubo_UEFS.xlsx
class RegistroAdubacao(models.Model):
    area = models.ForeignKey(AreaAplicacao, on_delete=models.CASCADE)
    data_hora_inicio = models.DateTimeField() # 
    data_hora_fim = models.DateTimeField() # 
    peso_residuos_kg = models.DecimalField(max_digits=15, decimal_places=2) # 
    
    # Análises Técnicas (Input para a IA e Gráficos)
    ph_pre_aplicacao = models.DecimalField(max_digits=4, decimal_places=2) # 
    ph_pos_aplicacao = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True) # 
    ndvi_pos_aplicacao = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True) # 
    resultado_analise = models.TextField() # Descrição detalhada 
    
    def __str__(self):
        return f"Adubação em {self.area.nome_local} - {self.data_hora_inicio.date()}"