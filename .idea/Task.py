import json
import os


class TaskList:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Загрузка задач из JSON-файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def save_tasks(self):
        """Сохранение задач в JSON-файл"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.tasks, file, ensure_ascii=False, indent=2)

    def add_task(self, description):
        """Добавление новой задачи"""
        if description.strip():
            task = {
                "id": len(self.tasks) + 1,
                "description": description.strip(),
                "status": "не выполнено"
            }
            self.tasks.append(task)
            self.save_tasks()
            print(f"✅ Задача добавлена (ID: {task['id']})")
        else:
            print("❌ Описание задачи не может быть пустым")

    def view_tasks(self):
        """Просмотр всех задач"""
        if not self.tasks:
            print("📝 Список задач пуст")
            return

        print("\n📋 Список задач:")
        print("-" * 40)
        for task in self.tasks:
            status_icon = "✅" if task["status"] == "выполнено" else "⏳"
            print(f"{task['id']}. {task['description']} {status_icon}")
        print("-" * 40)

    def delete_task(self, task_id):
        """Удаление задачи по ID"""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                deleted_task = self.tasks.pop(i)
                # Пересчитываем ID оставшихся задач
                for j, remaining_task in enumerate(self.tasks, 1):
                    remaining_task["id"] = j
                self.save_tasks()
                print(f"🗑️ Задача удалена: '{deleted_task['description']}'")
                return

        print(f"❌ Задача с ID {task_id} не найдена")

    def mark_completed(self, task_id):
        """Отметка задачи как выполненной"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "выполнено"
                self.save_tasks()
                print(f"✅ Задача отмечена как выполненная: '{task['description']}'")
                return

        print(f"❌ Задача с ID {task_id} не найдена")

    def show_menu(self):
        """Отображение главного меню"""
        print("\n" + "=" * 50)
        print("           🎯 СПИСОК ЗАДАЧ (TASKLIST MINI)")
        print("=" * 50)
        print("1. 📝 Просмотреть задачи")
        print("2. ➕ Добавить задачу")
        print("3. 🗑️ Удалить задачу")
        print("4. ✅ Отметить как выполненную")
        print("5. 🚪 Выход")
        print("=" * 50)


def main():
    task_list = TaskList()

    # Создаем начальные задачи, если файл пустой
    if not task_list.tasks:
        initial_tasks = [
            "Изучить Python",
            "Сделать практическую работу",
            "Изучить Git"
        ]
        for task in initial_tasks:
            task_list.add_task(task)

    while True:
        task_list.show_menu()

        try:
            choice = input("\nВыберите действие (1-5): ").strip()

            if choice == "1":
                task_list.view_tasks()

            elif choice == "2":
                description = input("Введите описание задачи: ")
                task_list.add_task(description)

            elif choice == "3":
                task_list.view_tasks()
                if task_list.tasks:
                    try:
                        task_id = int(input("Введите ID задачи для удаления: "))
                        task_list.delete_task(task_id)
                    except ValueError:
                        print("❌ Пожалуйста, введите числовой ID")

            elif choice == "4":
                task_list.view_tasks()
                if task_list.tasks:
                    try:
                        task_id = int(input("Введите ID задачи для отметки: "))
                        task_list.mark_completed(task_id)
                    except ValueError:
                        print("❌ Пожалуйста, введите числовой ID")

            elif choice == "5":
                print("👋 До свидания!")
                break

            else:
                print("❌ Неверный выбор. Пожалуйста, выберите от 1 до 5")

        except KeyboardInterrupt:
            print("\n👋 Программа завершена!")
            break
        except Exception as e:
            print(f"❌ Произошла ошибка: {e}")


if __name__ == "__main__":
    main()