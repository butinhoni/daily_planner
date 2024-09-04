import funcoes
import streamlit as st
import datetime as dt
import random
import os


dict_weekdays = {
    0: 'Segunda',
    1: 'Terça',
    2: 'Quarta',
    3: 'Quinta',
    4: 'Sexta',
    5: 'Sábado',
    6: 'Domingo'
}
moods = ['Voando','Bem', 'Normal', 'Mal','Derrubado']
#pega a data e o dia da semana
today = dt.datetime.today()
weekday = today.weekday()
dia_semana = dict_weekdays[weekday]
today = today.date()

#importa as coisas do banco de dados
tarefas = funcoes.read_tarefas()
frases = funcoes.read_frases()
manha = funcoes.read_morning_mood()
rotinas = funcoes.read_subtipos()
check = funcoes.read_tarefas_check()
imagens = os.listdir('imagens')



#vamos checar se o dia já começou
if today in manha['data'].to_list():
    day_started = bool(True)
else:
    day_started = bool(False)

#agora vamos checar se o dia já acabou
tarde = manha[manha['end'] == bool(False)]
if today in tarde['data'].to_list():
    day_end = bool(False)
else:
    day_end = bool(True)

#vou colocar um dicionario pra pautar o fim do dia baseado no desempenho
dict_result = {
    'Perfeito': 'Parabéns mano, tu cumpriu tudo que definiu pra hoje, isso é mó bom, mas se acontecer direto pode ser que esteja definindo objetivos de menos, daí pode tentar colocar uns opcionais a mais. Mas é isso, parabéns',
    'Ótimo': 'Ótimo mano, cumprimos quase tudo, não foi tudo, mas ta bom, PRA CIMA, VAMOS POR MAIS',
    'Aceitável': 'Mano, cumprimos bastante coisa, mas tem espaço pra melhorar né. vamos pra cima SEGUIMOS',
    'Ruim': 'Hoje não foi legal, mas mano, é normal também. acontece, ninguem vai ter todos os dias bons, todo mundo oscila, temos dias bons e ruins, amanhã tem mais.'
}


#Iniciar o dia
#essa parte vai ter que popular a tabela de check, como tudo como falso no default
tarefas['dias'] = list(tarefas['dias'].str.split(','))
hoje_tem = []

for i, row in tarefas.iterrows():
    if dia_semana in row['dias']:
        hoje_tem.append('sim')
    else:
        hoje_tem.append('não')
tarefas['hoje_tem'] = hoje_tem

tarefas_dia = tarefas[tarefas['hoje_tem'] == 'sim']
check_dia = check[check['data'] == today]
#check_dia['tipo'] = 'vazio'

#coloca a frase motivacional e seta o humor do dia
#essa parte também vai popular as tarefas do dia
if not day_started:
    imagem = random.choice(imagens)
    imagem = os.path.join('imagens',imagem)
    frase = random.choice(frases['frase'].to_list())
    autor = frases[frases['frase'] == frase]
    autor = autor['autor'].iloc[0]
    st.image(imagem)
    st.header(frase)
    st.markdown(autor)
    st.divider()
    st.header("Como está se sentindo hoje amigo?")
    for mood in moods:
        botão = st.button(mood,key = f'botao{mood}')
        if botão:
            funcoes.insert_morning_mood(today,mood)
            for i, row in tarefas_dia.iterrows():
                tarefa = row['tarefa']
                rotina = row['subtipo']
                funcoes.insert_diario_check(today, tarefa, rotina)

#antes de continar com a parte visual vamos fazer as contas das porcentagens e de quantas tarefas já foram feitas ou não
n_tarefas_feitas = check_dia['feita'].to_list().count(bool(True))
n_tarefas_nfeitas = check_dia['feita'].to_list().count(bool(False))
n_tarefas_dia = n_tarefas_nfeitas + n_tarefas_feitas
percent_dia = n_tarefas_feitas/n_tarefas_dia

#progresso geral do dia
if day_started and not day_end:
    cont_geral = st.container(border=True)
    cont_geral.markdown("Progresso Geral do Dia")
    cont_geral.text(f"{n_tarefas_feitas}/{n_tarefas_dia} Tarefas concluidas | {percent_dia*100:.2f}% Concluído" )
    cont_geral.progress(percent_dia)
    col1, col2 = cont_geral.columns(2)
    end_day = col2.button("Finalizar o dia")
    end_mood = col1.selectbox("Humor no fim do dia", moods) # depois tem que arrumar isso acho que não vai ficar bom, pode por junto com a msg final
    #tratar os dados pra levar pra tela de encerrar o dia
    if end_day:
        funcoes.end_day(today,end_mood)
        st.rerun()


#progresso por rotina (gostei dessa ideia)
if day_started and not day_end:
    for rotina in rotinas['subtipo'].to_list():
        exp = st.expander(rotina)
        df = tarefas_dia[tarefas_dia['subtipo'] == rotina]
        df2 = check_dia[check_dia['rotina'] == rotina]
        n_rotina_feitas = df2['feita'].to_list().count(bool(True))
        n_rotina_nfeitas = df2['feita'].to_list().count(bool(False))
        n_rotina_total = n_rotina_feitas + n_rotina_nfeitas
        percent_rotina = n_rotina_feitas/n_rotina_total
        exp.text(f'{n_rotina_feitas}/{n_rotina_total} | {percent_rotina*100:.2f}% Concluída')
        exp.progress(percent_rotina)
        for i, row in df.iterrows():
            tarefa_atual = row['tarefa']
            contTar = exp.container(border=True)
            col1, col2 = contTar.columns(2)
            col1.text(tarefa_atual)
            if check_dia.loc[check_dia['tarefa'] == tarefa_atual]['feita'].iloc[0]:
                col2.markdown(':blue[Feito]')
            else:
                botao2 = col2.button('Concluir', key=f'button{tarefa_atual}',type='primary')
            try:
                if botao2:
                    funcoes.tarefa_done(today,tarefa_atual)
                    st.rerun()
            except:
                pass



#tela de encerrar o dia
if day_end:
    imagem = random.choice(imagens)
    imagem = os.path.join('imagens',imagem)
    frase = random.choice(frases['frase'].to_list())
    autor = frases[frases['frase'] == frase]
    autor = autor['autor'].iloc[0]
    cont = st.container(border=True)
    cont.image(imagem)
    cont.subheader(frase)
    cont.text(autor)

    st.header("Parabéns amigo, você chegou ao fim do dia")
    st.markdown(f"Voce cumpriu {percent_dia*100:.0f}% do que você tinha determinado pra hoje")
    result = funcoes.dia_bão(percent_dia)
    st.markdown(dict_result[result])
    st.subheader('Mano, use esse espaço pra refletir sobre seu dia, tenta pensar sobre as ações que se orgulha e as que não se orgulha também, tenta revisitar as etapas do seu dia')
    reflex = st.text_area('Reflexão')
    fim = st.button('Encerrar o dia', type='primary')
    if fim:
        reflex(today, reflex)

