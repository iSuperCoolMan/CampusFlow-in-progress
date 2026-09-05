import gc
import os


pytest_plugins = [
    "tests.fixtures.db",
    "tests.fixtures.client",
    "tests.fixtures.user"
]


def pytest_sessionfinish(session, exitstatus):
    import app.database.database as db_module

    try:
        if hasattr(db_module, "engine"):
            db_module.engine.pool.dispose()
            db_module.engine.sync_engine.dispose()
    except Exception:
        pass

    from tests.fixtures.db import TEST_DB_FILENAME

    gc.collect()

    if os.path.exists(TEST_DB_FILENAME):
        try:
            os.remove(TEST_DB_FILENAME)
            print(f"\n🔥 Тестовая физическая база {TEST_DB_FILENAME} успешно удалена.")
        except PermissionError as e:
            print(f"\n⚠️ Windows все еще блокирует файл: {e}.")