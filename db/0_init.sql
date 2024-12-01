create database ArucoService;

\c ArucoService

create table  marks (
  id bigserial primary key,
  mark_id int not null,
  mark_type bigint not null
);

create table  objects (
  id bigserial primary key,
  name varchar(200),
  size float[3],
  location_id bigint not null,
  last_position float[3],
  last_update_time timestamp
);

create table  locations (
  id bigserial primary key,
  name varchar(200),
  min_pos float[3] not null,
  max_pos float[3] not null
);

create table  mark_types (
  id bigserial primary key,
  name varchar(100) not null,
  family varchar(100)
);

create table  user_actions (
  id bigserial primary key,
  action varchar(100) not null,
  user_id bigint not null,
  time timestamp not null
);

create table  users (
  id bigserial primary key,
  access_level bigint not null,
  login varchar(100),
  password varchar(64)
);

create table access_to_privileges (
  access_id bigint not null,
  privilege_id bigint not null
);

create table  access (
  id bigserial primary key,
  name varchar(100)
);

create table  privilege (
  id bigserial primary key,
  name varchar(100) not null
);

create table  marks_on_objects (
  mark_id bigint not null,
  object_id bigint not null,
  relative_pos float[3] not null
);
