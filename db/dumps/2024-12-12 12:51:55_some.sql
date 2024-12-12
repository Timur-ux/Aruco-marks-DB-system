--
-- PostgreSQL database dump
--

-- Dumped from database version 13.3 (Debian 13.3-1.pgdg100+1)
-- Dumped by pg_dump version 13.3 (Debian 13.3-1.pgdg100+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: access; Type: TABLE; Schema: public; Owner: Raison
--

CREATE TABLE public.access (
    id bigint NOT NULL,
    name character varying(100)
);


ALTER TABLE public.access OWNER TO "Raison";

--
-- Name: access_id_seq; Type: SEQUENCE; Schema: public; Owner: Raison
--

CREATE SEQUENCE public.access_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.access_id_seq OWNER TO "Raison";

--
-- Name: access_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Raison
--

ALTER SEQUENCE public.access_id_seq OWNED BY public.access.id;


--
-- Name: access_to_privileges; Type: TABLE; Schema: public; Owner: Raison
--

CREATE TABLE public.access_to_privileges (
    access_id bigint NOT NULL,
    privilege_id bigint NOT NULL
);


ALTER TABLE public.access_to_privileges OWNER TO "Raison";

--
-- Name: locations; Type: TABLE; Schema: public; Owner: Raison
--

CREATE TABLE public.locations (
    id bigint NOT NULL,
    name character varying(200),
    min_pos double precision[] NOT NULL,
    max_pos double precision[] NOT NULL
);


ALTER TABLE public.locations OWNER TO "Raison";

--
-- Name: locations_id_seq; Type: SEQUENCE; Schema: public; Owner: Raison
--

CREATE SEQUENCE public.locations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.locations_id_seq OWNER TO "Raison";

--
-- Name: locations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Raison
--

ALTER SEQUENCE public.locations_id_seq OWNED BY public.locations.id;


--
-- Name: mark_types; Type: TABLE; Schema: public; Owner: Raison
--

CREATE TABLE public.mark_types (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    family character varying(100)
);


ALTER TABLE public.mark_types OWNER TO "Raison";

--
-- Name: mark_types_id_seq; Type: SEQUENCE; Schema: public; Owner: Raison
--

CREATE SEQUENCE public.mark_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mark_types_id_seq OWNER TO "Raison";

--
-- Name: mark_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Raison
--

ALTER SEQUENCE public.mark_types_id_seq OWNED BY public.mark_types.id;


--
-- Name: marks; Type: TABLE; Schema: public; Owner: Raison
--

CREATE TABLE public.marks (
    id bigint NOT NULL,
    mark_id integer NOT NULL,
    mark_type bigint NOT NULL
);


ALTER TABLE public.marks OWNER TO "Raison";

--
-- Name: marks_id_seq; Type: SEQUENCE; Schema: public; Owner: Raison
--

CREATE SEQUENCE public.marks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marks_id_seq OWNER TO "Raison";

--
-- Name: marks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Raison
--

ALTER SEQUENCE public.marks_id_seq OWNED BY public.marks.id;


--
-- Name: marks_on_objects; Type: TABLE; Schema: public; Owner: Raison
--

CREATE TABLE public.marks_on_objects (
    mark_id bigint NOT NULL,
    object_id bigint NOT NULL,
    relative_pos double precision[] NOT NULL
);


ALTER TABLE public.marks_on_objects OWNER TO "Raison";

--
-- Name: objects; Type: TABLE; Schema: public; Owner: Raison
--

CREATE TABLE public.objects (
    id bigint NOT NULL,
    name character varying(200),
    size double precision[],
    location_id bigint NOT NULL,
    last_position double precision[],
    last_update_time timestamp without time zone
);


ALTER TABLE public.objects OWNER TO "Raison";

--
-- Name: objects_id_seq; Type: SEQUENCE; Schema: public; Owner: Raison
--

CREATE SEQUENCE public.objects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.objects_id_seq OWNER TO "Raison";

--
-- Name: objects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Raison
--

ALTER SEQUENCE public.objects_id_seq OWNED BY public.objects.id;


--
-- Name: privilege; Type: TABLE; Schema: public; Owner: Raison
--

CREATE TABLE public.privilege (
    id bigint NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.privilege OWNER TO "Raison";

--
-- Name: privilege_id_seq; Type: SEQUENCE; Schema: public; Owner: Raison
--

CREATE SEQUENCE public.privilege_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.privilege_id_seq OWNER TO "Raison";

--
-- Name: privilege_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Raison
--

ALTER SEQUENCE public.privilege_id_seq OWNED BY public.privilege.id;


--
-- Name: user_actions; Type: TABLE; Schema: public; Owner: Raison
--

CREATE TABLE public.user_actions (
    id bigint NOT NULL,
    action character varying(100) NOT NULL,
    user_id bigint NOT NULL,
    "time" timestamp without time zone NOT NULL
);


ALTER TABLE public.user_actions OWNER TO "Raison";

--
-- Name: user_actions_id_seq; Type: SEQUENCE; Schema: public; Owner: Raison
--

CREATE SEQUENCE public.user_actions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_actions_id_seq OWNER TO "Raison";

--
-- Name: user_actions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Raison
--

ALTER SEQUENCE public.user_actions_id_seq OWNED BY public.user_actions.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: Raison
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    access_level bigint NOT NULL,
    login character varying(100),
    password character varying(64)
);


ALTER TABLE public.users OWNER TO "Raison";

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: Raison
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO "Raison";

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Raison
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: access id; Type: DEFAULT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.access ALTER COLUMN id SET DEFAULT nextval('public.access_id_seq'::regclass);


--
-- Name: locations id; Type: DEFAULT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.locations ALTER COLUMN id SET DEFAULT nextval('public.locations_id_seq'::regclass);


--
-- Name: mark_types id; Type: DEFAULT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.mark_types ALTER COLUMN id SET DEFAULT nextval('public.mark_types_id_seq'::regclass);


--
-- Name: marks id; Type: DEFAULT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.marks ALTER COLUMN id SET DEFAULT nextval('public.marks_id_seq'::regclass);


--
-- Name: objects id; Type: DEFAULT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.objects ALTER COLUMN id SET DEFAULT nextval('public.objects_id_seq'::regclass);


--
-- Name: privilege id; Type: DEFAULT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.privilege ALTER COLUMN id SET DEFAULT nextval('public.privilege_id_seq'::regclass);


--
-- Name: user_actions id; Type: DEFAULT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.user_actions ALTER COLUMN id SET DEFAULT nextval('public.user_actions_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: access; Type: TABLE DATA; Schema: public; Owner: Raison
--

COPY public.access (id, name) FROM stdin;
1	user
2	redactor
3	administrator
\.


--
-- Data for Name: access_to_privileges; Type: TABLE DATA; Schema: public; Owner: Raison
--

COPY public.access_to_privileges (access_id, privilege_id) FROM stdin;
1	1
2	1
2	2
3	2
3	3
3	1
\.


--
-- Data for Name: locations; Type: TABLE DATA; Schema: public; Owner: Raison
--

COPY public.locations (id, name, min_pos, max_pos) FROM stdin;
1	hall	{0,0,0}	{5,5,5}
2	main_storage	{-45,0,0}	{0,15,25}
3	buffer_storage	{5,0,0}	{10,7,10}
\.


--
-- Data for Name: mark_types; Type: TABLE DATA; Schema: public; Owner: Raison
--

COPY public.mark_types (id, name, family) FROM stdin;
1	aruco	\N
2	apriltag	tag25h9
3	apriltag	tagStandart41h12
4	aruco	MIP_36h12
\.


--
-- Data for Name: marks; Type: TABLE DATA; Schema: public; Owner: Raison
--

COPY public.marks (id, mark_id, mark_type) FROM stdin;
1	24	1
2	124	1
3	22	2
4	18	1
\.


--
-- Data for Name: marks_on_objects; Type: TABLE DATA; Schema: public; Owner: Raison
--

COPY public.marks_on_objects (mark_id, object_id, relative_pos) FROM stdin;
\.


--
-- Data for Name: objects; Type: TABLE DATA; Schema: public; Owner: Raison
--

COPY public.objects (id, name, size, location_id, last_position, last_update_time) FROM stdin;
\.


--
-- Data for Name: privilege; Type: TABLE DATA; Schema: public; Owner: Raison
--

COPY public.privilege (id, name) FROM stdin;
1	read
2	edit_table
3	edit_users
\.


--
-- Data for Name: user_actions; Type: TABLE DATA; Schema: public; Owner: Raison
--

COPY public.user_actions (id, action, user_id, "time") FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: Raison
--

COPY public.users (id, access_level, login, password) FROM stdin;
1	3	admin	$2b$12$xrWOJHsG3HP0Zvrz.JjT7etvXIcL2fDKJDbyALbRQtnBRVg9rYF7u
2	3	admin2	$2b$12$xrWOJHsG3HP0Zvrz.JjT7etvXIcL2fDKJDbyALbRQtnBRVg9rYF7u
\.


--
-- Name: access_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Raison
--

SELECT pg_catalog.setval('public.access_id_seq', 3, true);


--
-- Name: locations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Raison
--

SELECT pg_catalog.setval('public.locations_id_seq', 3, true);


--
-- Name: mark_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Raison
--

SELECT pg_catalog.setval('public.mark_types_id_seq', 4, true);


--
-- Name: marks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Raison
--

SELECT pg_catalog.setval('public.marks_id_seq', 4, true);


--
-- Name: objects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Raison
--

SELECT pg_catalog.setval('public.objects_id_seq', 1, false);


--
-- Name: privilege_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Raison
--

SELECT pg_catalog.setval('public.privilege_id_seq', 3, true);


--
-- Name: user_actions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Raison
--

SELECT pg_catalog.setval('public.user_actions_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Raison
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: access access_pkey; Type: CONSTRAINT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.access
    ADD CONSTRAINT access_pkey PRIMARY KEY (id);


--
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (id);


--
-- Name: mark_types mark_types_pkey; Type: CONSTRAINT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.mark_types
    ADD CONSTRAINT mark_types_pkey PRIMARY KEY (id);


--
-- Name: marks marks_pkey; Type: CONSTRAINT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.marks
    ADD CONSTRAINT marks_pkey PRIMARY KEY (id);


--
-- Name: objects objects_pkey; Type: CONSTRAINT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.objects
    ADD CONSTRAINT objects_pkey PRIMARY KEY (id);


--
-- Name: privilege privilege_pkey; Type: CONSTRAINT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.privilege
    ADD CONSTRAINT privilege_pkey PRIMARY KEY (id);


--
-- Name: user_actions user_actions_pkey; Type: CONSTRAINT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.user_actions
    ADD CONSTRAINT user_actions_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: Raison
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

