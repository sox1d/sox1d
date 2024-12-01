import sys
import sqlite3
from plyer import notification

from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QTableWidgetItem, QStyledItemDelegate
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QDate, QDateTime, QPropertyAnimation
from PyQt6.QtGui import QColor, QTextCharFormat, QIcon
from plan import Ui_MainWindow
from new_edit import new_delete_Dialog, search_Dialog


class MyWidget(QMainWindow):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.deleted = False
        self.show_all_bool = False
        self.last_sorted_column = -1

        self.con = sqlite3.connect('Data_mark.sqlite')
        self.cur = self.con.cursor()

        self.initialize_database()

        self.ui.newButton.clicked.connect(self.open_dialog_window)
        self.ui.changeButton.clicked.connect(self.open_dialog_window)
        self.ui.deleteButton.clicked.connect(self.delete_mark)
        self.ui.all_Button.clicked.connect(self.show_all)
        self.ui.delete_completed_Button.clicked.connect(self.delete_completed_tasks)
        self.ui.calendarWidget.activated.connect(self.show_mark)
        self.ui.saerch_Button.clicked.connect(self.open_search_dialog)
        self.ui.dataTable.cellDoubleClicked.connect(self.show_full_note)
        self.ui.dataTable.horizontalHeader().sectionClicked.connect(self.sort)
        self.statistics()
        self.check_nearest_tasks()
        self.update_date_colors()
        self.apply_stylesheet()

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

    def open_dialog_window(self):
        self.new_window = QDialog()
        self.ui_window = new_delete_Dialog()
        self.ui_window.setupUi(self.new_window)

        sender = self.sender()
        if sender == self.ui.newButton:
            self.ui_window.dateEdit.setDate(self.ui.calendarWidget.selectedDate())
            self.ui_window.applyButton.clicked.connect(self.add_new_mark)
            self.ui_window.dateEdit.hide()
        else:
            selected_row = self.ui.dataTable.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите задачу для изменения.")
                return

            task_id = int(self.ui.dataTable.item(selected_row, 0).text())
            task_data = self.cur.execute("SELECT * FROM Mark WHERE id = ?", (task_id,)).fetchone()

            if task_data:
                date_str, time_str, content, priority, is_done = task_data[1:6]
                date = QtCore.QDate.fromString(date_str, "yyyy-MM-dd")
                time = QtCore.QTime.fromString(time_str, "HH:mm:ss")

                self.ui_window.dateEdit.setDate(date)
                self.ui_window.timeEdit.setTime(time)
                self.ui_window.contentEdit.setPlainText(content)
                self.ui_window.priorityBox.setCurrentText(priority)
                self.current_task_id = task_id
                self.ui_window.applyButton.clicked.connect(self.change_mark)

        self.new_window.show()

    def open_search_dialog(self):
        self.search_dialog = QDialog()
        self.ui_search = search_Dialog()
        self.ui_search.setupUi(self.search_dialog)

        self.ui_search.searchButton.clicked.connect(self.perform_search)
        self.ui_search.cancelButton.clicked.connect(self.search_dialog.close)

        self.search_dialog.show()

    def apply_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                font-weight: bold;
            }
        """
                           )
        self.ui.newButton.setIcon(QIcon('icons/pencil.png'))
        self.ui.changeButton.setIcon(QIcon('icons/customize.png'))
        self.ui.deleteButton.setIcon(QIcon('icons/trash.png'))
        self.ui.deleteButton.setIcon(QIcon('icons/folder-delete.png'))
        self.ui.saerch_Button.setIcon(QIcon('icons/search1.png'))
        self.ui.all_Button.setIcon(QIcon('icons/all.png'))
        self.ui.delete_completed_Button.setIcon(QIcon('icons/completed.png'))

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

    def show_full_note(self, row, column):
        if column == 3:
            full_text = self.ui.dataTable.item(row, column).text()
            QMessageBox.information(self, "Полный текст заметки", full_text)

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

    def show_all(self):
        self.data = self.cur.execute('SELECT * FROM Mark').fetchall()
        self.show_in_table()
        self.show_all_bool = True
        self.update_date_colors()

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

    def statistics(self):
        completed_count = self.cur.execute('''SELECT COUNT(*) FROM Mark WHERE is_done = "YES"''').fetchone()[0]
        active_count = self.cur.execute('''SELECT COUNT(*) FROM Mark WHERE is_done = "NO"''').fetchone()[0]
        self.ui.count_active.setText(str(active_count))
        self.ui.count_nonactive.setText(str(completed_count))

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

    def reset_calendar(self):
        self.ui.calendarWidget.setDateTextFormat(QDate(), QTextCharFormat())

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
