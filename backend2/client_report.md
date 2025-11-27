# Документация API Beauty Salon

## Базовый URL
`http://37.9.13.207:8080`

## Аутентификация
Большинство эндпоинтов требуют JWT токен в заголовке:
```
Authorization: Bearer <token>
```

---

## 1. Аутентификация (Auth)

### 1.1. Регистрация
**URL:** `POST /api/auth/register`  
**Аутентификация:** Не требуется

**Входные данные (Body):**
```json
{
  "login": "string",
  "password": "string",
  "full_name": "string",
  "phone_number": "string",
  "role": "CLIENT" | "VIZAZHIST" | "MANICURIST" | "STYLIST" | "BROWIST" (default: "CLIENT")
}
```

**Выходные данные:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "id": 0,
    "login": "string",
    "full_name": "string",
    "phone_number": "string",
    "role": "string",
    "created_at": "2025-01-01T00:00:00"
  }
}
```

---

### 1.2. Вход (Получение токена)
**URL:** `POST /api/auth/token`  
**Аутентификация:** Не требуется

**Входные данные (Form Data application/x-www-form-urlencoded):**
- `username`: string (логин пользователя)
- `password`: string (пароль пользователя)

**Выходные данные:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "id": 0,
    "login": "string",
    "full_name": "string",
    "phone_number": "string",
    "role": "string",
    "created_at": "2025-01-01T00:00:00"
  }
}
```

---

## 2. Пользователи (Users)

### 2.1. Информация о текущем пользователе
**URL:** `GET /api/users/me`  
**Аутентификация:** Требуется

**Входные данные:** Нет

**Выходные данные:**
```json
{
  "id": 0,
  "login": "string",
  "full_name": "string",
  "phone_number": "string",
  "role": "string",
  "created_at": "2025-01-01T00:00:00"
}
```

---

### 2.2. Список всех мастеров
**URL:** `GET /api/users/masters`  
**Аутентификация:** Требуется

**Входные данные:** Нет

**Выходные данные:**
```json
[
  {
    "id": 0,
    "full_name": "string",
    "role": "string",
    "phone_number": "string",
    "services_count": 0
  }
]
```

---

## 3. Услуги (Services)

### 3.1. Список всех услуг
**URL:** `GET /api/services`  
**Аутентификация:** Требуется

**Входные данные:** Нет

**Выходные данные:**
```json
[
  {
    "id": 0,
    "title": "string",
    "price": "0.00",
    "duration_quarters": 0,
    "master_id": 0,
    "master_full_name": "string",
    "master_role": "string",
    "master_phone_number": "string"
  }
]
```

---

### 3.2. Услуги мастера по ID
**URL:** `GET /api/services/masters/{master_id}`  
**Аутентификация:** Требуется

**Входные данные:**
- Path параметр: `master_id` (int)

**Выходные данные:**
```json
[
  {
    "id": 0,
    "title": "string",
    "price": "0.00",
    "duration_quarters": 0,
    "master_id": 0,
    "master_full_name": "string",
    "master_role": "string",
    "master_phone_number": "string"
  }
]
```

---

### 3.3. Свободные кварталы для услуги
**URL:** `GET /api/services/{service_id}/free_quarters`  
**Аутентификация:** Требуется

**Входные данные:**
- Path параметр: `service_id` (int)
- Query параметр: `date` (date, формат: YYYY-MM-DD, пример: "2025-11-27")

**Выходные данные:**
```json
{
  "free_quarters": [1, 2, 3, 5, 8, 9, 10]
}
```

**Примечание:** Возвращает список свободных стартовых кварталов (1-20) для указанной услуги на указанную дату. Учитывает все записи мастера и длительность услуги.

---

### 3.4. Услуга по ID
**URL:** `GET /api/services/{service_id}`  
**Аутентификация:** Требуется

**Входные данные:**
- Path параметр: `service_id` (int)

**Выходные данные:**
```json
{
  "id": 0,
  "title": "string",
  "price": "0.00",
  "duration_quarters": 0,
  "master_id": 0,
  "master_full_name": "string",
  "master_role": "string",
  "master_phone_number": "string"
}
```

---

### 3.5. Создание услуги
**URL:** `POST /api/services`  
**Аутентификация:** Требуется

**Входные данные (Body):**
```json
{
  "title": "string",
  "duration_quarters": 0,
  "price": "0.00",
  "master_id": 0
}
```

**Выходные данные:**
```json
{
  "id": 0,
  "title": "string",
  "duration_quarters": 0,
  "price": "0.00",
  "master_id": 0
}
```

---

### 3.6. Обновление услуги
**URL:** `PUT /api/services/{service_id}`  
**Аутентификация:** Требуется

**Входные данные:**
- Path параметр: `service_id` (int)
- Body (все поля опциональны):
```json
{
  "title": "string",
  "duration_quarters": 0,
  "price": "0.00",
  "master_id": 0
}
```

