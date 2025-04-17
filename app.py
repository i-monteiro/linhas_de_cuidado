# app.py
# ------------------------------------------------------------------
# REGISTRO DAS LINHAS DE CUIDADO  –  STREAMLIT
# versão “completa”, incluindo:
#   • menu Cadastrar (6 abas)
#   • menu Editar  (6 abas, com filtros + formulário pré‑preenchido
#                   ou vazio, salvando/atualizando CSVs)
#   • menu Indicadores (placeholder)
# ------------------------------------------------------------------

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --------------------------- Configuração --------------------------
st.set_page_config(page_title="Linhas de Cuidado", layout="wide")
st.title("📊 Registro das Linhas de Cuidado")

# session_state para propagar número/hospital durante o cadastro
if "numero_atendimento" not in st.session_state:
    st.session_state.numero_atendimento = ""
if "hospital" not in st.session_state:
    st.session_state.hospital = ""

# --------------------------- Sidebar -------------------------------
menu = st.sidebar.selectbox("Menu", ["Cadastrar", "Editar", "Indicadores"])

# --------------------------- Funções Aux. --------------------------
def save_csv(path: str, registro: dict):
    """Salva linha única no CSV (append ou cria)."""
    df = pd.DataFrame([registro])
    cols = list(registro.keys())
    if not os.path.isfile(path):
        df.to_csv(path, index=False, columns=cols)
    else:
        df.to_csv(path, mode="a", header=False, index=False, columns=cols)

def fetch_row(df_src: pd.DataFrame, chave: str) -> pd.Series:
    # se ainda não existe coluna (csv vazio), devolve Series vazio
    if "numeroAtendimento" not in df_src.columns:
        return pd.Series(dtype="object")          # nada para mostrar
    fil = df_src[df_src["numeroAtendimento"] == chave]
    if len(fil):
        return fil.iloc[0]
    # retorna Series com todas as colunas mas vazias
    return pd.Series({c: "" for c in df_src.columns})

