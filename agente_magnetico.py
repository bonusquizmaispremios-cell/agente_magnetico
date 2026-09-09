import streamlit as st
from groq import Groq
from datetime import datetime, timedelta
import re
import os
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="AGENTE MAGNÉTICO", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F8F9FA; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#495057,#343A40) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#343A40,#212529) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#1A1A2E !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F1F3F5,#E9ECEF); padding:20px; border-radius:14px; border:1px solid #CED4DA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#1A1A2E !important; }

    .card-dark { background:linear-gradient(135deg,#E9ECEF,#DEE2E6); padding:20px; border-radius:14px; border:1px solid #ADB5BD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#1A1A2E !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #CED4DA; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#1A1A2E !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #CED4DA; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#1A1A2E !important; }

    .badge { background:#495057; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#CED4DA,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #CED4DA; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#1A1A2E !important; }

    .chat-persona { background:#F8F9FA; border:1px solid #CED4DA; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#1A1A2E !important; }

    .questao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#1A1A2E !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#1A1A2E !important; }

    .meta-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#1A1A2E !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
""", unsafe_allow_html=True)

# --- PERSISTÊNCIA LOCAL (JSON) ---
def gerar_json_sessao() -> str:
    """Serializa historico + biblioteca em JSON para download."""
    dados = {
        'usuario': st.session_state.usuario,
        'historico': st.session_state.historico,
        'biblioteca': st.session_state.biblioteca,
        'resumo_semanal': st.session_state.resumo_semanal,
        'resumo_gerado_em': st.session_state.resumo_gerado_em,
        'plano_conquista': st.session_state.plano_conquista,
        'plano_pessoa': st.session_state.plano_pessoa,
        'salvo_em': datetime.now().strftime('%d/%m/%Y %H:%M'),
    }
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados: dict):
    """Restaura sessão a partir do JSON carregado."""
    st.session_state.historico       = dados.get('historico', [])
    st.session_state.biblioteca      = dados.get('biblioteca', [])
    st.session_state.resumo_semanal  = dados.get('resumo_semanal', '')
    st.session_state.resumo_gerado_em= dados.get('resumo_gerado_em', None)
    st.session_state.plano_conquista = dados.get('plano_conquista', '')
    st.session_state.plano_pessoa    = dados.get('plano_pessoa', '')

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa': "Login",
    'usuario': "", 'api_key': "",
    'pagina': "Home",
    'modo_confianca': False,
    'modo_dark': False,
    'historico': [],
    'biblioteca': [],
    'roleplay_hist': [],
    'roleplay_ativo': False,
    'roleplay_perfil': '',
    'roleplay_situacao': '',
    'resumo_semanal': "",
    'resumo_gerado_em': None,
    'plano_conquista': "",
    'plano_pessoa': "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- MOTOR DE IA ---
def mentor_milhao(prompt_usuario, sistema_extra="", historico_msgs=None):
    try:
        client = Groq(api_key=st.session_state.api_key)
        confianca = (
            "MODO CONFIANÇA ATIVADO: Respostas curtas, firmes, sem insegurança, mais diretas e dominantes."
            if st.session_state.modo_confianca
            else "Estilo natural, carismático e leve."
        )
        system_base = f"""Você é o Mentor do Agente Magnético. O usuário se chama {st.session_state.usuario}.
{confianca}
{sistema_extra}
Sempre que analisar ou gerar mensagens, siga esta estrutura:
1. 📊 LEITURA INVISÍVEL: Interesse (0-10), Energia (Fria/Quente), Posição (Passivo/Dominante).
2. 🎯 DIAGNÓSTICO: Curto e direto sobre o erro ou acerto.
3. 💬 RESPOSTA IDEAL: A sugestão pronta para copiar.
4. 🧠 MICRO-ENSINO: Por que isso funciona?
Sempre termine com: "👉 Quer que eu ajuste pro seu estilo?"
"""
        messages = [{"role": "system", "content": system_base}]
        if historico_msgs:
            messages.extend(historico_msgs)
        messages.append({"role": "user", "content": prompt_usuario})
        response = client.chat.completions.create(messages=messages, model="openai/gpt-oss-120b")
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na conexão: Verifique sua chave API. ({e})"

def extrair_interesse(texto_ia: str) -> int:
    matches = re.findall(r'Interesse[:\s]+(\d+)', texto_ia, re.IGNORECASE)
    return min(int(matches[0]), 10) if matches else 5

def salvar_historico(tipo: str, entrada: str, saida: str):
    st.session_state.historico.append({
        'data': datetime.now().strftime('%d/%m %H:%M'),
        'tipo': tipo,
        'entrada': entrada[:80] + ('...' if len(entrada) > 80 else ''),
        'saida': saida,
        'nivel_interesse': extrair_interesse(saida),
        'favoritado': False,
    })

def calcular_stats():
    h = st.session_state.historico
    total = len(h)
    if total == 0:
        return 0, 0, 0
    media = sum(x['nivel_interesse'] for x in h) / total
    quentes = sum(1 for x in h if x['nivel_interesse'] >= 7)
    return total, round(media, 1), round((quentes / total) * 100)

def exportar_historico_txt() -> str:
    linhas = [f"AGENTE MAGNÉTICO — Histórico de {st.session_state.usuario}\n{'='*50}\n"]
    for item in st.session_state.historico:
        linhas.append(f"[{item['data']}] {item['tipo']} | Interesse: {item['nivel_interesse']}/10")
        linhas.append(f"Entrada: {item['entrada']}\nAnálise:\n{item['saida']}\n" + "-"*40)
    return "\n".join(linhas)

def banner_manual():
    manual_txt = """AGENTE MAGNÉTICO — Manual Completo de Funcionalidades
Versão Milhão 2026
======================================================

🏠 HOME — Painel Principal
Tela inicial com estatísticas em tempo real.

⚡ RESPOSTA RÁPIDA
Gera 3 opções de resposta imediata para qualquer mensagem recebida.

💬 TURBINAR MENSAGEM
A IA reescreve sua mensagem com gatilhos poderosos.

🧠 ANALISAR CONVERSA
Diagnóstico completo de uma conversa inteira.

🎭 ROLEPLAY — TREINE ANTES DE ENVIAR
Simule uma conversa com a pessoa antes de falar de verdade.

📚 BIBLIOTECA DE ABERTURAS
Banco pessoal de mensagens de abertura salvas.

📸 ANÁLISE DE PERFIL E BIO
Leitura de personalidade + abordagem ideal.

⚔️ COMPARAR DUAS CONVERSAS
Analise duas conversas lado a lado.

🗓️ PLANO DE CONQUISTA — 7 DIAS
Roteiro personalizado de ações para os próximos 7 dias.

🚩 DETECTOR DE RED FLAGS
Identifica sinais de desinteresse ou comportamento problemático.

📈 PROGRESSO
Histórico completo com filtros, favoritos e exportação.

📋 RESUMO SEMANAL
Relatório gerado por IA com análise da sua evolução.

© 2026 Agente Magnético — Treinador Social de Elite
"""
    st.download_button(
        label="📖 Baixar Manual Completo do Agente Magnético",
        data=manual_txt.encode("utf-8"),
        file_name="manual_agente_magnetico.txt",
        mime="text/plain",
        use_container_width=False
    )

# ── BARRA LATERAL DE SALVAR/CARREGAR ─────────────────────────
def barra_salvar():
    """Botão discreto para salvar dados no computador — aparece no topo do app."""
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    json_dados = gerar_json_sessao()
    total, media, _ = calcular_stats()

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#FFF0F5;border:1px solid #FFB6C1;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#000;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador</strong> — assim você não perde nada se o servidor reiniciar.<br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} análises registradas · interesse médio {media}/10</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=json_dados,
            file_name=f"agente_magnetico_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
        )

    st.markdown("<hr class='divider-rosa'>", unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    with st.container():
        st.title("💎 AGENTE MAGNÉTICO")
        st.markdown("**Seu Treinador Social de Elite com Inteligência Artificial**")
        st.markdown("""<div style="background:#FFF0F5;border:1px solid #FFB6C1;border-radius:10px;
        padding:10px 16px;margin:10px 0 16px 0;font-size:0.88em;color:#000;line-height:1.6;">
        🔒 <strong>ACESSO RESTRITO A ASSOCIADOS DO QUIZ COM PRÊMIOS</strong><br>
        🔗 <a href="https://quizcompremios.com.br/" target="_blank"
        style="color:#C2185B;font-weight:600;text-decoration:none;">quizcompremios.com.br</a>
        </div>""", unsafe_allow_html=True)
        nome = st.text_input("Seu Nome:", key="input_nome_login")
        chave = st.text_input("Sua Chave API da Groq:", type="password")


        # ── UPLOADER: carrega dados se o servidor tiver zerado ──
        tem_dados = len(st.session_state.get('historico', [])) > 0 or len(st.session_state.get('biblioteca', [])) > 0
        if not tem_dados:
            st.markdown("""<div style="background:#FFF0F5;border:1px solid #FFB6C1;border-radius:10px;
            padding:12px 16px;font-size:0.86em;color:#000;line-height:1.7;margin-bottom:10px;">
            📥 <strong>Seus dados sumiram?</strong> Isso acontece quando o servidor reinicia.<br>
            Selecione abaixo o arquivo <strong>.json</strong> que você salvou antes — tudo volta como era.
            </div>""", unsafe_allow_html=True)
            arq_login = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_login")
        else:
            arq_login = None
            st.markdown(f"""<div style="background:#F0FFF4;border:1px solid #86EFAC;border-radius:10px;
            padding:10px 14px;font-size:0.84em;color:#000;margin-bottom:10px;">
            ✅ <strong>Seus dados estão no servidor.</strong> É só entrar normalmente.
            </div>""", unsafe_allow_html=True)

        if arq_login is not None:
            try:
                dados_login = json.load(arq_login)
                nome_login = dados_login.get('usuario', '')
                st.success(f"✅ Dados de **{nome_login}** reconhecidos! Clique em Desbloquear para entrar.")
            except Exception:
                st.error("Arquivo inválido.")
                dados_login = None
                arq_login = None
        else:
            dados_login = None

        if st.button("✨ DESBLOQUEAR ACESSO"):
            if nome and chave:
                st.session_state.usuario = nome
                st.session_state.api_key = chave
                if dados_login:
                    carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

        st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
        st.markdown("🔑 Não tem chave Groq? Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#C2185B;font-weight:600;'>console.groq.com/keys</a>", unsafe_allow_html=True)

# ============================================================
# TELA: APP
# ============================================================
elif st.session_state.etapa == "App":

    # MODO DARK DESATIVADO — padrão claro igual aos demais apps

    # BANNER DO MANUAL
    banner_manual()

    # ── BARRA DE SALVAR — SEMPRE VISÍVEL ─────────────────────


    # TABS — navegação nativa
    _tab_Home, _tab_Rapida, _tab_Turbinar, _tab_Analisar, _tab_Roleplay, _tab_Biblioteca, _tab_Perfil, _tab_Comparar, _tab_Plano, _tab_RedFlags, _tab_Progresso, _tab_Resumo = st.tabs(['🏠 Home', '⚡ Resposta Rápida', '💬 Turbinar Msg', '🧠 Analisar', '🎭 Roleplay', '📚 Biblioteca', '📸 Análise de Perfil', '⚔️ Comparar', '🗓️ Plano 7 Dias', '🚩 Red Flags', '📈 Progresso', '📋 Resumo Semanal'])

    with _tab_Home:
            pass

    with _tab_Rapida:
            pass

    with _tab_Turbinar:
            pass

    with _tab_Analisar:
            pass

    with _tab_Roleplay:
            pass

    with _tab_Biblioteca:
            pass

    with _tab_Perfil:
            pass

    with _tab_Comparar:
            pass

    with _tab_Plano:
            pass

    with _tab_RedFlags:
            pass

    with _tab_Progresso:
            pass

    with _tab_Resumo:
            pass

# --- MOTOR DE IA ---
def mentor_milhao(prompt_usuario, sistema_extra="", historico_msgs=None):
    try:
        client = Groq(api_key=st.session_state.api_key)
        confianca = (
            "MODO CONFIANÇA ATIVADO: Respostas curtas, firmes, sem insegurança, mais diretas e dominantes."
            if st.session_state.modo_confianca
            else "Estilo natural, carismático e leve."
        )
        system_base = f"""Você é o Mentor do Agente Magnético. O usuário se chama {st.session_state.usuario}.
{confianca}
{sistema_extra}
Sempre que analisar ou gerar mensagens, siga esta estrutura:
1. 📊 LEITURA INVISÍVEL: Interesse (0-10), Energia (Fria/Quente), Posição (Passivo/Dominante).
2. 🎯 DIAGNÓSTICO: Curto e direto sobre o erro ou acerto.
3. 💬 RESPOSTA IDEAL: A sugestão pronta para copiar.
4. 🧠 MICRO-ENSINO: Por que isso funciona?
Sempre termine com: "👉 Quer que eu ajuste pro seu estilo?"
"""
        messages = [{"role": "system", "content": system_base}]
        if historico_msgs:
            messages.extend(historico_msgs)
        messages.append({"role": "user", "content": prompt_usuario})
        response = client.chat.completions.create(messages=messages, model="openai/gpt-oss-120b")
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na conexão: Verifique sua chave API. ({e})"

def extrair_interesse(texto_ia: str) -> int:
    matches = re.findall(r'Interesse[:\s]+(\d+)', texto_ia, re.IGNORECASE)
    return min(int(matches[0]), 10) if matches else 5

def salvar_historico(tipo: str, entrada: str, saida: str):
    st.session_state.historico.append({
        'data': datetime.now().strftime('%d/%m %H:%M'),
        'tipo': tipo,
        'entrada': entrada[:80] + ('...' if len(entrada) > 80 else ''),
        'saida': saida,
        'nivel_interesse': extrair_interesse(saida),
        'favoritado': False,
    })

def calcular_stats():
    h = st.session_state.historico
    total = len(h)
    if total == 0:
        return 0, 0, 0
    media = sum(x['nivel_interesse'] for x in h) / total
    quentes = sum(1 for x in h if x['nivel_interesse'] >= 7)
    return total, round(media, 1), round((quentes / total) * 100)

def exportar_historico_txt() -> str:
    linhas = [f"AGENTE MAGNÉTICO — Histórico de {st.session_state.usuario}\n{'='*50}\n"]
    for item in st.session_state.historico:
        linhas.append(f"[{item['data']}] {item['tipo']} | Interesse: {item['nivel_interesse']}/10")
        linhas.append(f"Entrada: {item['entrada']}\nAnálise:\n{item['saida']}\n" + "-"*40)
    return "\n".join(linhas)

def banner_manual():
    manual_txt = """AGENTE MAGNÉTICO — Manual Completo de Funcionalidades
Versão Milhão 2026
======================================================

🏠 HOME — Painel Principal
Tela inicial com estatísticas em tempo real.

⚡ RESPOSTA RÁPIDA
Gera 3 opções de resposta imediata para qualquer mensagem recebida.

💬 TURBINAR MENSAGEM
A IA reescreve sua mensagem com gatilhos poderosos.

🧠 ANALISAR CONVERSA
Diagnóstico completo de uma conversa inteira.

🎭 ROLEPLAY — TREINE ANTES DE ENVIAR
Simule uma conversa com a pessoa antes de falar de verdade.

📚 BIBLIOTECA DE ABERTURAS
Banco pessoal de mensagens de abertura salvas.

📸 ANÁLISE DE PERFIL E BIO
Leitura de personalidade + abordagem ideal.

⚔️ COMPARAR DUAS CONVERSAS
Analise duas conversas lado a lado.

🗓️ PLANO DE CONQUISTA — 7 DIAS
Roteiro personalizado de ações para os próximos 7 dias.

🚩 DETECTOR DE RED FLAGS
Identifica sinais de desinteresse ou comportamento problemático.

📈 PROGRESSO
Histórico completo com filtros, favoritos e exportação.

📋 RESUMO SEMANAL
Relatório gerado por IA com análise da sua evolução.

"""
    st.download_button(
        label="📖 Baixar Manual Completo do Agente Magnético",
        data=manual_txt.encode("utf-8"),
        file_name="manual_agente_magnetico.txt",
        mime="text/plain",
        use_container_width=False
    )

# ── BARRA LATERAL DE SALVAR/CARREGAR ─────────────────────────
def barra_salvar():
    """Botão discreto para salvar dados no computador — aparece no topo do app."""
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    json_dados = gerar_json_sessao()
    total, media, _ = calcular_stats()

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#FFF0F5;border:1px solid #FFB6C1;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#000;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador</strong> — assim você não perde nada se o servidor reiniciar.<br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} análises registradas · interesse médio {media}/10</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=json_dados,
            file_name=f"agente_magnetico_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
        )

    st.markdown("<hr class='divider-rosa'>", unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    with st.container():
        st.title("💎 AGENTE MAGNÉTICO")
        st.markdown("**Seu Treinador Social de Elite com Inteligência Artificial**")
        st.markdown("""<div style="background:#FFF0F5;border:1px solid #FFB6C1;border-radius:10px;
        padding:10px 16px;margin:10px 0 16px 0;font-size:0.88em;color:#000;line-height:1.6;">
        🔒 <strong>ACESSO RESTRITO A ASSOCIADOS DO QUIZ COM PRÊMIOS</strong><br>
        🔗 <a href="https://quizcompremios.com.br/" target="_blank"
        style="color:#C2185B;font-weight:600;text-decoration:none;">quizcompremios.com.br</a>
        </div>""", unsafe_allow_html=True)
        nome = st.text_input("Seu Nome:", key="input_nome_login")
        chave = st.text_input("Sua Chave API da Groq:", type="password")


        # ── UPLOADER: carrega dados se o servidor tiver zerado ──
        tem_dados = len(st.session_state.get('historico', [])) > 0 or len(st.session_state.get('biblioteca', [])) > 0
        if not tem_dados:
            st.markdown("""<div style="background:#FFF0F5;border:1px solid #FFB6C1;border-radius:10px;
            padding:12px 16px;font-size:0.86em;color:#000;line-height:1.7;margin-bottom:10px;">
            📥 <strong>Seus dados sumiram?</strong> Isso acontece quando o servidor reinicia.<br>
            Selecione abaixo o arquivo <strong>.json</strong> que você salvou antes — tudo volta como era.
            </div>""", unsafe_allow_html=True)
            arq_login = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_login")
        else:
            arq_login = None
            st.markdown(f"""<div style="background:#F0FFF4;border:1px solid #86EFAC;border-radius:10px;
            padding:10px 14px;font-size:0.84em;color:#000;margin-bottom:10px;">
            ✅ <strong>Seus dados estão no servidor.</strong> É só entrar normalmente.
            </div>""", unsafe_allow_html=True)

        if arq_login is not None:
            try:
                dados_login = json.load(arq_login)
                nome_login = dados_login.get('usuario', '')
                st.success(f"✅ Dados de **{nome_login}** reconhecidos! Clique em Desbloquear para entrar.")
            except Exception:
                st.error("Arquivo inválido.")
                dados_login = None
                arq_login = None
        else:
            dados_login = None

        if st.button("✨ DESBLOQUEAR ACESSO"):
            if nome and chave:
                st.session_state.usuario = nome
                st.session_state.api_key = chave
                if dados_login:
                    carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

        st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
        st.markdown("🔑 Não tem chave Groq? Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#C2185B;font-weight:600;'>console.groq.com/keys</a>", unsafe_allow_html=True)

# ============================================================
# TELA: APP
# ============================================================
elif st.session_state.etapa == "App":

    # MODO DARK DESATIVADO — padrão claro igual aos demais apps

    # BANNER DO MANUAL
    banner_manual()

    # ── BARRA DE SALVAR — SEMPRE VISÍVEL ─────────────────────

