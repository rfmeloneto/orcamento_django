"""
setup_inicial.py — Orçamento Pessoal
Execute uma única vez após instalar o projeto:
  python setup_inicial.py

Cria o superusuário 'admin' (senha: admin123) e dispara os signals
que populam todas as categorias e estrutura de gastos padrão.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orcamento.settings')
django.setup()

from django.contrib.auth.models import User

def main():
    print("=" * 60)
    print("  ORÇAMENTO PESSOAL — Setup Inicial")
    print("=" * 60)

    username = input("\nNome de usuário (padrão: admin): ").strip() or "admin"
    email    = input("E-mail (opcional): ").strip() or ""
    password = input("Senha (padrão: admin123): ").strip() or "admin123"
    first_name = input("Primeiro nome: ").strip()
    last_name  = input("Sobrenome: ").strip()

    if User.objects.filter(username=username).exists():
        print(f"\n⚠️  Usuário '{username}' já existe. Nada foi alterado.")
        sys.exit(0)

    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    print(f"\n✅  Usuário '{username}' criado com sucesso!")
    print("    As categorias e estrutura de gastos foram populadas automaticamente.")
    print("\n" + "=" * 60)
    print("  Para iniciar o servidor na rede local:")
    print("  python manage.py runserver 0.0.0.0:8000")
    print("=" * 60 + "\n")

if __name__ == '__main__':
    main()
