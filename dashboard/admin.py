from django.contrib import admin
from .models import FornecedorResiduo, AreaAplicacao, RegistroAdubacao

@admin.register(FornecedorResiduo)
class FornecedorResiduoAdmin(admin.ModelAdmin):
    list_display = ('nome_mercado', 'cnpj', 'residuo_semanal_kg', 'residuo_mensal_kg')
    search_fields = ('nome_mercado', 'cnpj')
    list_filter = ('nome_mercado',)

@admin.register(AreaAplicacao)
class AreaAplicacaoAdmin(admin.ModelAdmin):
    list_display = ('nome_local', 'tipo_solo')
    search_fields = ('nome_local',)

@admin.register(RegistroAdubacao)
class RegistroAdubacaoAdmin(admin.ModelAdmin):
    # Organiza as colunas no painel admin para facilitar a leitura dos resultados
    list_display = (
        'area', 
        'data_hora_inicio', 
        'peso_residuos_kg', 
        'ph_pre_aplicacao', 
        'ph_pos_aplicacao', 
        'ndvi_pos_aplicacao'
    )
    
    # Filtros laterais para facilitar a análise por Talhão ou por data
    list_filter = ('area', 'data_hora_inicio')
    
    # Permite pesquisar pelo nome do local ou pelo resultado da análise
    search_fields = ('area__nome_local', 'resultado_analise')
    
    # Organiza os campos dentro do formulário de edição por categorias
    fieldsets = (
        ('Dados da Operação', {
            'fields': ('area', 'data_hora_inicio', 'data_hora_fim', 'peso_residuos_kg')
        }),
        ('Análise de Impacto (IA & Campo)', {
            'fields': ('ph_pre_aplicacao', 'ph_pos_aplicacao', 'ndvi_pos_aplicacao', 'resultado_analise'),
            'description': 'Estes dados alimentam os gráficos do Chart.js e as análises do Gemini.'
        }),
    )