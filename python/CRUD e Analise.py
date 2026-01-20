# 🧪 Sistema de Gerenciamento de Doações

# Este notebook demonstra uma aplicação completa para gerenciar um **Sistema de Doações** com banco de dados **PostgreSQL**.
# A interface permite gerenciar Usuários, Doadores, Beneficiários, Instituições, Campanhas, Doações, Ordens de Doação e Itens.
---

## 🛠️ Setup e Configuração

### Importações e Configuração do Banco de Dados
import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2 as pg
import sqlalchemy
from sqlalchemy import create_engine
import panel as pn
import matplotlib.pyplot as plt
from datetime import datetime, date
import warnings
warnings.filterwarnings('ignore')

# Carrega variáveis de ambiente
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

# Conexões ao banco
con = pg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
cnx = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
engine = sqlalchemy.create_engine(cnx)

# Inicializa Panel
pn.extension()
pn.extension('tabulator')
pn.extension(notifications=True)

print('✅ Conexão com banco estabelecida com sucesso!')

# ---

## 🏠 Componentes Principais de Navegação

# Container principal da aplicação
main_area = pn.Column()

def create_home_view():
    home = pn.Column(
        pn.pane.Markdown("## 🏠 Sistema de Doações"),
        pn.pane.Markdown("Escolha uma opção abaixo:"),
        pn.Spacer(height=20),
        pn.Column(
            btn_usuarios,
            btn_doadores,
            btn_beneficiarios,
            btn_instituicoes,
            btn_campanhas,
            btn_doacoes,
            btn_ordens,
            btn_itens,
            btn_graficos,
            width=250,
            spacing=10
        ),
        align="center",
        sizing_mode="stretch_width",
        margin=(50,50,50,50)
    )
    return home

def go_to_home():
    main_area.clear()
    main_area.append(create_home_view())

def create_btn_voltar():
    btn_voltar = pn.widgets.Button(name='⬅ Voltar para Home', button_type='default')
    btn_voltar.on_click(lambda e: go_to_home())
    return btn_voltar

---

## 👤 CRUD USUÁRIO

### Formulário e Botões
def create_usuario_widgets():
    return {
        "cpf_cnpj": pn.widgets.TextInput(name="CPF/CNPJ", placeholder="00000000000000", sizing_mode="stretch_width"),
        "nome": pn.widgets.TextInput(name="Nome", placeholder="Digite o nome", sizing_mode="stretch_width"),
        "email": pn.widgets.TextInput(name="Email", placeholder="email@example.com", sizing_mode="stretch_width"),
        "senha": pn.widgets.PasswordInput(name="Senha", placeholder="Senha", sizing_mode="stretch_width"),
        "celular": pn.widgets.TextInput(name="Celular", placeholder="88999999999", sizing_mode="stretch_width"),
        "rua": pn.widgets.TextInput(name="Rua", placeholder="Nome da rua", sizing_mode="stretch_width"),
        "numero": pn.widgets.TextInput(name="Número", placeholder="123", sizing_mode="stretch_width"),
        "bairro": pn.widgets.TextInput(name="Bairro", placeholder="Bairro", sizing_mode="stretch_width"),
        "cidade": pn.widgets.TextInput(name="Cidade", placeholder="Cidade", sizing_mode="stretch_width"),
        "estado": pn.widgets.TextInput(name="Estado", placeholder="CE", sizing_mode="stretch_width"),
        "cep": pn.widgets.TextInput(name="CEP", placeholder="63900000", sizing_mode="stretch_width"),
    }

usuario_widgets = create_usuario_widgets()
btn_consultar_usuarios = pn.widgets.Button(name='Consultar', button_type='primary')
btn_inserir_usuarios = pn.widgets.Button(name='Inserir', button_type='success')
btn_atualizar_usuarios = pn.widgets.Button(name='Atualizar', button_type='warning')
btn_deletar_usuarios = pn.widgets.Button(name='Deletar', button_type='danger')

### Funções CRUD Usuário
def query_all_usuarios():
    df = pd.read_sql_query("SELECT * FROM usuario ORDER BY cpf_cnpj", cnx)
    return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)

def on_consultar_usuarios(w):
    try:
        cpf = w["cpf_cnpj"].value
        if cpf:
            query = f"SELECT * FROM usuario WHERE cpf_cnpj = '{cpf}'"
        else:
            query = "SELECT * FROM usuario ORDER BY cpf_cnpj"
        df = pd.read_sql_query(query, cnx)
        return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)
    except Exception as e:
        return pn.pane.Alert(f'Erro: {str(e)}', alert_type='danger')

def on_inserir_usuarios(w):
    try:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO usuario(cpf_cnpj, nome, email, senha, celular, rua, numero, bairro, cidade, estado, cep) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (w["cpf_cnpj"].value, w["nome"].value, w["email"].value, w["senha"].value, w["celular"].value,
             w["rua"].value, w["numero"].value, w["bairro"].value, w["cidade"].value, w["estado"].value, w["cep"].value)
        )
        con.commit()
        cursor.close()
        pn.state.notifications.success('Usuário inserido com sucesso!')
        return query_all_usuarios()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro ao inserir: {str(e)}', alert_type='danger')

