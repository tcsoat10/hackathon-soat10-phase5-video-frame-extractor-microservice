import os
import sys
import importlib.util
from typing import List, Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def load_migration_module(migration_path: str):
    """
    Carrega um módulo de migração a partir do caminho do arquivo.
    """
    spec = importlib.util.spec_from_file_location("migration", migration_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_migration_info(migration_path: str) -> Dict[str, Any]:
    """
    Extrai informações de uma migração (revision, down_revision, etc.).
    """
    module = load_migration_module(migration_path)
    return {
        'revision': getattr(module, 'revision', None),
        'down_revision': getattr(module, 'down_revision', None),
        'branch_labels': getattr(module, 'branch_labels', None),
        'depends_on': getattr(module, 'depends_on', None),
        'module': module,
        'path': migration_path
    }

def sort_migrations(migrations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ordena as migrações baseado na dependência (down_revision).
    """
    sorted_migrations = []
    remaining_migrations = migrations.copy()
    
    while remaining_migrations:
        # Procura por migrações sem dependências ou com dependências já aplicadas
        for migration in remaining_migrations:
            if migration['down_revision'] is None:
                # Migração inicial (sem dependências)
                sorted_migrations.append(migration)
                remaining_migrations.remove(migration)
                break
            elif any(m['revision'] == migration['down_revision'] for m in sorted_migrations):
                # Dependência já foi aplicada
                sorted_migrations.append(migration)
                remaining_migrations.remove(migration)
                break
        else:
            if remaining_migrations:
                print(f"Warning: Unresolved dependencies for migrations: {[m['revision'] for m in remaining_migrations]}")
                # Adiciona as migrações restantes por ordem alfabética como fallback
                remaining_migrations.sort(key=lambda x: x['revision'])
                sorted_migrations.extend(remaining_migrations)
                break
    
    return sorted_migrations

def run_migrations():
    """
    Executa todas as migrações em ordem.
    """
    migrations_dir = os.path.join(os.path.dirname(__file__), "migrations")

    if not os.path.exists(migrations_dir):
        print(f"Migration directory {migrations_dir} does not exist.")
        return False

    migration_files = []
    for migration_file in os.listdir(migrations_dir):
        if migration_file.endswith(".py") and not migration_file.startswith("__"):
            migration_files.append(migration_file)

    if not migration_files:
        print("No migration files found.")
        return True

    migrations = []
    for migration_file in migration_files:
        migration_path = os.path.join(migrations_dir, migration_file)
        try:
            migration_info = get_migration_info(migration_path)
            migrations.append(migration_info)
            print(f"Loaded migration: {migration_file} (revision: {migration_info['revision']})")
        except Exception as e:
            print(f"Error loading migration {migration_file}: {e}")
            import traceback
            traceback.print_exc()
            return False

    sorted_migrations = sort_migrations(migrations)

    success_count = 0
    for migration in sorted_migrations:
        try:
            print(f"Applying migration {migration['revision']}...")
            
            # Execute the upgrade function
            if hasattr(migration['module'], 'upgrade'):
                migration['module'].upgrade()
                success_count += 1
                print(f"✓ Migration {migration['revision']} applied successfully.")
            else:
                print(f"Warning: Migration {migration['revision']} has no upgrade function.")
                
        except Exception as e:
            print(f"✗ Error applying migration {migration['revision']}: {e}")
            import traceback
            traceback.print_exc()
            return False

    print(f"\n🎉 Successfully applied {success_count} migrations!")
    return True

if __name__ == "__main__":
    try:
        success = run_migrations()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Migration process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error during migration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