# ==================================================================
#                               CADASTRAR
# ==================================================================
if menu == "Cadastrar":
    abas = st.tabs(["Pronto Atendimento", "Internação", "Tratamento",
                    "Permanência", "Pós-Alta", "Questionários"])

    # ------------------- 1) Pronto Atendimento --------------------
    with abas[0]:
        with st.form("form_pronto_atendimento"):
            st.subheader("📍 Pronto Atendimento")
            c1, c2, c3 = st.columns(3)

            with c1:
                hospital          = st.selectbox("Hospital", ["","Centro Médico", "Galileo", "HUC", "Irmãos Penteado", "Maternidade", "PUCC"])
                linha_cuidado     = st.selectbox("Linha de Cuidado", ["","AVC", "Chron", "Fratura de Fêmur", "ICC"])
                numero_atendimento= st.text_input("Número Atendimento")
                status            = st.selectbox("Status", ["", "Internado", "Alta", "Óbito"])

            with c2:
                numero_autorizacao= st.text_input("Número Autorização")
                numero_drg        = st.text_input("Número DRG")
                nome_paciente     = st.text_input("Nome Paciente")
                idade             = st.number_input("Idade", min_value=0)

            with c3:
                cid_principal     = st.text_input("CID Principal")
                dtps_date         = st.date_input("Data Internação PS")
                dtps_time         = st.time_input("Hora Internação PS")
                data_int_ps       = datetime.combine(dtps_date, dtps_time)
                ecg               = st.selectbox("ECG Realizado", ["", "Sim", "Não", "Sem Informação"])
                raio_x            = st.selectbox("Raio‑X Realizado", ["", "Sim", "Não", "Sem Informação"])
                exame_ps          = st.text_input("Exame PS Realizado")

            st.markdown("### 🧪 Dados dos Exames")
            dt_solic = datetime.combine(st.date_input("Data Solicitação"),
                                        st.time_input("Hora Solicitação"))
            dt_exec  = datetime.combine(st.date_input("Data Execução"),
                                        st.time_input("Hora Execução"))
            dt_laudo = datetime.combine(st.date_input("Data Laudo"),
                                        st.time_input("Hora Laudo"))
            tempo_exame = round((dt_laudo - dt_solic).total_seconds()/60, 2)
            st.info(f"⏱️ Tempo de Exame: {tempo_exame} minutos")

            if st.form_submit_button("Salvar Pronto Atendimento"):
                st.session_state.numero_atendimento = numero_atendimento
                st.session_state.hospital = hospital

                registro = {
                    "hospital": hospital,
                    "linhaCuidado": linha_cuidado,
                    "numeroAtendimento": numero_atendimento,
                    "status": status,
                    "numeroAutorizacao": numero_autorizacao,
                    "numeroDRG": numero_drg,
                    "nomePaciente": nome_paciente,
                    "idade": idade,
                    "cidPrincipal": cid_principal,
                    "dataHoraInternacaoPS": data_int_ps.isoformat(),
                    "ECG": ecg,
                    "raioX": raio_x,
                    "examePS": exame_ps,
                    "dataHoraSolicitacao": dt_solic.isoformat(),
                    "dataHoraExecucao": dt_exec.isoformat(),
                    "dataHoraLaudo": dt_laudo.isoformat(),
                    "tempoExame": tempo_exame
                }
                save_csv("dados_pronto_atendimento.csv", registro)
                st.success("Dados de Pronto Atendimento salvos! ✅")

    # ------------------- 2) Internação ----------------------------
    with abas[1]:
        with st.form("form_internacao"):
            st.subheader("🏥 Internação")
            st.text_input("Hospital", value=st.session_state.hospital, disabled=True)
            st.text_input("Número Atendimento", value=st.session_state.numero_atendimento,
                          disabled=True, key="int_numero")
            acomodacao      = st.text_input("Acomodação")
            dt_int_date     = st.date_input("Data Internação")
            dt_int_time     = st.time_input("Hora Internação")
            dt_internacao   = datetime.combine(dt_int_date, dt_int_time)
            exame_solic     = st.text_input("Exame Solicitado na Internação")
            dt_solic2       = datetime.combine(st.date_input("Data Solicitação"),
                                               st.time_input("Hora Solicitação"))
            dt_exec2        = datetime.combine(st.date_input("Data Execução"),
                                               st.time_input("Hora Execução"))
            dt_laudo2       = datetime.combine(st.date_input("Data Laudo"),
                                               st.time_input("Hora Laudo"))
            tempo_exame2    = round((dt_laudo2 - dt_solic2).total_seconds()/60, 2)
            st.info(f"⏱️ Tempo de Exame: {tempo_exame2} minutos")
            alta_uti        = st.checkbox("Alta da UTI para Enfermaria")
            tempo_uti       = st.number_input("Tempo UTI (dias)", min_value=0)

            if st.form_submit_button("Salvar Internação"):
                registro = {
                    "hospital": st.session_state.hospital,
                    "numeroAtendimento": st.session_state.numero_atendimento,
                    "acomodacao": acomodacao,
                    "dataHoraInternacao": dt_internacao.isoformat(),
                    "exameSolicitadoInternacao": exame_solic,
                    "dataHoraSolicitacao": dt_solic2.isoformat(),
                    "dataHoraExecucao": dt_exec2.isoformat(),
                    "dataHoraLaudo": dt_laudo2.isoformat(),
                    "tempoExame": tempo_exame2,
                    "altaUTIParaEnfermaria": alta_uti,
                    "tempoUTI": tempo_uti
                }
                save_csv("dados_internacao.csv", registro)
                st.success("Dados de Internação salvos! ✅")

    # ------------------- 3) Tratamento ----------------------------
    with abas[2]:
        with st.form("form_tratamento"):
            st.subheader("💉 Tratamento")
            st.text_input("Hospital", value=st.session_state.hospital, disabled=True)
            st.text_input("Número Atendimento", value=st.session_state.numero_atendimento,
                          disabled=True, key="trat_numero")
            procedimento    = st.text_input("Procedimento Cirúrgico")
            tipo_proc       = st.text_input("Tipo de Procedimento Cirúrgico")
            grau_sev        = st.selectbox("Grau de Severidade", ["", "Leve", "Moderado", "Grave"])

            if st.form_submit_button("Salvar Tratamento"):
                registro = {
                    "hospital": st.session_state.hospital,
                    "numeroAtendimento": st.session_state.numero_atendimento,
                    "procedimentoCirurgico": procedimento,
                    "tipoProcedimentoCirurgico": tipo_proc,
                    "grauSeveridade": grau_sev
                }
                save_csv("dados_tratamento.csv", registro)
                st.success("Dados de Tratamento salvos! ✅")

    # ------------------- 4) Permanência ---------------------------
    with abas[3]:
        with st.form("form_permanencia"):
            st.subheader("🛎️ Permanência")
            st.text_input("Hospital", value=st.session_state.hospital, disabled=True)
            st.text_input("Número Atendimento", value=st.session_state.numero_atendimento,
                          disabled=True, key="perm_numero")
            risco           = st.text_input("Estratificação de Risco")
            prev_drg        = st.number_input("Permanência Prevista DRG", min_value=0)
            real_dias       = st.number_input("Permanência Real", min_value=0)
            data_alta       = st.date_input("Data de Alta")
            acom_alta       = st.text_input("Acomodação (na alta)")

            if st.form_submit_button("Salvar Permanência"):
                registro = {
                    "hospital": st.session_state.hospital,
                    "numeroAtendimento": st.session_state.numero_atendimento,
                    "estratificacaoRisco": risco,
                    "permanenciaPrevistaDRG": prev_drg,
                    "permanenciaReal": real_dias,
                    "dataAlta": data_alta.isoformat(),
                    "acomodacao": acom_alta
                }
                save_csv("dados_permanencia.csv", registro)
                st.success("Dados de Permanência salvos! ✅")

    # ------------------- 5) Pós‑Alta ------------------------------
    with abas[4]:
        with st.form("form_pos_alta"):
            st.subheader("📦 Pós‑Alta")
            st.text_input("Hospital", value=st.session_state.hospital, disabled=True)
            st.text_input("Número Atendimento", value=st.session_state.numero_atendimento,
                          disabled=True, key="post_numero")
            gest_cron  = st.selectbox("Gestão de Crônicos", ["", "Sim", "Não"])
            reintern   = st.selectbox("Reinternação", ["", "Sim", "Não"])
            quantidade = st.number_input("Quantidade", min_value=0)
            obs        = st.text_area("Observação")

            if st.form_submit_button("Salvar Pós‑Alta"):
                registro = {
                    "hospital": st.session_state.hospital,
                    "numeroAtendimento": st.session_state.numero_atendimento,
                    "gestaoCronicos": gest_cron,
                    "reinternacao": reintern,
                    "quantidade": quantidade,
                    "observacao": obs
                }
                save_csv("dados_pos_alta.csv", registro)
                st.success("Dados de Pós‑Alta salvos! ✅")

    # ------------------- 6) Questionários -------------------------
    with abas[5]:
        with st.form("form_questionarios"):
            st.subheader("📝 Questionários")
            st.text_input("Hospital", value=st.session_state.hospital, disabled=True)
            st.text_input("Número Atendimento", value=st.session_state.numero_atendimento,
                          disabled=True, key="quest_numero")

            registro = {
                "hospital": st.session_state.hospital,
                "numeroAtendimento": st.session_state.numero_atendimento
            }
            for dia in [7, 30, 60, 90]:
                data_q = st.date_input(f"Data Questionário - Dia {dia}", key=f"q_date_{dia}")
                obs_q  = st.text_area(f"Observação Questionário - Dia {dia}", key=f"q_obs_{dia}")
                registro[f"dataQuestionarioPaciente{dia}"] = data_q.isoformat()
                registro[f"observacaoQuestionarioPaciente{dia}"] = obs_q

            if st.form_submit_button("Salvar Questionários"):
                save_csv("dados_questionarios.csv", registro)
                st.success("Dados de Questionários salvos! ✅")

