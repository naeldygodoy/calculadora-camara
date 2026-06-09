import streamlit as st
import math

# Configuração da página web
st.set_page_config(page_title="Calculadora Frigelar - Câmaras Frias", layout="wide")

st.title("❄️ Calculadora de Câmaras Frias (Módulo Completo)")
st.subheader("Gerador de Orçamentos Rápido e Técnico")
st.markdown("---")

# Layout em duas colunas: Entrada de dados na esquerda, Resultado na direita
col_esquerda, col_direita = st.columns([1, 1.3])

with col_esquerda:
    st.header("1. Dados da Câmara")
    
    comp_ext = st.number_input("Comprimento Externo (metros):", min_value=1.0, value=10.0, step=0.1)
    larg_ext = st.number_input("Largura Externa (metros):", min_value=1.0, value=7.0, step=0.1)
    alt_ext = st.number_input("Altura Externa (metros):", min_value=1.0, value=3.0, step=0.1)
    
    st.markdown("---")
    
    isolamento = st.selectbox("Tipo de Isolamento (Paredes/Teto):", ["EPS", "PIR"])
    temp_desejada = st.selectbox("Temperatura da Câmara:", [
        "0ºC a 15ºC (Resfriados)", 
        "-20ºC (Congelados)", 
        "Abaixo de -20ºC (Sorvetes/Túneis)"
    ])
    
    st.markdown("---")
    st.header("🚪 2. Configuração da Porta")
    
    # Seleção do Tipo de Movimento da Porta
    tipo_movimento = st.radio("Tipo de Porta:", ["Girar", "Correr"], horizontal=True)
    
    # Seleção de tamanho da porta
    tamanho_porta = st.selectbox("Tamanho da Porta (L x A):", ["0,80 x 1,80", "1,00 x 2,00"])
    larg_p, alt_p = (0.80, 1.80) if tamanho_porta == "0,80 x 1,80" else (1.00, 2.00)
    
    # Seleção de Batente (Válido para Girar e Correr)
    tipo_batente = st.radio("Modelo de Batente:", ["3B", "4B"], horizontal=True)
    
    # Regra de Reversibilidade e Lados
    if tipo_movimento == "Girar" and tipo_batente == "4B":
        detalhe_porta = "De Girar 4B (Reversível)"
        st.caption("ℹ️ O modelo 4B de girar é nativamente reversível na montagem.")
    else:
        texto_lado = "Lado de Abertura" if tipo_movimento == "Girar" else "Sentido de Correr"
        lado_selecionado = st.radio(f"{texto_lado} (Olhando por Fora):", ["Direita", "Esquerda"], horizontal=True)
        detalhe_porta = f"De {tipo_movimento} {tipo_batente} (Lado: {lado_selecionado})"
        
    # Regra de resistência baseada na temperatura
    if "Resfriados" in temp_desejada:
        resistencia_porta = "Sem resistência"
    else:
        resistencia_porta = "Com Resistência (Aquecimento de Batente)"

# ================= REGRAS DE NEGÓCIO E ESPESSURAS =================
if isolamento == "EPS":
    larg_modulo = 1.14
    if "Resfriados" in temp_desejada:    espessura_teto = 0.10
    elif "Congelados" in temp_desejada:  espessura_teto = 0.15
    else:                                espessura_teto = 0.20
else: # PIR
    larg_modulo = 1.12
    if "Resfriados" in temp_desejada:    espessura_teto = 0.07
    elif "Congelados" in temp_desejada:  espessura_teto = 0.12
    else:                                espessura_teto = 0.15

if "Resfriados" in temp_desejada:
    espessura_piso_eps = 0.10
    camadas_piso = "2 camadas de 5cm (5+5)"
elif "Congelados" in temp_desejada:
    espessura_piso_eps = 0.15
    camadas_piso = "1 camada de 5cm + 1 camada de 10cm (5+10)"
else:
    espessura_piso_eps = 0.20
    camadas_piso = "2 camadas de 10cm (10+10)"

# ================= CÁLCULO VOLUMÉTRICO E GEOMÉTRICO =================
comp_int = comp_ext - (2 * espessura_teto)
larg_int = larg_ext - (2 * espessura_teto)
alt_int = alt_ext - espessura_teto - espessura_piso_eps - 0.10 
volume_interno = comp_int * larg_int * alt_int

