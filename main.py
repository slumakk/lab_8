from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, Session, relationship
import datetime

# Підключення до бази даних
engine = create_engine('sqlite:///db.db', echo=False)
Base = declarative_base()

# Оголошення класів моделей
class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

class Categories(Base):
    __tablename__ = 'Categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String, nullable=False)

class Tasks(Base):
    __tablename__ = 'Tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(Date)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('Categories.id'), nullable=False)

    user = relationship("Users")
    category = relationship("Categories")

# Створення таблиць
Base.metadata.create_all(engine)

# Створення сесії
def create_session():
    return Session(engine)

# CRUD

# Створення нового користувача
def create_user(session, username, email, password):
    new_user = Users(username=username, email=email, password=password)
    session.add(new_user)
    session.commit()

# Отримання всіх користувачів
def get_all_users(session):
    return session.query(Users).all()

# Оновлення інформації про користувача
def update_user(session, user_id, new_username, new_email, new_password):
    user_to_update = session.query(Users).filter_by(id=user_id).first()
    if user_to_update:
        user_to_update.username = new_username
        user_to_update.email = new_email
        user_to_update.password = new_password
        session.commit()

# Видалення користувача
def delete_user(session, user_id):
    user_to_delete = session.query(Users).filter_by(id=user_id).first()
    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()

# Створення нового таску
def create_task(session, task_name, description, due_date, user_id, category_id):
    new_task = Tasks(task=task_name, description=description, due_date=due_date, user_id=user_id, category_id=category_id)
    session.add(new_task)
    session.commit()

# Отримання всіх тасків
def get_all_tasks(session):
    return session.query(Tasks).all()

# Оновлення інформації про таск
def update_task(session, task_id, new_task_name, new_description, new_due_date, new_user_id, new_category_id):
    task_to_update = session.query(Tasks).filter_by(id=task_id).first()
    if task_to_update:
        task_to_update.task = new_task_name
        task_to_update.description = new_description
        task_to_update.due_date = new_due_date
        task_to_update.user_id = new_user_id
        task_to_update.category_id = new_category_id
        session.commit()

# Видалення таску
def delete_task(session, task_id):
    task_to_delete = session.query(Tasks).filter_by(id=task_id).first()
    if task_to_delete:
        session.delete(task_to_delete)
        session.commit()

def current_timestamp():
    return datetime.datetime.now()

# Використання операцій CRUD
session = create_session()

# Створення нового користувача
create_user(session, 'JohnDoe', 'john.doe@email.com', 'password123')

# Оновлення інформації про користувача
update_user(session, user_id=10, new_username='UpdatedUser', new_email='updated@email.com', new_password='newpassword')

# Отримання всіх користувачів
all_users = get_all_users(session)
print("Всі користувачі:")
for user in all_users:
    print(user.id, user.username, user.email, user.password)

# Видалення користувача
delete_user(session, user_id=10)

# повторний вивід користувачів
all_users = get_all_users(session)
print("Всі користувачі:")
for user in all_users:
    print(user.id, user.username, user.email, user.password)

# Створення нового таску
create_task(session, 'Complete Project', 'Finish project report and submit it', current_timestamp(), user_id=1, category_id=1)

# Оновлення інформації про таск
update_task(session, task_id=10, new_task_name='Updated Task', new_description='Updated description', new_due_date=current_timestamp(), new_user_id=2, new_category_id=2)

# Отримання всіх тасків
all_tasks = get_all_tasks(session)
print("Всі таски:")
for task in all_tasks:
    print(task.id, task.task, task.description, task.due_date, task.user_id, task.category_id)

# Видалення таску
delete_task(session, task_id=10)

# повторне Отримання всіх тасків
all_tasks = get_all_tasks(session)
print("Всі таски:")
for task in all_tasks:
    print(task.id, task.task, task.description, task.due_date, task.user_id, task.category_id)

# Закриття сесії
session.close()