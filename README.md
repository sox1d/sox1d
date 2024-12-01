# Планировщик задач

**Планировщик задач** — это приложение на **PyQt6**, предназначенное для управления задачами с использованием календаря, таблицы и интерактивных функций. Программа позволяет создавать, изменять, удалять задачи, а также сортировать и фильтровать их по различным параметрам.

---

## Основные функции

- **Создание и редактирование задач**
  - Вы можете добавлять задачи с указанием даты, времени, содержания, приоритета и статуса выполнения.
  - Возможность редактирования существующих задач.

- **Просмотр задач**
  - Задачи отображаются в таблице с указанием всех параметров.
  - Таблица поддерживает сортировку по дате и приоритету.

- **Удаление задач**
  - Удаление выполненных задач или конкретной задачи.

- **Визуальные подсказки**
  - Даты с задачами выделяются цветами в календаре:
    - :closed_book:Красный — задачи с высоким приоритетом.
    - :ledger:Желтый — задачи со средним приоритетом.
    - :green_book: Зеленый — задачи с низким приоритетом.

- **Сортировка и поиск**
  - Возможность сортировки задач по заголовкам таблицы.
  - Поиск задач по дате или содержимому.

- **Просмотр статистики**
  - Количество выполненных и невыполненных задач

---

## Установка

### Шаг 1: Установите зависимости

Перед началом работы убедитесь, что на вашем компьютере установлены Python и необходимые библиотеки(**PYQT6, plyer**). Установите их с помощью команды:

```bash
pip install PyQt6 plyer
```

### Шаг 2: Настройка базы данных

Если база данных отсутствует, приложение автоматически создаст файл `Data_mark.sqlite` с таблицей для хранения задач. При последующих запусках данные будут использоваться из созданной базы данных.

---

## Запуск проекта

Для запуска приложения достаточно запустить приложение __main.exe__ или запуск проекта через __main.py__.

---

## Интерфейс

