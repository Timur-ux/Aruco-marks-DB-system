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
  access(name, privileges)
values
  (
    'user',
    array(select id from privilege where name = 'read')
  ),
  (
    'redactor',
    array(select id from privilege
     where name = 'read' or name = 'edit_table'
    )
  ),
  (
    'administrator',
    array(select id from privilege)
  );

insert into
 users(access_level, login, password)
values
  (
    (select id from access where name = 'administrator'),
    'admin',
    '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'
  );
