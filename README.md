setup and run application:
--------------------------
``` bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt 
python setup.py install
battle_field
```

Техпроцесс SMD уставновщика:
Стадия 1. Инициализация процесса.
    1) Загрузить файл с описанием pcb платы, получить описание.
(Необходимо либо работать с одним единым стандартом (если есть такой стандарт),
либо взять наиболее распространенный стандарт, конвертировать его в "свой" стандарт.)
    Что необходимо извлечь:
    А) Привязать систему координат платы либо к углу платы, либо к реперной точке. Найти эту точку на плате.
    Б) Информация в каком месте на координатной плоскости какой компонент должен быть и
        как он должен быть ориентирован.
    В) Информация о координатах всех монтажных медных площадках, на которые нужно наносить паяльную пасту

Стадия 2. Нанесение паяльной пасты.
Для каждой i-ой контактной площадки:
    1) Головка со шприцем с паяльной пастой передвигается в место с платой, камера делает снимок платы, распознает плату, находит реперные точки как основные ориентиры на плате, определяет точку начала координат из стадии 1
    2) относительно неё определяет свое местоположение
    3) головка перемещается (по координатам) в место, где должна быть площадка.
    4) делается снимок, уточняется положение контактной площадки относительно текущего положения головки
    5) корректируется положение головки
    6) головка опускается на площадку, наносится порция паяльной пасты

Стадия 3. Нанесение SMD компонентов из N лент
Для каждой i-ой ленты с SMD компонентами:
    1) подвести головку с камерой в то место, где находится лента c SMD компонентами
    2) сделать снимок, распознать ленту с SMD компонентами, распознать самый крайний компонент, 
    определить расстояние до него
    3) переместиться к его центру
    4) опустить головку, взять компонент
    5) переместиться в место с другой камерой, выполняющей снимок снизу
    6) сделать снимок с другой камеры, определить, как повернут захваченный компонент, а также по ориентирам, нанесенным на площадку, где устанавливается головка определить, насколько сдвинут центр компонента относительно центра захватывающей трубки
    7) сдвинуть головку (по координатам) в то место, где находится место под SMD компонент
    8) сделать снимок, распознать место, куда должен быть припаян компонент
    9) корректируем положение с учетом ошибки местоположения устанавливающей головки, того, насколько повернут компонент и того, насколько сдвинут центр компонента относительно захватывающей трубки
    10) опускаем компонент, бросаем его

Примечание:
    1) При каждом снимке срабатывает подсветка
    2) Перед работой с каждый изображением применяется калибровочная поправка конкретной камеры
