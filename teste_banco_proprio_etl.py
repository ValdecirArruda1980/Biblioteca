import pandas as pd
import sqlite3

print("=" * 60)
print("TESTE 2: ABORDAGEM BANCO PRÓPRIO (PIPELINE DE ETL E CLEANING)")
print("=" * 60)

# 1. Dados Brutos Inconsistentes
dados_brutos = {
    'id_emprestimo': [1, 2, 3, 4, 5],
    'nome_aluno': [' Valdecir Arruda ', 'jessica silva', 'VALDECIR ARRUDA', 'Ana Souza', 'Carlos Lima'],
    'curso': ['Engenharia de Software', 'engenharia de software', 'Eng. Software', 'Técnico em Dados', 'Téc. Dados'],
    'titulo_livro': ['Python Data Science', 'Clean Code', 'Python Data Science', 'SQL para Leigos', 'Clean Code'],
    'data_emprestimo': ['2026-08-01', '2026-08-03', '2026/08/05', '06/08/2026', '2026-08-10']
}

df_raw = pd.DataFrame(dados_brutos)
print("\n[1] Dados Brutos Recebidos:")
print(df_raw[['nome_aluno', 'curso', 'data_emprestimo']])

# 2. Transformação (ETL)
def padronizar_curso(curso):
    curso = str(curso).lower()
    if 'eng' in curso:
        return 'Engenharia de Software'
    elif 'dado' in curso:
        return 'Técnico em Ciência de Dados'
    return 'Outros'

df_cleaned = df_raw.copy()
df_cleaned['nome_aluno'] = df_cleaned['nome_aluno'].str.strip().str.title()
df_cleaned['curso'] = df_cleaned['curso'].apply(padronizar_curso)
df_cleaned['data_emprestimo'] = pd.to_datetime(df_cleaned['data_emprestimo'], dayfirst=False, format='mixed')

print("\n[2] Dados Tratados e Padronizados:")
print(df_cleaned[['nome_aluno', 'curso', 'data_emprestimo']])

# 3. Carga no Banco Relacional (SQLite em memória para teste)
conn = sqlite3.connect(':memory:')
df_cleaned.to_sql('fato_emprestimos', conn, index=False, if_exists='replace')

# Validação com SQL Analítico
query = """
SELECT curso, COUNT(*) as total_emprestimos 
FROM fato_emprestimos 
GROUP BY curso
"""
df_resultado = pd.read_sql_query(query, conn)
print("\n[3] Consulta SQL Analítica no Banco Resultante:")
print(df_resultado)
