import asyncio
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select

# 1. Налаштування бази даних та моделі
DATABASE_URL = "sqlite+aiosqlite:///network.db"
Base = declarative_base()


class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key=True)
    ip_address = Column(String, unique=True, nullable=False)
    status = Column(String, default="unknown")


# Створення асинхронного рушія та фабрики сесій
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 2. Асинхронні функції для роботи з БД
async def create_tables():
    """Створення таблиць у базі даних."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def reset_nodes():
    """Очищення таблиці перед новим запуском для уникнення помилок унікальності."""
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM nodes"))
        await session.commit()

async def add_nodes():
    """Додавання 10 нових мережевих вузлів."""
    async with AsyncSessionLocal() as session:
        nodes = [Node(ip_address=f"192.168.1.{i}", status="unknown") for i in range(1, 11)]
        session.add_all(nodes)
        await session.commit()
    print("10 вузлів успішно додано до бази даних.")

async def get_nodes(state="Поточний"):
    """Отримання та виведення списку вузлів."""
    print(f"\n--- {state} список вузлів ---")
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Node))
        nodes = result.scalars().all()
        for node in nodes:
            print(f"ID: {node.id:2} | IP: {node.ip_address:14} | Status: {node.status}")

async def monitor_nodes():
    """Імітація асинхронного збору статусів вузлів."""
    print("\n--- Запуск моніторингу вузлів (імітація мережевих запитів) ---")
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Node))
        nodes = result.scalars().all()

        for node in nodes:
            # Імітація затримки мережі (наприклад, ping до пристрою)
            await asyncio.sleep(0.2)

            # Логіка оновлення: парні IP - offline, непарні - active
            last_octet = int(node.ip_address.split('.')[-1])
            node.status = "offline" if last_octet % 2 == 0 else "active"

        await session.commit()
    print("Статуси всіх вузлів успішно оновлено та збережено.")


# ==========================================
# ГОЛОВНИЙ БЛОК ВИКОНАННЯ
# ==========================================
async def main():
    await create_tables()
    await reset_nodes()  # Очищаємо таблицю, щоб уникнути конфліктів при повторному запуску
    await add_nodes()

    # Виводимо вузли ДО моніторингу
    await get_nodes("Початковий")

    # Запускаємо процес оновлення
    await monitor_nodes()

    # Виводимо вузли ПІСЛЯ моніторингу
    await get_nodes("Оновлений")


if __name__ == "__main__":
    # Запуск асинхронної програми
    asyncio.run(main())