def on_atualizar_usuarios(w):
    try:
        cursor = con.cursor()
        cursor.execute(
            "UPDATE usuario SET nome=%s, email=%s, celular=%s, rua=%s, numero=%s, bairro=%s, cidade=%s, estado=%s, cep=%s WHERE cpf_cnpj=%s",
            (w["nome"].value, w["email"].value, w["celular"].value, w["rua"].value, w["numero"].value,
             w["bairro"].value, w["cidade"].value, w["estado"].value, w["cep"].value, w["cpf_cnpj"].value)
        )
        con.commit()
        cursor.close()
        pn.state.notifications.success('Usuário atualizado com sucesso!')
        return query_all_usuarios()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro ao atualizar: {str(e)}', alert_type='danger')

def on_deletar_usuarios(w):
    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM usuario WHERE cpf_cnpj=%s", (w["cpf_cnpj"].value,))
        con.commit()
        cursor.close()
        pn.state.notifications.success('Usuário deletado com sucesso!')
        return query_all_usuarios()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro ao deletar: {str(e)}', alert_type='danger')

def table_creator_usuarios(cons, ins, atu, dele, w):
    if cons: return on_consultar_usuarios(w)
    if ins: return on_inserir_usuarios(w)
    if atu: return on_atualizar_usuarios(w)
    if dele: return on_deletar_usuarios(w)
    return query_all_usuarios()

def create_interactive_table_usuarios():
    return pn.bind(table_creator_usuarios, btn_consultar_usuarios, btn_inserir_usuarios, btn_atualizar_usuarios, btn_deletar_usuarios, usuario_widgets)

def create_usuario_view(w):
    return pn.Row(
        pn.Column(
            pn.pane.Markdown("### 👤 Gerenciar Usuários"),
            w["cpf_cnpj"], w["nome"], w["email"], w["senha"], w["celular"],
            pn.pane.Markdown("**Endereço:**"),
            w["rua"], w["numero"], w["bairro"], w["cidade"], w["estado"], w["cep"],
            pn.Row(btn_consultar_usuarios, btn_inserir_usuarios),
            pn.Row(btn_atualizar_usuarios, btn_deletar_usuarios),
            pn.Spacer(height=10),
            create_btn_voltar(),
            sizing_mode='stretch_width',
            margin=(20, 20, 20, 20)
        ),
        pn.Column(create_interactive_table_usuarios(), sizing_mode='stretch_both')
    )

def go_to_usuarios():
    main_area.clear()
    main_area.append(create_usuario_view(usuario_widgets))

btn_usuarios = pn.widgets.Button(name="👤 Usuários", button_type="primary", width=250)
btn_usuarios.on_click(lambda e: go_to_usuarios())

# ---

## 🎁 CRUD DOADOR

def get_usuarios_list():
    try:
        return pd.read_sql_query("SELECT cpf_cnpj FROM usuario ORDER BY nome", cnx)['cpf_cnpj'].tolist()
    except:
        return []

def create_doador_widgets():
    usuarios = get_usuarios_list()
    return {
        "cpf_cnpj_d": pn.widgets.Select(name="CPF/CNPJ (Usuário)", options=usuarios, sizing_mode="stretch_width"),
        "data_nascimento": pn.widgets.DatePicker(name="Data de Nascimento"),
    }

doador_widgets = create_doador_widgets()
btn_consultar_doadores = pn.widgets.Button(name='Consultar', button_type='primary')
btn_inserir_doadores = pn.widgets.Button(name='Inserir', button_type='success')
btn_atualizar_doadores = pn.widgets.Button(name='Atualizar', button_type='warning')
btn_deletar_doadores = pn.widgets.Button(name='Deletar', button_type='danger')

def query_all_doadores():
    df = pd.read_sql_query(
        "SELECT d.cpf_cnpj_d, u.nome, d.data_nascimento FROM doador d JOIN usuario u ON d.cpf_cnpj_d = u.cpf_cnpj ORDER BY u.nome", 
        cnx
    )
    return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)

def on_consultar_doadores(w):
    try:
        cpf = w["cpf_cnpj_d"].value
        if cpf:
            query = f"SELECT d.cpf_cnpj_d, u.nome, d.data_nascimento FROM doador d JOIN usuario u ON d.cpf_cnpj_d = u.cpf_cnpj WHERE d.cpf_cnpj_d = '{cpf}'"
        else:
            query = "SELECT d.cpf_cnpj_d, u.nome, d.data_nascimento FROM doador d JOIN usuario u ON d.cpf_cnpj_d = u.cpf_cnpj ORDER BY u.nome"
        df = pd.read_sql_query(query, cnx)
        return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)
    except Exception as e:
        return pn.pane.Alert(f'Erro: {str(e)}', alert_type='danger')

def on_inserir_doadores(w):
    try:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO doador(cpf_cnpj_d, data_nascimento) VALUES (%s,%s)",
            (w["cpf_cnpj_d"].value, w["data_nascimento"].value)
        )
        con.commit()
        cursor.close()
        pn.state.notifications.success('Doador inserido com sucesso!')
        return query_all_doadores()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro ao inserir: {str(e)}', alert_type='danger')

def on_atualizar_doadores(w):
    try:
        cursor = con.cursor()
        cursor.execute(
            "UPDATE doador SET data_nascimento=%s WHERE cpf_cnpj_d=%s",
            (w["data_nascimento"].value, w["cpf_cnpj_d"].value)
        )
        con.commit()
        cursor.close()
        pn.state.notifications.success('Doador atualizado com sucesso!')
        return query_all_doadores()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro ao atualizar: {str(e)}', alert_type='danger')

def on_deletar_doadores(w):
    if cons: return on_consultar_doadores(w)
    if ins: return on_inserir_doadores(w)
    if atu: return on_atualizar_doadores(w)
    if dele: return on_deletar_doadores(w)