if "Resfriados" in temp_desejada:
    estocagem_ton = (volume_interno * 250 * 0.8) / 1000
    texto_estocagem = f"**{estocagem_ton:.2f} Toneladas**"
elif "Congelados" in temp_desejada:
    estocagem_ton = (volume_interno * 400 * 0.8) / 1000
    texto_estocagem = f"**{estocagem_ton:.2f} Toneladas**"
else:
    texto_estocagem = "⚠️ **Definir conforme movimentação**"

# ================= QUANTITATIVOS DE PAINÉIS E PISO =================
alt_painel = alt_ext - espessura_teto
total_placas_comp = math.ceil(math.ceil((comp_ext / larg_modulo) * 2) / 2 * 2)
total_placas_larg = math.ceil(math.ceil((larg_int / larg_modulo) * 2) / 2 * 2)
total_paineis_parede = total_placas_comp + total_placas_larg

total_paineis_teto = math.ceil(comp_ext / larg_modulo)
comprimento_painel_teto = larg_ext

area_externa = comp_ext * larg_ext
placas_piso_por_camada = math.ceil(area_externa / 1.15)

if "Resfriados" in temp_desejada:
    chapas_5cm, chapas_10cm = placas_piso_por_camada * 2, 0
elif "Congelados" in temp_desejada:
    chapas_5cm, chapas_10cm = placas_piso_por_camada, placas_piso_por_camada
else:
    chapas_5cm, chapas_10cm = 0, placas_piso_por_camada * 2

# ================= LOGICA DOS ACESSÓRIOS CORRIGIDA =================
trilho_inox_pcs = math.ceil(larg_p)
suporte_trilho_pcs = trilho_inox_pcs * 6

altura_tira = alt_p + 0.10
metragem_total_cortina = suporte_trilho_pcs * altura_tira
metragem_comercial_cortina = math.ceil(metragem_total_cortina / 10.0) * 10

espessura_cm = round(espessura_teto * 100)
if espessura_cm in [7, 10]:
    modelo_cantoneira = "40 x 140"
elif espessura_cm in [12, 15]:
    modelo_cantoneira = "40 x 190"
else:
    modelo_cantoneira = "40 x 240"

perimetro_ext = (comp_ext * 2) + (larg_ext * 2)
metragem_cantoneira = perimetro_ext + (4 * alt_ext)
barras_cantoneira_ext = math.ceil(metragem_cantoneira / 3.0)
barras_cantoneira_int = barras_cantoneira_ext

vao_porta = (larg_p * 2) + (alt_p * 2)
metragem_perfil_u = perimetro_ext + vao_porta
barras_perfil_u = math.ceil(metragem_perfil_u / 3.0)

total_barras_perfis = barras_cantoneira_ext + barras_cantoneira_int + barras_perfil_u
total_rebites_unidades = total_barras_perfis * 12
centos_rebites = math.ceil(total_rebites_unidades / 100)

total_metragem_perfis = (metragem_cantoneira * 2) + metragem_perfil_u
tubos_selante = math.ceil(total_metragem_perfis / 3.0)

area_manta = (comp_ext + 0.5) * (larg_ext + 0.5)
rolos_manta = math.ceil(area_manta / 10.0)
baldes_hidroasfalto = math.ceil(rolos_manta / 3.0)
pecas_lona = math.ceil((area_externa * 2) / 20.0)
spray_pu_pcs = 10