### Главное окно
![/main_window.png](https://github.com/sox1d/sox1d/blob/ed3264f7f5e9f4f8ecc9472d163efb35d6138084/main_window.png)

- **Календарь**: для выбора даты.
- **Таблица**: отображение задач.
- **Кнопки**:
  - `Добавить задачу`: открывает окно создания новой задачи.
  - `Изменить задачу`: позволяет редактировать выделенную задачу.
  - `Удалить задачу`: удаляет выделенную задачу.
  - `Все задачи`: Показывает все созданные задачи.
  - `Поиск`: Выполняет поиск по дате и содержанию задачи.
  - `Удалить выполненные`: удаляет выполненные(с пометкой *YES*) задачи.
- **Статистика**: 
  - `Выполненные`: показывает количесвто выполненных задач.
  - `Невыполненные`: показывает количесвто невыполненных задач.

---

## Как пользоваться основынми функциями

### 1. Создание задачи
- Выберете дату на календаре(изночально выбрана сегодняшная дата)
- Нажмите на кнопку **"Добавить задачу"**.
![/Dialog1.png](https://github.com/sox1d/sox1d/blob/57e022fe56555324e997041c712dd2228fc4627b/Dialog1.png)

- Заполните поля:
  - Дата и время.
  - Содержание задачи.
  - Приоритет (Lite, Medium, Hard).
  - Статус выполнения (YES/NO).
- Нажмите **"Применить"**.

```python
    def add_new_mark(self):
        self.ui_window.dateEdit.setDate(self.ui.calendarWidget.selectedDate())
        data = str(self.ui_window.dateEdit.date().toPyDate())
        time = str(self.ui_window.timeEdit.time().toPyTime())
        content = self.ui_window.contentEdit.toPlainText()
        priority = self.ui_window.priorityBox.currentText()
        is_done = self.ui_window.complitedBox.currentText()
        self.cur.execute('''INSERT INTO Mark(data,time,content,priority,is_done) VALUES(?,?,?,?,?)''',
                         (data, time, content, priority, is_done))
        self.con.commit()
        self.new_window.close()
        self.show_mark()
        self.statistics()
```

### 2. Редактирование задачи
- Выделите задачу в таблице.
- Нажмите **"Изменить задачу"**.
- Внесите изменения в открывшемся окне и нажмите **"Применить"**.

```python
    def change_mark(self):
        data = str(self.ui_window.dateEdit.date().toPyDate())
        time = str(self.ui_window.timeEdit.time().toPyTime())
        content = self.ui_window.contentEdit.toPlainText()
        priority = self.ui_window.priorityBox.currentText()
        is_done = self.ui_window.complitedBox.currentText()
        self.ui.calendarWidget.setSelectedDate(self.ui_window.dateEdit.date())
        self.cur.execute('''UPDATE Mark SET data = ?, time = ?, content = ?, priority = ?, is_done = ? WHERE id = ?''',
                         (data, time, content, priority, is_done, self.current_task_id))
        self.con.commit()
        self.new_window.close()
        if not self.show_all_bool:
            self.show_mark()
        else:
            self.show_all()
        self.statistics()
```

### 3. Удаление задачи
- Выделите задачу и нажмите **"Удалить задачу"**.
  ```python
      def delete_mark(self):
        try:
            id = self.ui.dataTable.currentRow()
            if id == -1:
                raise ValueError
            task_id = int(self.ui.dataTable.item(id, 0).text())
            reply = QMessageBox.question(self, 'Подтверждение удаления',
                                         "Вы уверены, что хотите удалить эту задачу?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.cur.execute("DELETE FROM Mark WHERE id = ?", (task_id,))
                QMessageBox.information(self, "Удалено", "Задача успешно удалена.")
            self.con.commit()
            self.statistics()
            self.deleted = True
            if not self.show_all_bool:
                self.show_mark()
            else:
                self.show_all()
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Заметка не выбрана")
            return
  ```
- Для удаления всех выполненных задач нажмите **"Удалить выполненные"**.
  ```python
      def delete_completed_tasks(self):
        reply = QMessageBox.question(self, 'Подтверждение удаления',
                                     "Вы уверены, что хотите удалить эту задачу?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.cur.execute('''DELETE FROM Mark WHERE is_done = "YES"''')
            self.con.commit()
            QMessageBox.information(self, "Удаление завершено", "Все выполненные задачи удалены")
            self.deleted = True
            if not self.show_all_bool:
                self.show_mark()
            else:
                self.show_all()
            self.statistics()
  ```
### 4. Промсмотр задач
+ Просмотр конкретной задачи
  + Двойным нажатием выберите дату, которую хотите просмотреть на наличии заметок
```python
    def show_mark(self):
        self.data = self.cur.execute('''SELECT * FROM Mark 
                    WHERE data = ?''', (str(self.ui.calendarWidget.selectedDate().toPyDate()),)).fetchall()
        if not self.data and not self.deleted:
            QMessageBox.warning(self, "Ошибка", "Отсутвие заметок на данную дату")
            return
        else:
            self.show_in_table()
        self.update_date_colors()
        if self.deleted:
            self.deleted = False
        self.show_all_bool = False
```
+ Просмотр всех задач
  + Нажмите на кнопку "Все задачи"
```python
    def show_all(self):
        self.data = self.cur.execute('SELECT * FROM Mark').fetchall()
        self.show_in_table()
        self.show_all_bool = True
        self.update_date_colors()
```

Сам вывод информации реализован с помощью таблицы.
```python
    def show_in_table(self):
        self.ui.dataTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.dataTable.setColumnCount(6)
        self.ui.dataTable.setHorizontalHeaderLabels(['id', 'Дата', 'Время', 'Содержание', 'Важность', 'Выполнена?'])
        self.ui.dataTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.ui.dataTable.setRowCount(0)
        for i, row in enumerate(self.data):
            self.ui.dataTable.setRowCount(self.ui.dataTable.rowCount() + 1)
            for j, elem in enumerate(row):
                self.ui.dataTable.setItem(i, j, QTableWidgetItem(str(elem)))
                self.ui.dataTable.item(i, j).setToolTip(self.ui.dataTable.item(i, j).text())
            priority = row[4]
            if priority == "Lite":
                color = "background-color: green; color: white;"
            elif priority == "Medium":
                color = "background-color: yellow; color: black;"
            elif priority == "Hard":
                color = "background-color: red; color: white;"
            for j in range(self.ui.dataTable.columnCount()):
                self.ui.dataTable.item(i, j).setBackground(
                    QColor(color.split(":")[1].split(";")[0].strip()))
                self.ui.dataTable.item(i, j).setForeground(
                    QColor(color.split(":")[2].split(";")[0].strip()))
        self.ui.dataTable.setColumnWidth(3, 600)
        self.ui.dataTable.setColumnWidth(4, 50)
        self.ui.dataTable.setColumnWidth(5, 50)
        self.ui.dataTable.setColumnWidth(0, 50)
        self.ui.dataTable.setColumnWidth(2, 60)
```

### 5. Поиск
- Нажмите на кнопку **"Поиск"**.
![/Searh.png](https://github.com/sox1d/sox1d/blob/82e1f3ad933c899ad0591a388957bacd1715f1e2/Search.png)
- Выберите критерий поиска (дата или содержимое) и введите запрос.
- Нажмите поиск.
```python
    def perform_search(self):
        date = self.ui_search.dateEdit.date().toString("yyyy-MM-dd")
        content = self.ui_search.contentEdit.text()
        query = "SELECT * FROM Mark WHERE 1=1"
        params = []
        if date and self.ui_search.checkBox.isChecked():
            query += " AND data = ?"
            params.append(date)
        if content:
            query += " AND content LIKE ?"
            params.append(f"%{content}%")
        self.data = self.cur.execute(query, params).fetchall()
        self.ui.dataTable.setRowCount(0)
        if self.data:
            self.show_in_table()
        else:
            QMessageBox.information(self, "Результат поиска", "Ничего не найдено.")
        self.search_dialog.close()
---
```
## Дополнительные функции

### Использование и создание при отсутсвии базы данных
- С помощью библиотеки **sqlite3** программа подключается в базе данных, которыая состоит из 6 стоблцов(id, data, time, content, priority, is_done).
- При ее отсутствии создает новую, которую в последствии использует.
  ```python
    def __init__(self):
      ***
        self.initialize_database()
      ***
  
    def initialize_database(self):
        try:
            self.cur.execute('SELECT 1 FROM Mark')
        except sqlite3.OperationalError:
            self.cur.execute('''
                CREATE TABLE Mark (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    time TEXT NOT NULL,
                    content TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    is_done TEXT DEFAULT "NO"
                )
            ''')
            self.con.commit()
            print("Таблица Mark создана.")
  ```

### Сортировка
- Нажмите на заголовок столбца таблицы, чтобы отсортировать задачи по дате или приоритету.
- Сортировка поддерживает как прямой, так и обратный порядок(реализовано с помощью флагов сортировки, где <ins>AscendingOrder</ins> - прямой, <ins>DescendingOrder</ins> - обратный).
  ```python
      def sort(self, index):
        if self.last_sorted_column == index:
            self.sort_order = (
                QtCore.Qt.SortOrder.DescendingOrder
                if self.sort_order == QtCore.Qt.SortOrder.AscendingOrder
                else QtCore.Qt.SortOrder.AscendingOrder
            )
        else:
            self.sort_order = QtCore.Qt.SortOrder.AscendingOrder
            self.last_sorted_column = index

        reverse = self.sort_order == QtCore.Qt.SortOrder.DescendingOrder

        if index == 1:
            self.data.sort(key=lambda row: QtCore.QDate.fromString(row[1], "yyyy-MM-dd"), reverse=reverse)
        elif index == 4:
            priority_order = {"Hard": 1, "Medium": 2, "Lite": 3}
            self.data.sort(key=lambda row: priority_order.get(row[4], 99), reverse=reverse)

        self.show_in_table()
  ```

### Статистика
- Анализирует задачи из базы данных и выводит в виде счётчика
  ```python
      def statistics(self):
        completed_count = self.cur.execute('''SELECT COUNT(*) FROM Mark WHERE is_done = "YES"''').fetchone()[0]
        active_count = self.cur.execute('''SELECT COUNT(*) FROM Mark WHERE is_done = "NO"''').fetchone()[0]
        self.ui.count_active.setText(str(active_count))
        self.ui.count_nonactive.setText(str(completed_count))
  ```
### Цветное оформление календаря, исходя из задач запланированных на определенную дату
- Анализирует задачи из бызы данных и перекращивает ячейки дат в зависимости от важности событий.
  ```python
    def update_date_colors(self):
        self.reset_calendar()

        self.cur.execute("SELECT data, priority FROM Mark")
        tasks = self.cur.fetchall()

        date_priorities = {}

        for task in tasks:
            date_str, priority = task
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            if date in date_priorities:
                date_priorities[date].add(priority)
            else:
                date_priorities[date] = {priority}
        for date, priorities in date_priorities.items():
            format = QTextCharFormat()

            if "Hard" in priorities:
                format.setBackground(QColor(255, 0, 0))
            elif "Medium" in priorities:
                format.setBackground(QColor(255, 255, 0))
            elif "Lite" in priorities:
                format.setBackground(QColor(0, 255, 0))
            self.ui.calendarWidget.setDateTextFormat(date, format)
  ```
- Обновляет календарь с помощью встроенного обнуления.
  ``` python
    def reset_calendar(self):
        self.ui.calendarWidget.setDateTextFormat(QDate(), QTextCharFormat())
  ```

### Примитивное уведомление
- Уведомляет при открытии программы, если существуют задачи в течении ближайших 24 часов(используется доп библиотека **pleyr**).
  ```python
    def check_nearest_tasks(self):
        current_datetime = QDateTime.currentDateTime()
        nearest_tasks = self.cur.execute('''
            SELECT id, data, time, content, priority 
            FROM Mark 
            WHERE datetime(data || " " || time) BETWEEN ? AND ?
        ''', (
            current_datetime.toString("yyyy-MM-dd HH:mm:ss"),
            (current_datetime.addSecs(24 * 60 * 60)).toString("yyyy-MM-dd HH:mm:ss")
        )).fetchall()
        if nearest_tasks:
            task_list = "\n".join([f"{task[3]} ({task[1]} {task[2]})" for task in nearest_tasks])
            notification.notify(
                title="Ближайшие задачи",
                message=task_list,
                timeout=15
            )
  ```
  ### Горячие клавиши
  - ```ALT + A``` - добавление задачи
  - ```ALT + D``` - удаление задачи
  - ```ALT + S``` - поиск задач
  - ```ALT + SHIFT + D``` - удаление выполненных задач
 ```python
    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.AltModifier:
            if event.key() == Qt.Key.Key_A:
                self.combo = True
                self.open_dialog_window()
            if event.key() == Qt.Key.Key_D:
                self.delete_mark()
            if event.key() == Qt.Key.Key_S:
                self.open_search_dialog()
        elif event.modifiers() == (Qt.KeyboardModifier.AltModifier | Qt.KeyboardModifier.ShiftModifier):
            if event.key() == Qt.Key.Key_D:
                self.delete_completed_tasks()

```
---

## Структура проекта

**Как PyCharm проект**

```
TaskScheduler/
│
├── main.py               # Главный файл для запуска приложения
├── plan.ui               # UI-файл главного окна (Qt Designer)
├── new_edit.ui           # UI-файл диалогового окна редактирования/создания задачи
├── Data_mark.sqlite      # База данных (создается автоматически, если отсутствует)
├── Icons                 # Иконки для кнопок
└── README.md             # Документация проекта
```

**Как цельное приложение**
```
TaskScheduler/
│
├── build                 # Папка с необходимыми для запуска файлами
├── dist                  # Папка с exe файлом через который происходит запуск программы
└── README.md             # Документация проекта
```
---

## Планы на будущее

- Добавить возможность экспорта задач в формате CSV или JSON.
- Улучшить систему уведомлений.
- Добавть изменение стиля оформления.
- Оптимизация кода.

---
