"""
API клиент для работы с Beauty Salon API
"""
import requests
from typing import Optional, List, Dict, Any
from datetime import date, datetime


class APIError(Exception):
    """Исключение для ошибок API"""
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class APIClient:
    """Клиент для работы с API"""
    
    BASE_URL = "http://37.9.13.207:8080"
    
    def __init__(self):
        self.token: Optional[str] = None
        self.user: Optional[Dict[str, Any]] = None
    
    def _get_headers(self, include_auth: bool = True) -> Dict[str, str]:
        """Получить заголовки для запроса"""
        headers = {"Content-Type": "application/json"}
        if include_auth and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def _handle_response(self, response: requests.Response) -> Any:
        """Обработать ответ API"""
        if response.status_code in [200, 201]:
            if response.content:
                return response.json()
            return None
        elif response.status_code == 204:
            return None
        elif response.status_code == 401:
            self.token = None
            self.user = None
            raise APIError("Требуется авторизация", 401)
        elif response.status_code == 404:
            raise APIError("Ресурс не найден", 404)
        else:
            error_msg = "Ошибка сервера"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_msg = error_data["detail"]
                elif "message" in error_data:
                    error_msg = error_data["message"]
            except:
                error_msg = response.text or f"Ошибка {response.status_code}"
            raise APIError(error_msg, response.status_code)
    
    # ========== Аутентификация ==========
    
    def register(self, login: str, password: str, full_name: str, 
                 phone_number: str, role: str = "CLIENT") -> Dict[str, Any]:
        """Регистрация пользователя"""
        url = f"{self.BASE_URL}/api/auth/register"
        data = {
            "login": login,
            "password": password,
            "full_name": full_name,
            "phone_number": phone_number,
            "role": role
        }
        response = requests.post(url, json=data, headers=self._get_headers(include_auth=False))
        result = self._handle_response(response)
        self.token = result["access_token"]
        self.user = result["user"]
        return result
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Вход пользователя"""
        url = f"{self.BASE_URL}/api/auth/token"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        result = self._handle_response(response)
        self.token = result["access_token"]
        self.user = result["user"]
        return result
    
    def get_current_user(self) -> Dict[str, Any]:
        """Получить информацию о текущем пользователе"""
        url = f"{self.BASE_URL}/api/users/me"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    def logout(self):
        """Выход (очистка токена)"""
        self.token = None
        self.user = None
    
    # ========== Услуги ==========
    
    def get_services(self) -> List[Dict[str, Any]]:
        """Получить список всех услуг"""
        url = f"{self.BASE_URL}/api/services"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    def get_master_services(self, master_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Получить услуги мастера"""
        if master_id:
            url = f"{self.BASE_URL}/api/services/masters/{master_id}"
        else:
            url = f"{self.BASE_URL}/api/services/masters/me"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    def get_service(self, service_id: int) -> Dict[str, Any]:
        """Получить услугу по ID"""
        url = f"{self.BASE_URL}/api/services/{service_id}"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    def create_service(self, title: str, duration_quarters: int, price: float, master_id: int) -> Dict[str, Any]:
        """Создать услугу"""
        url = f"{self.BASE_URL}/api/services"
        data = {
            "title": title,
            "duration_quarters": duration_quarters,
            "price": str(price),
            "master_id": master_id
        }
        response = requests.post(url, json=data, headers=self._get_headers())
        return self._handle_response(response)
    
    def update_service(self, service_id: int, title: Optional[str] = None,
                      duration_quarters: Optional[int] = None,
                      price: Optional[float] = None,
                      master_id: Optional[int] = None) -> Dict[str, Any]:
        """Обновить услугу"""
        url = f"{self.BASE_URL}/api/services/{service_id}"
        data = {}
        if title is not None:
            data["title"] = title
        if duration_quarters is not None:
            data["duration_quarters"] = duration_quarters
        if price is not None:
            data["price"] = str(price)
        if master_id is not None:
            data["master_id"] = master_id
        response = requests.put(url, json=data, headers=self._get_headers())
        return self._handle_response(response)
    
    def delete_service(self, service_id: int):
        """Удалить услугу"""
        url = f"{self.BASE_URL}/api/services/{service_id}"
        response = requests.delete(url, headers=self._get_headers())
        self._handle_response(response)
    
    def get_free_quarters(self, service_id: int, date_str: str) -> List[int]:
        """Получить свободные кварталы для услуги"""
        url = f"{self.BASE_URL}/api/services/{service_id}/free_quarters"
        params = {"date": date_str}
        response = requests.get(url, params=params, headers=self._get_headers())
        result = self._handle_response(response)
        return result.get("free_quarters", [])
    
    # ========== Записи ==========
    
    def get_appointments(self) -> List[Dict[str, Any]]:
        """Получить список всех записей"""
        url = f"{self.BASE_URL}/api/appointments"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    def get_master_appointments(self) -> List[Dict[str, Any]]:
        """Получить записи текущего мастера"""
        url = f"{self.BASE_URL}/api/appointments/master"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    def get_client_appointments(self) -> List[Dict[str, Any]]:
        """Получить записи текущего клиента"""
        url = f"{self.BASE_URL}/api/appointments/client"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    def get_appointment(self, appointment_id: int) -> Dict[str, Any]:
        """Получить запись по ID"""
        url = f"{self.BASE_URL}/api/appointments/{appointment_id}"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    def create_appointment(self, client_id: int, service_id: int, date_str: str,
                          quarter: int, status: str = "booked", is_paid: bool = False) -> Dict[str, Any]:
        """Создать запись"""
        url = f"{self.BASE_URL}/api/appointments"
        data = {
            "client_id": client_id,
            "service_id": service_id,
            "date": date_str,
            "quarter": quarter,
            "status": status,
            "is_paid": is_paid
        }
        response = requests.post(url, json=data, headers=self._get_headers())
        return self._handle_response(response)
    
    def delete_appointment(self, appointment_id: int):
        """Удалить запись"""
        url = f"{self.BASE_URL}/api/appointments/{appointment_id}"
        response = requests.delete(url, headers=self._get_headers())
        self._handle_response(response)
    
    def update_appointment_status(self, appointment_id: int, status: str) -> Dict[str, Any]:
        """Обновить статус записи
        
        Примечание: API может не поддерживать обновление записей.
        Если запрос не поддерживается, будет выброшено исключение APIError.
        """
        # Получаем текущую запись
        appointment = self.get_appointment(appointment_id)
        # Пытаемся обновить через PUT (если API поддерживает)
        url = f"{self.BASE_URL}/api/appointments/{appointment_id}"
        data = {
            "date": appointment["date"],
            "quarter": appointment["quarter"],
            "status": status,
            "is_paid": appointment.get("is_paid", False)
        }
        # Если в ответе есть client_id и service_id, добавляем их
        if "client_id" in appointment:
            data["client_id"] = appointment["client_id"]
        if "service_id" in appointment:
            data["service_id"] = appointment["service_id"]
        
        response = requests.put(url, json=data, headers=self._get_headers())
        return self._handle_response(response)
    
    def update_appointment_paid(self, appointment_id: int, is_paid: bool) -> Dict[str, Any]:
        """Обновить статус оплаты записи
        
        Примечание: API может не поддерживать обновление записей.
        Если запрос не поддерживается, будет выброшено исключение APIError.
        """
        # Получаем текущую запись
        appointment = self.get_appointment(appointment_id)
        # Пытаемся обновить через PUT (если API поддерживает)
        url = f"{self.BASE_URL}/api/appointments/{appointment_id}"
        data = {
            "date": appointment["date"],
            "quarter": appointment["quarter"],
            "status": appointment["status"],
            "is_paid": is_paid
        }
        # Если в ответе есть client_id и service_id, добавляем их
        if "client_id" in appointment:
            data["client_id"] = appointment["client_id"]
        if "service_id" in appointment:
            data["service_id"] = appointment["service_id"]
        
        response = requests.put(url, json=data, headers=self._get_headers())
        return self._handle_response(response)
    
    # ========== Оплаты ==========
    
    def get_master_payments(self) -> List[Dict[str, Any]]:
        """Получить оплаты текущего мастера"""
        url = f"{self.BASE_URL}/api/payments/me"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    def create_payment(self, appointment_id: int, amount: float) -> Dict[str, Any]:
        """Создать оплату"""
        url = f"{self.BASE_URL}/api/payments"
        data = {
            "appointment_id": appointment_id,
            "amount": str(amount)
        }
        response = requests.post(url, json=data, headers=self._get_headers())
        return self._handle_response(response)