**Выходные данные:**
```json
{
  "id": 0,
  "title": "string",
  "duration_quarters": 0,
  "price": "0.00",
  "master_id": 0
}
```

---

### 3.7. Удаление услуги
**URL:** `DELETE /api/services/{service_id}`  
**Аутентификация:** Требуется

**Входные данные:**
- Path параметр: `service_id` (int)

**Выходные данные:** 204 No Content

---

## 4. Записи (Appointments)

### 4.1. Список всех записей
**URL:** `GET /api/appointments`  
**Аутентификация:** Требуется

**Входные данные:** Нет

**Выходные данные:**
```json
[
  {
    "id": 0,
    "date": "2025-11-27",
    "quarter": 0,
    "status": "booked" | "in_progress" | "completed",
    "is_paid": false,
    "master_full_name": "string",
    "service_title": "string",
    "service_price": "0.00",
    "client_full_name": "string"
  }
]
```

---

### 4.2. Записи текущего клиента
**URL:** `GET /api/appointments/client`  
**Аутентификация:** Требуется

**Входные данные:** Нет

**Выходные данные:**
```json
[
  {
    "id": 0,
    "date": "2025-11-27",
    "quarter": 0,
    "status": "booked" | "in_progress" | "completed",
    "is_paid": false,
    "master_full_name": "string",
    "service_title": "string",
    "service_price": "0.00",
    "client_full_name": "string"
  }
]
```

---

### 4.3. Записи текущего мастера
**URL:** `GET /api/appointments/master`  
**Аутентификация:** Требуется

**Входные данные:** Нет

**Выходные данные:**
```json
[
  {
    "id": 0,
    "date": "2025-11-27",
    "quarter": 0,
    "status": "booked" | "in_progress" | "completed",
    "is_paid": false,
    "master_full_name": "string",
    "service_title": "string",
    "service_price": "0.00",
    "client_full_name": "string"
  }
]
```

---

### 4.4. Запись по ID
**URL:** `GET /api/appointments/{appointment_id}`  
**Аутентификация:** Требуется

**Входные данные:**
- Path параметр: `appointment_id` (int)

**Выходные данные:**
```json
{
  "id": 0,
  "date": "2025-11-27",
  "quarter": 0,
  "status": "booked" | "in_progress" | "completed",
  "is_paid": false,
  "master_full_name": "string",
  "service_title": "string",
  "service_price": "0.00",
  "client_full_name": "string"
}
```

---

### 4.5. Создание записи
**URL:** `POST /api/appointments`  
**Аутентификация:** Требуется

**Входные данные (Body):**
```json
{
  "client_id": 0,
  "service_id": 0,
  "date": "2025-11-27",
  "quarter": 0,
  "status": "booked" | "in_progress" | "completed" (default: "booked"),
  "is_paid": false
}
```

**Выходные данные:**
```json
{
  "id": 0,
  "date": "2025-11-27",
  "quarter": 0,
  "status": "booked" | "in_progress" | "completed",
  "is_paid": false,
  "master_full_name": "string",
  "service_title": "string",
  "service_price": "0.00",
  "client_full_name": "string"
}
```

**Валидация:**
- Проверяется, что запись не выходит за границы 20 кварталов (17:30)
- Проверяется, что запись не накладывается на другие записи мастера в этот день
- При ошибке валидации возвращается 400 Bad Request с описанием проблемы

**Примечания:**
- `quarter`: число от 1 до 20 (1 квартал = 30 минут, начало рабочего дня в 8:00)
- Рабочий день: 8:00-18:00 (20 кварталов по 30 минут)

---

### 4.6. Удаление записи
**URL:** `DELETE /api/appointments/{appointment_id}`  
**Аутентификация:** Требуется

**Входные данные:**
- Path параметр: `appointment_id` (int)

**Выходные данные:** 204 No Content

---

## Коды ответов

- `200 OK` - Успешный запрос
- `201 Created` - Ресурс успешно создан
- `204 No Content` - Успешное удаление
- `400 Bad Request` - Ошибка валидации или некорректные данные
- `401 Unauthorized` - Требуется аутентификация или неверный токен
- `404 Not Found` - Ресурс не найден

---

## Типы данных

- `date`: строка в формате YYYY-MM-DD (например, "2025-11-27")
- `datetime`: строка в формате ISO 8601 (например, "2025-01-01T00:00:00")
- `Decimal`: число с плавающей точкой в виде строки (например, "1500.00")
- `int`: целое число
- `string`: строка
- `bool`: логическое значение (true/false)

---

## Статусы записи

- `booked` - Забронировано
- `in_progress` - В процессе
- `completed` - Завершено

---

## Роли пользователей

- `CLIENT` - Клиент
- `VIZAZHIST` - Визажист
- `MANICURIST` - Маникюрщик
- `STYLIST` - Стилист
- `BROWIST` - Бровист


