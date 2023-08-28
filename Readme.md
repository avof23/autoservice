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
}

Table boxes {
  id serial [primary key]
  box_name varchar(20) [not null]
  size smallint [default: 1]
}

Table orders {
  id bigserial [primary key]
  status_id integer [not null, ref: > statuses.id]
  start_date timestamp [default: `now()`]
  end_date timestamp
  credit_summ money [default: 0]
  order_summ money [default: 0]
  client_id bigint [ref: > clients.id]
  master_id integer [ref: > masters.id]
  box_id integer [ref: > boxes.id]
  description text
  Note: 'Stores orders data'

  indexes {
    id
    start_date [name: 'created_at_index', note: 'Date']
    end_date [name: 'close_at_index', note: 'Date']
  }
}

Table statuses {
  id smallserial [primary key]
  status varchar(15) [not null]
}

Table clients {
  id bigserial [primary key]
  name varchar(30)
  phone varchar(15)
  email varchar(30)
  auto varchar(30)
  number varchar(10) [not null, unique]
  description text
  Note: 'Stores clients data'

  indexes {
      (id, number) [pk] // composite primary key
  }
}

Table works {
  id bigserial [primary key]
  work_name varchar(200) [not null]
  price money [default: 0]
  norm_hour real [default: 1]
  description text
  Note: 'Stores autoservice work data'

  indexes {
    work_name
  }
}

Table parts {
  id bigserial [primary key]
  part_name varchar(200) [not null]
  part_number varchar(15)
  original_number varchar(15)
  price money [default: 0]
  compatibility varchar(150)
  description text
  Note: 'Stores auto parts data'

  indexes {
      part_name
      (part_number, original_number) [unique]
  }
}

Table content_orders {
  id bigserial [primary key]
  order_id bigint [not null, ref: > orders.id]
  work_id bigint [ref: > works.id]
  part_id bigint [ref: > parts.id]
  Note: 'Stores item of orders'
}
```

### Author
A.Vlashchenkov