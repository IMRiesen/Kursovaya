import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import pymysql


class AdminWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Пользователи и роли")
        self.setFixedSize(800, 600)

        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        screen_center = screen_geometry.center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

        layout = QtWidgets.QVBoxLayout(self)

        search_layout = QtWidgets.QGridLayout()

        self.username_label = QtWidgets.QLabel("Имя пользователя:")
        self.username_input = QtWidgets.QLineEdit()
        self.username_search_button = QtWidgets.QPushButton("Найти")
        self.username_search_button.clicked.connect(self.search_by_username)

        self.role_label = QtWidgets.QLabel("Роль:")
        self.role_input = QtWidgets.QLineEdit()
        self.role_search_button = QtWidgets.QPushButton("Найти")
        self.role_search_button.clicked.connect(self.search_by_role)

        search_layout.addWidget(self.username_label, 0, 0)
        search_layout.addWidget(self.username_input, 0, 1)
        search_layout.addWidget(self.username_search_button, 0, 2)

        search_layout.addWidget(self.role_label, 1, 0)
        search_layout.addWidget(self.role_input, 1, 1)
        search_layout.addWidget(self.role_search_button, 1, 2)

        layout.addLayout(search_layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Пользователь", "Роль", "Дата создания", "Действия"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        layout.addWidget(self.table)

        self.back_button = QtWidgets.QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.load_all_users()

    def load_all_users(self):
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT username, role, created_at FROM users")
                results = cursor.fetchall()

                self.table.setRowCount(0)
                for row_number, row_data in enumerate(results):
                    self.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

                    delete_button = QtWidgets.QPushButton("Удалить")
                    delete_button.clicked.connect(lambda _, row=row_number: self.delete_user(row))
                    self.table.setCellWidget(row_number, 3, delete_button)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")
        finally:
            connection.close()

    def search_by_username(self):
        username = self.username_input.text()
        self.search_users(username=username)

    def search_by_role(self):
        role = self.role_input.text()
        self.search_users(role=role)

    def search_users(self, username=None, role=None):
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )

        try:
            with connection.cursor() as cursor:
                query = "SELECT username, role, created_at FROM users WHERE 1=1"
                params = []

                if username:
                    query += " AND username LIKE %s"
                    params.append(f"%{username}%")
                if role:
                    query += " AND role LIKE %s"
                    params.append(f"%{role}%")

                cursor.execute(query, tuple(params))
                results = cursor.fetchall()

                self.table.setRowCount(0)
                for row_number, row_data in enumerate(results):
                    self.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

                    delete_button = QtWidgets.QPushButton("Удалить")
                    delete_button.clicked.connect(lambda _, row=row_number: self.delete_user(row))
                    self.table.setCellWidget(row_number, 3, delete_button)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при поиске: {e}")
        finally:
            connection.close()

    def delete_user(self, row):
        username = self.table.item(row, 0).text()

        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE username = %s", (username,))
                connection.commit()

                QtWidgets.QMessageBox.information(self, "Успех", f"Пользователь '{username}' успешно удалён!")
                self.load_all_users()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось удалить пользователя: {e}")
        finally:
            connection.close()

    def go_back(self):
        self.main_window.show()
        self.close()

class ReportsWindow(QtWidgets.QWidget):
    def __init__(self, procurement_window):
        super().__init__()

        self.procurement_window = procurement_window
        self.setWindowTitle("Отчёты")
        self.setFixedSize(800, 600)

        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        screen_center = screen_geometry.center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

        layout = QtWidgets.QVBoxLayout(self)

        self.report_type_label = QtWidgets.QLabel("Выбор отчёта:")
        self.report_type_combobox = QtWidgets.QComboBox()

        self.load_report_types()

        self.report_type_combobox.currentIndexChanged.connect(self.on_report_type_change)

        layout.addWidget(self.report_type_label)
        layout.addWidget(self.report_type_combobox)

        self.period_label = QtWidgets.QLabel("Период:")
        self.start_date = QtWidgets.QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("yyyy-MM-dd")

        # Устанавливаем начало периода на 2024-12-01
        self.start_date.setDate(QtCore.QDate(2024, 12, 1))

        self.end_date = QtWidgets.QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDisplayFormat("yyyy-MM-dd")

        # Устанавливаем конец периода на 2024-12-07
        self.end_date.setDate(QtCore.QDate(2024, 12, 7))

        layout.addWidget(self.period_label)
        layout.addWidget(self.start_date)
        layout.addWidget(self.end_date)

        # Кнопка для формирования отчёта
        self.generate_report_button = QtWidgets.QPushButton("Сформировать отчёт")
        self.generate_report_button.clicked.connect(self.generate_report)
        layout.addWidget(self.generate_report_button)

        # Место для отображения отчёта
        self.report_table = QtWidgets.QTableWidget()
        layout.addWidget(self.report_table)

        self.back_button = QtWidgets.QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

    def load_report_types(self):
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, report_name FROM report_types")
                report_types = cursor.fetchall()

                for report_type in report_types:
                    self.report_type_combobox.addItem(report_type[1], userData=report_type[0])
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке типов отчётов: {e}")
        finally:
            connection.close()

    def on_report_type_change(self):
        pass

    def generate_report(self):
        report_type_id = self.report_type_combobox.currentData()
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")

        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(""" 
                    SELECT r.date, r.material, r.quantity, r.status
                    FROM reports r
                    WHERE r.report_type_id = %s AND r.date BETWEEN %s AND %s
                    ORDER BY r.date
                """, (report_type_id, start_date, end_date))

                results = cursor.fetchall()

                self.report_table.setRowCount(0)
                self.report_table.setColumnCount(4)
                self.report_table.setHorizontalHeaderLabels(["Дата", "Сырьё", "Количество", "Статус"])

                header = self.report_table.horizontalHeader()
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
                header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
                header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

                for row_number, row_data in enumerate(results):
                    self.report_table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.report_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при формировании отчёта: {e}")
        finally:
            connection.close()

    def go_back(self):
        self.procurement_window.show()
        self.close()

class QualityControlWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setWindowTitle("Контроль качества")
        self.setFixedSize(800, 600)

        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        screen_center = screen_geometry.center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

        layout = QtWidgets.QVBoxLayout(self)

        search_layout = QtWidgets.QGridLayout()

        self.material_label = QtWidgets.QLabel("Сырье:")
        self.material_input = QtWidgets.QLineEdit()
        self.material_search_button = QtWidgets.QPushButton("Найти")
        self.material_search_button.clicked.connect(self.search_by_material)

        self.batch_label = QtWidgets.QLabel("Партия:")
        self.batch_input = QtWidgets.QLineEdit()
        self.batch_search_button = QtWidgets.QPushButton("Найти")
        self.batch_search_button.clicked.connect(self.search_by_batch)

        search_layout.addWidget(self.material_label, 0, 0)
        search_layout.addWidget(self.material_input, 0, 1)
        search_layout.addWidget(self.material_search_button, 0, 2)

        search_layout.addWidget(self.batch_label, 1, 0)
        search_layout.addWidget(self.batch_input, 1, 1)
        search_layout.addWidget(self.batch_search_button, 1, 2)

        layout.addLayout(search_layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Сырье", "Партия", "Тип теста", "Результат", "Дата"])

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        layout.addWidget(self.table)

        button_layout = QtWidgets.QHBoxLayout()
        self.new_test_button = QtWidgets.QPushButton("Новое тестирование")
        self.back_button = QtWidgets.QPushButton("Назад")

        self.new_test_button.clicked.connect(self.open_new_test_window)
        self.back_button.clicked.connect(self.go_back)

        button_layout.addWidget(self.new_test_button)
        button_layout.addWidget(self.back_button)

        layout.addLayout(button_layout)

        self.load_quality_tests()

    def load_quality_tests(self):
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT m.name, b.name, qt.test_type, qt.test_result, qt.test_date
                    FROM quality_tests qt
                    JOIN batches b ON qt.batch_id = b.id
                    JOIN materials m ON qt.material_id = m.id
                    ORDER BY qt.test_date DESC
                """)
                results = cursor.fetchall()

                self.table.setRowCount(0)
                for row_number, row_data in enumerate(results):
                    self.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить тесты: {e}")
        finally:
            connection.close()

    def search_by_material(self):
        material_name = self.material_input.text()
        self._search_tests("m.name LIKE %s", ('%' + material_name + '%',))

    def search_by_batch(self):
        batch_name = self.batch_input.text()
        self._search_tests("b.name LIKE %s", ('%' + batch_name + '%',))

    def _search_tests(self, condition, params):
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )
        try:
            with connection.cursor() as cursor:
                query = f"""
                    SELECT m.name, b.name, qt.test_type, qt.test_result, qt.test_date
                    FROM quality_tests qt
                    JOIN batches b ON qt.batch_id = b.id
                    JOIN materials m ON qt.material_id = m.id
                    WHERE {condition}
                """
                cursor.execute(query, params)
                results = cursor.fetchall()

                self.table.setRowCount(0)
                for row_number, row_data in enumerate(results):
                    self.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при поиске: {e}")
        finally:
            connection.close()

    def open_new_test_window(self):
        try:
            if hasattr(self, 'new_test_window') and self.new_test_window is not None:
                self.new_test_window.raise_()
                self.new_test_window.activateWindow()
            else:
                self.new_test_window = NewTestWindow(self)
                self.new_test_window.show()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при открытии окна: {e}")

    def go_back(self):
        self.main_window.show()
        self.close()

class NewTestWindow(QtWidgets.QWidget):
    def __init__(self, quality_control_window):
        super().__init__()

        self.quality_control_window = quality_control_window
        self.setWindowTitle("Новое тестирование")
        self.setFixedSize(600, 400)

        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        screen_center = screen_geometry.center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

        layout = QtWidgets.QVBoxLayout(self)

        form_layout = QtWidgets.QFormLayout()

        self.material_input = QtWidgets.QComboBox()
        self.material_input.setEditable(False)
        self.material_input.addItem("Выберите сырье")
        self.load_materials()

        self.batch_input = QtWidgets.QLineEdit()
        self.batch_input.setPlaceholderText("Например: 001")

        self.test_type_input = QtWidgets.QLineEdit()
        self.test_result_input = QtWidgets.QLineEdit()

        form_layout.addRow("Сырье:", self.material_input)
        form_layout.addRow("Партия:", self.batch_input)
        form_layout.addRow("Тип теста:", self.test_type_input)
        form_layout.addRow("Результат:", self.test_result_input)

        layout.addLayout(form_layout)

        button_layout = QtWidgets.QHBoxLayout()
        self.save_button = QtWidgets.QPushButton("Сохранить")
        self.cancel_button = QtWidgets.QPushButton("Отмена")

        self.save_button.clicked.connect(self.save_test)
        self.cancel_button.clicked.connect(self.close)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.material_input.currentIndexChanged.connect(self.update_batch_input)

    def update_batch_input(self):
        material_name = self.material_input.currentText()
        if material_name and material_name != "Выберите сырье":
            self.batch_input.setText(f"{material_name} 001")

    def load_materials(self):
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name FROM materials")
                materials = cursor.fetchall()

                for material in materials:
                    self.material_input.addItem(material[1], material[0])

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить сырье: {e}")
        finally:
            connection.close()

    def save_test(self):
        material_id = self.material_input.currentData()
        batch_number = self.batch_input.text().strip()
        test_type = self.test_type_input.text().strip()
        test_result = self.test_result_input.text().strip()

        if not material_id or not batch_number or not test_type or not test_result or self.material_input.currentText() == "Выберите сырье":
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Заполните все поля.")
            return

        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM batches WHERE name = %s AND material_id = %s",
                    (batch_number, material_id)
                )
                batch = cursor.fetchone()

                if not batch:
                    cursor.execute(
                        "INSERT INTO batches (name, material_id) VALUES (%s, %s)",
                        (batch_number, material_id)
                    )
                    connection.commit()
                    batch_id = cursor.lastrowid
                else:
                    batch_id = batch[0]

                cursor.execute(
                    "INSERT INTO quality_tests (batch_id, material_id, test_type, test_result, test_date) "
                    "VALUES (%s, %s, %s, %s, CURDATE())",
                    (batch_id, material_id, test_type, test_result)
                )
                connection.commit()

                QtWidgets.QMessageBox.information(self, "Успех", f"Тестирование сохранено для партии №: {batch_number}")

                if hasattr(self.quality_control_window, "load_quality_tests"):
                    self.quality_control_window.load_quality_tests()

                self.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить тестирование: {e}")
        finally:
            connection.close()

    def closeEvent(self, event):
        self.quality_control_window.new_test_window = None
        super().closeEvent(event)

class ProductionPlanWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("План производства")
        self.setFixedSize(800, 600)

        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        screen_center = screen_geometry.center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

        layout = QtWidgets.QVBoxLayout(self)

        self.product_dropdown = QtWidgets.QComboBox()
        self.load_products()

        self.production_date_input = QtWidgets.QDateEdit()
        self.production_date_input.setCalendarPopup(True)
        self.production_date_input.setDisplayFormat("yyyy-MM-dd")
        self.production_date_input.setDate(QtCore.QDate.currentDate())

        self.find_button = QtWidgets.QPushButton("Найти")
        self.find_button.clicked.connect(self.filter_production_plan)

        self.reset_button = QtWidgets.QPushButton("Сбросить фильтры")
        self.reset_button.clicked.connect(self.reset_filters)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Продукция:", self.product_dropdown)
        form_layout.addRow("Дата выпуска:", self.production_date_input)

        filter_button_layout = QtWidgets.QHBoxLayout()
        filter_button_layout.addWidget(self.find_button)
        filter_button_layout.addWidget(self.reset_button)

        layout.addLayout(form_layout)
        layout.addLayout(filter_button_layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Продукция", "Партия", "Сырье", "Потребность", "Дата выпуска"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.table)

        button_layout = QtWidgets.QHBoxLayout()
        self.add_product_button = QtWidgets.QPushButton("Добавить продукцию")
        self.back_button = QtWidgets.QPushButton("Назад")

        self.add_product_button.clicked.connect(self.open_create_batch_window)
        self.back_button.clicked.connect(self.go_back)

        button_layout.addWidget(self.add_product_button)
        button_layout.addWidget(self.back_button)

        layout.addLayout(button_layout)

        self.load_production_plan()

    def load_products(self):
        connection = pymysql.connect(host="localhost", user="root", password="12345", database="raw_materials")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name FROM products")
                for row in cursor.fetchall():
                    self.product_dropdown.addItem(row[1], row[0])
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки продукции: {e}")
        finally:
            connection.close()

    def load_production_plan(self, product_id=None, production_date=None):
        connection = pymysql.connect(host="localhost", user="root", password="12345", database="raw_materials")
        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT products.name, production_plans.batch_name, production_plans.raw_material,
                           production_plans.need_quantity, production_plans.production_date
                    FROM production_plans
                    INNER JOIN products ON production_plans.product_id = products.id
                """
                params = []
                if product_id or production_date:
                    query += " WHERE"
                    conditions = []
                    if product_id:
                        conditions.append(" products.id = %s")
                        params.append(product_id)
                    if production_date:
                        conditions.append(" production_plans.production_date = %s")
                        params.append(production_date)
                    query += " AND ".join(conditions)

                cursor.execute(query, params)
                rows = cursor.fetchall()
                self.table.setRowCount(0)
                for row in rows:
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)
                    for col, data in enumerate(row):
                        self.table.setItem(row_position, col, QtWidgets.QTableWidgetItem(str(data)))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки плана производства: {e}")
        finally:
            connection.close()

    def filter_production_plan(self):
        product_id = self.product_dropdown.currentData()
        production_date = self.production_date_input.date().toString("yyyy-MM-dd")
        self.load_production_plan(product_id=product_id, production_date=production_date)

    def reset_filters(self):
        self.product_dropdown.setCurrentIndex(0)
        self.production_date_input.setDate(QtCore.QDate.currentDate())
        self.load_production_plan()

    def open_create_batch_window(self):
        if not hasattr(self, 'create_batch_window') or not self.create_batch_window.isVisible():
            self.create_batch_window = self.CreateBatchWindow(self)
            self.create_batch_window.show()

    class CreateBatchWindow(QtWidgets.QWidget):
        def __init__(self, production_plan_window):
            super().__init__()
            self.production_plan_window = production_plan_window

            self.setWindowTitle("Создание партии")
            self.setFixedSize(600, 400)

            self.center_window()

            layout = QtWidgets.QVBoxLayout(self)

            form_layout = QtWidgets.QFormLayout()

            self.product_name_input = QtWidgets.QLineEdit()
            self.raw_material_input = QtWidgets.QLineEdit()

            self.need_quantity_layout = QtWidgets.QHBoxLayout()
            self.need_quantity_input = QtWidgets.QLineEdit()
            self.need_quantity_input.setFixedWidth(100)
            self.kg_label = QtWidgets.QLabel("кг")
            self.need_quantity_layout.addWidget(self.need_quantity_input)
            self.need_quantity_layout.addWidget(self.kg_label)

            self.production_date_input = QtWidgets.QDateEdit()
            self.production_date_input.setCalendarPopup(True)
            self.production_date_input.setDisplayFormat("yyyy-MM-dd")
            self.production_date_input.setFixedWidth(100)

            form_layout.addRow("Название продукции:", self.product_name_input)
            form_layout.addRow("Сырье:", self.raw_material_input)
            form_layout.addRow("Потребность:", self.need_quantity_layout)
            form_layout.addRow("Дата выпуска:", self.production_date_input)

            layout.addLayout(form_layout)

            button_layout = QtWidgets.QHBoxLayout()
            self.save_button = QtWidgets.QPushButton("Сохранить")
            self.cancel_button = QtWidgets.QPushButton("Отмена")

            self.save_button.clicked.connect(self.save_batch)
            self.cancel_button.clicked.connect(self.cancel_batch)

            button_layout.addWidget(self.save_button)
            button_layout.addWidget(self.cancel_button)

            layout.addLayout(button_layout)

        def center_window(self):
            screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
            screen_center = screen_geometry.center()
            window_geometry = self.frameGeometry()
            window_geometry.moveCenter(screen_center)
            self.move(window_geometry.topLeft())

        def save_batch(self):
            product_name = self.product_name_input.text()
            raw_material = self.raw_material_input.text()
            need_quantity = self.need_quantity_input.text()
            production_date = self.production_date_input.date().toString("yyyy-MM-dd")

            connection = pymysql.connect(host="localhost", user="root", password="12345", database="raw_materials")
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id FROM products WHERE name = %s", (product_name,))
                    product = cursor.fetchone()
                    if not product:
                        QtWidgets.QMessageBox.critical(self, "Ошибка", "Указанная продукция не найдена!")
                        return

                    product_id = product[0]

                    batch_name = f"{product_name} партия {product_id}"
                    cursor.execute(""" 
                        INSERT INTO production_plans (product_id, batch_name, raw_material, need_quantity, production_date)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (product_id, batch_name, raw_material, need_quantity, production_date))
                    connection.commit()

                    QtWidgets.QMessageBox.information(self, "Успех", "Партия успешно добавлена!")
                    self.production_plan_window.load_production_plan()
                    self.close()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении партии: {e}")
            finally:
                connection.close()

        def cancel_batch(self):
            self.close()

    def go_back(self):
        self.main_window.show()
        self.close()

class WarehouseWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setWindowTitle("Склад")
        self.setFixedSize(800, 600)

        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        screen_center = screen_geometry.center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

        layout = QtWidgets.QVBoxLayout(self)

        search_layout = QtWidgets.QGridLayout()

        self.material_label = QtWidgets.QLabel("Название сырья:")
        self.material_input = QtWidgets.QLineEdit()
        self.material_search_button = QtWidgets.QPushButton("Найти")
        self.material_search_button.clicked.connect(self.search_by_material)

        self.category_label = QtWidgets.QLabel("Категория:")
        self.category_input = QtWidgets.QLineEdit()
        self.category_search_button = QtWidgets.QPushButton("Найти")
        self.category_search_button.clicked.connect(self.search_by_category)

        search_layout.addWidget(self.material_label, 0, 0)
        search_layout.addWidget(self.material_input, 0, 1)
        search_layout.addWidget(self.material_search_button, 0, 2)

        search_layout.addWidget(self.category_label, 1, 0)
        search_layout.addWidget(self.category_input, 1, 1)
        search_layout.addWidget(self.category_search_button, 1, 2)

        layout.addLayout(search_layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Название", "Категория", "Единица измерения", "Количество", "Срок годности"])

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        layout.addWidget(self.table)

        button_layout = QtWidgets.QHBoxLayout()
        self.add_button = QtWidgets.QPushButton("Добавить сырьё")
        self.update_button = QtWidgets.QPushButton("Обновить количество")
        self.back_button = QtWidgets.QPushButton("Назад")

        self.add_button.clicked.connect(self.open_add_material_window)
        self.update_button.clicked.connect(self.open_update_material_window)
        self.back_button.clicked.connect(self.go_back)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.back_button)

        layout.addLayout(button_layout)

    def search_by_material(self):
        material_name = self.material_input.text()

        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT name, category, unit, quantity, shelf_life FROM raw_material WHERE name LIKE %s",
                    ('%' + material_name + '%',)
                )
                results = cursor.fetchall()

                self.table.setRowCount(0)
                for row_number, row_data in enumerate(results):
                    self.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при поиске: {e}")
        finally:
            connection.close()

    def search_by_category(self):
        category_name = self.category_input.text()

        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT name, category, unit, quantity, shelf_life FROM raw_material WHERE category LIKE %s",
                    ('%' + category_name + '%',)
                )
                results = cursor.fetchall()

                self.table.setRowCount(0)
                for row_number, row_data in enumerate(results):
                    self.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при поиске: {e}")
        finally:
            connection.close()

    def open_add_material_window(self):
        self.add_material_window = AddMaterialWindow(self)
        self.add_material_window.show()

    def open_update_material_window(self):
        self.update_material_window = UpdateMaterialWindow(self)
        self.update_material_window.show()

    def go_back(self):
        self.main_window.show()
        self.close()

    def refresh_table(self):
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name, category, unit, quantity, shelf_life FROM raw_material")
                results = cursor.fetchall()

                self.table.setRowCount(0)
                for row_number, row_data in enumerate(results):
                    self.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении таблицы: {e}")
        finally:
            connection.close()

    def open_add_material_window(self):
        self.add_material_window = AddMaterialWindow(self)
        self.add_material_window.show()

    def open_update_material_window(self):
        self.update_material_window = UpdateMaterialWindow(self)
        self.update_material_window.show()

    def go_back(self):
        self.main_window.show()
        self.close()

class AddMaterialWindow(QtWidgets.QWidget):
    def __init__(self, warehouse_window):
        super().__init__()

        self.warehouse_window = warehouse_window
        self.setWindowTitle("Добавить сырье на склад")
        self.setFixedSize(600, 400)

        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        screen_center = screen_geometry.center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

        layout = QtWidgets.QVBoxLayout(self)

        form_layout = QtWidgets.QFormLayout()

        self.name_input = QtWidgets.QLineEdit()
        self.category_input = QtWidgets.QLineEdit()

        self.unit_input = QtWidgets.QLineEdit()
        self.unit_input.setFixedWidth(150)

        self.quantity_input = QtWidgets.QLineEdit()
        self.quantity_input.setFixedWidth(150)

        self.shelf_life_input = QtWidgets.QLineEdit()
        self.shelf_life_input.setFixedWidth(150)

        form_layout.addRow("Название сырья:", self.name_input)
        form_layout.addRow("Категория:", self.category_input)
        form_layout.addRow("Единица измерения:", self.unit_input)
        form_layout.addRow("Количество:", self.quantity_input)
        form_layout.addRow("Срок хранения (дни):", self.shelf_life_input)

        layout.addLayout(form_layout)

        button_layout = QtWidgets.QHBoxLayout()
        self.save_button = QtWidgets.QPushButton("Сохранить")
        self.cancel_button = QtWidgets.QPushButton("Отмена")

        self.save_button.clicked.connect(self.save_material)
        self.cancel_button.clicked.connect(self.cancel_material)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def save_material(self):
        name = self.name_input.text()
        category = self.category_input.text()
        unit = self.unit_input.text()
        quantity = self.quantity_input.text()
        shelf_life = self.shelf_life_input.text()

        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO raw_material (name, category, unit, quantity, shelf_life) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (name, category, unit, quantity, shelf_life)
                )
                connection.commit()
                QtWidgets.QMessageBox.information(self, "Успех", "Сырье успешно добавлено!")
                self.warehouse_window.refresh_table()
                self.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении сырья: {e}")
        finally:
            connection.close()

    def cancel_material(self):
        self.close()

class UpdateMaterialWindow(QtWidgets.QWidget):
    def __init__(self, warehouse_window):
        super().__init__()

        self.warehouse_window = warehouse_window
        self.setWindowTitle("Обновить количество сырья")
        self.setFixedSize(600, 400)

        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        screen_center = screen_geometry.center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

        layout = QtWidgets.QVBoxLayout(self)

        form_layout = QtWidgets.QFormLayout()

        self.name_input = QtWidgets.QLineEdit()
        self.quantity_input = QtWidgets.QLineEdit()

        form_layout.addRow("Название сырья:", self.name_input)
        form_layout.addRow("Количество:", self.quantity_input)

        layout.addLayout(form_layout)

        button_layout = QtWidgets.QHBoxLayout()
        self.update_button = QtWidgets.QPushButton("Обновить")
        self.cancel_button = QtWidgets.QPushButton("Отмена")

        self.update_button.clicked.connect(self.update_material)
        self.cancel_button.clicked.connect(self.close)

        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def update_material(self):
        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()

        if not name or not quantity:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            quantity = float(quantity)
            if quantity <= 0:
                raise ValueError("Количество должно быть положительным.")
        except ValueError as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Некорректное количество: {e}")
            return

        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE raw_material SET quantity = quantity + %s WHERE name = %s",
                    (quantity, name)
                )
                if cursor.rowcount == 0:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Сырье с указанным названием не найдено.")
                else:
                    connection.commit()
                    QtWidgets.QMessageBox.information(self, "Успех", "Количество сырья успешно обновлено!")
                    self.warehouse_window.refresh_table()
                    self.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении количества сырья: {e}")
        finally:
            connection.close()

class ProcurementWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setWindowTitle("Закупки")
        self.setFixedSize(800, 600)

        self.center_window()

        layout = QtWidgets.QVBoxLayout(self)

        search_layout = QtWidgets.QGridLayout()

        self.supplier_label = QtWidgets.QLabel("Поставщик:")
        self.supplier_input = QtWidgets.QLineEdit()
        self.supplier_search_button = QtWidgets.QPushButton("Найти")
        self.supplier_search_button.clicked.connect(self.search_by_supplier)

        self.material_label = QtWidgets.QLabel("Название сырья:")
        self.material_input = QtWidgets.QLineEdit()
        self.material_search_button = QtWidgets.QPushButton("Найти")
        self.material_search_button.clicked.connect(self.search_by_material)

        search_layout.addWidget(self.supplier_label, 0, 0)
        search_layout.addWidget(self.supplier_input, 0, 1)
        search_layout.addWidget(self.supplier_search_button, 0, 2)

        search_layout.addWidget(self.material_label, 1, 0)
        search_layout.addWidget(self.material_input, 1, 1)
        search_layout.addWidget(self.material_search_button, 1, 2)

        layout.addLayout(search_layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Поставщик", "Сырье", "Количество", "Дата поставки", "Цена за единицу в рублях"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        layout.addWidget(self.table)

        button_layout = QtWidgets.QHBoxLayout()
        self.create_order_button = QtWidgets.QPushButton("Создать заявку")
        self.history_button = QtWidgets.QPushButton("История заказов")
        self.back_button = QtWidgets.QPushButton("Назад")

        self.create_order_button.clicked.connect(self.open_create_order_window)
        self.history_button.clicked.connect(self.open_history_window)
        self.back_button.clicked.connect(self.go_back)

        button_layout.addWidget(self.create_order_button)
        button_layout.addWidget(self.history_button)
        button_layout.addWidget(self.back_button)

        layout.addLayout(button_layout)

    def center_window(self):
        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        screen_center = screen_geometry.center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

    def search_by_supplier(self):
        supplier_name = self.supplier_input.text()

        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT s.name, p.raw_material_name, p.quantity, p.delivery_date, p.unit_price
                    FROM purchases p
                    JOIN suppliers s ON p.supplier_id = s.id
                    WHERE s.name LIKE %s
                    """, ('%' + supplier_name + '%',)
                )
                results = cursor.fetchall()

                results = self.sort_supplier_data(results)

                self.table.setRowCount(0)
                for row_number, row_data in enumerate(results):
                    self.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при поиске: {e}")
        finally:
            connection.close()

    def search_by_material(self):
        material_name = self.material_input.text()

        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT s.name, p.raw_material_name, p.quantity, p.delivery_date, p.unit_price
                    FROM purchases p
                    JOIN suppliers s ON p.supplier_id = s.id
                    WHERE p.raw_material_name LIKE %s
                    """, ('%' + material_name + '%',)
                )
                results = cursor.fetchall()

                results = self.sort_supplier_data(results)

                self.table.setRowCount(0)
                for row_number, row_data in enumerate(results):
                    self.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при поиске: {e}")
        finally:
            connection.close()

    def sort_supplier_data(self, data):
        sorted_data = [row for row in data if row[1] != "Карамель"]
        caramel_row = next((row for row in data if row[1] == "Карамель"), None)
        if caramel_row:
            sorted_data.insert(2, caramel_row)
        return sorted_data

    def open_create_order_window(self):
        self.create_order_window = CreateOrderWindow(self)
        self.create_order_window.show()

    def open_history_window(self):
        self.history_window = OrderHistoryWindow(self)
        self.history_window.show()
        self.close()

    def go_back(self):
        self.main_window.show()
        self.close()

class OrderHistoryWindow(QtWidgets.QWidget):
    def __init__(self, procurement_window):
        super().__init__()

        self.procurement_window = procurement_window
        self.setWindowTitle("История заказов")
        self.setFixedSize(800, 600)

        self.center_window()

        layout = QtWidgets.QVBoxLayout(self)

        search_layout = QtWidgets.QGridLayout()

        self.supplier_label = QtWidgets.QLabel("Поставщик:")
        self.supplier_input = QtWidgets.QLineEdit()
        self.supplier_search_button = QtWidgets.QPushButton("Найти")
        self.supplier_search_button.clicked.connect(self.search_by_supplier)

        search_layout.addWidget(self.supplier_label, 0, 0)
        search_layout.addWidget(self.supplier_input, 0, 1)
        search_layout.addWidget(self.supplier_search_button, 0, 2)

        layout.addLayout(search_layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Поставщик", "Сырье", "Количество", "Дата поставки"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        layout.addWidget(self.table)

        button_layout = QtWidgets.QHBoxLayout()
        self.back_button = QtWidgets.QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        button_layout.addWidget(self.back_button)
        layout.addLayout(button_layout)

    def center_window(self):
        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        screen_center = screen_geometry.center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

    def search_by_supplier(self):
        supplier_name = self.supplier_input.text()
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT s.name, p.raw_material_name, p.quantity, p.delivery_date
                    FROM purchases p
                    JOIN suppliers s ON p.supplier_id = s.id
                    WHERE s.name LIKE %s
                    """, ('%' + supplier_name + '%',)
                )
                results = cursor.fetchall()

                self.table.setRowCount(0)
                for row_number, row_data in enumerate(results):
                    self.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при поиске: {e}")
        finally:
            connection.close()

    def go_back(self):
        self.procurement_window.show()
        self.close()

