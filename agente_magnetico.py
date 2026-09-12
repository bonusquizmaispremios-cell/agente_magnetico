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

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\d+$', k): continue
        st.session_state[k] = v

# --- INICIALIZAÇÃO DE ESTADO ---
CHAVES_SALVAR = ['usuario', 'pagina', 'modo_confianca', 'modo_dark', 'historico', 'biblioteca', 'roleplay_hist', 'roleplay_ativo', 'roleplay_perfil', 'roleplay_situacao', 'resumo_semanal', 'resumo_gerado_em', 'plano_conquista', 'plano_pessoa', 'xp_total', 'nivel']

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
    'xp_total': 0,
    'nivel': "Iniciante",
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
        'nivel_interesse': 5,
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
    media = sum(x.get('nivel_interesse', 5) for x in h) / total
    quentes = sum(1 for x in h if x.get('nivel_interesse', 0) >= 7)
    return total, round(media, 1), round((quentes / total) * 100)

def exportar_historico_txt() -> str:
    linhas = [f"AGENTE MAGNÉTICO — Histórico de {st.session_state.usuario}\n{'='*50}\n"]
    for item in st.session_state.historico:
        linhas.append(f"[{item.get('data','')}] {item.get('tipo','')} | Interesse: {item.get('nivel_interesse', item.get('nivel','-'))}/10")
        linhas.append(f"Entrada: {item.get('entrada','')}\nAnálise:\n{item.get('saida','')}\n" + "-"*40)
    return "\n".join(linhas)

