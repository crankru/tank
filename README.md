# Описание прогресса
В этом файле я буду рассказывать о прогрессе в работе над роботом. Детали заказываю на алиэкспрессе так что процесс будет неспешным.

## Сборка первых деталей
- Шасси для робота
- Raspberry pi 3B
- Плата драйвера для моторов и сервоприводов Stepper Motor HAT v0.1

После сборки шасси и подключения малины с драйвером к стационарному питанию получилось примерно следующее

![Танк версия 0.1](./docs/images/20180501_214324_.jpg)

Целая куча проводов от моторов это датчики Холла, не придумал для чего они могут понадобиться.

## Мысли о концепции управления
Изначально я планировал сделать управление через приложение blynk.cc и даже сделал прототип управления ([blynk.py](/blynk.py)), но потом я понял что в этом приложении уместить все элементы управления на маленьком экранчике смартфона не получится. Было решено пилить веб-интерфейс. В качестве языка бекэнда выбрал опять же Python, а фреймворком решил использовать Flask. Почти сразу стало понятно что делать интерфейс на ajax неправильно, получалась достаточно большая задержка. Так что я переписал все на websocket.

## Первая проба видео
Вначале я тупо взял самую простую веб-камеру и прикрутил ее к малине. Насколько я потом понял мне повезло с моделью, т.к. далеко не все камеры работают с малиной.

![Первая проба с видео камерой](./docs/images/20180508_204327_.jpg)

В качестве библиотеки для работы с видео была выбрана OpenCV. Пока на удивление все работало.

## Питание от аккумулятора
Дальше ко мне пришли детали для организации автономного питания:
 - LiPo аккумулятор (7.4v 5200mA/h)
 - Понижающий преобразователь питания с вольтметром (один для малины и еще один для драйвера моторов)
 - Модуль защиты от переразряда аккумулятора

 ## Первые проблемы
 - Неработает вольтметр на плате защиты от переразряда и умирает банка на аккуме
 - При включенном видео очень сильно тормозит управление