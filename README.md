# Инфраструктура для Red-Blue battle
<!-- header: RB - что это? -->
## Red-blue battle - формат CTF, где одна команда защищает свои сервисы, а другая - атакует их

Команда Синих защищается, а красных - атакует. Команда красных получает очки за флаги, украденные с сервиса синих, а синие - за время, которые сервисы работают нормально.



# Начисление очков 

 Игра состоит из нескольких раунда по 2-4 минуты. Красные за каждый раунд могут сдать 20 флагов из базы данных синей команды. Синяя команда получает очки только по итогу раунда по статусу своего сервиса. 

# Необходимые минимальные знания 
* ОС Windows и Linux
* Web уязвимости
* Протоколы передачи данных 
* Языки программировани, желательно python
* Базы данных

# Статусы сервисов у синих
* Up - Сервис работает нормально
* Mumble - чекер не находит на сервисе флагов за предыдущие раунды
* Corrupt - Сервис работает не правильно
* Down - Сервис не отвечат на запросы


Такой формат соревнований мы предлагаем использовать для оффлайн-финала какого-то турнира. Отбор на финал будет проходить в формате task-based
Мы предлагаем проводить Red-blue blattle в формате playoff


 Для проведения соревновыний нужен сервер с проверяющей системой и веб-сервером, выдавающий состояние игры в текущий момент. Для игры также потребуется сервер для синей команды. 
 У игроков обоих команд должны быть компьютеры для подключения к серверам.



Для проверки состояния сервиса синей команды на сервере жюри нужен сервис для проверки состояния сервиса синих, сервис приема флагов от красных,и отображения состояния игры для всех желающих.

Для чекера нужна база данных со всеми предыдущими флагами

# Backend:

* Python
* PostgreeSQL
* Redis
* Docker
* Nginx
* Celery
* Tornado

# Frontend:
ReactJS
---
## CTF в формате шоу    
В отличие от обычного Attack-defence, командам не нужно делиться на атакующих и защищающихся, вместо этого они все вместе ищут уязвмиости. Также для синей команды можно сделать более сложную сеть с большим количеством серверов и устройств. Можно добавить компоненты умного дома, сложные системы защиты и так далее.
Такой формат соревнований может быть зрелищным, но это требует очень тонкой настройки системы подсчета очков и разработки сети для синих.
