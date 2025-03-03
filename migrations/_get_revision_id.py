from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import argv
from typing import Final

# Шлях до директорії з міграціями за замовчуванням
_DEFAULT_PATH: Final[str] = "./migrations/versions"


def get_next_revision_id(path: Path) -> int:
    """
    Визначає наступний ідентифікатор ревізії на основі кількості існуючих міграцій.
    
    Функція підраховує кількість Python-файлів у вказаній директорії
    та повертає наступний порядковий номер для нової міграції.
    
    Args:
        path: Шлях до директорії з файлами міграцій
        
    Returns:
        Наступний порядковий номер ревізії (кількість існуючих файлів + 1)
    """
    return len(list(path.glob("*.py"))) + 1


def main() -> str:
    """
    Головна функція для отримання форматованого ідентифікатора наступної ревізії.
    
    Функція парсить аргументи командного рядка для отримання шляху до директорії
    з міграціями та повертає форматований ідентифікатор у вигляді трицифрового числа.
    
    Returns:
        Форматований ідентифікатор ревізії у форматі "NNN" (наприклад, "001", "023")
    """
    # Створюємо парсер аргументів командного рядка
    parser: ArgumentParser = ArgumentParser()
    # Додаємо опцію для вказання шляху до директорії з міграціями
    parser.add_argument("-p", "--path", dest="path", type=Path, default=_DEFAULT_PATH)
    # Парсимо аргументи командного рядка
    namespace: Namespace = parser.parse_args(argv[1:])
    # Повертаємо форматований ідентифікатор ревізії
    return "{id:03}".format(id=get_next_revision_id(path=namespace.path))


if __name__ == "__main__":
    print(main())  # noqa: T201