def create_interactive_table_doadores():
    return pn.bind(table_creator_doadores, btn_consultar_doadores, btn_inserir_doadores, btn_atualizar_doadores, btn_deletar_doadores, doador_widgets)

def create_doador_view(w):
    return pn.Row(
        pn.Column(
            pn.pane.Markdown("### 🎁 Gerenciar Doadores"),
            w["cpf_cnpj_d"], w["data_nascimento"],
            pn.Row(btn_consultar_doadores, btn_inserir_doadores),
            pn.Row(btn_atualizar_doadores, btn_deletar_doadores),
            pn.Spacer(height=10),
            create_btn_voltar(),
            sizing_mode='stretch_width',
            margin=(20, 20, 20, 20)
        ),
        pn.Column(create_interactive_table_doadores(), sizing_mode='stretch_both')
    )

def go_to_doadores():
    main_area.clear()
    main_area.append(create_doador_view(doador_widgets))

btn_doadores = pn.widgets.Button(name="🎁 Doadores", button_type="primary", width=250)
btn_doadores.on_click(lambda e: go_to_doadores())

# ---

## 🤝 CRUD BENEFICIÁRIO

def create_beneficiario_widgets():
    todos_usuarios = pd.read_sql_query("SELECT cpf_cnpj FROM usuario", cnx)['cpf_cnpj'].tolist()
    
    return {
        "cpf_cnpj_b": pn.widgets.Select(name="CPF/CNPJ (Usuário)", options=todos_usuarios, sizing_mode="stretch_width"),
        "data_nascimento": pn.widgets.DatePicker(name="Data de Nascimento"),
    }

beneficiario_widgets = create_beneficiario_widgets()
btn_consultar_beneficiarios = pn.widgets.Button(name='Consultar', button_type='primary')
btn_inserir_beneficiarios = pn.widgets.Button(name='Inserir', button_type='success')
btn_atualizar_beneficiarios = pn.widgets.Button(name='Atualizar', button_type='warning')
btn_deletar_beneficiarios = pn.widgets.Button(name='Deletar', button_type='danger')

def query_all_beneficiarios():
    df = pd.read_sql_query(
        "SELECT b.cpf_cnpj_b, u.nome, b.data_nascimento FROM beneficiario b JOIN usuario u ON b.cpf_cnpj_b = u.cpf_cnpj", 
        cnx
    )
    return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)

def on_consultar_beneficiarios(w):
    try:
        cpf = w["cpf_cnpj_b"].value
        if cpf:
            query = f"SELECT b.cpf_cnpj_b, u.nome, b.data_nascimento FROM beneficiario b JOIN usuario u ON b.cpf_cnpj_b = u.cpf_cnpj WHERE b.cpf_cnpj_b = '{cpf}'"
        else:
            query = "SELECT b.cpf_cnpj_b, u.nome, b.data_nascimento FROM beneficiario b JOIN usuario u ON b.cpf_cnpj_b = u.cpf_cnpj"
        df = pd.read_sql_query(query, cnx)
        return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)
    except Exception as e:
        return pn.pane.Alert(f'Erro: {str(e)}', alert_type='danger')

def on_inserir_beneficiarios(w):
    try:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO beneficiario(cpf_cnpj_b, data_nascimento) VALUES (%s,%s)",
            (w["cpf_cnpj_b"].value, w["data_nascimento"].value)
        )
        con.commit()
        cursor.close()
        return query_all_beneficiarios()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro ao inserir: {str(e)}', alert_type='danger')

def on_atualizar_beneficiarios(w):
    try:
        cursor = con.cursor()
        cursor.execute(
            "UPDATE beneficiario SET data_nascimento=%s WHERE cpf_cnpj_b=%s",
            (w["data_nascimento"].value, w["cpf_cnpj_b"].value)
        )
        con.commit()
        cursor.close()
        return query_all_beneficiarios()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro ao atualizar: {str(e)}', alert_type='danger')

def on_deletar_beneficiarios(w):
    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM beneficiario WHERE cpf_cnpj_b=%s", (w["cpf_cnpj_b"].value,))
        con.commit()
        cursor.close()
        return query_all_beneficiarios()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro ao deletar: {str(e)}', alert_type='danger')

def table_creator_beneficiarios(cons, ins, atu, dele, w):
    if cons: return on_consultar_beneficiarios(w)
    if ins: return on_inserir_beneficiarios(w)
    if atu: return on_atualizar_beneficiarios(w)
    if dele: return on_deletar_beneficiarios(w)

def create_interactive_table_beneficiarios():
    return pn.bind(table_creator_beneficiarios, btn_consultar_beneficiarios, btn_inserir_beneficiarios, btn_atualizar_beneficiarios, btn_deletar_beneficiarios, beneficiario_widgets)

def create_beneficiario_view(w):
    return pn.Row(
        pn.Column(
            pn.pane.Markdown("### 🤝 Gerenciar Beneficiários"),
            w["cpf_cnpj_b"], w["data_nascimento"],
            pn.Row(btn_consultar_beneficiarios, btn_inserir_beneficiarios),
            pn.Row(btn_atualizar_beneficiarios, btn_deletar_beneficiarios),
            pn.Spacer(height=10),
            create_btn_voltar(),
            sizing_mode='stretch_width',
            margin=(20, 20, 20, 20)
        ),
        pn.Column(create_interactive_table_beneficiarios(), sizing_mode='stretch_both')
    )

def go_to_beneficiarios():
    main_area.clear()
    main_area.append(create_beneficiario_view(beneficiario_widgets))

