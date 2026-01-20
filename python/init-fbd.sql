
-- Tabela principal de usuários 
CREATE TABLE usuario(cpf_cnpj VARCHAR(14) PRIMARY KEY NOT NULL, nome VARCHAR(100) NOT NULL, email VARCHAR(100) UNIQUE, senha VARCHAR(100), celular CHAR(14) UNIQUE, rua VARCHAR(100), numero VARCHAR(10), bairro VARCHAR(50), cidade VARCHAR(50), estado VARCHAR(50), cep CHAR(8));
-- Tipos específicos de usuário
CREATE TABLE doador(cpf_cnpj_d VARCHAR(14) PRIMARY KEY NOT NULL REFERENCES usuario(cpf_cnpj), data_nascimento DATE); 
CREATE TABLE beneficiario(cpf_cnpj_b VARCHAR(14) PRIMARY KEY NOT NULL REFERENCES usuario(cpf_cnpj), data_nascimento DATE); 
CREATE TABLE instituicao(cpf_cnpj_i VARCHAR(14) PRIMARY KEY NOT NULL REFERENCES usuario(cpf_cnpj));
-- Tabela de campanhas 
CREATE TABLE campanha(id_campanha SERIAL PRIMARY KEY NOT NULL, nome VARCHAR(100) NOT NULL, data_inicio DATE, data_fim DATE, status VARCHAR(30), cpf_cnpj_i VARCHAR(14) NOT NULL REFERENCES instituicao(cpf_cnpj_i));
-- Doações realizadas
CREATE TABLE doacao(id_doacao SERIAL PRIMARY KEY NOT NULL, data_doacao TIMESTAMP, cpf_cnpj_d VARCHAR(14) REFERENCES doador(cpf_cnpj_d), id_campanha INT NOT NULL REFERENCES campanha(id_campanha));
-- Registro das ordem_de_doacaos 
CREATE TABLE ordem_de_doacao(id_ordem_doacao SERIAL PRIMARY KEY NOT NULL, data_hora_criacao TIMESTAMP, data_hora_retirada TIMESTAMP, status VARCHAR(30), rua VARCHAR(100), numero VARCHAR(10), bairro VARCHAR(50), cidade VARCHAR(50), estado VARCHAR(30), cep VARCHAR(8), cpf_cnpj_b VARCHAR(14) REFERENCES beneficiario(cpf_cnpj_b), cpf_cnpj_i VARCHAR(14) NOT NULL REFERENCES instituicao(cpf_cnpj_i));
-- Itens de cada doação 
CREATE TABLE item_doacao(id_item SERIAL NOT NULL, id_doacao INT NOT NULL REFERENCES doacao(id_doacao), id_ordem_doacao INT REFERENCES ordem_de_doacao(id_ordem_doacao), nome VARCHAR(100), descricao TEXT, estado_conservacao VARCHAR(50), peso NUMERIC(10,2), volume NUMERIC(10,2), tamanho VARCHAR(50), cor VARCHAR(30), PRIMARY KEY(id_item, id_doacao));;

