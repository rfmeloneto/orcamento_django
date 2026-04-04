# 💰 Orçamento Pessoal

Sistema completo de orçamento financeiro pessoal com Django. Controle rigoroso de gastos categorizados, metas financeiras e dashboard analítico com gráficos em tempo real.

---

## 🚀 Instalação Rápida

### 1. Pré-requisitos
- Python 3.10+ instalado
- pip atualizado

### 2. Clone / copie o projeto
```bash
cd /caminho/onde/quer/instalar
# Coloque a pasta orcamento_pessoal aqui
```

### 3. Crie e ative o ambiente virtual
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux / macOS:
source venv/bin/activate
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

### 5. Configure o ambiente
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o .env e coloque uma SECRET_KEY segura
# (use: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
```

### 6. Crie o banco de dados
```bash
python manage.py migrate
```

### 7. Execute o setup inicial (cria usuário + categorias)
```bash
python setup_inicial.py
```

### 8. Inicie o servidor
```bash
# Acessível apenas localmente:
python manage.py runserver

# Acessível em toda a rede local (recomendado para uso em LAN):
python manage.py runserver 0.0.0.0:8000
```

### 9. Acesse no navegador
- **Local:** http://localhost:8000
- **Rede local:** http://SEU-IP-LOCAL:8000
- **Admin:** http://localhost:8000/admin

---

## 📁 Estrutura do Projeto

```
orcamento_pessoal/
├── manage.py
├── setup_inicial.py          ← Roda uma vez após instalar
├── requirements.txt
├── .env.example
│
├── orcamento/                ← Configurações Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                     ← App principal
│   ├── models.py             ← Todos os modelos normalizados
│   ├── admin.py              ← Painel admin configurado
│   ├── apps.py
│   ├── signals.py            ← Cria dados padrão ao criar usuário
│   ├── forms.py              ← Todos os formulários
│   ├── urls.py               ← Roteamento completo
│   ├── views/
│   │   ├── dashboard.py
│   │   ├── income.py
│   │   ├── expenses.py
│   │   ├── investments.py
│   │   └── goals.py
│   └── api/
│       └── views.py          ← Endpoints JSON para Chart.js
│
├── static/
│   ├── css/main.css          ← Design System completo (light + dark)
│   └── js/
│       ├── main.js           ← Sidebar, tema, utilitários
│       └── charts.js         ← Todos os gráficos Chart.js
│
└── templates/
    ├── base.html             ← Layout principal (sidebar + topbar)
    ├── confirm_delete.html
    ├── auth/login.html
    ├── dashboard/index.html
    ├── income/
    ├── investments/
    ├── goals/
    ├── expenses/
    └── profile/
```

---

## 🗃️ Modelo de Dados

```
Profile ──── User (1:1)

IncomeCategory ──── Income (User)
InvestmentCategory ──── Investment (User)
EmergencyReserve (User, 1:1)
FinancialGoal (User)

ExpenseGroup (User)
  └── ExpenseSubgroup
        └── ExpenseItem
              └── Transaction (User)
```

---

## 🎯 Funcionalidades

| Módulo | Funcionalidades |
|---|---|
| **Dashboard** | Cards de resumo, Donut por grupo, Barras 6 meses, Linha patrimônio, Metas, Reserva |
| **Receitas** | CRUD completo, categorias customizáveis, filtros por período |
| **Gastos** | Hierarquia Grupo→Subgrupo→Item, % alvo por grupo, desvio em tempo real |
| **Transações** | Registro de gastos reais, formas de pagamento, filtros |
| **Investimentos** | Renda Fixa, Variável, Reserva, ganho/perda automático |
| **Metas** | Curto/Médio/Longo prazo, progresso, valor mensal necessário |
| **Tema** | Light/Dark com persistência em localStorage |

---

## 🌐 Acesso na Rede Local

Para acessar de outros dispositivos na mesma rede Wi-Fi:

1. Descubra seu IP local:
   - **Windows:** `ipconfig` → Endereço IPv4
   - **Linux/macOS:** `ip addr` ou `ifconfig`

2. Inicie com: `python manage.py runserver 0.0.0.0:8000`

3. Acesse de qualquer dispositivo: `http://192.168.x.x:8000`

4. Adicione o IP ao `ALLOWED_HOSTS` no `.env`:
   ```
   ALLOWED_HOSTS=localhost,127.0.0.1,192.168.x.x
   ```

---

## 🛡️ Segurança (rede local)

Este sistema foi projetado para uso **exclusivo em rede local privada**.
- `DEBUG=True` está habilitado (não use em produção pública)
- SQLite como banco de dados (suficiente para uso pessoal)
- Autenticação por sessão Django

---

## 📦 Tech Stack

| Tecnologia | Versão | Função |
|---|---|---|
| Django | 4.2 | Backend + ORM |
| Bootstrap | 5.3 | Grid + componentes |
| Chart.js | 4.4 | Gráficos |
| Lucide | Latest | Ícones |
| Day.js | 1.11 | Datas |
| Sora + DM Sans | — | Tipografia |
| WhiteNoise | 6.6 | Estáticos |

---

## 🐛 Problemas Comuns

**"No module named 'decouple'"**
```bash
pip install python-decouple
```

**Erro de ALLOWED_HOSTS**
Adicione seu IP ao `.env`:
```
ALLOWED_HOSTS=localhost,127.0.0.1,SEU-IP
```

**Gráficos não aparecem**
Verifique se o JavaScript está sem erros no console do navegador (F12).

**Reiniciar dados padrão de um usuário**
Acesse o admin Django (`/admin/`) e delete o usuário → crie novamente via `setup_inicial.py`.
