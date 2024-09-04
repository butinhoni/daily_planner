import streamlit as st
import funcoes

weekdays = ['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo']

tipos = ['Obrigatória', 'Opcional']
frequencias = ['Todo dia', 'Dias uteis', 'Dias especificos']


st.header('Cadastro de Rotinas')
with st.expander("Novo Subtipo", expanded= False):
    subtipo = st.text_input('Subtipo')
    cad_tipo = st.button("Cadastrar")
    if cad_tipo:
        funcoes.insert_subtipo(subtipo)

tarsubs = funcoes.read_subtipos()
tarsubs = tarsubs['subtipo'].to_list()

st.header('Cadastro de Tarefas')

tar = st.expander('Nova Tarefa', expanded= True)
col1, col2 = tar.columns(2)
tar_name = col1.text_input("Nome da Tarefa")
tar_freq = col2.selectbox('Frequencia', frequencias)
tar_tipo = col1.selectbox('Tipo',tipos)
tar_sub = col2.selectbox('Rotina',tarsubs)
tar_dias = []

if tar_freq == 'Todo dia':
    tar_dias = weekdays
if tar_freq == 'Dias uteis':
    tar_dias = weekdays[:5]

if tar_freq == 'Dias especificos':
    for day in weekdays:
        check = tar.checkbox(day, False, key = f'check{day}')
        if check == True:
            tar_dias.append(day)

cad_tarefa = tar.button("Cadastrar tarefa")
tar_dias_str = ','.join(map(str, tar_dias))
#tar_data = [tar_name, tar_freq, tar_tipo, tar_sub, tar_dias_str]

if cad_tarefa:
    funcoes.insert_tarefa(tar_name, tar_freq, tar_tipo, tar_sub, tar_dias_str)

