--
-- PostgreSQL database dump
--

\restrict fLOljKrK2fv8egkdSibjefWcSaN98kPEzHmKOELWXaJoIKSpQoP7nMh7MJ729al

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.sessions DROP CONSTRAINT IF EXISTS sessions_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.saved_properties DROP CONSTRAINT IF EXISTS saved_properties_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.saved_properties DROP CONSTRAINT IF EXISTS saved_properties_property_id_fkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_email_key;
ALTER TABLE IF EXISTS ONLY public.sessions DROP CONSTRAINT IF EXISTS sessions_pkey;
ALTER TABLE IF EXISTS ONLY public.saved_properties DROP CONSTRAINT IF EXISTS saved_properties_pkey;
ALTER TABLE IF EXISTS ONLY public.properties DROP CONSTRAINT IF EXISTS properties_pkey;
ALTER TABLE IF EXISTS public.users ALTER COLUMN user_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.sessions ALTER COLUMN session_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.saved_properties ALTER COLUMN saved_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.properties ALTER COLUMN property_id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.users_user_id_seq;
DROP TABLE IF EXISTS public.users;
DROP SEQUENCE IF EXISTS public.sessions_session_id_seq;
DROP TABLE IF EXISTS public.sessions;
DROP SEQUENCE IF EXISTS public.saved_properties_saved_id_seq;
DROP TABLE IF EXISTS public.saved_properties;
DROP SEQUENCE IF EXISTS public.properties_property_id_seq;
DROP TABLE IF EXISTS public.properties;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: properties; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.properties (
    property_id integer NOT NULL,
    title character varying(150) NOT NULL,
    region character varying(50) NOT NULL,
    neighborhood character varying(100) NOT NULL,
    price bigint NOT NULL,
    description text,
    image_path text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: properties_property_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.properties_property_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: properties_property_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.properties_property_id_seq OWNED BY public.properties.property_id;


--
-- Name: saved_properties; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.saved_properties (
    saved_id integer NOT NULL,
    user_id integer,
    property_id integer,
    saved_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: saved_properties_saved_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.saved_properties_saved_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: saved_properties_saved_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.saved_properties_saved_id_seq OWNED BY public.saved_properties.saved_id;


--
-- Name: sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sessions (
    session_id integer NOT NULL,
    user_id integer,
    login_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    is_active boolean DEFAULT true
);


--
-- Name: sessions_session_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sessions_session_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sessions_session_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sessions_session_id_seq OWNED BY public.sessions.session_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    full_name character varying(100) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: properties property_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.properties ALTER COLUMN property_id SET DEFAULT nextval('public.properties_property_id_seq'::regclass);


--
-- Name: saved_properties saved_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saved_properties ALTER COLUMN saved_id SET DEFAULT nextval('public.saved_properties_saved_id_seq'::regclass);


--
-- Name: sessions session_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessions ALTER COLUMN session_id SET DEFAULT nextval('public.sessions_session_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: properties; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.properties (property_id, title, region, neighborhood, price, description, image_path, created_at) FROM stdin;
1	3 Bedroom Duplex	Mainland	Ikeja	35000000	Spacious duplex with parking and modern finishing.	assets/images/ikeja_duplex.jpg	2026-05-21 22:09:20.277902
2	Modern Mini Flat	Mainland	Yaba	18000000	Affordable mini flat close to tech hubs and transport.	assets/images/yaba_flat.jpg	2026-05-21 22:09:20.277902
3	Luxury Apartment	Mainland	Surulere	42000000	Elegant apartment with premium interiors.	assets/images/surulere_apartment.jpg	2026-05-21 22:09:20.277902
4	Family House	Mainland	Maryland	55000000	Large family house in a quiet neighborhood.	assets/images/maryland_house.jpg	2026-05-21 22:09:20.277902
5	Executive Flat	Mainland	Gbagada	28000000	Modern flat with excellent road access.	assets/images/gbagada_flat.jpg	2026-05-21 22:09:20.277902
6	Luxury Penthouse	Island	Lekki	120000000	Premium penthouse with ocean view.	assets/images/lekki_penthouse.jpg	2026-05-21 22:09:20.277902
7	Beachfront Apartment	Island	Victoria Island	95000000	Apartment close to business districts and beaches.	assets/images/vi_apartment.jpg	2026-05-21 22:09:20.277902
8	Smart Home Duplex	Island	Ikoyi	150000000	Fully automated smart home with security systems.	assets/images/ikoyi_duplex.jpg	2026-05-21 22:09:20.277902
9	Contemporary Apartment	Island	Ajah	45000000	Stylish apartment in a fast-growing area.	assets/images/ajah_apartment.jpg	2026-05-21 22:09:20.277902
10	Luxury Terrace	Island	Chevron	70000000	Modern terrace property with premium facilities.	assets/images/chevron_terrace.jpg	2026-05-21 22:09:20.277902
\.


--
-- Data for Name: saved_properties; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.saved_properties (saved_id, user_id, property_id, saved_at) FROM stdin;
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sessions (session_id, user_id, login_time, is_active) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (user_id, full_name, email, password_hash, created_at) FROM stdin;
\.


--
-- Name: properties_property_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.properties_property_id_seq', 10, true);


--
-- Name: saved_properties_saved_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.saved_properties_saved_id_seq', 1, false);


--
-- Name: sessions_session_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sessions_session_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- Name: properties properties_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.properties
    ADD CONSTRAINT properties_pkey PRIMARY KEY (property_id);


--
-- Name: saved_properties saved_properties_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saved_properties
    ADD CONSTRAINT saved_properties_pkey PRIMARY KEY (saved_id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (session_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: saved_properties saved_properties_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saved_properties
    ADD CONSTRAINT saved_properties_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(property_id) ON DELETE CASCADE;


--
-- Name: saved_properties saved_properties_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saved_properties
    ADD CONSTRAINT saved_properties_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: sessions sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict fLOljKrK2fv8egkdSibjefWcSaN98kPEzHmKOELWXaJoIKSpQoP7nMh7MJ729al

