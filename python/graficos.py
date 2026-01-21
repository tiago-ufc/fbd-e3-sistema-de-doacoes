import pandas as pd
import matplotlib.pyplot as plt
import panel as pn

pn.extension('matplotlib')


def _safe_df_query(query, cnx):
    try:
        df = pd.read_sql_query(query, cnx)
        return df
    except Exception as e:
        raise


def grafico_doacoes_por_campanha(cnx):
    """Quantidade de doações por campanha"""
    try:
        df = _safe_df_query(
            "SELECT c.nome, COUNT(d.id_doacao) as total FROM doacao d JOIN campanha c ON d.id_campanha = c.id_campanha GROUP BY c.nome ORDER BY total DESC",
            cnx,
        )
        if df.empty:
            return pn.pane.Alert('Nenhum dado encontrado para Doações por Campanha.', alert_type='warning')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df["nome"], df["total"], color='#1f77b4', edgecolor='black')
        ax.set_title("Doações por Campanha", fontsize=14, fontweight='bold')
        ax.set_ylabel("Total de Doações", fontsize=12)
        ax.set_xlabel("Campanha", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')
    except Exception as e:
        return pn.pane.Alert(f'Erro ao gerar gráfico: {str(e)}', alert_type='danger')


def grafico_status_ordens(cnx):
    """Distribuição de status das ordens de doação"""
    try:
        df = _safe_df_query(
            "SELECT status, COUNT(id_ordem_doacao) as total FROM ordem_de_doacao GROUP BY status",
            cnx,
        )
        if df.empty:
            return pn.pane.Alert('Nenhum dado encontrado para Status das Ordens.', alert_type='warning')
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = ['#2ca02c', '#ff7f0e', '#d62728', '#9467bd']
        ax.pie(df["total"], labels=df["status"], autopct='%d', colors=colors[: len(df)], startangle=90)
        ax.set_title("Status das Ordens de Doação", fontsize=14, fontweight='bold')
        return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')
    except Exception as e:
        return pn.pane.Alert(f'Erro ao gerar gráfico: {str(e)}', alert_type='danger')


def grafico_tipos_itens(cnx):
    """Itens mais doados (Top 10)"""
    try:
        df = _safe_df_query(
            "SELECT nome, COUNT(id_item) as total FROM item_doacao GROUP BY nome ORDER BY total DESC LIMIT 10",
            cnx,
        )
        if df.empty:
            return pn.pane.Alert('Nenhum dado encontrado para Itens Mais Doados.', alert_type='warning')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(df["nome"], df["total"], color='#17becf', edgecolor='black')
        ax.set_title("Top 10 Itens Mais Doados", fontsize=14, fontweight='bold')
        ax.set_xlabel("Quantidade", fontsize=12)
        for i, v in enumerate(df["total"]):
            ax.text(v + 0.1, i, str(int(v)), va='center')
        plt.tight_layout()
        return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')
    except Exception as e:
        return pn.pane.Alert(f'Erro ao gerar gráfico: {str(e)}', alert_type='danger')


def grafico_campanhas_status(cnx):
    """Status das campanhas"""
    try:
        df = _safe_df_query(
            "SELECT status, COUNT(id_campanha) as total FROM campanha GROUP BY status",
            cnx,
        )
        if df.empty:
            return pn.pane.Alert('Nenhum dado encontrado para Status das Campanhas.', alert_type='warning')
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = ['#2ca02c', '#ff7f0e', '#d62728']
        ax.pie(df["total"], labels=df["status"], autopct='%d', colors=colors[: len(df)], startangle=90)
        ax.set_title("Status das Campanhas", fontsize=14, fontweight='bold')
        return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')
    except Exception as e:
        return pn.pane.Alert(f'Erro ao gerar gráfico: {str(e)}', alert_type='danger')


def grafico_peso_itens(cnx):
    """Peso total dos itens por campanha"""
    try:
        df = _safe_df_query(
            "SELECT c.nome, SUM(item.peso) as peso_total FROM item_doacao item JOIN doacao d ON item.id_doacao = d.id_doacao JOIN campanha c ON d.id_campanha = c.id_campanha GROUP BY c.nome ORDER BY peso_total DESC",
            cnx,
        )
        if df.empty:
            return pn.pane.Alert('Nenhum dado encontrado para Peso de Itens por Campanha.', alert_type='warning')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df["nome"], df["peso_total"], color='#ff7f0e', edgecolor='black')
        ax.set_title("Peso Total de Itens por Campanha", fontsize=14, fontweight='bold')
        ax.set_ylabel("Peso (kg)", fontsize=12)
        ax.set_xlabel("Campanha", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')
    except Exception as e:
        return pn.pane.Alert(f'Erro ao gerar gráfico: {str(e)}', alert_type='danger')


def grafico_conservacao_itens(cnx):
    """Estado de conservação dos itens"""
    try:
        df = _safe_df_query(
            "SELECT estado_conservacao, COUNT(id_item) as total FROM item_doacao GROUP BY estado_conservacao",
            cnx,
        )
        if df.empty:
            return pn.pane.Alert('Nenhum dado encontrado para Estado de Conservação.', alert_type='warning')
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = ['#2ca02c', '#ff7f0e', '#1f77b4']
        ax.pie(df["total"], labels=df["estado_conservacao"], autopct='%d', colors=colors[: len(df)], startangle=90)
        ax.set_title("Estado de Conservação dos Itens", fontsize=14, fontweight='bold')
        return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')
    except Exception as e:
        return pn.pane.Alert(f'Erro ao gerar gráfico: {str(e)}', alert_type='danger')


def grafico_doacoes_por_doador(cnx):
    """Top doadores"""
    try:
        df = _safe_df_query(
            "SELECT u.nome, COUNT(d.id_doacao) as total FROM doacao d JOIN doador doa ON d.cpf_cnpj_d = doa.cpf_cnpj_d JOIN usuario u ON doa.cpf_cnpj_d = u.cpf_cnpj GROUP BY u.nome ORDER BY total DESC LIMIT 10",
            cnx,
        )
        if df.empty:
            return pn.pane.Alert('Nenhum dado encontrado para Top Doadores.', alert_type='warning')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(df["nome"], df["total"], color='#1f77b4', edgecolor='black')
        ax.set_title("Top 10 Doadores", fontsize=14, fontweight='bold')
        ax.set_xlabel("Total de Doações", fontsize=12)
        for i, v in enumerate(df["total"]):
            ax.text(v + 0.1, i, str(int(v)), va='center')
        plt.tight_layout()
        return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')
    except Exception as e:
        return pn.pane.Alert(f'Erro ao gerar gráfico: {str(e)}', alert_type='danger')


def grafico_distribuicao_por_tipo(cnx):
    """Gráfico de pizza mostrando distribuição de tipos de usuários"""
    try:
        df = _safe_df_query(
            """SELECT 
                CASE 
                    WHEN d.cpf_cnpj_d IS NOT NULL THEN 'Doador'
                    WHEN b.cpf_cnpj_b IS NOT NULL THEN 'Beneficiário'
                    WHEN i.cpf_cnpj_i IS NOT NULL THEN 'Instituição'
                END AS tipo,
                COUNT(*) AS quantidade
            FROM usuario u
            LEFT JOIN doador d ON u.cpf_cnpj = d.cpf_cnpj_d
            LEFT JOIN beneficiario b ON u.cpf_cnpj = b.cpf_cnpj_b
            LEFT JOIN instituicao i ON u.cpf_cnpj = i.cpf_cnpj_i
            GROUP BY tipo""",
            cnx,
        )
        if df.empty:
            return pn.pane.Alert('Nenhum dado encontrado para Distribuição por Tipo.', alert_type='warning')
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        ax.pie(df["quantidade"], labels=df["tipo"], autopct='%d', colors=colors[: len(df)], startangle=90)
        ax.set_title("Distribuição de Usuários por Tipo", fontsize=14, fontweight='bold')
        return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')
    except Exception as e:
        return pn.pane.Alert(f'Erro ao gerar gráfico: {str(e)}', alert_type='danger')


def grafico_instituicoes(cnx):
    """Gráfico de barras mostrando instituições cadastradas"""
    try:
        df = _safe_df_query(
            """SELECT u.nome, COUNT(c.id_campanha)::INTEGER AS campanhas
            FROM usuario u
            LEFT JOIN instituicao i ON u.cpf_cnpj = i.cpf_cnpj_i
            LEFT JOIN campanha c ON i.cpf_cnpj_i = c.cpf_cnpj_i
            WHERE i.cpf_cnpj_i IS NOT NULL
            GROUP BY u.nome
            ORDER BY campanhas DESC""",
            cnx,
        )
        if df.empty:
            return pn.pane.Alert('Nenhuma instituição cadastrada', alert_type='info')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(df["nome"], df["campanhas"], color='#17becf', edgecolor='black')
        ax.set_xlabel("Número de Campanhas", fontsize=12)
        ax.set_title("Campanhas por Instituição", fontsize=14, fontweight='bold')
        max_campanhas = df["campanhas"].max()
        ax.set_xticks(range(0, int(max_campanhas) + 2))
        for i, v in enumerate(df["campanhas"]):
            ax.text(v + 0.1, i, str(int(v)), va='center')
        plt.tight_layout()
        return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')
    except Exception as e:
        return pn.pane.Alert(f'Erro ao gerar gráfico: {str(e)}', alert_type='danger')


def grafico_total_usuarios(cnx):
    """Gráfico de barras mostrando total de usuários por tipo"""
    try:
        df = _safe_df_query(
            """SELECT 
                CASE 
                    WHEN d.cpf_cnpj_d IS NOT NULL THEN 'Doador'
                    WHEN b.cpf_cnpj_b IS NOT NULL THEN 'Beneficiário'
                    WHEN i.cpf_cnpj_i IS NOT NULL THEN 'Instituição'
                    ELSE 'Sem Tipo'
                END AS tipo,
                COUNT(*) AS total
            FROM usuario u
            LEFT JOIN doador d ON u.cpf_cnpj = d.cpf_cnpj_d
            LEFT JOIN beneficiario b ON u.cpf_cnpj = b.cpf_cnpj_b
            LEFT JOIN instituicao i ON u.cpf_cnpj = i.cpf_cnpj_i
            GROUP BY tipo
            ORDER BY total DESC""",
            cnx,
        )
        if df.empty:
            return pn.pane.Alert('Nenhum usuário encontrado.', alert_type='warning')
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#95E1D3']
        ax.bar(df["tipo"], df["total"], color=colors[:len(df)], edgecolor='black')
        ax.set_ylabel("Quantidade", fontsize=12)
        ax.set_xlabel("Tipo de Usuário", fontsize=12)
        ax.set_title("Total de Usuários por Tipo", fontsize=14, fontweight='bold')
        # Garantir ticks inteiros no eixo Y
        max_total = df["total"].max()
        ax.set_yticks(range(0, int(max_total) + 2))
        for i, v in enumerate(df["total"]):
            ax.text(i, v + 0.2, str(int(v)), ha='center', va='bottom', fontsize=12, fontweight='bold')
        plt.tight_layout()
        return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')
    except Exception as e:
        return pn.pane.Alert(f'Erro ao gerar gráfico: {str(e)}', alert_type='danger')


def create_graficos_view(cnx, create_btn_voltar=None):
    """Cria a view de gráficos organizada em abas por view do sistema.

    Parâmetros:
    - cnx: conexão com o banco de dados (aceita qualquer objeto compatível com pandas.read_sql_query)
    - create_btn_voltar: callable que retorna um botão "voltar" (opcional)
    """
    titulo = pn.pane.Markdown("### 📊 Análise de Dados do Sistema de Doações")

    # Abas por view
    aba_usuarios = pn.Column(
        pn.pane.Markdown("**Usuários**"),
        grafico_total_usuarios(cnx),
        grafico_distribuicao_por_tipo(cnx),
        grafico_doacoes_por_doador(cnx),
        sizing_mode='stretch_width',
    )

    aba_campanhas = pn.Column(
        pn.pane.Markdown("**Campanhas**"),
        grafico_doacoes_por_campanha(cnx),
        grafico_campanhas_status(cnx),
        grafico_peso_itens(cnx),
        grafico_instituicoes(cnx),
        sizing_mode='stretch_width',
    )

    aba_ordem = pn.Column(
        pn.pane.Markdown("**Ordens de Doação**"),
        grafico_status_ordens(cnx),
        sizing_mode='stretch_width',
    )

    aba_doacoes = pn.Column(
        pn.pane.Markdown("**Doações**"),
        grafico_doacoes_por_campanha(cnx),
        grafico_doacoes_por_doador(cnx),
        sizing_mode='stretch_width',
    )

    aba_itens = pn.Column(
        pn.pane.Markdown("**Itens de Doação**"),
        grafico_tipos_itens(cnx),
        grafico_conservacao_itens(cnx),
        sizing_mode='stretch_width',
    )

    tabs = pn.Tabs(
        ("Usuários", aba_usuarios),
        ("Campanhas", aba_campanhas),
        ("Ordens", aba_ordem),
        ("Doações", aba_doacoes),
        ("Itens", aba_itens),
        sizing_mode='stretch_width',
    )

    components = [titulo, tabs]
    if create_btn_voltar is not None:
        try:
            components.append(create_btn_voltar())
        except Exception:
            # se create_btn_voltar não for callable, ignore
            if hasattr(create_btn_voltar, 'name'):
                components.append(create_btn_voltar)

    layout = pn.Column(*components, sizing_mode='stretch_width', margin=(20, 20, 20, 20))
    return layout


# Pequeno snippet para ajudar integração no notebook
button_snippet = '''# Exemplo de integração no notebook
from graficos import create_graficos_view
# supondo que `cnx` e `main_area` já existam no notebook
main_area.clear()
main_area.append(create_graficos_view(cnx, create_btn_voltar))
'''
