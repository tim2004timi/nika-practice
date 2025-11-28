import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                               QListWidget, QListWidgetItem, QFormLayout, 
                               QMessageBox, QComboBox, QSpinBox, QDoubleSpinBox,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QMenuBar, QMenu, QFrame, QScrollArea, QStackedWidget)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon
from datetime import datetime, date, timedelta
from api_client import APIClient, APIError
from styles import get_stylesheet, PRIMARY, PRIMARY_FOREGROUND, MUTED_FOREGROUND, CARD, BORDER


class LoginPage(QWidget):
    def __init__(self, api_client: APIClient, on_login_success):
        super().__init__()
        self.api_client = api_client
        self.on_login_success = on_login_success
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        
        # Заголовок
        title = QLabel("Николь Бьюти")
        title.setProperty("labelStyle", "h1")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {PRIMARY};")
        
        subtitle = QLabel("Добро пожаловать")
        subtitle.setProperty("labelStyle", "muted")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px;")
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        # Форма входа
        form_layout = QFormLayout()
        form_layout.setSpacing(8)
        
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        form_layout.addRow("Логин:", self.login_input)
        form_layout.addRow("Пароль:", self.password_input)
        
        login_btn = QPushButton("Войти")
        login_btn.setProperty("buttonStyle", "default")
        login_btn.clicked.connect(self.handle_login)
        
        register_link = QPushButton("Регистрация")
        register_link.setProperty("buttonStyle", "ghost")
        register_link.setStyleSheet("font-size: 14px;")
        register_link.clicked.connect(lambda: self.on_login_success("register"))
        
        layout.addLayout(title_layout)
        layout.addLayout(form_layout)
        layout.addWidget(login_btn)
        layout.addWidget(register_link)
        
        self.setLayout(layout)
    
    def handle_login(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()
        
        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        
        try:
            result = self.api_client.login(login, password)
            user = result["user"]
            
            # Проверяем, что это мастер
            if user["role"] == "CLIENT":
                QMessageBox.warning(self, "Ошибка", "Это приложение только для мастеров")
                self.api_client.logout()
                return
            
            self.on_login_success("home", user)
        except APIError as e:
            QMessageBox.warning(self, "Ошибка", e.message)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")


class RegisterPage(QWidget):
    def __init__(self, api_client: APIClient, on_register_success):
        super().__init__()
        self.api_client = api_client
        self.on_register_success = on_register_success
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        
        # Заголовок
        title = QLabel("Николь Бьюти")
        title.setProperty("labelStyle", "h1")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {PRIMARY};")
        
        subtitle = QLabel("Регистрация")
        subtitle.setProperty("labelStyle", "muted")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px;")
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        # Форма регистрации
        form_layout = QFormLayout()
        form_layout.setSpacing(6)
        
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        
        self.full_name_input = QLineEdit()
        self.full_name_input.setPlaceholderText("ФИО")
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("+7")
        self.phone_input.setText("+7")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.password_confirm_input = QLineEdit()
        self.password_confirm_input.setPlaceholderText("Повторите пароль")
        self.password_confirm_input.setEchoMode(QLineEdit.Password)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Визажист", "Маникюрист", "Стилист", "Бровист"])
        
        form_layout.addRow("Логин:", self.login_input)
        form_layout.addRow("ФИО:", self.full_name_input)
        form_layout.addRow("Телефон:", self.phone_input)
        form_layout.addRow("Пароль:", self.password_input)
        form_layout.addRow("Повторите пароль:", self.password_confirm_input)
        form_layout.addRow("Роль:", self.role_combo)
        
        register_btn = QPushButton("Зарегистрироваться")
        register_btn.setProperty("buttonStyle", "default")
        register_btn.clicked.connect(self.handle_register)
        
        login_link = QPushButton("Вход")
        login_link.setProperty("buttonStyle", "ghost")
        login_link.setStyleSheet("font-size: 14px;")
        login_link.clicked.connect(lambda: self.on_register_success("login"))
        
        layout.addLayout(title_layout)
        layout.addLayout(form_layout)
        layout.addWidget(register_btn)
        layout.addWidget(login_link)
        
        self.setLayout(layout)
    
    def handle_register(self):
        login = self.login_input.text().strip()
        full_name = self.full_name_input.text().strip()
        phone = self.phone_input.text().strip()
        password = self.password_input.text().strip()
        password_confirm = self.password_confirm_input.text().strip()
        
        if not all([login, full_name, phone, password, password_confirm]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        
        if not phone.startswith("+7"):
            QMessageBox.warning(self, "Ошибка", "Телефон должен начинаться с +7")
            return
        
        if password != password_confirm:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return
        
        role_map = {
            "Визажист": "VIZAZHIST",
            "Маникюрист": "MANICURIST",
            "Стилист": "STYLIST",
            "Бровист": "BROWIST"
        }
        
        role = role_map[self.role_combo.currentText()]
        
        try:
            result = self.api_client.register(login, password, full_name, phone, role)
            user = result["user"]
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно")
            self.on_register_success("home", user)
        except APIError as e:
            QMessageBox.warning(self, "Ошибка", e.message)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")


class HomePage(QWidget):
    def __init__(self, api_client: APIClient, user: dict, on_navigate):
        super().__init__()
        self.api_client = api_client
        self.user = user
        self.on_navigate = on_navigate
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Шапка
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        user_info = QVBoxLayout()
        user_info.setSpacing(2)
        
        greeting = QLabel(f"Здравствуйте, {self.user['full_name']}")
        greeting.setStyleSheet("font-size: 18px; font-weight: 700;")
        
        subtitle = QLabel("Ваши записи")
        subtitle.setProperty("labelStyle", "muted")
        subtitle.setStyleSheet("font-size: 12px;")
        
        user_info.addWidget(greeting)
        user_info.addWidget(subtitle)
        
        logout_btn = QPushButton("Выход")
        logout_btn.setProperty("buttonStyle", "ghost")
        logout_btn.clicked.connect(lambda: self.on_navigate("logout"))
        
        header_layout.addLayout(user_info)
        header_layout.addStretch()
        header_layout.addWidget(logout_btn)
        
        # Меню навигации
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(6)
        
        services_btn = QPushButton("Услуги")
        services_btn.setProperty("buttonStyle", "outline")
        services_btn.clicked.connect(lambda: self.on_navigate("services"))
        
        payments_btn = QPushButton("Оплаты")
        payments_btn.setProperty("buttonStyle", "outline")
        payments_btn.clicked.connect(lambda: self.on_navigate("payments"))
        
        menu_layout.addWidget(services_btn)
        menu_layout.addWidget(payments_btn)
        menu_layout.addStretch()
        
        # Список записей
        appointments_header = QHBoxLayout()
        appointments_header.setContentsMargins(0, 0, 0, 0)
        
        appointments_label = QLabel("Записи")
        appointments_label.setStyleSheet("font-size: 16px; font-weight: 600;")
        
        # Фильтр по статусу
        filter_label = QLabel("Фильтр:")
        filter_label.setStyleSheet("font-size: 12px;")
        
        self.status_filter = QComboBox()
        self.status_filter.addItems(["Все", "Забронировано", "В процессе", "Завершено"])
        self.status_filter.setStyleSheet("font-size: 12px; padding: 4px; min-height: 24px;")
        self.status_filter.currentTextChanged.connect(self.load_appointments)
        
        refresh_btn = QPushButton("Обновить")
        refresh_btn.setProperty("buttonStyle", "outline")
        refresh_btn.setStyleSheet("font-size: 12px; padding: 4px 8px; min-height: 24px;")
        refresh_btn.clicked.connect(self.load_appointments)
        
        appointments_header.addWidget(appointments_label)
        appointments_header.addStretch()
        appointments_header.addWidget(filter_label)
        appointments_header.addWidget(self.status_filter)
        appointments_header.addWidget(refresh_btn)
        
        # Scroll area для записей
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        self.appointments_container = QWidget()
        self.appointments_layout = QVBoxLayout()
        self.appointments_layout.setSpacing(6)
        self.appointments_layout.setContentsMargins(0, 0, 0, 0)
        self.appointments_container.setLayout(self.appointments_layout)
        
        scroll.setWidget(self.appointments_container)
        
        layout.addLayout(header_layout)
        layout.addLayout(menu_layout)
        layout.addLayout(appointments_header)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
        self.load_appointments()
    
    def load_appointments(self):
        # Очищаем контейнер
        while self.appointments_layout.count():
            child = self.appointments_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        try:
            appointments = self.api_client.get_master_appointments()
        except APIError as e:
            QMessageBox.warning(self, "Ошибка", e.message)
            return
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
            return
        
        if not appointments:
            no_appointments = QLabel("У вас пока нет записей")
            no_appointments.setProperty("labelStyle", "muted")
            no_appointments.setAlignment(Qt.AlignCenter)
            no_appointments.setStyleSheet("padding: 20px; font-size: 12px;")
            self.appointments_layout.addWidget(no_appointments)
            self.appointments_layout.addStretch()
            return
        
        # Фильтруем по статусу
        filter_text = self.status_filter.currentText()
        if filter_text != "Все":
            status_map = {
                "Забронировано": "booked",
                "В процессе": "in_progress",
                "Завершено": "completed"
            }
            filter_status = status_map.get(filter_text)
            if filter_status:
                appointments = [a for a in appointments if a["status"] == filter_status]
        
        # Сортируем по дате и времени
        appointments_sorted = sorted(appointments, key=lambda a: (a["date"], a["quarter"]))
        
        for appointment in appointments_sorted:
            # Создаем карточку записи
            card = QFrame()
            card.setStyleSheet(f"background-color: {CARD}; border: 1px solid {BORDER}; border-radius: 8px; padding: 8px;")
            card_layout = QHBoxLayout()
            card_layout.setSpacing(8)
            card_layout.setContentsMargins(8, 6, 8, 6)
            
            # Форматируем время
            hours = 8 + (appointment["quarter"] - 1) // 2
            minutes = ((appointment["quarter"] - 1) % 2) * 30
            time_str = f"{hours:02d}:{minutes:02d}"
            
            # Парсим дату
            appointment_date = datetime.strptime(appointment["date"], "%Y-%m-%d").date()
            
            # Левая часть - основная информация
            left_info = QVBoxLayout()
            left_info.setSpacing(2)
            left_info.setContentsMargins(0, 0, 0, 0)
            
            # Первая строка: дата/время и услуга
            top_row = QHBoxLayout()
            top_row.setSpacing(8)
            top_row.setContentsMargins(0, 0, 0, 0)
            
            date_time_label = QLabel(f"{appointment_date.strftime('%d.%m')} {time_str}")
            date_time_label.setStyleSheet(f"color: {PRIMARY}; font-weight: 600; font-size: 13px; min-width: 80px;")
            
            service_label = QLabel(appointment["service_title"])
            service_label.setStyleSheet("font-weight: 600; font-size: 13px;")
            
            top_row.addWidget(date_time_label)
            top_row.addWidget(service_label)
            top_row.addStretch()
            
            # Вторая строка: клиент
            client_label = QLabel(f"Клиент: {appointment['client_full_name']}")
            client_label.setStyleSheet("font-size: 11px; color: " + MUTED_FOREGROUND + "; margin: 0px; padding: 0px;")
            
            # Третья строка: статус и оплата в одну строку
            status_row = QHBoxLayout()
            status_row.setSpacing(8)
            status_row.setContentsMargins(0, 0, 0, 0)
            
            status_map = {
                "booked": "Забронировано",
                "in_progress": "В процессе",
                "completed": "Завершено"
            }
            status_text = status_map.get(appointment["status"], appointment["status"])
            status_label = QLabel(f"Статус: {status_text}")
            status_label.setStyleSheet("font-size: 11px; margin: 0px; padding: 0px;")
            
            paid_text = "Оплачено" if appointment["is_paid"] else "Не оплачено"
            paid_label = QLabel(f"Оплата: {paid_text}")
            paid_label.setStyleSheet(f"font-size: 11px; color: {'#4ade80' if appointment['is_paid'] else '#f87171'}; margin: 0px; padding: 0px;")
            
            status_row.addWidget(status_label)
            status_row.addWidget(paid_label)
            status_row.addStretch()
            
            left_info.addLayout(top_row)
            left_info.addWidget(client_label)
            left_info.addLayout(status_row)
            
            # Правая часть - управление
            right_controls = QVBoxLayout()
            right_controls.setSpacing(4)
            right_controls.setContentsMargins(0, 0, 0, 0)
            
            # Комбо статуса
            status_combo = QComboBox()
            status_combo.addItems(["Забронировано", "В процессе", "Завершено"])
            status_combo.setCurrentText(status_text)
            status_combo.setStyleSheet("font-size: 11px; padding: 4px; min-height: 24px;")
            status_combo.currentTextChanged.connect(
                lambda text, app_id=appointment["id"]: self.update_status(app_id, text)
            )
            
            right_controls.addWidget(status_combo)
            
            # Кнопка оплаты (только если не оплачено)
            if not appointment["is_paid"]:
                paid_btn = QPushButton("Оплата")
                paid_btn.setProperty("buttonStyle", "outline")
                paid_btn.setStyleSheet("font-size: 11px; padding: 4px 8px; min-height: 24px;")
                paid_btn.clicked.connect(
                    lambda checked, app_id=appointment["id"]: self.toggle_payment(app_id)
                )
                right_controls.addWidget(paid_btn)
            
            right_controls.addStretch()
            
            card_layout.addLayout(left_info, 1)
            card_layout.addLayout(right_controls, 0)
            
            card.setLayout(card_layout)
            self.appointments_layout.addWidget(card)
        
        self.appointments_layout.addStretch()
    
    def update_status(self, appointment_id: int, status_text: str):
        status_map = {
            "Забронировано": "booked",
            "В процессе": "in_progress",
            "Завершено": "completed"
        }
        status = status_map.get(status_text)
        if status:
            try:
                self.api_client.update_appointment_status(appointment_id, status)
                self.load_appointments()
            except APIError as e:
                QMessageBox.warning(self, "Ошибка", e.message)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
    
    def toggle_payment(self, appointment_id: int):
        try:
            # Получаем текущую запись для получения цены услуги
            appointment = self.api_client.get_appointment(appointment_id)
            
            # Устанавливаем оплату
            self.api_client.update_appointment_paid(appointment_id, True)
            
            # Создаем запись об оплате
            amount = float(appointment["service_price"])
            self.api_client.create_payment(appointment_id, amount)
            
            self.load_appointments()
        except APIError as e:
            QMessageBox.warning(self, "Ошибка", f"{e.message} (Код: {e.status_code})")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")


class ServicesPage(QWidget):
    def __init__(self, api_client: APIClient, user: dict, on_back):
        super().__init__()
        self.api_client = api_client
        self.user = user
        self.on_back = on_back
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Заголовок и кнопка назад
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        back_btn = QPushButton("← Назад")
        back_btn.setProperty("buttonStyle", "ghost")
        back_btn.clicked.connect(self.on_back)
        
        title = QLabel("Услуги")
        title.setStyleSheet("font-size: 18px; font-weight: 700;")
        
        header_layout.addWidget(back_btn)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Форма добавления услуги
        add_form = QFrame()
        add_form.setStyleSheet(f"background-color: {CARD}; border: 1px solid {BORDER}; border-radius: 8px; padding: 8px;")
        add_form_layout = QFormLayout()
        add_form_layout.setSpacing(6)
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название услуги")
        
        self.duration_input = QSpinBox()
        self.duration_input.setMinimum(1)
        self.duration_input.setMaximum(20)
        self.duration_input.setValue(2)
        self.duration_input.setSuffix(" кварталов (30 мин каждый)")
        
        self.price_input = QDoubleSpinBox()
        self.price_input.setMinimum(0)
        self.price_input.setMaximum(100000)
        self.price_input.setValue(1000)
        self.price_input.setSuffix(" ₽")
        
        add_form_layout.addRow("Название:", self.title_input)
        add_form_layout.addRow("Длительность:", self.duration_input)
        add_form_layout.addRow("Цена:", self.price_input)
        
        add_btn = QPushButton("Добавить услугу")
        add_btn.setProperty("buttonStyle", "default")
        add_btn.setStyleSheet(f"background-color: {PRIMARY}; color: {PRIMARY_FOREGROUND}; border: none; border-radius: 8px; padding: 6px 12px; font-weight: 500; font-size: 13px; min-height: 28px;")
        add_btn.clicked.connect(self.add_service)
        
        add_form_layout.addRow("", add_btn)
        add_form.setLayout(add_form_layout)
        
        # Список услуг
        services_label = QLabel("Мои услуги")
        services_label.setStyleSheet("font-size: 14px; font-weight: 600;")
        
        # Scroll area для услуг
        services_scroll = QScrollArea()
        services_scroll.setWidgetResizable(True)
        services_scroll.setStyleSheet("border: none;")
        
        self.services_container = QWidget()
        self.services_layout = QVBoxLayout()
        self.services_layout.setSpacing(6)
        self.services_layout.setContentsMargins(0, 0, 0, 0)
        self.services_container.setLayout(self.services_layout)
        
        services_scroll.setWidget(self.services_container)
        
        layout.addLayout(header_layout)
        layout.addWidget(add_form)
        layout.addWidget(services_label)
        layout.addWidget(services_scroll)
        
        self.setLayout(layout)
        self.load_services()
    
    def add_service(self):
        title = self.title_input.text().strip()
        duration = self.duration_input.value()
        price = self.price_input.value()
        
        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите название услуги")
            return
        
        try:
            self.api_client.create_service(title, duration, price, self.user["id"])
            self.title_input.clear()
            self.duration_input.setValue(2)
            self.price_input.setValue(1000)
            self.load_services()
        except APIError as e:
            QMessageBox.warning(self, "Ошибка", e.message)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
    
    def load_services(self):
        # Очищаем контейнер
        while self.services_layout.count():
            child = self.services_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        try:
            services = self.api_client.get_master_services()
        except APIError as e:
            QMessageBox.warning(self, "Ошибка", e.message)
            return
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
            return
        
        if not services:
            no_services = QLabel("У вас пока нет услуг")
            no_services.setProperty("labelStyle", "muted")
            no_services.setAlignment(Qt.AlignCenter)
            no_services.setStyleSheet("padding: 20px; font-size: 12px;")
            self.services_layout.addWidget(no_services)
            self.services_layout.addStretch()
            return
        
        for service in services:
            # Создаем карточку услуги
            card = QFrame()
            card.setStyleSheet(f"background-color: {CARD}; border: 1px solid {BORDER}; border-radius: 8px; padding: 8px;")
            
            # Основной layout с горизонтальным расположением
            main_layout = QHBoxLayout()
            main_layout.setSpacing(8)
            main_layout.setContentsMargins(0, 0, 0, 0)
            
            duration_hours = service["duration_quarters"] * 30 / 60
            if duration_hours < 1:
                duration_str = f"{service['duration_quarters'] * 30} мин"
            elif duration_hours == int(duration_hours):
                duration_str = f"{int(duration_hours)}ч"
            else:
                hours = int(duration_hours)
                minutes = int((duration_hours - hours) * 60)
                duration_str = f"{hours}ч {minutes} мин"
            
            price = float(service["price"])
            
            # Текст услуги
            item_text = f"{service['title']}\nДлительность: {duration_str}\nЦена: {price:.0f} ₽"
            service_label = QLabel(item_text)
            service_label.setStyleSheet("font-size: 13px;")
            
            # Кнопка удаления
            delete_btn = QPushButton("×")
            delete_btn.setProperty("buttonStyle", "ghost")
            delete_btn.setStyleSheet("font-size: 18px; font-weight: bold; padding: 0px; min-width: 20px; min-height: 20px; max-width: 20px; max-height: 20px; color: #f87171;")
            delete_btn.clicked.connect(lambda checked, service_id=service["id"]: self.delete_service(service_id))
            
            main_layout.addWidget(service_label, 1)
            main_layout.addWidget(delete_btn, 0, Qt.AlignTop | Qt.AlignRight)
            
            card.setLayout(main_layout)
            self.services_layout.addWidget(card)
        
        self.services_layout.addStretch()
    
    def delete_service(self, service_id: int):
        try:
            self.api_client.delete_service(service_id)
            self.load_services()
        except APIError as e:
            QMessageBox.warning(self, "Ошибка", e.message)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")


class PaymentsPage(QWidget):
    def __init__(self, api_client: APIClient, user: dict, on_back):
        super().__init__()
        self.api_client = api_client
        self.user = user
        self.on_back = on_back
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Заголовок и кнопка назад
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        back_btn = QPushButton("← Назад")
        back_btn.setProperty("buttonStyle", "ghost")
        back_btn.clicked.connect(self.on_back)
        
        title = QLabel("Оплаты")
        title.setStyleSheet("font-size: 18px; font-weight: 700;")
        
        header_layout.addWidget(back_btn)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Таблица оплат
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(5)
        self.payments_table.setHorizontalHeaderLabels(["Дата", "Время", "Услуга", "Клиент", "Сумма"])
        self.payments_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.payments_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.payments_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.payments_table)
        
        self.setLayout(layout)
        self.load_payments()
    
    def load_payments(self):
        try:
            payments = self.api_client.get_master_payments()
        except APIError as e:
            QMessageBox.warning(self, "Ошибка", e.message)
            return
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
            return
        
        self.payments_table.setRowCount(len(payments))
        
        for row, payment in enumerate(payments):
            # Форматируем дату
            payment_date = datetime.strptime(payment["date"], "%Y-%m-%d").date()
            
            self.payments_table.setItem(row, 0, QTableWidgetItem(payment_date.strftime('%d.%m.%Y')))
            self.payments_table.setItem(row, 1, QTableWidgetItem(payment["time"]))
            self.payments_table.setItem(row, 2, QTableWidgetItem(payment["service_title"]))
            self.payments_table.setItem(row, 3, QTableWidgetItem(payment["client_full_name"]))
            amount = float(payment["amount"])
            self.payments_table.setItem(row, 4, QTableWidgetItem(f"{amount:.0f} ₽"))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.current_user = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Николь Бьюти - Приложение для мастеров")
        self.setMinimumSize(800, 600)
        self.resize(1000, 700)
        
        # Используем QStackedWidget для переключения страниц
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Создаем страницы
        self.login_page = LoginPage(self.api_client, self.handle_navigation)
        self.register_page = RegisterPage(self.api_client, self.handle_navigation)
        
        # Добавляем страницы в стек
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)
        
        # Начальная страница - вход
        self.stacked_widget.setCurrentWidget(self.login_page)
    
    def show_login(self):
        self.current_user = None
        self.stacked_widget.setCurrentWidget(self.login_page)
    
    def show_register(self):
        self.stacked_widget.setCurrentWidget(self.register_page)
    
    def show_home(self, user: dict):
        if not user:
            return
        self.current_user = user
        # Всегда создаем новую страницу для обновления данных
        home_page = HomePage(self.api_client, user, self.handle_navigation)
        self.stacked_widget.addWidget(home_page)
        self.stacked_widget.setCurrentWidget(home_page)
        self.stacked_widget.update()
        self.update()
    
    def show_services(self, user: dict):
        if not user:
            user = self.current_user
        if not user:
            QMessageBox.warning(self, "Ошибка", "Пользователь не авторизован")
            return
        # Всегда создаем новую страницу
        services_page = ServicesPage(self.api_client, user, lambda: self.show_home(user))
        self.stacked_widget.addWidget(services_page)
        self.stacked_widget.setCurrentWidget(services_page)
        self.stacked_widget.update()
        self.update()
    
    def show_payments(self, user: dict):
        if not user:
            user = self.current_user
        if not user:
            QMessageBox.warning(self, "Ошибка", "Пользователь не авторизован")
            return
        # Всегда создаем новую страницу
        payments_page = PaymentsPage(self.api_client, user, lambda: self.show_home(user))
        self.stacked_widget.addWidget(payments_page)
        self.stacked_widget.setCurrentWidget(payments_page)
        self.stacked_widget.update()
        self.update()
    
    def handle_navigation(self, page: str, user: dict = None):
        try:
            if page == "login":
                self.show_login()
            elif page == "register":
                self.show_register()
            elif page == "home":
                if user:
                    self.show_home(user)
                elif self.current_user:
                    self.show_home(self.current_user)
                else:
                    QMessageBox.warning(self, "Ошибка", "Пользователь не авторизован")
            elif page == "services":
                if user:
                    self.show_services(user)
                elif self.current_user:
                    self.show_services(self.current_user)
                else:
                    QMessageBox.warning(self, "Ошибка", "Пользователь не авторизован")
            elif page == "payments":
                if user:
                    self.show_payments(user)
                elif self.current_user:
                    self.show_payments(self.current_user)
                else:
                    QMessageBox.warning(self, "Ошибка", "Пользователь не авторизован")
            elif page == "logout":
                self.current_user = None
                self.api_client.logout()
                self.show_login()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
            import traceback
            traceback.print_exc()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(get_stylesheet())
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