# ==================================================================
#                               EDITAR
# ==================================================================
elif menu == "Editar":
    st.subheader("✏️ Editar Pronto Atendimento")
    pa_path = "dados_pronto_atendimento.csv"

    if not os.path.exists(pa_path):
        st.warning("Nenhum registro para editar.")
        st.stop()

    df_pa = pd.read_csv(pa_path)

    # -------- filtros ----------
    c1, c2 = st.columns(2)
    with c1:
        hosp_sel = st.selectbox(
            "Filtrar por Hospital",
            [""] + sorted(df_pa["hospital"].dropna().unique())
        )
    with c2:
        linhas = (
            df_pa[df_pa["hospital"] == hosp_sel]["linhaCuidado"].dropna().unique()
            if hosp_sel else df_pa["linhaCuidado"].dropna().unique()
        )
        linha_sel = st.selectbox(
            "Filtrar por Linha de Cuidado",
            [""] + sorted(linhas.tolist())
        )

    df_filtro = df_pa.copy()
    if hosp_sel:
        df_filtro = df_filtro[df_filtro["hospital"] == hosp_sel]
    if linha_sel:
        df_filtro = df_filtro[df_filtro["linhaCuidado"] == linha_sel]

    st.dataframe(
        df_filtro[["hospital", "linhaCuidado", "numeroAtendimento", "numeroDRG"]],
        use_container_width=True
    )

    atend_sel = st.selectbox(
        "Selecione Atendimento",
        [""] + df_filtro["numeroAtendimento"].tolist()
    )
    if not atend_sel:
        st.stop()

    # -------- abas de edição --------
    tabs_ed = st.tabs([
        "Pronto Atendimento", "Internação", "Tratamento",
        "Permanência", "Pós-Alta", "Questionários"
    ])

    # ================== Aba 1 : Pronto Atendimento =================
    with tabs_ed[0]:
        rec = fetch_row(df_pa, atend_sel)

        with st.form("edit_pa"):
            st.subheader("✏️ Editar Pronto Atendimento")
            c1, c2, c3 = st.columns(3)

            with c1:
                hospital_e = st.text_input("Hospital", value=rec["hospital"])
                linha_e    = st.text_input("Linha de Cuidado", value=rec["linhaCuidado"])
                st.text_input("Número Atendimento", value=atend_sel, disabled=True)
                status_e   = st.selectbox(
                    "Status", ["", "Internado", "Alta", "Óbito"],
                    index=["", "Internado", "Alta", "Óbito"].index(rec["status"])
                    if rec["status"] in ["Internado", "Alta", "Óbito"] else 0
                )

            with c2:
                num_aut_e = st.text_input("Número Autorização", value=rec["numeroAutorizacao"])
                num_drg_e = st.text_input("Número DRG", value=rec["numeroDRG"])
                nome_e    = st.text_input("Nome Paciente", value=rec["nomePaciente"])
                idade_e   = st.number_input("Idade", value=int(rec["idade"] or 0), min_value=0)

            with c3:
                cid_e   = st.text_input("CID Principal", value=rec["cidPrincipal"])
                base_dt = datetime.fromisoformat(rec["dataHoraInternacaoPS"]) \
                          if rec["dataHoraInternacaoPS"] else datetime.now()
                di = st.date_input("Data Internação PS", base_dt.date())
                ti = st.time_input("Hora Internação PS", base_dt.time())
                ecg_e = st.selectbox(
                    "ECG Realizado", ["", "Sim", "Não", "Sem Informação"],
                    index=["", "Sim", "Não", "Sem Informação"].index(rec["ECG"])
                    if rec["ECG"] in ["Sim", "Não", "Sem Informação"] else 0
                )
                rx_e = st.selectbox(
                    "Raio‑X Realizado", ["", "Sim", "Não", "Sem Informação"],
                    index=["", "Sim", "Não", "Sem Informação"].index(rec["raioX"])
                    if rec["raioX"] in ["Sim", "Não", "Sem Informação"] else 0
                )
                exps_e = st.text_input("Exame PS Realizado", value=rec["examePS"])

            st.markdown("### 🧪 Recalcular Tempo")
            base_sol = datetime.fromisoformat(rec["dataHoraSolicitacao"]) \
                       if rec["dataHoraSolicitacao"] else datetime.now()
            dsol = st.date_input("Data Solicitação", base_sol.date(), key="pa_sol_d")
            tsol = st.time_input("Hora Solicitação", base_sol.time(), key="pa_sol_t")

            base_lau = datetime.fromisoformat(rec["dataHoraLaudo"]) \
                       if rec["dataHoraLaudo"] else datetime.now()
            dla = st.date_input("Data Laudo", base_lau.date(), key="pa_lau_d")
            tla = st.time_input("Hora Laudo", base_lau.time(), key="pa_lau_t")

            new_tempo = round(
                (datetime.combine(dla, tla) - datetime.combine(dsol, tsol)).total_seconds() / 60,
                2
            )
            st.info(f"⏱️ Novo Tempo de Exame: {new_tempo} minutos")

            if st.form_submit_button("Salvar PA"):
                linha_nova = {
                    "hospital": hospital_e,
                    "linhaCuidado": linha_e,
                    "numeroAtendimento": atend_sel,
                    "status": status_e,
                    "numeroAutorizacao": num_aut_e,
                    "numeroDRG": num_drg_e,
                    "nomePaciente": nome_e,
                    "idade": idade_e,
                    "cidPrincipal": cid_e,
                    "dataHoraInternacaoPS": datetime.combine(di, ti).isoformat(),
                    "ECG": ecg_e,
                    "raioX": rx_e,
                    "examePS": exps_e,
                    "dataHoraSolicitacao": datetime.combine(dsol, tsol).isoformat(),
                    "dataHoraExecucao": rec["dataHoraExecucao"],  # não editado aqui
                    "dataHoraLaudo": datetime.combine(dla, tla).isoformat(),
                    "tempoExame": new_tempo
                }

                if len(rec.dropna()):
                    idx = df_pa[df_pa["numeroAtendimento"] == atend_sel].index[0]
                    df_pa.loc[idx, :] = linha_nova.values()
                else:
                    df_pa = pd.concat(
                        [df_pa, pd.DataFrame([linha_nova])],
                        ignore_index=True
                    )

                df_pa.to_csv(pa_path, index=False)
                st.success("Pronto Atendimento salvo! ✅")

    # ================== Aba 2 : Internação ========================
    with tabs_ed[1]:
        int_path = "dados_internacao.csv"
        df_int_all = pd.read_csv(int_path) if os.path.exists(int_path) else pd.DataFrame()
        rec_int = fetch_row(df_int_all, atend_sel)

        with st.form("edit_int"):
            st.subheader("✏️ Editar Internação")
            st.text_input("Hospital", value=rec_int.get("hospital", hosp_sel), disabled=True)
            st.text_input("Número Atendimento", value=atend_sel, disabled=True)

            acomod_e = st.text_input("Acomodação", value=rec_int.get("acomodacao", ""))

            base_dt = datetime.fromisoformat(rec_int["dataHoraInternacao"]) \
                      if rec_int.get("dataHoraInternacao") else datetime.now()
            di_int = st.date_input("Data Internação", base_dt.date())
            ti_int = st.time_input("Hora Internação", base_dt.time())

            exame_e = st.text_input(
                "Exame Solicitado na Internação",
                value=rec_int.get("exameSolicitadoInternacao", "")
            )

            base_sol = datetime.fromisoformat(rec_int["dataHoraSolicitacao"]) \
                       if rec_int.get("dataHoraSolicitacao") else datetime.now()
            dsol = st.date_input("Data Solicitação", base_sol.date(), key="int_sol_d")
            tsol = st.time_input("Hora Solicitação", base_sol.time(), key="int_sol_t")

            base_exc = datetime.fromisoformat(rec_int["dataHoraExecucao"]) \
                       if rec_int.get("dataHoraExecucao") else datetime.now()
            dexc = st.date_input("Data Execução", base_exc.date(), key="int_exc_d")
            texc = st.time_input("Hora Execução", base_exc.time(), key="int_exc_t")

            base_lau = datetime.fromisoformat(rec_int["dataHoraLaudo"]) \
                       if rec_int.get("dataHoraLaudo") else datetime.now()
            dlau = st.date_input("Data Laudo", base_lau.date(), key="int_lau_d")
            tlau = st.time_input("Hora Laudo", base_lau.time(), key="int_lau_t")

            alta_uti_e = st.checkbox(
                "Alta da UTI para Enfermaria",
                value=bool(rec_int.get("altaUTIParaEnfermaria"))
            )
            tempo_uti_e = st.number_input(
                "Tempo UTI (dias)",
                value=int(rec_int.get("tempoUTI") or 0),
                min_value=0
            )

            new_tempo_int = round(
                (datetime.combine(dlau, tlau) - datetime.combine(dsol, tsol)).total_seconds() / 60,
                2
            )
            st.info(f"⏱️ Novo Tempo de Exame: {new_tempo_int} minutos")

            if st.form_submit_button("Salvar Internação"):
                linha_int = {
                    "hospital": hosp_sel,
                    "numeroAtendimento": atend_sel,
                    "acomodacao": acomod_e,
                    "dataHoraInternacao": datetime.combine(di_int, ti_int).isoformat(),
                    "exameSolicitadoInternacao": exame_e,
                    "dataHoraSolicitacao": datetime.combine(dsol, tsol).isoformat(),
                    "dataHoraExecucao": datetime.combine(dexc, texc).isoformat(),
                    "dataHoraLaudo": datetime.combine(dlau, tlau).isoformat(),
                    "tempoExame": new_tempo_int,
                    "altaUTIParaEnfermaria": alta_uti_e,
                    "tempoUTI": tempo_uti_e
                }

                if len(rec_int.dropna()):
                    idx = df_int_all[df_int_all["numeroAtendimento"] == atend_sel].index[0]
                    df_int_all.loc[idx, :] = linha_int.values()
                else:
                    df_int_all = pd.concat(
                        [df_int_all, pd.DataFrame([linha_int])],
                        ignore_index=True
                    )

                df_int_all.to_csv(int_path, index=False)
                st.success("Internação salva! ✅")

    # ================== Aba 3 : Tratamento ========================
    with tabs_ed[2]:
        trat_path = "dados_tratamento.csv"
        df_trat = pd.read_csv(trat_path) if os.path.exists(trat_path) else pd.DataFrame()
        rec_trat = fetch_row(df_trat, atend_sel)

        with st.form("edit_trat"):
            st.subheader("✏️ Editar Tratamento")
            st.text_input("Hospital", value=rec_trat.get("hospital", hosp_sel), disabled=True)
            st.text_input("Número Atendimento", value=atend_sel, disabled=True)

            proc_e = st.text_input(
                "Procedimento Cirúrgico",
                value=rec_trat.get("procedimentoCirurgico", "")
            )
            tipo_e = st.text_input(
                "Tipo de Procedimento Cirúrgico",
                value=rec_trat.get("tipoProcedimentoCirurgico", "")
            )
            grau_e = st.selectbox(
                "Grau de Severidade", ["", "Leve", "Moderado", "Grave"],
                index=["", "Leve", "Moderado", "Grave"].index(rec_trat.get("grauSeveridade", ""))
                if rec_trat.get("grauSeveridade", "") in ["Leve", "Moderado", "Grave"] else 0
            )

            if st.form_submit_button("Salvar Tratamento"):
                reg = {
                    "hospital": hosp_sel,
                    "numeroAtendimento": atend_sel,
                    "procedimentoCirurgico": proc_e,
                    "tipoProcedimentoCirurgico": tipo_e,
                    "grauSeveridade": grau_e
                }
                if len(rec_trat.dropna()):
                    idx = df_trat[df_trat["numeroAtendimento"] == atend_sel].index[0]
                    df_trat.loc[idx, :] = reg.values()
                else:
                    df_trat = pd.concat([df_trat, pd.DataFrame([reg])], ignore_index=True)
                df_trat.to_csv(trat_path, index=False)
                st.success("Tratamento salvo! ✅")

    # ================== Aba 4 : Permanência =======================
    with tabs_ed[3]:
        perm_path = "dados_permanencia.csv"
        df_perm = pd.read_csv(perm_path) if os.path.exists(perm_path) else pd.DataFrame()
        rec_perm = fetch_row(df_perm, atend_sel)

        with st.form("edit_perm"):
            st.subheader("✏️ Editar Permanência")
            st.text_input("Hospital", value=rec_perm.get("hospital", hosp_sel), disabled=True)
            st.text_input("Número Atendimento", value=atend_sel, disabled=True)

            risco_e = st.text_input(
                "Estratificação de Risco",
                value=rec_perm.get("estratificacaoRisco", "")
            )
            prev_e = st.number_input(
                "Permanência Prevista DRG",
                value=int(rec_perm.get("permanenciaPrevistaDRG") or 0),
                min_value=0
            )
            real_e = st.number_input(
                "Permanência Real",
                value=int(rec_perm.get("permanenciaReal") or 0),
                min_value=0
            )
            alta_dt_base = datetime.fromisoformat(rec_perm["dataAlta"]) \
                           if rec_perm.get("dataAlta") else datetime.now()
            alta_e = st.date_input("Data de Alta", alta_dt_base.date())
            acom_e = st.text_input("Acomodação (na alta)", value=rec_perm.get("acomodacao", ""))

            if st.form_submit_button("Salvar Permanência"):
                reg = {
                    "hospital": hosp_sel,
                    "numeroAtendimento": atend_sel,
                    "estratificacaoRisco": risco_e,
                    "permanenciaPrevistaDRG": prev_e,
                    "permanenciaReal": real_e,
                    "dataAlta": alta_e.isoformat(),
                    "acomodacao": acom_e
                }
                if len(rec_perm.dropna()):
                    idx = df_perm[df_perm["numeroAtendimento"] == atend_sel].index[0]
                    df_perm.loc[idx, :] = reg.values()
                else:
                    df_perm = pd.concat([df_perm, pd.DataFrame([reg])], ignore_index=True)
                df_perm.to_csv(perm_path, index=False)
                st.success("Permanência salva! ✅")

    # ================== Aba 5 : Pós‑Alta ==========================
    with tabs_ed[4]:
        pos_path = "dados_pos_alta.csv"
        df_pos = pd.read_csv(pos_path) if os.path.exists(pos_path) else pd.DataFrame()
        rec_pos = fetch_row(df_pos, atend_sel)

        with st.form("edit_pos"):
            st.subheader("✏️ Editar Pós‑Alta")
            st.text_input("Hospital", value=rec_pos.get("hospital", hosp_sel), disabled=True)
            st.text_input("Número Atendimento", value=atend_sel, disabled=True)

            gest_e = st.selectbox(
                "Gestão de Crônicos", ["", "Sim", "Não"],
                index=["", "Sim", "Não"].index(rec_pos.get("gestaoCronicos", ""))
                if rec_pos.get("gestaoCronicos", "") in ["Sim", "Não"] else 0
            )
            rein_e = st.selectbox(
                "Reinternação", ["", "Sim", "Não"],
                index=["", "Sim", "Não"].index(rec_pos.get("reinternacao", ""))
                if rec_pos.get("reinternacao", "") in ["Sim", "Não"] else 0
            )
            quant_e = st.number_input(
                "Quantidade", value=int(rec_pos.get("quantidade") or 0), min_value=0
            )
            obs_e = st.text_area("Observação", value=rec_pos.get("observacao", ""))

            if st.form_submit_button("Salvar Pós‑Alta"):
                reg = {
                    "hospital": hosp_sel,
                    "numeroAtendimento": atend_sel,
                    "gestaoCronicos": gest_e,
                    "reinternacao": rein_e,
                    "quantidade": quant_e,
                    "observacao": obs_e
                }
                if len(rec_pos.dropna()):
                    idx = df_pos[df_pos["numeroAtendimento"] == atend_sel].index[0]
                    df_pos.loc[idx, :] = reg.values()
                else:
                    df_pos = pd.concat([df_pos, pd.DataFrame([reg])], ignore_index=True)
                df_pos.to_csv(pos_path, index=False)
                st.success("Pós‑Alta salva! ✅")

    # ================== Aba 6 : Questionários =====================
    with tabs_ed[5]:
        q_path = "dados_questionarios.csv"
        df_q = pd.read_csv(q_path) if os.path.exists(q_path) else pd.DataFrame()
        rec_q = fetch_row(df_q, atend_sel)

        with st.form("edit_q"):
            st.subheader("✏️ Editar Questionários")
            st.text_input("Hospital", value=rec_q.get("hospital", hosp_sel), disabled=True)
            st.text_input("Número Atendimento", value=atend_sel, disabled=True)

            registro = {
                "hospital": hosp_sel,
                "numeroAtendimento": atend_sel
            }
            for dia in [7, 30, 60, 90]:
                d_key = f"dataQuestionarioPaciente{dia}"
                o_key = f"observacaoQuestionarioPaciente{dia}"

                base_dt = datetime.fromisoformat(rec_q[d_key]) \
                          if rec_q.get(d_key) else datetime.now()
                data_e  = st.date_input(
                    f"Data Questionário – Dia {dia}",
                    base_dt.date(), key=f"q_d_{dia}"
                )
                obs_e   = st.text_area(
                    f"Observação Dia {dia}",
                    value=rec_q.get(o_key, ""),
                    key=f"q_o_{dia}"
                )

                registro[d_key] = data_e.isoformat()
                registro[o_key] = obs_e

            if st.form_submit_button("Salvar Questionários"):
                if len(rec_q.dropna()):
                    idx = df_q[df_q["numeroAtendimento"] == atend_sel].index[0]
                    df_q.loc[idx, :] = registro.values()
                else:
                    df_q = pd.concat([df_q, pd.DataFrame([registro])], ignore_index=True)
                df_q.to_csv(q_path, index=False)
                st.success("Questionários salvos! ✅")

# ==================================================================
#                               INDICADORES
# ==================================================================
elif menu == "Indicadores":
    st.subheader("📈 Indicadores (em breve)")
    st.info("Aqui virão gráficos e métricas geradas a partir dos CSVs.")
