from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import RegistroAdubacao
from .services import GeminiService
from django.views.generic import TemplateView
from .models import RegistroAdubacao, FornecedorResiduo
from django.views.generic import TemplateView
from django.db.models import Sum, Avg


class Dashboard(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Dados Principais (Ordenados por data para consistência visual)
        registros = RegistroAdubacao.objects.all().order_by('area__nome_local')
        fornecedores = FornecedorResiduo.objects.all()

        # 1. Preparação para Gráficos de Linha/Barra (Talhões)
        # Usamos list comprehension para criar listas simples que o JS entende
        context['labels_areas'] = [r.area.nome_local.replace(' – UEFS', '') for r in registros]
        context['data_ph_pre'] = [float(r.ph_pre_aplicacao) for r in registros]
        context['data_ph_pos'] = [float(r.ph_pos_aplicacao) for r in registros]
        context['data_ndvi'] = [float(r.ndvi_pos_aplicacao) for r in registros]
        context['data_residuos_area'] = [float(r.peso_residuos_kg) for r in registros]

        # 2. Preparação para Gráfico de Pizza (Fornecedores)
        context['labels_fornecedores'] = [f.nome_mercado for f in fornecedores]
        context['data_residuos_fornecedores'] = [float(f.residuo_mensal_kg) for f in fornecedores]

        # 3. KPIs (Cards do Topo) - Cálculos de negócio
        total_kg = registros.aggregate(Sum('peso_residuos_kg'))['peso_residuos_kg__sum'] or 0
        media_ndvi = registros.aggregate(Avg('ndvi_pos_aplicacao'))['ndvi_pos_aplicacao__avg'] or 0
        # Calculando melhoria média do pH
        avg_pre = registros.aggregate(Avg('ph_pre_aplicacao'))['ph_pre_aplicacao__avg'] or 0
        avg_pos = registros.aggregate(Avg('ph_pos_aplicacao'))['ph_pos_aplicacao__avg'] or 0
        melhoria_ph = ((avg_pos - avg_pre) / avg_pre * 100) if avg_pre else 0

        context['kpi_total_kg'] = f"{total_kg:,.0f}".replace(',', '.')
        context['kpi_media_ndvi'] = f"{media_ndvi:.2f}"
        context['kpi_melhoria_ph'] = f"+{melhoria_ph:.1f}%"

        return context
    


class ConsultaIaImpacto(View):

    def get(self, registro_id):
        try:
            registro = RegistroAdubacao.objects.get(id=registro_id)
            gemini = GeminiService()
            
            # Chama a IA
            analise = gemini.analisar_impacto_solo(registro)
            
            return JsonResponse({
                'status': 'sucesso',
                'analise': analise,
                'id': registro_id
            })
        except RegistroAdubacao.DoesNotExist:
            return JsonResponse({'status': 'erro', 'message': 'Registro não encontrado'}, status=404)

