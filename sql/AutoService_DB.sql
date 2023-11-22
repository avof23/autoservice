CREATE TABLE "masters" (
  "id" serial PRIMARY KEY,
  "master_name" varchar(30) NOT NULL
);

CREATE TABLE "boxes" (
  "id" serial PRIMARY KEY,
  "box_name" varchar(20) NOT NULL,
  "size" smallint DEFAULT 1
);

CREATE TABLE "orders" (
  "id" bigserial PRIMARY KEY,
  "status_id" integer NOT NULL,
  "start_date" timestamp DEFAULT (now()),
  "end_date" timestamp,
  "credit_summ" "numeric(8, 2)" DEFAULT 0,
  "order_summ" "numeric(8, 2)" DEFAULT 0,
  "client_id" bigint,
  "master_id" integer,
  "box_id" integer,
  "description" text
);

CREATE TABLE "statuses" (
  "id" serial PRIMARY KEY,
  "status" varchar(15) NOT NULL
);

CREATE TABLE "clients" (
  "id" bigserial PRIMARY KEY,
  "name" varchar(30),
  "phone" varchar(15),
  "email" varchar(30),
  "auto" varchar(30),
  "number" varchar(10) UNIQUE NOT NULL,
  "description" text
);

CREATE TABLE "works" (
  "id" bigserial PRIMARY KEY,
  "work_name" varchar(200) NOT NULL,
  "price" "numeric(8, 2)" DEFAULT 0,
  "norm_hour" "numeric(4, 2)" DEFAULT 1,
  "for_selection" boolean DEFAULT false,
  "description" text
);

CREATE TABLE "parts" (
  "id" bigserial PRIMARY KEY,
  "part_name" varchar(200) NOT NULL,
  "part_number" varchar(15),
  "original_number" varchar(15),
  "price" "numeric(8, 2)" DEFAULT 0,
  "compatibility" varchar(150),
  "description" text
);

CREATE TABLE "content_orders" (
  "id" bigserial PRIMARY KEY,
  "order_id" bigint NOT NULL,
  "work_id" bigint,
  "part_id" bigint,
  "quantity" integer DEFAULT 1
);

CREATE INDEX ON "clients" ("id", "number");

COMMENT ON TABLE "orders" IS 'Stores orders data';

COMMENT ON TABLE "clients" IS 'Stores clients data';

COMMENT ON TABLE "works" IS 'Stores autoservice work data';

COMMENT ON TABLE "parts" IS 'Stores auto parts data';

COMMENT ON TABLE "content_orders" IS 'Stores item of orders';

ALTER TABLE "orders" ADD FOREIGN KEY ("status_id") REFERENCES "statuses" ("id");

ALTER TABLE "orders" ADD FOREIGN KEY ("client_id") REFERENCES "clients" ("id");

ALTER TABLE "orders" ADD FOREIGN KEY ("master_id") REFERENCES "masters" ("id");

ALTER TABLE "orders" ADD FOREIGN KEY ("box_id") REFERENCES "boxes" ("id");

ALTER TABLE "content_orders" ADD FOREIGN KEY ("order_id") REFERENCES "orders" ("id");

ALTER TABLE "content_orders" ADD FOREIGN KEY ("work_id") REFERENCES "works" ("id");

ALTER TABLE "content_orders" ADD FOREIGN KEY ("part_id") REFERENCES "parts" ("id");
