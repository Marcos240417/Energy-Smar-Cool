# 📘 README – Sistema de Monitoramento e Economia de Energia em Refrigeração Industrial
## ❄️ Visão Geral do Projeto

Este projeto tem como objetivo desenvolver um sistema completo para monitoramento contínuo da temperatura em equipamentos de refrigeração industrial, permitindo que empresas acompanhem o funcionamento de câmaras frias, identifiquem anomalias rapidamente e reduzam custos de energia.

A solução é composta por:

API Backend (Django + MongoDB)
Responsável por receber medições dos sensores, armazenar, processar e disponibilizar para o dashboard.

Dashboard Web
Interface visual onde administradores e clientes acompanham os dados, alertas e relatórios.

Sensores (ESP32 ou similares)
Dispositivos que enviam temperatura e outros dados em tempo real.

# 🚀 Tecnologias Utilizadas
# 🔧 Backend (API)

Python 3.12+

Django 5+

Django REST Framework

PyMongo / Djongo

MongoDB (banco NoSQL)

JWT Authentication (SimpleJWT)

Swagger (drf-yasg) para documentação

# 🎨 Frontend (Dashboard)

 (definir com equipe)

Chart.js / ngx-charts

Axios / HttpClient

# 🐳 Infraestrutura

Docker

Docker Compose

Mongo Express (opcional)

Insomnia / Postman para testes


# 🧠 Arquitetura do Sistema

```bash
ESP32 (sensores)
      ↓
API Django REST
      ↓
MongoDB (Time Series Collections)
      ↓
Dashboard Web
```
## 🧩 Épicos da API

```bash
| Código | Épico                  | Objetivo                                    |
| ------ | ---------------------- | ------------------------------------------- |
| E1     | Ingestão de Dados      | Receber e armazenar medições em tempo real. |
| E2     | Gestão de Entidades    | CRUDs de sensores, lojas e equipamentos.    |
| E3     | Autenticação JWT       | Registro, login e segurança.                |
| E4     | Histórico e Relatórios | Consultar temperaturas e calcular médias.   |
| E5     | Alertas Inteligentes   | Detectar anomalias.                         |
| E6     | Deploy e Infra         | Containerização e variáveis de ambiente.    |
```

## ⚙️ Requisitos Funcionais (RF)

```bash
| Código | Requisito                    | Prioridade |
| ------ | ---------------------------- | ---------- |
| RF01   | POST /api/medicoes/          | Alta       |
| RF02   | GET /api/medicoes/ (filtros) | Alta       |
| RF03   | GET /api/medicoes/ultimas/   | Alta       |
| RF04   | CRUD de Sensores             | Média      |
| RF05   | CRUD de Lojas                | Média      |
| RF06   | Autenticação JWT             | Alta       |
| RF07   | Alertas Automáticos          | Média      |
| RF08   | Exportar CSV                 | Baixa      |
| RF10   | Deploy com Docker            | Alta       |
```

# 📁 Estrutura de Pastas da API 

```bash
api/
│
├── docs/                       # Documentação geral do projeto
│   ├── architecture.md
│   ├── database.md
│   ├── api-specs.md
│   └── examples/
│
├── src/                        # Código-fonte principal da API
│   ├── config/                 # Configurações do Django
│   │   ├── __init__.py
│   │   ├── settings.py         # Config principal
│   │   ├── urls.py             # URLs globais
│   │   └── wsgi.py
│   │
│   ├── core/                   # Módulo de utilidades gerais
│   │   ├── helpers.py
│   │   ├── exceptions.py
│   │   ├── pagination.py
│   │   ├── permissions.py
│   │   └── validators.py
│   │
│   ├── users/                  # App responsável por autenticação e usuários
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── services.py
│   │
│   ├── sensores/               # CRUD de sensores
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   └── services.py
│   │
│   ├── lojas/                  # CRUD de lojas
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   └── services.py
│   │
│   ├── medicoes/               # Módulo principal: ingestão e consultas
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   ├── selectors.py        # Consultas específicas (ex: médicas filtradas)
│   │   ├── services.py         # Lógica de negócio (criar medição, média etc.)
│   │   └── tasks.py
│   │
│   ├── alertas/                # Módulo de alertas automáticos
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   ├── rules.py            # Regras de disparo de alerta
│   │   └── services.py
│
├── tests/                      # Testes automatizados
│   ├── test_users.py
│   ├── test_medicoes.py
│   ├── test_alertas.py
│   └── test_sensores.py
│
├── scripts/                    # Scripts auxiliares
│   ├── seed.py                 # Popular o banco
│   ├── cleanup.py              # Limpar dados
│   └── export_csv.py
│
├── .env.example               # Modelo de variáveis de ambiente
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── requirements.txt
└── README.md
```

# 👥 Equipe

Product Owner: 

Dev Backend: 

Dev Frontend: 

Orientador: Prof.Wellington