# ================= EXIBIÇÃO DOS RESULTADOS =================
with col_direita:
    st.header("2. Relatório Técnico de Materiais")
    
    st.info(f"""
    📐 **Dimensões Internas Úteis:** {comp_int:.2f}m (C) x {larg_int:.2f}m (L) x {alt_int:.2f}m (A)  
    📦 **Volume Interno Útil:** {volume_interno:.2f} m³  
    ⚖️ **Previsão de Estocagem:** {texto_estocagem}
    """)
    
    st.markdown("---")
    st.markdown("### 📋 Lista de Materiais (Isolamento)")
    
    # CORREÇÃO DO VALUEERROR: Mudança manual de :.2m para :.2f
    dados_tabela = [
        {"Item": "Total de painéis de parede", "Quantidade": f"{total_paineis_parede} pçs", "Descrição": f"Painéis de {alt_painel:.2f}m x {larg_modulo:.2f}m x {espessura_teto:.2f}m"},
        {"Item": "Total de painéis de teto", "Quantidade": f"{total_paineis_teto} pçs", "Descrição": f"Painéis de {comprimento_painel_teto:.2f}m x {larg_modulo:.2f}m x {espessura_teto:.2f}m"},
        {"Item": "Total de chapas de piso (EPS 5cm)", "Quantidade": f"{chapas_5cm} pçs", "Descrição": "Chapas de 1,15m x 1,00m x 0,05m"},
        {"Item": "Total de chapas de piso (EPS 10cm)", "Quantidade": f"{chapas_10cm} pçs", "Descrição": "Chapas de 1,15m x 1,00m x 0,10m"},
        {"Item": f"Porta Frigorífica {tamanho_porta}", "Quantidade": "1 pç", "Descrição": f"Modelo {detalhe_porta} | {resistencia_porta}"}
    ]
    st.table(dados_tabela)
    
    st.markdown("### 🛠️ 3. Acessórios de Isolamento e Portas")
    
    # CORREÇÃO DO KEYERROR: Removido o dicionário fantasma 'res_acessorios' e mapeado para as variáveis reais
    tabela_acessorios = [
        {"Item": "Trilho Inox", "Quantidade": f"{trilho_inox_pcs} pç", "Descrição": f"Trilho comercial de {trilho_inox_pcs:.2f}m para vão de {larg_p:.2f}m"},
        {"Item": "Suporte de Trilho", "Quantidade": f"{suporte_trilho_pcs} pçs", "Descrição": "Fixadores do trilho (Garante 6 pçs por metro linear de barra)"},
        {"Item": "Cortina Plástica Polar", "Quantidade": f"{metragem_comercial_cortina} metros", "Descrição": f"Tiras cortadas com {alt_p + 0.10:.2f}m (Venda fracionada múltiplo de 10m)"},
        {"Item": f"Cantoneira Externa {modelo_cantoneira}", "Quantidade": f"{barras_cantoneira_ext} barras", "Descrição": "Acabamento de cantos externos | Barras de 3,00m"},
        {"Item": "Cantoneira Interna 40 x 40", "Quantidade": f"{barras_cantoneira_int} barras", "Descrição": f"Modelo {modelo_cantoneira} conforme espessura | Barras de 3,00m"},
        {"Item": f"Perfil U 40 x {espessura_cm} x 40", "Quantidade": f"{barras_perfil_u} barras", "Descrição": "Perfil de base e contorno do vão | Barras de 3,00m"},
        {"Item": "Rebite Repuxo Alumínio Branco (312)", "Quantidade": f"{centos_rebites} centos", "Descrição": "Fixador 3.2 x 12mm (Calculado 12 pçs por barra de acabamento)"},
        {"Item": "Selante PU", "Quantidade": f"{tubos_selante} tubos", "Descrição": "Vedação profissional de juntas de poliuretano/vedação externa"},
        {"Item": "Manta Asfáltica", "Quantidade": f"{rolos_manta} rolos", "Descrição": f"Impermeabilização c/ dobra de segurança (Área considerada c/ sobra: {area_manta:.2f}m²)"},
        {"Item": "Hidroasfalto", "Quantidade": f"{baldes_hidroasfalto} balde(s)", "Descrição": "Primer de aderência (Proporção de 1 balde a cada 3 rolos de manta)"},
        {"Item": "Lona Plástica", "Quantidade": f"{pecas_lona} pçs", "Descrição": "Proteção complementar de piso (Peças de 20m² aplicadas em 2 camadas)"},
        {"Item": "Poliuretano Spray", "Quantidade": f"{spray_pu_pcs} pçs", "Descrição": "Espuma expansiva p/ junções e falhas térmicas (Padrão de obra)"},
    ]
    st.table(tabela_acessorios)
    
    st.info("""
    💡 **INFORMAÇÃO IMPORTANTE:** Os dados e quantitativos apresentados neste relatório foram consolidados com base na análise técnica dos parâmetros fornecidos pelo cliente, o qual é inteiramente responsável pela exatidão das dimensões e especificações de entrada do projeto.
    """)