INSERT INTO usuario (cpf_cnpj, nome, celular, email, estado, cidade, bairro, rua, numero, cep, senha)
VALUES ('11122233344', 'Maria Silva Santos', '88991234567', 'maria.silva@email.com', 'CE', 'Quixadá', 'Centro', 'Rua A', '123', '63900000', 'senha123'),
 ('22233344455', 'João Pereira Lima', '88992345678', 'joao.pereira@email.com', 'CE', 'Quixadá', 'Alto São Francisco', 'Rua B', '456', '63900000', 'senha123'),
 ('33344455566', 'Ana Costa Oliveira', '88993456789', 'ana.costa@email.com', 'CE', 'Quixadá', 'Campo Velho', 'Rua C', '789', '63900000', 'senha123'),
 ('44455566677', 'Pedro Alves Souza', '88994567890', 'pedro.alves@email.com', 'CE', 'Quixadá', 'Planalto', 'Rua D', '321', '63900000', 'senha123'),
 ('55566677788', 'Carla Mendes Lima', '88995678901', 'carla.mendes@email.com', 'CE', 'Quixadá', 'São João', 'Rua E', '654', '63900000', 'senha123'),
 ('66677788899', 'Roberto Santos Costa', '88996789012', 'roberto.santos@email.com', 'CE', 'Quixadá', 'Centenário', 'Rua F', '987', '63900000', 'senha123'),
 ('77788899900', 'Juliana Lima Alves', '88997890123', 'juliana.lima@email.com', 'CE', 'Quixadá', 'Cedro', 'Rua G', '147', '63900000', 'senha123'),
 ('88899900011', 'Ricardo Oliveira Silva', '88998901234', 'ricardo.oliveira@email.com', 'CE', 'Quixadá', 'Jardim dos Monólitos', 'Rua H', '258', '63900000', 'senha123'),
 ('99900011122', 'Amanda Souza Pereira', '88999012345', 'amanda.souza@email.com', 'CE', 'Quixadá', 'Vila Feliz', 'Rua I', '369', '63900000', 'senha123'),
 ('00011122233', 'Bruno Costa Mendes', '88990123456', 'bruno.costa@email.com', 'CE', 'Quixadá', 'Novo Horizonte', 'Rua J', '741', '63900000', 'senha123'),
 ('11122233345', 'José Santos Costa', '88991234568', 'jose.santos@email.com', 'CE', 'Quixadá', 'Centro', 'Rua K', '111', '63900000', 'senha123'),
 ('22233344456', 'Fernanda Lima Alves', '88992345679', 'fernanda.lima@email.com', 'CE', 'Quixadá', 'Alto São Francisco', 'Rua L', '222', '63900000', 'senha123'),
 ('33344455567', 'Carlos Oliveira Silva', '88993456780', 'carlos.oliveira@email.com', 'CE', 'Quixadá', 'Campo Velho', 'Rua M', '333', '63900000', 'senha123'),
 ('44455566678', 'Patrícia Souza Pereira', '88994567891', 'patricia.souza@email.com', 'CE', 'Quixadá', 'Planalto', 'Rua N', '444', '63900000', 'senha123'),
 ('55566677789', 'Lucas Costa Mendes', '88995678902', 'lucas.costa@email.com', 'CE', 'Quixadá', 'São João', 'Rua O', '555', '63900000', 'senha123'),
 ('66677788890', 'Mariana Santos Costa', '88996789013', 'mariana.santos@email.com', 'CE', 'Quixadá', 'Centenário', 'Rua P', '666', '63900000', 'senha123'),
 ('77788899901', 'Paulo Lima Alves', '88997890124', 'paulo.lima@email.com', 'CE', 'Quixadá', 'Cedro', 'Rua Q', '777', '63900000', 'senha123'),
 ('88899900012', 'Camila Oliveira Silva', '88998901235', 'camila.oliveira@email.com', 'CE', 'Quixadá', 'Jardim dos Monólitos', 'Rua R', '888', '63900000', 'senha123'),
 ('99900011123', 'Rafael Souza Pereira', '88999012346', 'rafael.souza@email.com', 'CE', 'Quixadá', 'Vila Feliz', 'Rua S', '999', '63900000', 'senha123'),
 ('00011122234', 'Tatiane Costa Mendes', '88990123457', 'tatiane.costa@email.com', 'CE', 'Quixadá', 'Novo Horizonte', 'Rua T', '101', '63900000', 'senha123'),
 ('11222333000144', 'Lar da Criança Feliz', '88991122334', 'lar.crianca@email.com', 'CE', 'Quixadá', 'Centro', 'Av. Principal', '100', '63900000', 'senha123'),
 ('22333444000155', 'Asilo São Vicente', '88992233445', 'asilo.sv@email.com', 'CE', 'Quixadá', 'Alto São Francisco', 'Rua das Flores', '200', '63900000', 'senha123'),
 ('33444555000166', 'Casa de Apoio Esperança', '88993344556', 'casa.esperanca@email.com', 'CE', 'Quixadá', 'Campo Velho', 'Travessa da Paz', '300', '63900000', 'senha123'),
 ('44555666000177', 'Centro Comunitário União', '88994455667', 'centro.uniao@email.com', 'CE', 'Quixadá', 'Planalto', 'Rua da União', '400', '63900000', 'senha123'),
 ('55666777000188', 'Associação Amigos do Bem', '88995566778', 'amigos.bem@email.com', 'CE', 'Quixadá', 'São João', 'Av. Solidária', '500', '63900000', 'senha123'),
 ('66777888000199', 'Creche Esperança Infantil', '88996677889', 'creche.esperanca@email.com', 'CE', 'Quixadá', 'Centenário', 'Rua da Amizade', '600', '63900000', 'senha123'),
 ('77888999000100', 'Casa do Idoso Bem Estar', '88997788990', 'casa.idoso@email.com', 'CE', 'Quixadá', 'Cedro', 'Travessa da Saúde', '700', '63900000', 'senha123'),
 ('88999000000111', 'Instituto Educação para Todos', '88998899001', 'instituto.educacao@email.com', 'CE', 'Quixadá', 'Jardim dos Monólitos', 'Rua do Saber', '800', '63900000', 'senha123'),
 ('99000111000122', 'Fundação Alimentar', '88999900112', 'fundacao.alimentar@email.com', 'CE', 'Quixadá', 'Vila Feliz', 'Av. da Nutrição', '900', '63900000', 'senha123'),
 ('00111222000133', 'ONG Mãos Solidárias', '88990011223', 'ong.maos@email.com', 'CE', 'Quixadá', 'Novo Horizonte', 'Rua da Solidariedade', '1000', '63900000', 'senha123'); 
