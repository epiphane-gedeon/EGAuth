#!/usr/bin/env python3
"""
Script pour vérifier l'état de la base de données EGAuth
"""

import asyncio
import sys
from pathlib import Path

# Ajouter le répertoire du projet au path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import get_settings
from app.database import engine, Base
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def check_database():
    """Vérifie la connexion et l'état de la base de données"""
    settings = get_settings()

    print("🔍 Vérification de la base de données EGAuth")
    print(f"📍 URL: {settings.DATABASE_URL}")
    print("-" * 50)

    try:
        # Test de connexion
        async with engine.begin() as conn:
            print("✅ Connexion à la base de données réussie")

            # Vérifier si les tables existent
            result = await conn.execute(
                text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            )

            tables = result.fetchall()
            table_names = [row[0] for row in tables]

            print(f"📊 Tables trouvées: {len(table_names)}")

            expected_tables = ["users", "clients", "auth_codes", "sessions"]
            for table in expected_tables:
                if table in table_names:
                    print(f"✅ Table '{table}' existe")
                else:
                    print(f"❌ Table '{table}' manquante")

            # Compter les utilisateurs
            if "users" in table_names:
                result = await conn.execute(text("SELECT COUNT(*) FROM users"))
                user_count = result.scalar()
                print(f"👥 Utilisateurs enregistrés: {user_count}")

            # Compter les clients
            if "clients" in table_names:
                result = await conn.execute(text("SELECT COUNT(*) FROM clients"))
                client_count = result.scalar()
                print(f"🏢 Clients OAuth enregistrés: {client_count}")

        print("-" * 50)
        print("🎉 Base de données opérationnelle !")

    except Exception as e:
        print(f"❌ Erreur de base de données: {e}")
        print("💡 Vérifiez que PostgreSQL est démarré et accessible")
        return False

    return True


async def create_tables_if_needed():
    """Crée les tables si elles n'existent pas"""
    print("\n🔨 Création des tables si nécessaire...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables créées/mises à jour")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--create":
        # Mode création de tables
        asyncio.run(create_tables_if_needed())
    else:
        # Mode vérification
        success = asyncio.run(check_database())
        sys.exit(0 if success else 1)