btn_beneficiarios = pn.widgets.Button(name="🤝 Beneficiários", button_type="primary", width=250)
btn_beneficiarios.on_click(lambda e: go_to_beneficiarios())

# ---

## 🏢 CRUD INSTITUIÇÃO

def create_instituicao_widgets():
    todos_usuarios = pd.read_sql_query("SELECT cpf_cnpj FROM usuario", cnx)['cpf_cnpj'].tolist()
    
    return {
        "cpf_cnpj_i": pn.widgets.Select(name="CPF/CNPJ (Usuário)", options=todos_usuarios, sizing_mode="stretch_width"),
    }

instituicao_widgets = create_instituicao_widgets()
btn_consultar_instituicoes = pn.widgets.Button(name='Consultar', button_type='primary')
btn_inserir_instituicoes = pn.widgets.Button(name='Inserir', button_type='success')
btn_deletar_instituicoes = pn.widgets.Button(name='Deletar', button_type='danger')

def query_all_instituicoes():
    df = pd.read_sql_query(
        "SELECT i.cpf_cnpj_i, u.nome, u.email, u.celular FROM instituicao i JOIN usuario u ON i.cpf_cnpj_i = u.cpf_cnpj", 
        cnx
    )
    return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)

def on_consultar_instituicoes(w):
    try:
        cpf = w["cpf_cnpj_i"].value
        if cpf:
            query = f"SELECT i.cpf_cnpj_i, u.nome, u.email, u.celular FROM instituicao i JOIN usuario u ON i.cpf_cnpj_i = u.cpf_cnpj WHERE i.cpf_cnpj_i = '{cpf}'"
        else:
            query = "SELECT i.cpf_cnpj_i, u.nome, u.email, u.celular FROM instituicao i JOIN usuario u ON i.cpf_cnpj_i = u.cpf_cnpj"
        df = pd.read_sql_query(query, cnx)
        return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)
    except Exception as e:
        return pn.pane.Alert(f'Erro: {str(e)}', alert_type='danger')

def on_inserir_instituicoes(w):
    try:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO instituicao(cpf_cnpj_i) VALUES (%s)",
            (w["cpf_cnpj_i"].value,)
        )
        con.commit()
        cursor.close()
        return query_all_instituicoes()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro ao inserir: {str(e)}', alert_type='danger')

def on_deletar_instituicoes(w):
    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM instituicao WHERE cpf_cnpj_i=%s", (w["cpf_cnpj_i"].value,))
        con.commit()
        cursor.close()
        return query_all_instituicoes()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro ao deletar: {str(e)}', alert_type='danger')

def table_creator_instituicoes(cons, ins, dele, w):
    if cons: return on_consultar_instituicoes(w)
    if ins: return on_inserir_instituicoes(w)
    if dele: return on_deletar_instituicoes(w)

def create_interactive_table_instituicoes():
    return pn.bind(table_creator_instituicoes, btn_consultar_instituicoes, btn_inserir_instituicoes, btn_deletar_instituicoes, instituicao_widgets)

def create_instituicao_view(w):
    return pn.Row(
        pn.Column(
            pn.pane.Markdown("### 🏢 Gerenciar Instituições"),
            w["cpf_cnpj_i"],
            pn.Row(btn_consultar_instituicoes, btn_inserir_instituicoes),
            btn_deletar_instituicoes,
            pn.Spacer(height=10),
            create_btn_voltar(),
            sizing_mode='stretch_width',
            margin=(20, 20, 20, 20)
        ),
        pn.Column(create_interactive_table_instituicoes(), sizing_mode='stretch_both')
    )

def go_to_instituicoes():
    main_area.clear()
    main_area.append(create_instituicao_view(instituicao_widgets))

btn_instituicoes = pn.widgets.Button(name="🏢 Instituições", button_type="primary", width=250)
btn_instituicoes.on_click(lambda e: go_to_instituicoes())

# ---

## 📢 CRUD CAMPANHA

def create_campanha_widgets():
    instituicoes = pd.read_sql_query("SELECT cpf_cnpj_i FROM instituicao", cnx)['cpf_cnpj_i'].tolist()
    
    return {
        "nome": pn.widgets.TextInput(name="Nome da Campanha", placeholder="Digite o nome", sizing_mode="stretch_width"),
        "data_inicio": pn.widgets.DatePicker(name="Data de Início"),
        "data_fim": pn.widgets.DatePicker(name="Data de Término"),
        "status": pn.widgets.Select(name="Status", options=['Planejada', 'Ativa', 'Concluída'], sizing_mode="stretch_width"),
        "cpf_cnpj_i": pn.widgets.Select(name="Instituição", options=instituicoes, sizing_mode="stretch_width"),
    }

campanha_widgets = create_campanha_widgets()
btn_consultar_campanhas = pn.widgets.Button(name='Consultar', button_type='primary')
btn_inserir_campanhas = pn.widgets.Button(name='Inserir', button_type='success')
btn_atualizar_campanhas = pn.widgets.Button(name='Atualizar', button_type='warning')
btn_deletar_campanhas = pn.widgets.Button(name='Deletar', button_type='danger')

def query_all_campanhas():
    df = pd.read_sql_query(
        "SELECT c.id_campanha, c.nome, c.data_inicio, c.data_fim, c.status, u.nome as instituicao FROM campanha c JOIN instituicao i ON c.cpf_cnpj_i = i.cpf_cnpj_i JOIN usuario u ON i.cpf_cnpj_i = u.cpf_cnpj", 
        cnx
    )
    return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)

