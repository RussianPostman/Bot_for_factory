Телеграм бот для промышленного предприятия ООО «Цинк» (lilmet.ru) является частью проекта цифровизации документооборота предприятия. С помощью него работники отчитываются о проделанной работе как при сдельной оплате труда (выбирая наименование, количество, количество брака), так и при почасовой оплате. Данные с пользователями и деталями хранятся в PostgreSQL. Для удобства, база данных синхронизирована с гугл таблицами.
Технологии: aiogram SQLAlchemy, alembic, Google API, Docker, apscheduler

В качестве описания проекта представляю ТЗ заказчика с некотьорыми комментариями:

```
Сотрудники изготавливают детали, их зарплата сдельная. В конце каждой смены они заносят данные в таблицу при помощи бота.
Имеют возможность посмотреть сумму заработанных денег за сегодня и за промежуток с 5 по 4 число. У деталей есть 10 категорий,
в каждой категории по 50 деталей +-. У пользователей три роли: оператор, литейщик, админ. У литейщика и оператора разные расценки на 
одну и ту же делать.
Для сдачи отчета - пользователь выбирает категорию, далее выбирает деталь и вводит количество сделанных деталей, следующей 
кнопкой указывает количество брака, была ли упаковка и может оставить комментарий в свободной форме. Пользователь может 
сдать несколько отчетов за смену. 

Данные хранятся в базе данных, синхронизируются с гугл таблицами. (синхронизацию проводит администратор) 
 - Таблицы куда бот загружает данные:
1. Таблица конкретного работника. При регистрации должна создаться таблица для каждого работника. В ней хранится история действий 
2.  Таблица где каждый месяц формируется итоговая ЗП каждого работника и фиксируется в истории.

 - Бот берёт данные и отслеживает изменения в таблице с расценками на детали

— Права доступа —
Работник - 
1) отправить отчёт
2) узнать сколько наработал в этом месяце (начиная с последнего 5го числа) 

Админ -  
1. Добавить пользователя.
2. Удалить пользователя
3. Открыть таблицу с деталями и отчетом.
4. Узнать отчет пользователя с 5 по 4 число, введя ID 
```