def banner_manual(key_suffix="1"):
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
        use_container_width=False,
        key=f"dl_manual_{key_suffix}"
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
            key="agentema1"
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
        🔗 <a href="https://quizcompremios.com.br" target="_blank"
        style="color:#C2185B;font-weight:600;text-decoration:none;">quizcompremios.com.br</a>
        </div>""", unsafe_allow_html=True)
        nome = st.text_input("Seu Nome:", key="input_nome_login")
        chave = st.text_input("Sua Chave API da Groq:", type="password", key="agentema1_d2")


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

        if st.button("✨ DESBLOQUEAR ACESSO", key="agentema2"):
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

    # BANNER DO MANUAL
    banner_manual(key_suffix="1")

    # TABS — navegação nativa com scroll horizontal
    (_tab_Home, _tab_Rapida, _tab_Turbinar, _tab_Analisar, _tab_Roleplay,
     _tab_Biblioteca, _tab_Perfil, _tab_Comparar, _tab_Plano,
     _tab_RedFlags, _tab_Progresso, _tab_Resumo) = st.tabs([
        "🏠 Home", "⚡ Resposta Rápida", "💬 Turbinar Msg", "🧠 Analisar",
        "🎭 Roleplay", "📚 Biblioteca", "📸 Perfil", "⚔️ Comparar",
        "🗓️ Plano 7 Dias", "🚩 Red Flags", "📈 Progresso", "📋 Resumo Semanal"
    ])

    # ── BARRA SALVAR ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
            st.download_button("💾 Baixar meus dados (.json)",
                data=_jsv.dumps(_dsv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_barra_sv_agmag")
        with _bsc2:
            _fupsv = st.file_uploader("📂 Carregar dados salvos:", type=["json"], key="ul_barra_sv_agmag", label_visibility="collapsed")
            if _fupsv:
                try:
                    import json as _jld
                    for _k2,_v2 in _jld.loads(_fupsv.read().decode()).items():
                        if _k2 not in ('api_key','etapa'): st.session_state[_k2] = _v2
                    st.success("✅ Dados restaurados!"); st.rerun()
                except: st.error("Arquivo inválido.")


    with _tab_Home:
        st.header("🏠 Painel Principal")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='card' style='text-align:center;'><div style='font-size:2em;'>💬</div><div><b>{len(st.session_state.historico)}</b><br><small>Interações</small></div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='card' style='text-align:center;'><div style='font-size:2em;'>⭐</div><div><b>{st.session_state.xp_total}</b><br><small>XP Total</small></div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='card' style='text-align:center;'><div style='font-size:2em;'>🏆</div><div><b>{st.session_state.nivel}</b><br><small>Nível</small></div></div>", unsafe_allow_html=True)
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 🧭 Guia das Abas")
        for ic, nm, desc in [
            ("⚡","Resposta Rápida","Gera 3 opções de resposta imediata para qualquer mensagem recebida."),
            ("💬","Turbinar Msg","Reescreve sua mensagem com gatilhos psicológicos poderosos."),
            ("🧠","Analisar","Diagnóstico completo de uma conversa inteira."),
            ("🎭","Roleplay","Simule uma conversa antes de falar de verdade."),
            ("📚","Biblioteca","Banco pessoal de mensagens de abertura salvas."),
            ("📸","Perfil","Análise de perfil e bio — leitura invisível."),
            ("⚔️","Comparar","Compare duas conversas e veja qual está indo melhor."),
            ("🗓️","Plano 7 Dias","Plano de reconquista ou avanço em 7 dias."),
            ("🚩","Red Flags","Detecta sinais de alerta na conversa."),
            ("📈","Progresso","Seu histórico e evolução ao longo do tempo."),
            ("📋","Resumo Semanal","Resumo semanal com insights e próximos passos."),
        ]:
            st.markdown(f"**{ic} {nm}** — {desc}")
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        col_sv, _ = st.columns([1,3])
        with col_sv:
            st.download_button("💾 Salvar dados", data=exportar_historico_txt(), file_name="agente_magnetico.txt", mime="text/plain", key="dl_home_sv1")

    with _tab_Rapida:
        st.header("⚡ Resposta Rápida")
        st.markdown("Cole a mensagem que você recebeu e a IA gera 3 opções de resposta poderosas.")
        msg_r = st.text_area("📱 Mensagem recebida:", height=120, key="ta_rapida1", placeholder="Cole aqui a mensagem...")
        contexto_r = st.text_input("🎯 Contexto (opcional):", key="ti_rapida_ctx1", placeholder="Ex: segundo encontro, ela está fria...")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            tom_r = st.selectbox("Tom:", ["Natural e carismático","Misterioso","Engraçado e leve","Direto e confiante","Romântico"], key="sel_rapida_tom1")
        with col_r2:
            modo_r = st.checkbox("Modo Confiança 🔥", value=st.session_state.modo_confianca, key="chk_rapida_conf1")
            if modo_r != st.session_state.modo_confianca:
                st.session_state.modo_confianca = modo_r
        if st.button("⚡ GERAR RESPOSTAS", key="btn_rapida1", use_container_width=True):
            if msg_r.strip():
                with st.spinner("Gerando respostas..."):
                    prompt = f"Mensagem recebida: '{msg_r}'\nContexto: {contexto_r or 'não informado'}\nTom desejado: {tom_r}\n\nGere EXATAMENTE 3 opções de resposta numeradas (1. 2. 3.) com tom {tom_r}. Cada resposta em linha separada."
                    resp = mentor_milhao(prompt)
                st.session_state.historico.append({"nivel_interesse": 5, "data": datetime.now().strftime("%d/%m %H:%M"), "tipo": "Resposta Rápida", "nivel": "⚡", "entrada": msg_r[:100], "saida": resp})
                st.markdown(f"<div class='card'>{resp}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar", data=resp, file_name="respostas.txt", key="dl_rapida_res1")
            else:
                st.warning("Cole uma mensagem primeiro.")

    with _tab_Turbinar:
        st.header("💬 Turbinar Mensagem")
        st.markdown("Sua mensagem, reescrita com gatilhos psicológicos para gerar mais interesse.")
        msg_t = st.text_area("✍️ Sua mensagem atual:", height=120, key="ta_turbinar1", placeholder="Digite sua mensagem...")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            obj_t = st.selectbox("Objetivo:", ["Gerar interesse","Marcar encontro","Retomar contato","Criar tensão","Finalizar conversa"], key="sel_turb_obj1")
        with col_t2:
            nivel_t = st.selectbox("Intensidade:", ["Sutil","Moderado","Intenso"], key="sel_turb_niv1")
        if st.button("💬 TURBINAR", key="btn_turbinar1", use_container_width=True):
            if msg_t.strip():
                with st.spinner("Turbinando..."):
                    prompt = f"Mensagem original: '{msg_t}'\nObjetivo: {obj_t}\nIntensidade: {nivel_t}\n\nReescreva com gatilhos psicológicos. Mostre: VERSÃO ORIGINAL / VERSÃO TURBINADA / POR QUE FUNCIONA"
                    resp = mentor_milhao(prompt)
                st.session_state.historico.append({"nivel_interesse": 5, "data": datetime.now().strftime("%d/%m %H:%M"), "tipo": "Turbinar", "nivel": "💬", "entrada": msg_t[:100], "saida": resp})
                st.markdown(f"<div class='card'>{resp}</div>", unsafe_allow_html=True)
            else:
                st.warning("Digite sua mensagem primeiro.")

    with _tab_Analisar:
        st.header("🧠 Analisar Conversa")
        st.markdown("Cole a conversa completa e receba um diagnóstico detalhado.")
        conv_a = st.text_area("📋 Conversa completa:", height=200, key="ta_analisar1", placeholder="Cole a conversa aqui (você: / ela: ou nome: )")
        if st.button("🧠 ANALISAR", key="btn_analisar1", use_container_width=True):
            if conv_a.strip():
                with st.spinner("Analisando..."):
                    prompt = f"Conversa para analisar:\n{conv_a}\n\nFaça diagnóstico completo: 1) Nível de interesse atual (0-10) 2) Dinâmica de poder 3) Erros cometidos 4) Acertos 5) Próximos 3 passos estratégicos"
                    resp = mentor_milhao(prompt)
                st.session_state.historico.append({"nivel_interesse": 5, "data": datetime.now().strftime("%d/%m %H:%M"), "tipo": "Analisar", "nivel": "🧠", "entrada": conv_a[:100], "saida": resp})
                st.markdown(f"<div class='card'>{resp}</div>", unsafe_allow_html=True)
            else:
                st.warning("Cole a conversa primeiro.")

    with _tab_Roleplay:
        st.header("🎭 Roleplay — Treine Antes de Enviar")
        st.markdown("Simule uma conversa com a pessoa antes de falar de verdade.")
        if "roleplay_hist" not in st.session_state:
            st.session_state.roleplay_hist = []
        perfil_rp = st.text_area("👤 Perfil da pessoa (nome, personalidade, contexto):", height=80, key="ta_roleplay_perfil1", placeholder="Ex: Ana, 28 anos, reservada, nos conhecemos no trabalho...")
        for msg_rp in st.session_state.roleplay_hist:
            css_rp = "chat-user" if msg_rp["role"] == "user" else "chat-persona"
            autor_rp = "🙂 Você" if msg_rp["role"] == "user" else "🎭 Personagem"
            st.markdown(f"<div class='{css_rp}'><b>{autor_rp}:</b> {msg_rp['content']}</div>", unsafe_allow_html=True)
        msg_rp_in = st.text_input("💬 Sua mensagem:", key="ti_roleplay_in1", placeholder="O que você vai dizer?")
        col_rp1, col_rp2 = st.columns(2)
        with col_rp1:
            if st.button("📤 Enviar", key="btn_roleplay_send1", use_container_width=True):
                if msg_rp_in and perfil_rp:
                    st.session_state.roleplay_hist.append({"role":"user","content":msg_rp_in})
                    with st.spinner("Personagem respondendo..."):
                        hist_txt = "\n".join(f"{'Você' if m['role']=='user' else 'Personagem'}: {m['content']}" for m in st.session_state.roleplay_hist[-10:])
                        prompt_rp = f"Perfil: {perfil_rp}\n\nConversa:\n{hist_txt}\n\nResponda como a personagem de forma realista. Depois avalie minha última mensagem (1 linha)."
                        resp_rp = mentor_milhao(prompt_rp)
                    st.session_state.roleplay_hist.append({"role":"assistant","content":resp_rp})
                    st.rerun()
        with col_rp2:
            if st.button("🗑️ Resetar", key="btn_roleplay_reset1", use_container_width=True):
                st.session_state.roleplay_hist = []; st.rerun()

    with _tab_Biblioteca:
        st.header("📚 Biblioteca de Aberturas")
        st.markdown("Salve suas melhores aberturas e acesse quando precisar.")
        if "biblioteca" not in st.session_state:
            st.session_state.biblioteca = []
        nova_ab = st.text_area("✍️ Nova abertura para salvar:", height=80, key="ta_biblio_nova1", placeholder="Digite sua abertura...")
        cat_ab = st.selectbox("Categoria:", ["Casual","Direto","Engraçado","Misterioso","Romântico"], key="sel_biblio_cat1")
        if st.button("💾 Salvar abertura", key="btn_biblio_salvar1", use_container_width=True):
            if nova_ab.strip():
                st.session_state.biblioteca.append({"texto": nova_ab, "categoria": cat_ab, "data": datetime.now().strftime("%d/%m")})
                st.success("Salvo!"); st.rerun()
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        if st.session_state.biblioteca:
            for i, item in enumerate(reversed(st.session_state.biblioteca)):
                col_b1, col_b2 = st.columns([5,1])
                with col_b1:
                    st.markdown(f"<div class='card'><span class='badge'>{item['categoria']}</span> <small>{item['data']}</small><br>{item['texto']}</div>", unsafe_allow_html=True)
                with col_b2:
                    if st.button("✕", key=f"del_bib_{i}1"):
                        st.session_state.biblioteca.pop(-(i+1)); st.rerun()
        else:
            st.info("Nenhuma abertura salva ainda.")

    with _tab_Perfil:
        st.header("📸 Análise de Perfil e Bio")
        st.markdown("Cole o perfil ou bio da pessoa e a IA faz uma leitura invisível completa.")
        bio_p = st.text_area("📋 Bio / Perfil da pessoa:", height=150, key="ta_perfil_bio1", placeholder="Cole aqui a bio, fotos descritas, legendas, interesses...")
        if st.button("🔍 ANALISAR PERFIL", key="btn_perfil_analisar1", use_container_width=True):
            if bio_p.strip():
                with st.spinner("Lendo o perfil..."):
                    prompt_p = f"Perfil/Bio para analisar:\n{bio_p}\n\nFaça leitura completa: 1) Personalidade provável 2) O que ela valoriza 3) Como se aproximar 4) Tom ideal para falar com ela 5) O que NUNCA fazer"
                    resp_p = mentor_milhao(prompt_p)
                st.session_state.historico.append({"nivel_interesse": 5, "data": datetime.now().strftime("%d/%m %H:%M"), "tipo": "Análise de Perfil", "nivel": "📸", "entrada": bio_p[:100], "saida": resp_p})
                st.markdown(f"<div class='card'>{resp_p}</div>", unsafe_allow_html=True)
            else:
                st.warning("Cole o perfil primeiro.")

    with _tab_Comparar:
        st.header("⚔️ Comparar Conversas")
        st.markdown("Compare duas conversas e descubra qual está indo melhor e por quê.")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            conv_c1 = st.text_area("Conversa A:", height=200, key="ta_comp_a1", placeholder="Cole a primeira conversa...")
        with col_c2:
            conv_c2 = st.text_area("Conversa B:", height=200, key="ta_comp_b1", placeholder="Cole a segunda conversa...")
        if st.button("⚔️ COMPARAR", key="btn_comparar1", use_container_width=True):
            if conv_c1.strip() and conv_c2.strip():
                with st.spinner("Comparando..."):
                    prompt_c = f"Conversa A:\n{conv_c1}\n\nConversa B:\n{conv_c2}\n\nCompare as duas: qual está indo melhor, quais os erros de cada uma e o que fazer em cada caso."
                    resp_c = mentor_milhao(prompt_c)
                st.markdown(f"<div class='card'>{resp_c}</div>", unsafe_allow_html=True)
            else:
                st.warning("Cole as duas conversas.")

    with _tab_Plano:
        st.header("🗓️ Plano 7 Dias")
        st.markdown("Plano estratégico personalizado para avançar ou reconquistar em 7 dias.")
        sit_p = st.text_area("📋 Sua situação atual:", height=120, key="ta_plano_sit1", placeholder="Descreva onde você está na conversa...")
        obj_p7 = st.selectbox("🎯 Objetivo:", ["Marcar encontro","Criar interesse","Reconquistar","Avançar no relacionamento","Sair da friendzone"], key="sel_plano_obj1")
        if st.button("🗓️ GERAR PLANO", key="btn_plano1", use_container_width=True):
            if sit_p.strip():
                with st.spinner("Criando plano..."):
                    prompt_p7 = f"Situação: {sit_p}\nObjetivo: {obj_p7}\n\nCrie um plano dia a dia (Dia 1 a Dia 7) com ações específicas, mensagens sugeridas e o que fazer se ela responder bem ou não."
                    resp_p7 = mentor_milhao(prompt_p7)
                st.markdown(f"<div class='card'>{resp_p7}</div>", unsafe_allow_html=True)
            else:
                st.warning("Descreva sua situação.")

    with _tab_RedFlags:
        st.header("🚩 Detector de Red Flags")
        st.markdown("A IA detecta sinais de alerta na conversa que você pode estar ignorando.")
        conv_rf = st.text_area("📋 Conversa para analisar:", height=200, key="ta_redflags1", placeholder="Cole a conversa aqui...")
        if st.button("🚩 DETECTAR RED FLAGS", key="btn_redflags1", use_container_width=True):
            if conv_rf.strip():
                with st.spinner("Analisando sinais..."):
                    prompt_rf = f"Conversa:\n{conv_rf}\n\nDetecte RED FLAGS: comportamentos passivos-agressivos, ghosting, manipulação, falta de interesse real, inconsistências. Avalie risco (baixo/médio/alto) e o que fazer."
                    resp_rf = mentor_milhao(prompt_rf)
                st.session_state.historico.append({"nivel_interesse": 5, "data": datetime.now().strftime("%d/%m %H:%M"), "tipo": "Red Flags", "nivel": "🚩", "entrada": conv_rf[:100], "saida": resp_rf})
                st.markdown(f"<div class='card'>{resp_rf}</div>", unsafe_allow_html=True)
            else:
                st.warning("Cole a conversa primeiro.")

    with _tab_Progresso:
        st.header("📈 Meu Progresso")
        st.markdown(f"**XP Total:** {st.session_state.xp_total} | **Nível:** {st.session_state.nivel} | **Interações:** {len(st.session_state.historico)}")
        if st.session_state.historico:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 🕐 Histórico Recente")
            for item in reversed(st.session_state.historico[-20:]):
                st.markdown(f"<div class='hist-item'><b>{item['nivel']} {item['tipo']}</b> <small>— {item['data']}</small><br><small>{item['entrada'][:80]}...</small></div>", unsafe_allow_html=True)
            st.download_button("📥 Baixar histórico completo", data=exportar_historico_txt(), file_name="historico_agente.txt", mime="text/plain", key="dl_prog_hist1")
        else:
            st.info("Nenhuma interação ainda. Use as abas acima para começar!")

    with _tab_Resumo:
        st.header("📋 Resumo Semanal")
        st.markdown("Análise semanal com insights e próximos passos estratégicos.")
        if st.session_state.historico:
            if st.button("📊 GERAR RESUMO SEMANAL", key="btn_resumo1", use_container_width=True):
                with st.spinner("Gerando resumo..."):
                    hist_txt = "\n".join(f"[{h['data']}] {h['tipo']}: {h['entrada'][:60]}" for h in st.session_state.historico[-30:])
                    prompt_rs = f"Histórico de interações da semana:\n{hist_txt}\n\nGere um resumo executivo: 1) Padrões identificados 2) Principais erros 3) Evolução percebida 4) Top 3 prioridades para a próxima semana"
                    resp_rs = mentor_milhao(prompt_rs)
                st.markdown(f"<div class='card'>{resp_rs}</div>", unsafe_allow_html=True)
        else:
            st.info("Faça algumas interações primeiro para gerar o resumo.")
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            st.download_button("💾 Salvar dados (.json)", data=json.dumps({k:st.session_state.get(k) for k in CHAVES_SALVAR}, ensure_ascii=False, indent=2, default=str), file_name=f"agente_{st.session_state.usuario}.json", mime="application/json", key="dl_resumo_json1")
        with col_exp2:
            st.download_button("📥 Exportar histórico (.txt)", data=exportar_historico_txt(), file_name="historico_agente.txt", mime="text/plain", key="dl_resumo_txt1")

# --- RODAPÉ ---
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
