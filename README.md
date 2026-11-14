# ✅ To-Do App Full Stack com Login

Aplicação web de tarefas com **cadastro, login e CRUD completo** (criar, listar, concluir e excluir), com API REST em Flask e front-end em HTML + JavaScript puro.

## 🏗️ Arquitetura
```
Navegador (static/index.html + fetch)
        │  JSON
        ▼
API REST Flask (app.py) ── sessão com cookie seguro
        │
        ▼
SQLite (todo.db)
```

## 🔌 Endpoints
| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/register` | Cria usuário |
| POST | `/api/login` | Faz login |
| POST | `/api/logout` | Sai |
| GET | `/api/tasks` | Lista as tarefas do usuário |
| POST | `/api/tasks` | Cria tarefa |
| PATCH | `/api/tasks/<id>` | Marca/desmarca como concluída |
| DELETE | `/api/tasks/<id>` | Exclui tarefa |

## 🧰 Tecnologias
- Back-end: Python, Flask, SQLite, Werkzeug (hash de senha)
- Front-end: HTML, CSS e JavaScript (Fetch API)

## 🚀 Como rodar
```bash
git clone https://github.com/MoniqueSilva79/todo-app-fullstack.git
cd todo-app-fullstack
pip install -r requirements.txt
export SECRET_KEY="troque-esta-chave"
python app.py
```
Acesse http://localhost:5000

## 🔒 Segurança
- Senhas guardadas com hash seguro (Werkzeug), nunca em texto puro
- Cada usuário só acessa as próprias tarefas
- Consultas SQL parametrizadas (evita SQL injection)

## 📚 O que pratiquei
- API REST e verbos HTTP
- Autenticação com sessão
- Integração front-end ↔ back-end

## 🗺️ Próximos passos
- [ ] Reescrever o front em React
- [ ] Datas de vencimento e prioridades
- [ ] Deploy no Cloud Run com Cloud SQL
