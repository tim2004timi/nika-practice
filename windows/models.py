from datetime import datetime, date
from typing import List, Optional
from enum import Enum
import hashlib


class UserRole(Enum):
    CLIENT = "client"
    VIZAZHIST = "vizazhist"
    MANICURIST = "manicurist"
    STYLIST = "stylist"
    BROWIST = "browist"


class AppointmentStatus(Enum):
    BOOKED = "booked"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class User:
    def __init__(self, id: int, login: str, password_hash: str, full_name: str, 
                 phone_number: str, role: UserRole, created_at: Optional[datetime] = None):
        self.id = id
        self.login = login
        self.password_hash = password_hash
        self.full_name = full_name
        self.phone_number = phone_number
        self.role = role
        self.created_at = created_at or datetime.now()
    
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password: str) -> bool:
        return self.password_hash == User.hash_password(password)


class Service:
    def __init__(self, id: int, title: str, duration_quarters: int, price: float, master_id: int):
        self.id = id
        self.title = title
        self.duration_quarters = duration_quarters
        self.price = price
        self.master_id = master_id


class Appointment:
    def __init__(self, id: int, client_id: int, service_id: int, date: date, 
                 quarter: int, status: AppointmentStatus, is_paid: bool):
        self.id = id
        self.client_id = client_id
        self.service_id = service_id
        self.date = date
        self.quarter = quarter
        self.status = status
        self.is_paid = is_paid


class Payment:
    def __init__(self, id: int, appointment_id: int, amount: float):
        self.id = id
        self.appointment_id = appointment_id
        self.amount = amount


class Database:
    def __init__(self):
        self.users: List[User] = []
        self.services: List[Service] = []
        self.appointments: List[Appointment] = []
        self.payments: List[Payment] = []
        self._next_user_id = 1
        self._next_service_id = 1
        self._next_appointment_id = 1
        self._next_payment_id = 1
        self._init_data()
    
    def _init_data(self):
        # Создаем пользователя tim
        nikol_user = User(
            id=self._next_user_id,
            login="nikol",
            password_hash=User.hash_password("123"),
            full_name="Медведева Николь Валентиновна",
            phone_number="+7 (999) 123-45-67",
            role=UserRole.MANICURIST
        )
        self.users.append(nikol_user)
        self._next_user_id += 1
        
        # Создаем еще несколько мастеров
        master2 = User(
            id=self._next_user_id,
            login="anna",
            password_hash=User.hash_password("123"),
            full_name="Анна Маникюрист",
            phone_number="+7 (999) 234-56-78",
            role=UserRole.MANICURIST
        )
        self.users.append(master2)
        self._next_user_id += 1
        
        master3 = User(
            id=self._next_user_id,
            login="maria",
            password_hash=User.hash_password("123"),
            full_name="Мария Стилист",
            phone_number="+7 (999) 345-67-89",
            role=UserRole.STYLIST
        )
        self.users.append(master3)
        self._next_user_id += 1
        
        # Создаем клиентов
        client1 = User(
            id=self._next_user_id,
            login="client1",
            password_hash=User.hash_password("123"),
            full_name="Иван Иванов",
            phone_number="+7 (999) 111-11-11",
            role=UserRole.CLIENT
        )
        self.users.append(client1)
        self._next_user_id += 1
        
        client2 = User(
            id=self._next_user_id,
            login="client2",
            password_hash=User.hash_password("123"),
            full_name="Петр Петров",
            phone_number="+7 (999) 222-22-22",
            role=UserRole.CLIENT
        )
        self.users.append(client2)
        self._next_user_id += 1
        
        # Создаем услуги для tim
        service1 = Service(
            id=self._next_service_id,
            title="Макияж дневной",
            duration_quarters=2,  # 1 час
            price=3500.0,
            master_id=nikol_user.id
        )
        self.services.append(service1)
        self._next_service_id += 1
        
        service2 = Service(
            id=self._next_service_id,
            title="Макияж вечерний",
            duration_quarters=3,  # 1.5 часа
            price=5000.0,
            master_id=nikol_user.id
        )
        self.services.append(service2)
        self._next_service_id += 1
        
        service3 = Service(
            id=self._next_service_id,
            title="Коррекция бровей",
            duration_quarters=1,  # 30 минут
            price=1500.0,
            master_id=nikol_user.id
        )
        self.services.append(service3)
        self._next_service_id += 1
        
        # Создаем записи для tim
        from datetime import date, timedelta
        today = date.today()
        
        appointment1 = Appointment(
            id=self._next_appointment_id,
            client_id=client1.id,
            service_id=service1.id,
            date=today,
            quarter=10,  # 14:00
            status=AppointmentStatus.BOOKED,
            is_paid=False
        )
        self.appointments.append(appointment1)
        self._next_appointment_id += 1
        
        appointment2 = Appointment(
            id=self._next_appointment_id,
            client_id=client2.id,
            service_id=service2.id,
            date=today + timedelta(days=1),
            quarter=14,  # 15:00
            status=AppointmentStatus.BOOKED,
            is_paid=True
        )
        self.appointments.append(appointment2)
        self._next_appointment_id += 1
        
        appointment3 = Appointment(
            id=self._next_appointment_id,
            client_id=client1.id,
            service_id=service3.id,
            date=today + timedelta(days=2),
            quarter=8,  # 12:00
            status=AppointmentStatus.COMPLETED,
            is_paid=True
        )
        self.appointments.append(appointment3)
        self._next_appointment_id += 1
    
    def get_user_by_login(self, login: str) -> Optional[User]:
        for user in self.users:
            if user.login == login:
                return user
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def get_services_by_master(self, master_id: int) -> List[Service]:
        return [s for s in self.services if s.master_id == master_id]
    
    def get_appointments_by_master(self, master_id: int) -> List[Appointment]:
        master_service_ids = [s.id for s in self.services if s.master_id == master_id]
        return [a for a in self.appointments if a.service_id in master_service_ids]
    
    def get_service_by_id(self, service_id: int) -> Optional[Service]:
        for service in self.services:
            if service.id == service_id:
                return service
        return None
    
    def add_user(self, login: str, password: str, full_name: str, phone_number: str, role: UserRole) -> User:
        user = User(
            id=self._next_user_id,
            login=login,
            password_hash=User.hash_password(password),
            full_name=full_name,
            phone_number=phone_number,
            role=role
        )
        self.users.append(user)
        self._next_user_id += 1
        return user
    
    def add_service(self, title: str, duration_quarters: int, price: float, master_id: int) -> Service:
        service = Service(
            id=self._next_service_id,
            title=title,
            duration_quarters=duration_quarters,
            price=price,
            master_id=master_id
        )
        self.services.append(service)
        self._next_service_id += 1
        return service
    
    def get_payments_by_master(self, master_id: int) -> List[Payment]:
        master_service_ids = [s.id for s in self.services if s.master_id == master_id]
        master_appointment_ids = [a.id for a in self.appointments if a.service_id in master_service_ids]
        return [p for p in self.payments if p.appointment_id in master_appointment_ids]
    
    def add_payment(self, appointment_id: int, amount: float) -> Payment:
        payment = Payment(
            id=self._next_payment_id,
            appointment_id=appointment_id,
            amount=amount
        )
        self.payments.append(payment)
        self._next_payment_id += 1
        return payment
    
    def update_appointment_status(self, appointment_id: int, status: AppointmentStatus):
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                appointment.status = status
                break
    
    def update_appointment_paid(self, appointment_id: int, is_paid: bool):
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                appointment.is_paid = is_paid
                break





