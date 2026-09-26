import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics.pairwise import cosine_similarity

print("=" * 60)
print("TESTE 1: ABORDAGEM KOHA (ANÁLISE PREDITIVA E RECOMENDAÇÃO)")
print("=" * 60)

# ---------------------------------------------------------
# TESTE A: Previsão de Demanda Mensal de Empréstimos
# ---------------------------------------------------------
print("\n--- A: PREVISÃO DE DEMANDA DE EMPRÉSTIMOS ---")

np.random.seed(42)
datas = pd.date_range(start='2024-01-01', periods=24, freq='ME')
demanda_historica = [120, 150, 310, 280, 260, 210, 110, 340, 290, 270, 220, 90,
                     130, 160, 330, 290, 270, 220, 115, 350, 300, 280, 230, 95]

df_demanda = pd.DataFrame({'Data': datas, 'Emprestimos': demanda_historica})
df_demanda['Mes'] = df_demanda['Data'].dt.month
df_demanda['Lag_1M'] = df_demanda['Emprestimos'].shift(1)
df_demanda.dropna(inplace=True)

X = df_demanda[['Mes', 'Lag_1M']]
y = df_demanda['Emprestimos']

X_train, X_test = X[:-4], X[-4:]
y_train, y_test = y[:-4], y[-4:]

model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
model_rf.fit(X_train, y_train)

predicoes = model_rf.predict(X_test)

print(f"Erro Médio Absoluto (MAE): {mean_absolute_error(y_test, predicoes):.2f} livros")
print("Valores Reais dos últimos 4 meses:", list(y_test))
print("Valores Previstos pelo Modelo:    ", [round(p, 1) for p in predicoes])

# ---------------------------------------------------------
# TESTE B: Sistema de Recomendação (Filtragem Colaborativa)
# ---------------------------------------------------------
print("\n--- B: SISTEMA DE RECOMENDAÇÃO ---")

dados_interacao = {
    'Aluno_ID': [101, 101, 101, 102, 102, 103, 103, 104, 104, 105],
    'Livro': ['Python para Dados', 'Engenharia de Software', 'Clean Code', 
              'Python para Dados', 'Clean Code', 'Engenharia de Software', 
              'Banco de Dados SQL', 'Banco de Dados SQL', 'Python para Dados', 'Clean Code'],
    'Score': [5, 4, 5, 5, 4, 5, 5, 4, 5, 4]
}

df_interacoes = pd.DataFrame(dados_interacao)
matriz_usuario_item = df_interacoes.pivot_table(index='Aluno_ID', columns='Livro', values='Score').fillna(0)

similaridade = cosine_similarity(matriz_usuario_item.T)
df_similaridade = pd.DataFrame(similaridade, index=matriz_usuario_item.columns, columns=matriz_usuario_item.columns)

print("Matriz de Similaridade entre Livros:")
print(df_similaridade.round(2))