def on_consultar_campanhas(w):
    try:
        query = "SELECT c.id_campanha, c.nome, c.data_inicio, c.data_fim, c.status, u.nome as instituicao FROM campanha c JOIN instituicao i ON c.cpf_cnpj_i = i.cpf_cnpj_i JOIN usuario u ON i.cpf_cnpj_i = u.cpf_cnpj"
        df = pd.read_sql_query(query, cnx)
        return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)
    except Exception as e:
        return pn.pane.Alert(f'Erro: {str(e)}', alert_type='danger')

def on_inserir_campanhas(w):
    try:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO campanha(nome, data_inicio, data_fim, status, cpf_cnpj_i) VALUES (%s,%s,%s,%s,%s)",
            (w["nome"].value, w["data_inicio"].value, w["data_fim"].value, w["status"].value, w["cpf_cnpj_i"].value)
        )
        con.commit()
        cursor.close()
        return query_all_campanhas()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro ao inserir: {str(e)}', alert_type='danger')

def on_atualizar_campanhas(w):
    try:
        cursor = con.cursor()
        # Aqui você precisaria de um campo ID para identificar qual atualizar
        # Por simplicidade, não implementado neste exemplo
        cursor.close()
        return pn.pane.Alert('Função não implementada', alert_type='info')
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro: {str(e)}', alert_type='danger')

def on_deletar_campanhas(w):
    try:
        cursor = con.cursor()
        # Seria necessário um campo ID para deletar
        cursor.close()
        return query_all_campanhas()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro: {str(e)}', alert_type='danger')

def table_creator_campanhas(cons, ins, atu, dele, w):
    if cons: return on_consultar_campanhas(w)
    if ins: return on_inserir_campanhas(w)
    if atu: return on_atualizar_campanhas(w)
    if dele: return on_deletar_campanhas(w)

def create_interactive_table_campanhas():
    return pn.bind(table_creator_campanhas, btn_consultar_campanhas, btn_inserir_campanhas, btn_atualizar_campanhas, btn_deletar_campanhas, campanha_widgets)

def create_campanha_view(w):
    return pn.Row(
        pn.Column(
            pn.pane.Markdown("### 📢 Gerenciar Campanhas"),
            w["nome"], w["data_inicio"], w["data_fim"], w["status"], w["cpf_cnpj_i"],
            pn.Row(btn_consultar_campanhas, btn_inserir_campanhas),
            pn.Row(btn_atualizar_campanhas, btn_deletar_campanhas),
            pn.Spacer(height=10),
            create_btn_voltar(),
            sizing_mode='stretch_width',
            margin=(20, 20, 20, 20)
        ),
        pn.Column(create_interactive_table_campanhas(), sizing_mode='stretch_both')
    )

def go_to_campanhas():
    main_area.clear()
    main_area.append(create_campanha_view(campanha_widgets))

btn_campanhas = pn.widgets.Button(name="📢 Campanhas", button_type="primary", width=250)
btn_campanhas.on_click(lambda e: go_to_campanhas())

# ---

## 💝 CRUD DOAÇÃO

def create_doacao_widgets():
    doadores = pd.read_sql_query("SELECT cpf_cnpj_d FROM doador", cnx)['cpf_cnpj_d'].tolist()
    campanhas = pd.read_sql_query("SELECT id_campanha, nome FROM campanha", cnx)
    
    return {
        "data_doacao": pn.widgets.DatetimePicker(name="Data da Doação"),
        "cpf_cnpj_d": pn.widgets.Select(name="Doador", options=doadores, sizing_mode="stretch_width"),
        "id_campanha": pn.widgets.Select(name="Campanha", options=campanhas['id_campanha'].tolist(), sizing_mode="stretch_width"),
    }

doacao_widgets = create_doacao_widgets()
btn_consultar_doacoes = pn.widgets.Button(name='Consultar', button_type='primary')
btn_inserir_doacoes = pn.widgets.Button(name='Inserir', button_type='success')
btn_deletar_doacoes = pn.widgets.Button(name='Deletar', button_type='danger')

def query_all_doacoes():
    df = pd.read_sql_query(
        "SELECT d.id_doacao, u.nome as doador, d.data_doacao, c.nome as campanha FROM doacao d JOIN doador do ON d.cpf_cnpj_d = do.cpf_cnpj_d JOIN usuario u ON do.cpf_cnpj_d = u.cpf_cnpj JOIN campanha c ON d.id_campanha = c.id_campanha", 
        cnx
    )
    return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)

def on_consultar_doacoes(w):
    try:
        query = "SELECT d.id_doacao, u.nome as doador, d.data_doacao, c.nome as campanha FROM doacao d JOIN doador do ON d.cpf_cnpj_d = do.cpf_cnpj_d JOIN usuario u ON do.cpf_cnpj_d = u.cpf_cnpj JOIN campanha c ON d.id_campanha = c.id_campanha"
        df = pd.read_sql_query(query, cnx)
        return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)
    except Exception as e:
        return pn.pane.Alert(f'Erro: {str(e)}', alert_type='danger')

def on_inserir_doacoes(w):
    try:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO doacao(data_doacao, cpf_cnpj_d, id_campanha) VALUES (%s,%s,%s)",
            (w["data_doacao"].value, w["cpf_cnpj_d"].value, w["id_campanha"].value)
        )
        con.commit()
        cursor.close()
        return query_all_doacoes()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro ao inserir: {str(e)}', alert_type='danger')

def on_deletar_doacoes(w):
    try:
        cursor = con.cursor()
        # Seria necessário um field ID para deletar
        cursor.close()
        return query_all_doacoes()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro: {str(e)}', alert_type='danger')

