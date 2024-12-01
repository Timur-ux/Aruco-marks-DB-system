insert into
  locations (name, min_pos, max_pos)
values
  (
    'hall',
    array[0.0, 0.0, 0.0],
    array[5.0, 5.0, 5.0]
  ),
  (
    'main_storage',
    array[-45.0, 0.0, 0.0],
    array[0.0, 15.0, 25.0]
  ),
  (
    'buffer_storage',
    array[5.0, 0.0, 0.0],
    array[10.0, 7.0, 10.0]
  );

insert into
  mark_types (name, family)
values
  (
    'aruco',
    null
  ),
  (
    'apriltag',
    'tag25h9'
  ),
  (
    'apriltag',
    'tagStandart41h12'
  ),
  (
    'aruco',
    'MIP_36h12'
  );

insert into
  privilege (name)
values
  ( 'read' ),
  ( 'edit_table' ),
  ( 'edit_users' );

insert into
  access(name)
values
  (
    'user'
  ),
  (
    'redactor'
  ),
  (
    'administrator'
  );

insert into
  access_to_privileges(access_id, privilege_id)
values
  (
    (select id from access where name='user'),
    (select id from privilege where name = 'read')
  ),
  (
    (select id from access where name='redactor'),
    (select id from privilege where name = 'read')
  ),
  (
    (select id from access where name='redactor'),
    (select id from privilege where name = 'edit_table')
  ),
  (
    (select id from access where name='administrator'),
    (select id from privilege where name = 'edit_table')
  ),
  (
    (select id from access where name='administrator'),
    (select id from privilege where name = 'edit_users')
  ),
  (
    (select id from access where name='administrator'),
    (select id from privilege where name = 'read')
  );



insert into
 users(access_level, login, password)
values
  (
    (select id from access where name = 'administrator'),
    'admin',
    '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'
  ),
  (
    (select id from access where name = 'administrator'),
    'admin2',
    '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'
  );

insert into
  marks(mark_id, mark_type)
values
  (
    24,
    (select id from mark_types where name = 'aruco' limit 1)
  ),
  (
    124,
    (select id from mark_types where name = 'aruco' limit 1)
  ),
  (
    22,
    (select id from mark_types where name = 'apriltag' limit 1)
  ),
  (
    18,
    (select id from mark_types where name = 'aruco' limit 1)
  );
