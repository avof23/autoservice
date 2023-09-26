# Telegram-bot for auto-service

### Description

#### Basic functionality
The bot accepts requests to record a car for a service.
After determining the free date, it makes an entry and assigns an order number.
By number, you can track the status of the order and see the cost.

#### Additional functionality
- Receive push notifications about a status change or an upcoming scheduled event
- Get a full invoice by order number

### Database structure

```
Project autoservice {
  database_type: 'PostgreSQL'
  Note: 'Telegram-bot for automation  small autoservice'
}

Table masters {
  id serial [primary key]
  master_name varchar(30) [not null]
  qualification varchar(15) [default: 'gen']
}

Table orders {
  id bigserial [primary key]
  status_id integer [not null, ref: > statuses.id]
  start_date timestamp [default: `now()`]
  end_date timestamp
  credit_summ numeric(8, 2) [default: 0.0]
  order_summ numeric(8, 2) [default: 0.0]
  client_id bigint [ref: > clients.id]
  master_id integer [ref: > masters.id]
  description text
  Note: 'Stores orders data'
}

Table statuses {
  id serial [primary key]
  status varchar(15) [not null]
}

Table clients {
  id bigserial [primary key, Note:'chat_id']
  name varchar(30)
  phone varchar(15)
  email varchar(30)
  auto varchar(30)
  number varchar(10) [unique]
  description text
  Note: 'Stores clients data'

  indexes {
      (id, number)
  }
}

Table works {
  id bigserial [primary key]
  work_name varchar(200) [not null]
  price numeric(8, 2) [default: 0.0]
  norm_min integer [default: 60]
  for_selection boolean [default: false]
  requirements varchar(5) [default: 'gen']
  description text
  Note: 'Stores autoservice work data'
}

Table parts {
  id bigserial [primary key]
  part_name varchar(200) [not null]
  part_number varchar(15)
  original_number varchar(15)
  price numeric(8, 2) [default: 0.0]
  compatibility varchar(150)
  description text
  Note: 'Stores auto parts data'
}

Table content_orders {
  id bigserial [primary key]
  order_id bigint [not null, ref: > orders.id]
  work_id bigint [ref: > works.id]
  part_id bigint [ref: > parts.id]
  quantity integer [default: 1]
  Note: 'Stores item of orders'
}
```

- При запросе /status надо определять по user_id есть ли такой пользователь в базе
и выводить его активный статус заказа
- push уведомления
- меню
- Отдачу заказ-наряда в виде pdf


### Author
A.Vlashchenkov