def table_creator_doacoes(cons, ins, dele, w):
    if cons: return on_consultar_doacoes(w)
    if ins: return on_inserir_doacoes(w)
    if dele: return on_deletar_doacoes(w)

def create_interactive_table_doacoes():
    return pn.bind(table_creator_doacoes, btn_consultar_doacoes, btn_inserir_doacoes, btn_deletar_doacoes, doacao_widgets)

def create_doacao_view(w):
    return pn.Row(
        pn.Column(
            pn.pane.Markdown("### 💝 Gerenciar Doações"),
            w["data_doacao"], w["cpf_cnpj_d"], w["id_campanha"],
            pn.Row(btn_consultar_doacoes, btn_inserir_doacoes),
            btn_deletar_doacoes,
            pn.Spacer(height=10),
            create_btn_voltar(),
            sizing_mode='stretch_width',
            margin=(20, 20, 20, 20)
        ),
        pn.Column(create_interactive_table_doacoes(), sizing_mode='stretch_both')
    )

def go_to_doacoes():
    main_area.clear()
    main_area.append(create_doacao_view(doacao_widgets))

btn_doacoes = pn.widgets.Button(name="💝 Doações", button_type="primary", width=250)
btn_doacoes.on_click(lambda e: go_to_doacoes())

# ---

## 📦 CRUD ORDEM DE DOAÇÃO

def create_ordem_widgets():
    beneficiarios = pd.read_sql_query("SELECT cpf_cnpj_b FROM beneficiario", cnx)['cpf_cnpj_b'].tolist()
    instituicoes = pd.read_sql_query("SELECT cpf_cnpj_i FROM instituicao", cnx)['cpf_cnpj_i'].tolist()
    
    return {
        "data_hora_criacao": pn.widgets.DatetimePicker(name="Data de Criação"),
        "data_hora_retirada": pn.widgets.DatetimePicker(name="Data de Retirada"),
        "status": pn.widgets.Select(name="Status", options=['Pendente', 'Processando', 'Entregue', 'Cancelada'], sizing_mode="stretch_width"),
        "rua": pn.widgets.TextInput(name="Rua", placeholder="Rua", sizing_mode="stretch_width"),
        "numero": pn.widgets.TextInput(name="Número", placeholder="123", sizing_mode="stretch_width"),
        "bairro": pn.widgets.TextInput(name="Bairro", placeholder="Bairro", sizing_mode="stretch_width"),
        "cidade": pn.widgets.TextInput(name="Cidade", placeholder="Cidade", sizing_mode="stretch_width"),
        "estado": pn.widgets.TextInput(name="Estado", placeholder="CE", sizing_mode="stretch_width"),
        "cep": pn.widgets.TextInput(name="CEP", placeholder="63900000", sizing_mode="stretch_width"),
        "cpf_cnpj_b": pn.widgets.Select(name="Beneficiário", options=beneficiarios, sizing_mode="stretch_width"),
        "cpf_cnpj_i": pn.widgets.Select(name="Instituição", options=instituicoes, sizing_mode="stretch_width"),
    }

ordem_widgets = create_ordem_widgets()
btn_consultar_ordens = pn.widgets.Button(name='Consultar', button_type='primary')
btn_inserir_ordens = pn.widgets.Button(name='Inserir', button_type='success')
btn_atualizar_ordens = pn.widgets.Button(name='Atualizar', button_type='warning')
btn_deletar_ordens = pn.widgets.Button(name='Deletar', button_type='danger')

def query_all_ordens():
    df = pd.read_sql_query(
        "SELECT od.id_ordem_doacao, ub.nome as beneficiario, ui.nome as instituicao, od.status, od.data_hora_criacao FROM ordem_de_doacao od JOIN beneficiario b ON od.cpf_cnpj_b = b.cpf_cnpj_b JOIN usuario ub ON b.cpf_cnpj_b = ub.cpf_cnpj JOIN instituicao i ON od.cpf_cnpj_i = i.cpf_cnpj_i JOIN usuario ui ON i.cpf_cnpj_i = ui.cpf_cnpj", 
        cnx
    )
    return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)

def on_consultar_ordens(w):
    try:
        query = "SELECT od.id_ordem_doacao, ub.nome as beneficiario, ui.nome as instituicao, od.status, od.data_hora_criacao FROM ordem_de_doacao od JOIN beneficiario b ON od.cpf_cnpj_b = b.cpf_cnpj_b JOIN usuario ub ON b.cpf_cnpj_b = ub.cpf_cnpj JOIN instituicao i ON od.cpf_cnpj_i = i.cpf_cnpj_i JOIN usuario ui ON i.cpf_cnpj_i = ui.cpf_cnpj"
        df = pd.read_sql_query(query, cnx)
        return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)
    except Exception as e:
        return pn.pane.Alert(f'Erro: {str(e)}', alert_type='danger')

def on_inserir_ordens(w):
    try:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO ordem_de_doacao(data_hora_criacao, data_hora_retirada, status, rua, numero, bairro, cidade, estado, cep, cpf_cnpj_b, cpf_cnpj_i) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (w["data_hora_criacao"].value, w["data_hora_retirada"].value, w["status"].value, w["rua"].value, w["numero"].value,
             w["bairro"].value, w["cidade"].value, w["estado"].value, w["cep"].value, w["cpf_cnpj_b"].value, w["cpf_cnpj_i"].value)
        )
        con.commit()
        cursor.close()
        return query_all_ordens()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro ao inserir: {str(e)}', alert_type='danger')

