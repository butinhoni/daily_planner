import psycopg2
import pandas as pd

host_server = '10.147.20.66'


def read_subtipos():
    conn = psycopg2.connect(database = 'prog_diario',
            user = 'postgres',
            host = host_server,
            password = '051296',
            port = 5432)

    cur = conn.cursor()
    cur.execute('SELECT * FROM public.subtipos')
    colunas = ['id','subtipo']
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=colunas)
    df['subtipo'] = df['subtipo'].str.title()
    cur.close()
    conn.close()
    return(df)

def read_tarefas():
    conn = psycopg2.connect(database = 'prog_diario',
                user = 'postgres',
                host = host_server,
                password = '051296',
                port = 5432)

    cur = conn.cursor()
    cur.execute('SELECT * FROM public.tarefas')
    colunas = ['tarefa','frequencia','tipo','subtipo','dias']
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=colunas)
    cur.close()
    conn.close()
    return(df)

def read_tarefas_check():
    conn = psycopg2.connect(database = 'prog_diario',
            user = 'postgres',
            host = host_server,
            password = '051296',
            port = 5432)

    cur = conn.cursor()
    cur.execute('SELECT * FROM public.diario_check')
    colunas = ['data','tarefa', 'feita','rotina']
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=colunas)
    cur.close()
    conn.close()
    return(df)    

def read_frases():
    conn = psycopg2.connect(database = 'prog_diario',
        user = 'postgres',
        host = host_server,
        password = '051296',
        port = 5432)

    cur = conn.cursor()
    cur.execute('SELECT * FROM public.motivacionais')
    colunas = ['id','frase','autor']
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=colunas)
    cur.close()
    conn.close()
    return(df)

def read_morning_mood():
    conn = psycopg2.connect(database = 'prog_diario',
        user = 'postgres',
        host = host_server,
        password = '051296',
        port = 5432)

    cur = conn.cursor()
    cur.execute('SELECT * FROM public.morning_mood')
    colunas = ['data','humor','end','end_humor','diario']
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=colunas)
    cur.close()
    conn.close()
    return(df)

def insert_subtipo(sub):
    conn = psycopg2.connect(database = 'prog_diario',
            user = 'postgres',
            host = host_server,
            password = '051296',
            port = 5432)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO public.subtipos(subtipo) VALUES ('{sub}')");
    cur.close()
    conn.commit()
    conn.close()

def insert_tarefa(name,freq,tipo,subtipo,dias):
    conn = psycopg2.connect(database = 'prog_diario',
        user = 'postgres',
        host = host_server,
        password = '051296',
        port = 5432)
    cur = conn.cursor()
    #for d in data:
        #query = cur.mogrify("INSERT INTO public.tarefas(tarefa, frequencia, tipo, subtipo, dias) VALUES (%s, %s, %s, %s, %s)", d)
    cur.execute(f"INSERT INTO public.tarefas(tarefa, frequencia, tipo, subtipo, dias) VALUES ('{name}','{freq}','{tipo}','{subtipo}','{dias}')");
    cur.close()
    conn.commit()
    conn.close()

def insert_diario_check(dia, tarefa, rotina):
    conn = psycopg2.connect(database = 'prog_diario',
        user = 'postgres',
        host = host_server,
        password = '051296',
        port = 5432)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO public.diario_check(data, tarefa, feita, rotina) VALUES ('{dia}','{tarefa}','False', '{rotina}')")
    cur.close()
    conn.commit()
    conn.close()

def insert_morning_mood(dia,mood):
    conn = psycopg2.connect(database = 'prog_diario',
        user = 'postgres',
        host = host_server,
        password = '051296',
        port = 5432)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO public.morning_mood(data, mood) VALUES ('{dia}','{mood}')")
    cur.close()
    conn.commit()
    conn.close()

def tarefa_done(dia, tarefa):
    conn = psycopg2.connect(database = 'prog_diario',
        user = 'postgres',
        host = host_server,
        password = '051296',
        port = 5432)
    cur = conn.cursor() 
    cur.execute(f"""UPDATE public.diario_check
                SET feita = True
                WHERE data = '{dia}' AND tarefa = '{tarefa}'""")
    cur.close()
    conn.commit()
    conn.close()

def end_day(dia, humor):
    conn = psycopg2.connect(database = 'prog_diario',
        user = 'postgres',
        host = host_server,
        password = '051296',
        port = 5432)
    cur = conn.cursor() 
    cur.execute(f"""UPDATE public.morning_mood 
                SET "end" = 'true' 
                WHERE "data" = '{dia}'""")
    cur.execute(f"""UPDATE public.morning_mood 
                SET "end_mood" = '{humor}' 
                WHERE "data" = '{dia}'""")
    cur.close()
    conn.commit()
    conn.close()

def reflex(dia, msg):
    conn = psycopg2.connect(database = 'prog_diario',
        user = 'postgres',
        host = host_server,
        password = '051296',
        port = 5432)
    cur = conn.cursor()
    cur.execute(f"""UPDATE public.morning_mood
                SET "reflexao" = '{msg}'
                WHERE "data" = '{dia}'
                """)
    cur.close()
    conn.commit()
    conn.close()

def dia_bão(percent):
    if percent == 1:
        return('Perfeito')
    if percent > 0.8:
        return("Ótimo")
    if percent > 0.5:
        return('Aceitável')
    if percent > 0:
        return('Ruim')
    else:
        return('Zero')