INSERT INTO doador (cpf_cnpj_d, data_nascimento)
VALUES ('11122233344','1985-03-15'),('22233344455','1990-07-22'),('33344455566','1978-11-30'),('44455566677','1982-05-10'),
 ('55566677788','1995-09-18'),('66677788899','1988-12-05'),('77788899900','1975-04-20'),('88899900011','1992-08-15'),
 ('99900011122','1980-01-30'),('00011122233','1998-06-25'); 
INSERT INTO beneficiario (cpf_cnpj_b, data_nascimento)
VALUES ('11122233345','1960-01-25'),('22233344456','1955-08-12'),('33344455567','1972-12-05'),('44455566678','1988-04-20'),
 ('55566677789','1993-06-08'),('66677788890','1965-03-18'),('77788899901','1958-11-22'),('88899900012','1970-07-14'),
 ('99900011123','1985-09-30'),('00011122234','1990-02-28'); 
INSERT INTO instituicao (cpf_cnpj_i)
VALUES ('11222333000144'),('22333444000155'),('33444555000166'),('44555666000177'),('55666777000188'),
 ('66777888000199'),('77888999000100'),('88999000000111'),('99000111000122'),('00111222000133'); 
INSERT INTO campanha (nome, data_inicio, data_fim, status, cpf_cnpj_i)
VALUES ('Campanha do Agasalho 2024','2024-05-01', '2024-08-31', 'Ativa', '11222333000144'),
 ('Natal Solidário 2024','2024-11-01','2024-12-20','Planejada','22333444000155'),
 ('Páscoa com Amor','2024-03-01','2024-04-10','Concluída','33444555000166'),
 ('Volta às Aulas Solidária','2024-01-15','2024-02-28','Concluída','44555666000177'),
 ('Doação de Livros','2024-04-01','2024-12-31','Ativa','55666777000188'),
 ('Alimentos não Perecíveis','2024-06-01','2024-12-31','Ativa','66777888000199'),
 ('Brinquedos para Crianças','2024-09-01','2024-12-15','Planejada','77888999000100'),
 ('Material de Higiene','2024-03-15','2024-11-30','Ativa','88999000000111'),
 ('Móveis Usados','2024-02-01','2024-12-31','Ativa','99000111000122'),
 ('Eletrodomésticos','2024-01-01','2024-12-31','Ativa','00111222000133'); 