def on_atualizar_ordens(w):
    try:
        cursor = con.cursor()
        # Seria necessário ID
        cursor.close()
        return pn.pane.Alert('Função não implementada', alert_type='info')
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro: {str(e)}', alert_type='danger')

def on_deletar_ordens(w):
    try:
        cursor = con.cursor()
        cursor.close()
        return query_all_ordens()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro: {str(e)}', alert_type='danger')

def table_creator_ordens(cons, ins, atu, dele, w):
    if cons: return on_consultar_ordens(w)
    if ins: return on_inserir_ordens(w)
    if atu: return on_atualizar_ordens(w)
    if dele: return on_deletar_ordens(w)

def create_interactive_table_ordens():
    return pn.bind(table_creator_ordens, btn_consultar_ordens, btn_inserir_ordens, btn_atualizar_ordens, btn_deletar_ordens, ordem_widgets)

def create_ordem_view(w):
    return pn.Row(
        pn.Column(
            pn.pane.Markdown("### 📦 Gerenciar Ordens de Doação"),
            w["data_hora_criacao"], w["data_hora_retirada"], w["status"],
            pn.pane.Markdown("**Endereço para Retirada:**"),
            w["rua"], w["numero"], w["bairro"], w["cidade"], w["estado"], w["cep"],
            w["cpf_cnpj_b"], w["cpf_cnpj_i"],
            pn.Row(btn_consultar_ordens, btn_inserir_ordens),
            pn.Row(btn_atualizar_ordens, btn_deletar_ordens),
            pn.Spacer(height=10),
            create_btn_voltar(),
            sizing_mode='stretch_width',
            margin=(20, 20, 20, 20)
        ),
        pn.Column(create_interactive_table_ordens(), sizing_mode='stretch_both')
    )

def go_to_ordens():
    main_area.clear()
    main_area.append(create_ordem_view(ordem_widgets))

btn_ordens = pn.widgets.Button(name="📦 Ordens de Doação", button_type="primary", width=250)
btn_ordens.on_click(lambda e: go_to_ordens())

# ---

## 🎯 CRUD ITEM DE DOAÇÃO

def create_item_widgets():
    doacoes = pd.read_sql_query("SELECT id_doacao FROM doacao", cnx)['id_doacao'].tolist()
    ordens = pd.read_sql_query("SELECT id_ordem_doacao FROM ordem_de_doacao", cnx)['id_ordem_doacao'].tolist()
    
    return {
        "id_doacao": pn.widgets.Select(name="Doação", options=doacoes, sizing_mode="stretch_width"),
        "id_ordem_doacao": pn.widgets.Select(name="Ordem de Doação", options=ordens + [None], sizing_mode="stretch_width"),
        "nome": pn.widgets.TextInput(name="Nome do Item", placeholder="Nome", sizing_mode="stretch_width"),
        "descricao": pn.widgets.TextAreaInput(name="Descrição", placeholder="Descrição", sizing_mode="stretch_width", height=100),
        "estado_conservacao": pn.widgets.Select(name="Estado de Conservação", options=['Novo', 'Bom', 'Usado'], sizing_mode="stretch_width"),
        "peso": pn.widgets.FloatInput(name="Peso (kg)", value=0.0, start=0),
        "volume": pn.widgets.FloatInput(name="Volume (m³)", value=0.0, start=0),
        "tamanho": pn.widgets.TextInput(name="Tamanho", placeholder="P, M, G", sizing_mode="stretch_width"),
        "cor": pn.widgets.TextInput(name="Cor", placeholder="Cor", sizing_mode="stretch_width"),
    }

item_widgets = create_item_widgets()
btn_consultar_itens = pn.widgets.Button(name='Consultar', button_type='primary')
btn_inserir_itens = pn.widgets.Button(name='Inserir', button_type='success')
btn_deletar_itens = pn.widgets.Button(name='Deletar', button_type='danger')

def query_all_itens():
    df = pd.read_sql_query(
        "SELECT id.id_item, id.id_doacao, id.nome, id.estado_conservacao, id.peso, id.tamanho, id.cor FROM item_doacao id", 
        cnx
    )
    return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)

def on_consultar_itens(w):
    try:
        query = "SELECT id.id_item, id.id_doacao, id.nome, id.estado_conservacao, id.peso, id.tamanho, id.cor FROM item_doacao id"
        df = pd.read_sql_query(query, cnx)
        return pn.widgets.Tabulator(df, show_index=False, sizing_mode='stretch_width', height=400)
    except Exception as e:
        return pn.pane.Alert(f'Erro: {str(e)}', alert_type='danger')

def on_inserir_itens(w):
    try:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO item_doacao(id_doacao, id_ordem_doacao, nome, descricao, estado_conservacao, peso, volume, tamanho, cor) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (w["id_doacao"].value, w["id_ordem_doacao"].value if w["id_ordem_doacao"].value else None, w["nome"].value, w["descricao"].value, w["estado_conservacao"].value,
             w["peso"].value, w["volume"].value, w["tamanho"].value, w["cor"].value)
        )
        con.commit()
        cursor.close()
        return query_all_itens()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro ao inserir: {str(e)}', alert_type='danger')

def on_deletar_itens(w):
    try:
        cursor = con.cursor()
        cursor.close()
        return query_all_itens()
    except Exception as e:
        con.rollback()
        return pn.pane.Alert(f'Erro: {str(e)}', alert_type='danger')

def table_creator_itens(cons, ins, dele, w):
    if cons: return on_consultar_itens(w)
    if ins: return on_inserir_itens(w)
    if dele: return on_deletar_itens(w)

