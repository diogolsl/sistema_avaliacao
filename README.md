# Sistema de Avaliação de Filmes
Este projeto é uma plataforma web para catálogo e avaliação de filmes, desenvolvida como parte de um trabalho acadêmico para demonstrar o uso de relacionamentos em bancos de dados e integridade de regras de negócio.

### Descrição do Sistema
O sistema permite a gestão de um catálogo de filmes organizados por gênero. Usuários podem visualizar o acervo e registrar avaliações para os títulos disponíveis. O foco principal da aplicação é a integridade dos dados, garantindo que o sistema de notas não permita duplicidades por usuário.

### Rotas Disponíveis 
#### Usuários (/usuarios)

`GET /usuarios/` : Renderiza a página com a lista de todos os usuários.

`POST /usuarios/novo` : Recebe o formulário e cadastra um novo usuário.

`POST /usuarios/editar/<id>` : Atualiza o nome ou e-mail de um usuário específico.

`POST /usuarios/deletar/<id>` : Exclui um usuário do sistema.

#### Filmes (/filmes)

`GET /filmes/` : Lista o catálogo de filmes.

`POST /filmes/novo` : Cadastra um novo filme vinculando-o a um gênero.

`POST /filmes/editar/<id>` : Atualiza as informações do filme.

`POST /filmes/deletar/<id>` : Remove o filme do catálogo.

#### Gêneros (/generos)

`GET /generos/` : Lista as categorias cadastradas.

`POST /generos/novo` : Cria um novo gênero.

`POST /generos/editar/<id>` : Altera o nome do gênero.

`POST /generos/deletar/<id>` : Exclui o gênero.

#### Avaliações (/avaliacoes)

`GET /avaliacoes/` : Lista as avaliações registradas.

`POST /avaliacoes/novo` : Registra uma nova nota de um usuário para um filme.

`POST /avaliacoes/editar/<id>` : Permite alterar a nota dada.

`POST /avaliacoes/deletar/<id>` : Remove a avaliação.

### Explicação das Tabelas
Entidades:
* Usuario
    * id_usuario (pk)
    * nome
    * email

* Genero
    * id_genero (pk)
    * nome

    * filmes --relacionamento com a tabela Filme


* Filme
    * id_filme (pk)
    * titulo
    * ano_lancamento
    * sinopse
    * id_genero (fk)

    * avaliacoes --relacionamento com a tabela Avaliacao


* Avaliacao
    * id_avaliacao (pk)
    * id_usuario (fk)
    * id_filme (fk)
    * nota

    Regras da tabela: 
    UK_usuario_filme: (id_usuario, id filme) -- garante unicidade

    Check_nota_range: (nota >= 1 AND nota <= 5) -- garante notas dentro de 1 a 5


### Regras de negócio do sistema
* A principal regra de negócio é impedir que um mesmo usuário avalie o mesmo filme mais de uma vez, assegurando a integridade das avaliações.

* Notas das avaliações dos filmes devem estar dentro de 1 a 5.

### Como Executar o Projeto em sua Máquina
Siga os passos abaixo para configurar o ambiente de desenvolvimento local.

#### Pré-requisitos
* Python 3.8+ instalado.
* Gerenciador de pacotes pip.

#### Clone o repositório

```bash
git clone https://github.com/diogolsl/sistema_avaliacao.git
cd sistema_avaliacao
```

#### Configuração do Ambiente Virtual

É altamente recomendável utilizar um ambiente virtual para isolar as dependências do projeto:


No Windows
```bash
python -m venv venv
.\venv\Scripts\activate
```

No Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Instalação de Dependências

Com o ambiente virtual ativo, instale os pacotes necessários:

```bash
pip install -r requirements.txt
```

#### Variáveis de Ambiente

O projeto utiliza o pacote python-dotenv. Configure seu arquivo .env na raiz do projeto  e certifique-se de que ele contém as seguintes chaves:

```
FLASK_APP=run.py
FLASK_DEBUG=1
DATABASE_URL=sqlite:///avaliacoes.db  # Ou sua string de conexão SQL
```

#### Inicialização do Banco de Dados

Como o projeto utiliza Flask-Migrate, execute os comandos para criar e popular o banco de dados antes de iniciar o sistema:

```bash
flask db upgrade
```
#### Rodando a Aplicação

```bash
python run.py
```

O sistema estará disponível em: http://127.0.0.1:5000

#### Execução de Testes

Este projeto já conta com suporte a testes automatizados via pytest e pytest-flask. Para rodar a suíte de testes, execute:

```bash
pytest
```
