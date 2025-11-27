import '../models/service.dart';
import '../models/master.dart';

class DataService {
  // Mock data for services
  static List<Service> getServices() {
    return [
      Service(
        id: '1',
        name: 'Маникюр классический',
        price: 1500,
        durationMinutes: 60,
        masterId: '1',
        masterName: 'Анна Иванова',
        masterType: 'маникюрист',
      ),
      Service(
        id: '2',
        name: 'Покрытие гель-лак',
        price: 2000,
        durationMinutes: 90,
        masterId: '1',
        masterName: 'Анна Иванова',
        masterType: 'маникюрист',
      ),
      Service(
        id: '3',
        name: 'Макияж дневной',
        price: 2500,
        durationMinutes: 60,
        masterId: '2',
        masterName: 'Мария Петрова',
        masterType: 'визажист',
      ),
      Service(
        id: '4',
        name: 'Макияж вечерний',
        price: 3500,
        durationMinutes: 90,
        masterId: '2',
        masterName: 'Мария Петрова',
        masterType: 'визажист',
      ),
      Service(
        id: '5',
        name: 'Стрижка женская',
        price: 2000,
        durationMinutes: 60,
        masterId: '3',
        masterName: 'Елена Смирнова',
        masterType: 'стилист',
      ),
      Service(
        id: '6',
        name: 'Окрашивание волос',
        price: 4500,
        durationMinutes: 120,
        masterId: '3',
        masterName: 'Елена Смирнова',
        masterType: 'стилист',
      ),
      Service(
        id: '7',
        name: 'Коррекция бровей',
        price: 1000,
        durationMinutes: 30,
        masterId: '4',
        masterName: 'Ольга Козлова',
        masterType: 'бровист',
      ),
      Service(
        id: '8',
        name: 'Окрашивание бровей',
        price: 1500,
        durationMinutes: 45,
        masterId: '4',
        masterName: 'Ольга Козлова',
        masterType: 'бровист',
      ),
    ];
  }

  // Mock data for masters
  static List<Master> getMasters() {
    return [
      Master(
        id: '1',
        name: 'Анна Иванова',
        type: 'маникюрист',
        phone: '+7 (999) 123-45-67',
      ),
      Master(
        id: '2',
        name: 'Мария Петрова',
        type: 'визажист',
        phone: '+7 (999) 234-56-78',
      ),
      Master(
        id: '3',
        name: 'Елена Смирнова',
        type: 'стилист',
        phone: '+7 (999) 345-67-89',
      ),
      Master(
        id: '4',
        name: 'Ольга Козлова',
        type: 'бровист',
        phone: '+7 (999) 456-78-90',
      ),
    ];
  }

  static Service? getServiceById(String id) {
    try {
      return getServices().firstWhere((s) => s.id == id);
    } catch (e) {
      return null;
    }
  }

  static Master? getMasterById(String id) {
    try {
      return getMasters().firstWhere((m) => m.id == id);
    } catch (e) {
      return null;
    }
  }

  static List<Service> getServicesByMasterId(String masterId) {
    return getServices().where((s) => s.masterId == masterId).toList();
  }
}