def create_interactive_table_itens():
    return pn.bind(table_creator_itens, btn_consultar_itens, btn_inserir_itens, btn_deletar_itens, item_widgets)

def create_item_view(w):
    return pn.Row(
        pn.Column(
            pn.pane.Markdown("### 🎯 Gerenciar Itens de Doação"),
            w["id_doacao"], w["id_ordem_doacao"], w["nome"], w["descricao"],
            w["estado_conservacao"], w["peso"], w["volume"], w["tamanho"], w["cor"],
            pn.Row(btn_consultar_itens, btn_inserir_itens),
            btn_deletar_itens,
            pn.Spacer(height=10),
            create_btn_voltar(),
            sizing_mode='stretch_width',
            margin=(20, 20, 20, 20)
        ),
        pn.Column(create_interactive_table_itens(), sizing_mode='stretch_both')
    )

def go_to_itens():
    main_area.clear()
    main_area.append(create_item_view(item_widgets))

btn_itens = pn.widgets.Button(name="🎯 Itens de Doação", button_type="primary", width=250)
btn_itens.on_click(lambda e: go_to_itens())

# ---

## 📊 TELAS DE GRÁFICOS

### Gráficos Relevantes
def grafico_doacoes_por_campanha():
    """Quantidade de doações por campanha"""
    df = pd.read_sql_query(
        "SELECT c.nome, COUNT(d.id_doacao) as total FROM doacao d JOIN campanha c ON d.id_campanha = c.id_campanha GROUP BY c.nome",
        cnx
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df["nome"], df["total"], color='#1f77b4')
    ax.set_title("Doações por Campanha")
    ax.set_ylabel("Total de Doações")
    ax.set_xlabel("Campanha")
    plt.xticks(rotation=45, ha='right')
    return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')

def grafico_status_ordens():
    """Distribuição de status das ordens de doação"""
    df = pd.read_sql_query(
        "SELECT status, COUNT(id_ordem_doacao) as total FROM ordem_de_doacao GROUP BY status",
        cnx
    )
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#2ca02c', '#ff7f0e', '#d62728', '#9467bd']
    ax.pie(df["total"], labels=df["status"], autopct='%1.1f%%', colors=colors)
    ax.set_title("Status das Ordens de Doação")
    return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')

def grafico_tipos_itens():
    """Itens mais doados"""
    df = pd.read_sql_query(
        "SELECT nome, COUNT(id_item) as total FROM item_doacao GROUP BY nome ORDER BY total DESC LIMIT 10",
        cnx
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df["nome"], df["total"], color='#17becf')
    ax.set_title("Top 10 Itens Mais Doados")
    ax.set_xlabel("Quantidade")
    plt.tight_layout()
    return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')

def grafico_campanhas_status():
    """Status das campanhas"""
    df = pd.read_sql_query(
        "SELECT status, COUNT(id_campanha) as total FROM campanha GROUP BY status",
        cnx
    )
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#2ca02c', '#ff7f0e', '#d62728']
    ax.pie(df["total"], labels=df["status"], autopct='%1.1f%%', colors=colors)
    ax.set_title("Status das Campanhas")
    return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')

def grafico_peso_itens():
    """Peso total dos itens por campanha"""
    df = pd.read_sql_query(
        "SELECT c.nome, SUM(id.peso) as peso_total FROM item_doacao id JOIN doacao d ON id.id_doacao = d.id_doacao JOIN campanha c ON d.id_campanha = c.id_campanha GROUP BY c.nome",
        cnx
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df["nome"], df["peso_total"], color='#ff7f0e')
    ax.set_title("Peso Total de Itens por Campanha")
    ax.set_ylabel("Peso (kg)")
    ax.set_xlabel("Campanha")
    plt.xticks(rotation=45, ha='right')
    return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')

def grafico_conservacao_itens():
    """Estado de conservação dos itens"""
    df = pd.read_sql_query(
        "SELECT estado_conservacao, COUNT(id_item) as total FROM item_doacao GROUP BY estado_conservacao",
        cnx
    )
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#2ca02c', '#ff7f0e', '#1f77b4']
    ax.pie(df["total"], labels=df["estado_conservacao"], autopct='%1.1f%%', colors=colors)
    ax.set_title("Distribuição de Estado de Conservação dos Itens")
    return pn.pane.Matplotlib(fig, tight=True, sizing_mode='stretch_width')

def create_graficos_view():
    graficos_layout = pn.Column(
        pn.pane.Markdown("### 📊 Análise de Dados"),
        pn.Tabs(
            ("Doações por Campanha", grafico_doacoes_por_campanha()),
            ("Status das Ordens", grafico_status_ordens()),
            ("Items Mais Doados", grafico_tipos_itens()),
            ("Status das Campanhas", grafico_campanhas_status()),
            ("Peso por Campanha", grafico_peso_itens()),
            ("Conservação dos Items", grafico_conservacao_itens()),
        ),
        create_btn_voltar(),
        sizing_mode='stretch_width',
        margin=(20,20,20,20)
    )
    return graficos_layout

def go_to_graficos():
    main_area.clear()
    main_area.append(create_graficos_view())

btn_graficos = pn.widgets.Button(name="📊 Gráficos e Análises", button_type="success", width=250)
btn_graficos.on_click(lambda e: go_to_graficos())

# ---

## 🚀 Inicialização da Aplicação

# Inicializa com a tela Home
go_to_home()

# App principal
pn.Column(
    pn.pane.Markdown("# 🏥 Sistema de Gerenciamento de Doações"),
    main_area
).servable()