INSERT INTO doacao (data_doacao, cpf_cnpj_d, id_campanha)
VALUES ('2024-05-10 14:30:00', '11122233344', 1),
 ('2024-05-12 10:15:00', '22233344455', 1),
 ('2024-05-15 16:45:00', '33344455566', 3),
 ('2024-05-18 09:20:00', '44455566677', 5),
 ('2024-05-20 11:30:00', '55566677788', 6),
 ('2024-05-22 13:15:00', '66677788899', 8),
 ('2024-05-25 15:40:00', '77788899900', 9),
 ('2024-05-28 08:50:00', '88899900011', 10),
 ('2024-06-01 14:20:00', '99900011122', 4),
 ('2024-06-05 10:10:00', '00011122233', 2); 
INSERT INTO item_doacao (id_doacao, nome, descricao, estado_conservacao, peso, volume, tamanho, cor)
VALUES (1,'Casaco de Inverno','Casaco quente para adultos','Bom',0.8,0.02,'M','Azul'),
 (1,'Calça Jeans','Calça jeans masculina','Usado',0.6,0.015,'38','Azul'),
 (1,'Blusa de Frio','Blusa de lã feminina','Novo',0.5,0.01,'P','Vermelho'),
 (1,'Tênis Esportivo','Tênis para caminhada','Bom',0.7,0.008,'40','Branco'),
 (1,'Meias de Lã','Pacote com 3 pares de meias','Novo',0.2,0.001,'Único','Cinza'),
 (1,'Gorro','Gorro de lã para inverno','Novo',0.1,0.0005,'Adulto','Preto'),
 (1,'Cachecol','Cachecol de lã longo','Bom',0.3,0.002,'Padrão','Verde'),
 (1,'Luvas','Par de luvas de lã','Novo',0.15,0.0008,'M','Marrom'),
 (1,'Jaqueta Corta Vento','Jaqueta impermeável','Usado',0.9,0.025,'G','Azul Marinho'),
 (1,'Calça Moletom','Calça de moletom confortável','Bom',0.6,0.018,'M','Cinza'),
 (2,'Cobertor','Cobertor de lã queen size','Bom',2.5,0.05,'Queen','Azul'),
 (2,'Edredom','Edredom antialérgico','Novo',3.0,0.06,'King','Branco'),
 (2,'Fronha','Conjunto com 4 fronhas','Novo',0.4,0.003,'Standard','Branco'),
 (2,'Toalha de Banho','Toalha de banho grande','Bom',0.8,0.004,'Grande','Azul Claro'),
 (2,'Toalha de Rosto','Toalha de rosto média','Novo',0.3,0.002,'Média','Branca'),
 (2,'Roupão','Roupão de banho','Usado',1.2,0.03,'G','Azul Marinho'),
 (2,'Tapete','Tapete de banheiro','Bom',1.0,0.02,'60x90cm','Cinza'),
 (2,'Cortina','Cortina blackout','Novo',2.8,0.04,'3x2m','Bege'),
 (2,'Almofada','Almofada decorativa','Bom',0.5,0.01,'45x45cm','Verde'),
 (2,'Colcha','Colcha de cama casal','Usado',1.8,0.035,'Casal','Rosa'),
 (3,'Ovo de Páscoa','Ovo de chocolate ao leite 500g','Novo',0.6,0.005,'Médio','Colorido'),
 (3,'Cesta Básica','Cesta com alimentos essenciais','Novo',8.0,0.08,'Grande','Variada'),
 (3,'Biscoito','Pacote de biscoito cream cracker','Novo',0.4,0.003,'400g','Dourado'),
 (3,'Achocolatado','Pote de achocolatado 400g','Novo',0.5,0.004,'400g','Marrom'),
 (3,'Leite em Pó','Pacote de leite em pó 1kg','Novo',1.1,0.006,'1kg','Branco'),
 (3,'Café','Pacote de café 500g','Novo',0.6,0.004,'500g','Marrom'),
 (3,'Açúcar','Pacote de açúcar 1kg','Novo',1.1,0.005,'1kg','Branco'),
 (3,'Farinha','Pacote de farinha 1kg','Novo',1.1,0.005,'1kg','Branca'),
 (3,'Óleo','Litro de óleo de soja','Novo',0.95,0.001,'1L','Amarelo'),
 (3,'Feijão','Pacote de feijão 1kg','Novo',1.1,0.005,'1kg','Marrom'),
 (4,'Livro Redes De Computadores e a internet','Livro para ser inteligente','Bom',0.7,0.005,'A4','Verde'),
 (4,'Livro Cálculo Diferencial','Cálculo diferencial e integral - volume 1','Usado',1.2,0.008,'Grande','Azul'),
 (4,'Livro Álgebra Linear','Álgebra linear e suas aplicações','Bom',0.9,0.006,'Médio','Amarelo'),
 (4,'Livro Geometria Analítica','Geometria analítica e vetorial','Usado',0.8,0.005,'A4','Vermelho'),
 (4,'Livro Matemática Financeira','Matemática financeira aplicada','Novo',0.6,0.004,'A5','Azul'),
 (4,'Livro Estatística Básica','Noções de estatística e probabilidade','Bom',0.7,0.005,'A4','Verde'),
 (4,'Livro Trigonometria','Trigonometria e suas aplicações','Novo',0.5,0.004,'Médio','Laranja'),
 (4,'Livro Matemática Discreta','Fundamentos de matemática discreta','Usado',0.8,0.006,'A4','Marrom'),
 (4,'Livro Cálculo Avançado','Cálculo de várias variáveis','Bom',1.1,0.007,'Grande','Cinza'),
 (4,'Livro História da Matemática','Evolução histórica da matemática','Novo',0.7,0.005,'A4','Bege'),
 (5,'Arroz','Pacote de arroz 5kg','Novo',5.0,0.008,'Pequeno','Branco'),
 (5,'Macarrão','Pacote de macarrão 1kg','Novo',1.1,0.004,'1kg','Amarelo'),
 (5,'Molho de Tomate','Lata de molho de tomate','Novo',0.5,0.002,'340g','Vermelho'),
 (5,'Milho','Lata de milho verde','Novo',0.4,0.002,'300g','Amarelo'),
 (5,'Ervilha','Lata de ervilha','Novo',0.4,0.002,'300g','Verde'),
 (5,'Sardinha','Lata de sardinha','Novo',0.3,0.001,'125g','Laranja'),
 (5,'Leite Condensado','Lata de leite condensado','Novo',0.4,0.002,'395g','Azul'),
 (5,'Creme de Leite','Lata de creme de leite','Novo',0.3,0.001,'200g','Vermelho'),
 (5,'Extrato de Tomate','Lata de extrato de tomate','Novo',0.2,0.001,'140g','Vermelho'),
 (5,'Feijão Enlatado','Lata de feijão pronto','Novo',0.5,0.002,'400g','Marrom');
