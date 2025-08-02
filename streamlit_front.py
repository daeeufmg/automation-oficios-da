import streamlit as st
import datetime
from generate_oficio import gerar_pdf

def main():
    st.title("Gerador de Ofício DAEE - UFMG")

    # Listas de cursos de graduação e pós-graduação
    cursos_graduacao = [
        "Engenharia Aeroespacial",
        "Engenharia Ambiental",
        "Engenharia Civil",
        "Engenharia de Controle e Automação",
        "Engenharia Elétrica",
        "Engenharia Mecânica",
        "Engenharia Metalúrgica e de Materiais",
        "Engenharia de Minas",
        "Engenharia de Produção",
        "Engenharia Química",
        "Engenharia de Sistemas",
        "Engenharia de Computação"
    ]
    
    # Listas de programas de pós-graduação em formato completo e abreviado
    cursos_pos_graduacao_completos = [
        "Programa de Pós-Graduação em Ciências e Técnicas Nucleares",
        "Programa de Pós-Graduação em Engenharia Elétrica",
        "Programa de Pós-Graduação em Engenharia de Estruturas",
        "Programa de Pós-Graduação em Engenharia de Produção",
        "Programa de Pós-Graduação em Engenharia Mecânica",
        "Programa de Pós-Graduação em Engenharia Metalúrgica, Materiais e de Minas",
        "Programa de Pós-Graduação em Engenharia Química",
        "Programa de Pós-Graduação em Saneamento, Meio Ambiente e Recursos Hídricos",
        "Programa de Pós-Graduação em Construção Civil",
        "Programa de Pós-Graduação em Geotecnia e Transportes"
    ]

    cursos_pos_graduacao_abreviados = [
        "PPG em Ciências e Técnicas Nucleares",
        "PPG em Engenharia Elétrica",
        "PPG em Engenharia de Estruturas",
        "PPG em Engenharia de Produção",
        "PPG em Engenharia Mecânica",
        "PPG em Engenharia Metalúrgica, Materiais e de Minas",
        "PPG em Engenharia Química",
        "PPG em Saneamento, Meio Ambiente e Recursos Hídricos",
        "PPG em Construção Civil",
        "PPG em Geotecnia e Transportes"
    ]
    
    # Dicionário para mapear nomes abreviados para completos (para salvar no estado)
    map_abreviado_para_completo = dict(zip(cursos_pos_graduacao_abreviados, cursos_pos_graduacao_completos))
    # Dicionário para mapear nomes completos para abreviados (para exibir no selectbox)
    map_completo_para_abreviado = dict(zip(cursos_pos_graduacao_completos, cursos_pos_graduacao_abreviados))

    # Cria uma lista única com separadores visuais para o selectbox
    cursos_agrupados_display = [
        "-- Graduação --",
        *cursos_graduacao,
        "-- Pós-Graduação --",
        *cursos_pos_graduacao_abreviados
    ]
    
    # Lista de separadores para verificação
    separadores = ["-- Graduação --", "-- Pós-Graduação --"]

    if "cadeiras" not in st.session_state:
        st.session_state.cadeiras = []

    st.markdown("---")
    st.subheader("Dados do Ofício")
    
    # Organiza o número do Ofício e a Data na mesma linha
    cols_oficio_data = st.columns(2)
    oficio = cols_oficio_data[0].text_input("Número do Ofício", "46/2025")
    data = cols_oficio_data[1].date_input("Data", value=datetime.date(2025, 6, 4))
    
    # Organiza o Nome do Órgão e o Tipo do Órgão em uma nova linha, com o campo de tipo menor
    cols_orgao = st.columns([0.7, 0.3])
    orgao = cols_orgao[0].text_input("Órgão", "Colegiado do Programa de Pós-Graduação em Engenharia Química")
    tipo_orgao = cols_orgao[1].selectbox("Tipo do Órgão", ["O", "A"], index=0)
    
    st.markdown("---")
    st.subheader("Dados dos Contatos")

    cols_contato = st.columns(3)
    presidente = cols_contato[0].text_input("Presidente do DA", "TALVANI DE SOUZA BARBOSA")
    contato_da = cols_contato[1].text_input("Contato DA", "da@eng.ufmg.br")
    contato_presidente = cols_contato[2].text_input("Contato Presidente", "talvaniufmg@outlook.com | 31 97345-1487")

    st.markdown("---")
    st.subheader("Gestão de Cadeiras")

    # Exibir as cadeiras e o botão de deletar
    for i, cadeira in enumerate(st.session_state.cadeiras):
        with st.expander(f"Cadeira {i + 1}  ", expanded=True):
            col_exp_title, col_exp_btn = st.columns([0.9, 0.1])
            col_exp_title.markdown(f"**Detalhes da Cadeira {i + 1}**")
            
            if col_exp_btn.button("🗑️", key=f"delete_btn_{i}", help="Deletar esta cadeira"):
                del st.session_state.cadeiras[i]
                st.rerun()

            # Campos do titular
            st.markdown("##### Titular")
            cols_titular_1, cols_titular_2 = st.columns(2)
            cadeira["titular"]["nome"] = cols_titular_1.text_input("Nome", cadeira["titular"]["nome"], key=f"t_nome_{i}")
            
            # Lógica para exibir o nome abreviado e salvar o nome completo
            curso_armazenado_titular = cadeira["titular"]["curso"]
            curso_exibido_titular = map_completo_para_abreviado.get(curso_armazenado_titular, curso_armazenado_titular)
            
            if curso_exibido_titular in cursos_agrupados_display:
                curso_titular_index = cursos_agrupados_display.index(curso_exibido_titular)
            else:
                curso_titular_index = 1 # Padrão para o primeiro curso de graduação
                
            selected_curso_titular_display = cols_titular_2.selectbox("Curso", cursos_agrupados_display, index=curso_titular_index, key=f"t_curso_{i}")
            
            if selected_curso_titular_display not in separadores:
                # Salva o nome completo se for um PPG, ou o nome normal se for graduação
                cadeira["titular"]["curso"] = map_abreviado_para_completo.get(selected_curso_titular_display, selected_curso_titular_display)

            cols_titular_3, cols_titular_4 = st.columns(2)
            cadeira["titular"]["matricula"] = cols_titular_3.text_input("Matrícula", cadeira["titular"]["matricula"], key=f"t_matricula_{i}")
            cadeira["titular"]["telefone"] = cols_titular_4.text_input("Telefone", cadeira["titular"]["telefone"], key=f"t_telefone_{i}")

            cols_titular_5, cols_titular_6 = st.columns(2)
            cadeira["titular"]["email"] = cols_titular_5.text_input("Email", cadeira["titular"]["email"], key=f"t_email_{i}")
            cadeira["titular"]["email_ufmg"] = cols_titular_6.text_input("Email UFMG", cadeira["titular"]["email_ufmg"], key=f"t_email_ufmg_{i}")


            # Campos do suplente
            st.markdown("##### Suplente")
            cols_suplente_1, cols_suplente_2 = st.columns(2)
            cadeira["suplente"]["nome"] = cols_suplente_1.text_input("Nome", cadeira["suplente"]["nome"], key=f"s_nome_{i}")
            
            # Lógica para exibir o nome abreviado e salvar o nome completo
            curso_armazenado_suplente = cadeira["suplente"]["curso"]
            curso_exibido_suplente = map_completo_para_abreviado.get(curso_armazenado_suplente, curso_armazenado_suplente)

            if curso_exibido_suplente in cursos_agrupados_display:
                curso_suplente_index = cursos_agrupados_display.index(curso_exibido_suplente)
            else:
                curso_suplente_index = 1 # Padrão para o primeiro curso de graduação
            
            selected_curso_suplente_display = cols_suplente_2.selectbox("Curso", cursos_agrupados_display, index=curso_suplente_index, key=f"s_curso_{i}")

            if selected_curso_suplente_display not in separadores:
                # Salva o nome completo se for um PPG, ou o nome normal se for graduação
                cadeira["suplente"]["curso"] = map_abreviado_para_completo.get(selected_curso_suplente_display, selected_curso_suplente_display)
            
            cols_suplente_3, cols_suplente_4 = st.columns(2)
            cadeira["suplente"]["matricula"] = cols_suplente_3.text_input("Matrícula", cadeira["suplente"]["matricula"], key=f"s_matricula_{i}")
            cadeira["suplente"]["telefone"] = cols_suplente_4.text_input("Telefone", cadeira["suplente"]["telefone"], key=f"s_telefone_{i}")

            cols_suplente_5, cols_suplente_6 = st.columns(2)
            cadeira["suplente"]["email"] = cols_suplente_5.text_input("Email", cadeira["suplente"]["email"], key=f"s_email_{i}")
            cadeira["suplente"]["email_ufmg"] = cols_suplente_6.text_input("Email UFMG", cadeira["suplente"]["email_ufmg"], key=f"s_email_ufmg_{i}")
        
        st.markdown("---")

    # Botão para adicionar uma nova cadeira (agora no final)
    if st.button("Adicionar Cadeira +"):
        st.session_state.cadeiras.append({
            "titular": {
                "nome": "",
                "curso": cursos_graduacao[0], # Define o curso padrão ao adicionar
                "matricula": "",
                "email": "",
                "email_ufmg": "",
                "telefone": "",
                "tipo": "Titular"
            },
            "suplente": {
                "nome": "",
                "curso": cursos_graduacao[0], # Define o curso padrão ao adicionar
                "matricula": "",
                "email": "",
                "email_ufmg": "",
                "telefone": "",
                "tipo": "Suplente"
            }
        })
        st.rerun()
        
    # Botão principal para gerar o PDF
    if st.button("Gerar PDF"):
        config = {
            "oficio": oficio,
            "data": data,
            "orgao": orgao,
            "tipo_orgao": tipo_orgao,
            "presidente": presidente,
            "contato_da": contato_da,
            "contato_presidente": contato_presidente,
            "cadeiras": st.session_state.cadeiras
        }

        try:
            pdf_buffer = gerar_pdf(config)
            st.success("PDF gerado com sucesso!")
            st.download_button(
                label="Baixar PDF",
                data=pdf_buffer,
                file_name=f"Oficio_{oficio.replace('/', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")

if __name__ == "__main__":
    main()