class CreateOrderWindow(QtWidgets.QWidget):
    def __init__(self, procurement_window):
        super().__init__()

        self.procurement_window = procurement_window
        self.setWindowTitle("Создание заявки на закупку")
        self.setFixedSize(600, 400)

        self.center_window()

        layout = QtWidgets.QVBoxLayout(self)

        form_layout = QtWidgets.QFormLayout()

        self.supplier_input = QtWidgets.QLineEdit()
        self.material_input = QtWidgets.QLineEdit()

        self.quantity_layout = QtWidgets.QHBoxLayout()
        self.quantity_input = QtWidgets.QLineEdit()
        self.quantity_input.setMaxLength(10)
        self.quantity_input.setFixedWidth(100)
        self.kg_label = QtWidgets.QLabel("кг")
        self.quantity_layout.addWidget(self.quantity_input)
        self.quantity_layout.addWidget(self.kg_label)

        self.date_input = QtWidgets.QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setFixedWidth(100)

        self.price_layout = QtWidgets.QHBoxLayout()
        self.price_input = QtWidgets.QLineEdit()
        self.price_input.setMaxLength(10)
        self.price_input.setFixedWidth(100)
        self.rub_label = QtWidgets.QLabel("руб.")
        self.price_layout.addWidget(self.price_input)
        self.price_layout.addWidget(self.rub_label)

        form_layout.addRow("Поставщик:", self.supplier_input)
        form_layout.addRow("Название сырья:", self.material_input)
        form_layout.addRow("Количество:", self.quantity_layout)
        form_layout.addRow("Дата поставки:", self.date_input)
        form_layout.addRow("Цена за единицу:", self.price_layout)

        layout.addLayout(form_layout)

        button_layout = QtWidgets.QHBoxLayout()
        self.save_button = QtWidgets.QPushButton("Сохранить")
        self.back_button = QtWidgets.QPushButton("Назад")

        self.save_button.clicked.connect(self.save_order)
        self.back_button.clicked.connect(self.go_back)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.back_button)

        layout.addLayout(button_layout)

    def center_window(self):
        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        screen_center = screen_geometry.center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

    def save_order(self):
        supplier_name = self.supplier_input.text()
        material_name = self.material_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()
        delivery_date = self.date_input.date().toString("yyyy-MM-dd")

        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="raw_materials"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM suppliers WHERE name = %s", (supplier_name,))
                supplier = cursor.fetchone()

                if not supplier:
                    cursor.execute("INSERT INTO suppliers (name) VALUES (%s)", (supplier_name,))
                    connection.commit()
                    supplier_id = cursor.lastrowid
                else:
                    supplier_id = supplier[0]

                cursor.execute(
                    "INSERT INTO purchases (supplier_id, raw_material_name, quantity, unit_price, delivery_date) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (supplier_id, material_name, quantity, price, delivery_date)
                )
                connection.commit()

                QtWidgets.QMessageBox.information(self, "Успех", "Заявка успешно сохранена!")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить заявку: {e}")

        finally:
            connection.close()

    def go_back(self):
        """Закрытие окна и возврат к предыдущему."""
        self.close()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Учет сырья на Кондитерской фабрике")
        self.setFixedSize(800, 600)

        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        screen_center = screen_geometry.center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        self.title_label = QtWidgets.QLabel("Учет сырья на кондитерской фабрике", central_widget)
        self.title_label.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Bold))
        self.title_label.move(180, 50)
        self.title_label.adjustSize()

        buttons_layout = QtWidgets.QGridLayout()
        self.create_button("Закупки", buttons_layout, 0, 0, self.open_procurement, 300, 100)
        self.create_button("Контроль качества", buttons_layout, 0, 1, self.open_quality_control, 300, 100)
        self.create_button("Склад", buttons_layout, 1, 0, self.open_warehouse, 300, 100)
        self.create_button("Отчеты", buttons_layout, 1, 1, self.open_reports, 300, 100)
        self.create_button("Производство", buttons_layout, 2, 0, self.open_production, 300, 100)
        self.create_button("Администрирование", buttons_layout, 2, 1, self.open_administration, 300, 100)

        layout.addLayout(buttons_layout)

        self.exit_button = QtWidgets.QPushButton("Выход")
        self.exit_button.setFont(QtGui.QFont("Arial", 16))
        self.exit_button.setFixedSize(150, 50)
        self.exit_button.clicked.connect(self.close)

        self.exit_button.move(600, 500)
        self.exit_button.setParent(central_widget)
        self.exit_button.show()

    def create_button(self, text, layout, row, col, action, width, height):
        button = QtWidgets.QPushButton(text)
        button.setFont(QtGui.QFont("Arial", 16))
        button.setFixedSize(width, height)
        button.clicked.connect(action)
        layout.addWidget(button, row, col)

    def open_procurement(self):
        self.procurement_window = ProcurementWindow(self)
        self.procurement_window.show()
        self.hide()

    def open_quality_control(self):
        self.quality_control_window = QualityControlWindow(self)
        self.quality_control_window.show()
        self.hide()

    def open_warehouse(self):
        self.warehouse_window = WarehouseWindow(self)
        self.warehouse_window.show()
        self.hide()

    def open_reports(self):
        self.reports_window = ReportsWindow(self)
        self.reports_window.show()
        self.hide()

    def open_production(self):
        self.production_window = ProductionPlanWindow(self)
        self.production_window.show()
        self.hide()

    def open_administration(self):
        self.admin_window = AdminWindow(self)
        self.admin_window.show()
        self.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())