INSERT INTO ordem_de_doacao (data_hora_criacao, data_hora_retirada, status, estado, cidade, bairro, rua, numero, cep, cpf_cnpj_b, cpf_cnpj_i) 
 VALUES ('2024-05-11 09:00:00','2024-05-12 14:00:00','Entregue','Ceará','Quixadá','Centro','Rua A','123','63900000','11122233345','11222333000144'),
 ('2024-05-13 10:30:00','2024-05-14 11:15:00','Entregue','Ceará','Quixadá','Alto São Francisco','Rua B','456','63900000','22233344456','22333444000155'),
 ('2024-05-16 08:45:00',NULL,'Pendente','Ceará','Quixadá','Campo Velho','Rua C','789','63900000','33344455567','33444555000166'),
 ('2024-05-19 14:20:00','2024-05-20 10:30:00','Entregue','Ceará','Quixadá','Planalto','Rua D','321','63900000','44455566678','44555666000177'),
 ('2024-05-21 11:10:00',NULL,'Processando','Ceará','Quixadá','São João','Rua E','654','63900000','55566677789','55666777000188'),
 ('2024-05-23 16:30:00','2024-05-24 09:45:00','Entregue','Ceará','Quixadá','Centenário','Rua F','987','63900000','66677788890','66777888000199'),
 ('2024-05-26 13:15:00',NULL,'Cancelada','Ceará','Quixadá','Cedro','Rua G','147','63900000','77788899901','77888999000100'),
 ('2024-05-29 10:00:00','2024-05-30 15:20:00','Entregue','Ceará','Quixadá','Jardim dos Monólitos','Rua H','258','63900000','88899900012','88999000000111');