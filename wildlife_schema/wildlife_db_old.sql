--
-- PostgreSQL database dump
--

-- Dumped from database version 10.4 (Ubuntu 10.4-0ubuntu0.18.04)
-- Dumped by pg_dump version 10.4 (Ubuntu 10.4-0ubuntu0.18.04)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: basemap_data; Type: SCHEMA; Schema: -; Owner: wildlife_db
--

CREATE SCHEMA basemap_data;


ALTER SCHEMA basemap_data OWNER TO wildlife_db;

--
-- Name: dev_data; Type: SCHEMA; Schema: -; Owner: wildlife_db
--

CREATE SCHEMA dev_data;


ALTER SCHEMA dev_data OWNER TO wildlife_db;

--
-- Name: prod_data; Type: SCHEMA; Schema: -; Owner: wildlife_db
--

CREATE SCHEMA prod_data;


ALTER SCHEMA prod_data OWNER TO wildlife_db;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- Name: city_seq; Type: SEQUENCE; Schema: basemap_data; Owner: wildlife_db
--

CREATE SEQUENCE basemap_data.city_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9999999999999999
    CACHE 1;


ALTER TABLE basemap_data.city_seq OWNER TO wildlife_db;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: city; Type: TABLE; Schema: basemap_data; Owner: wildlife_db
--

CREATE TABLE basemap_data.city (
    city_id integer DEFAULT nextval('basemap_data.city_seq'::regclass) NOT NULL,
    name character(100) NOT NULL,
    polygon public.geometry(MultiPolygon,4326)
);


ALTER TABLE basemap_data.city OWNER TO wildlife_db;

--
-- Name: country_seq; Type: SEQUENCE; Schema: basemap_data; Owner: wildlife_db
--

CREATE SEQUENCE basemap_data.country_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9999999999999999
    CACHE 1;


ALTER TABLE basemap_data.country_seq OWNER TO wildlife_db;

--
-- Name: country; Type: TABLE; Schema: basemap_data; Owner: wildlife_db
--

CREATE TABLE basemap_data.country (
    country_id integer DEFAULT nextval('basemap_data.country_seq'::regclass) NOT NULL,
    name character(100) NOT NULL,
    polygon public.geometry(MultiPolygon,4326)
);


ALTER TABLE basemap_data.country OWNER TO wildlife_db;

--
-- Name: county_seq; Type: SEQUENCE; Schema: basemap_data; Owner: wildlife_db
--

CREATE SEQUENCE basemap_data.county_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9999999999999999
    CACHE 1;


ALTER TABLE basemap_data.county_seq OWNER TO wildlife_db;

--
-- Name: county; Type: TABLE; Schema: basemap_data; Owner: wildlife_db
--

CREATE TABLE basemap_data.county (
    county_id integer DEFAULT nextval('basemap_data.county_seq'::regclass) NOT NULL,
    name character(100) NOT NULL,
    polygon public.geometry(MultiPolygon,4326)
);


ALTER TABLE basemap_data.county OWNER TO wildlife_db;

--
-- Name: nat_for_seq; Type: SEQUENCE; Schema: basemap_data; Owner: wildlife_db
--

CREATE SEQUENCE basemap_data.nat_for_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9999999999999999
    CACHE 1;


ALTER TABLE basemap_data.nat_for_seq OWNER TO wildlife_db;

--
-- Name: nat_mon_seq; Type: SEQUENCE; Schema: basemap_data; Owner: wildlife_db
--

CREATE SEQUENCE basemap_data.nat_mon_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9999999999999999
    CACHE 1;


ALTER TABLE basemap_data.nat_mon_seq OWNER TO wildlife_db;

--
-- Name: nat_park_seq; Type: SEQUENCE; Schema: basemap_data; Owner: wildlife_db
--

CREATE SEQUENCE basemap_data.nat_park_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9999999999999999
    CACHE 1;


ALTER TABLE basemap_data.nat_park_seq OWNER TO wildlife_db;

--
-- Name: national_forest; Type: TABLE; Schema: basemap_data; Owner: wildlife_db
--

CREATE TABLE basemap_data.national_forest (
    national_forest_id integer DEFAULT nextval('basemap_data.nat_for_seq'::regclass) NOT NULL,
    name character(100) NOT NULL,
    polygon public.geometry(MultiPolygon,4326)
);


ALTER TABLE basemap_data.national_forest OWNER TO wildlife_db;

--
-- Name: national_mon; Type: TABLE; Schema: basemap_data; Owner: wildlife_db
--

CREATE TABLE basemap_data.national_mon (
    national_mon_id integer DEFAULT nextval('basemap_data.nat_mon_seq'::regclass) NOT NULL,
    name character(100) NOT NULL,
    polygon public.geometry(MultiPolygon,4326)
);


ALTER TABLE basemap_data.national_mon OWNER TO wildlife_db;

--
-- Name: national_park; Type: TABLE; Schema: basemap_data; Owner: wildlife_db
--

CREATE TABLE basemap_data.national_park (
    national_park_id integer DEFAULT nextval('basemap_data.nat_park_seq'::regclass) NOT NULL,
    name character(100) NOT NULL,
    polygon public.geometry(MultiPolygon,4326)
);


ALTER TABLE basemap_data.national_park OWNER TO wildlife_db;

--
-- Name: state_seq; Type: SEQUENCE; Schema: basemap_data; Owner: wildlife_db
--

CREATE SEQUENCE basemap_data.state_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9999999999999999
    CACHE 1;


ALTER TABLE basemap_data.state_seq OWNER TO wildlife_db;

--
-- Name: state; Type: TABLE; Schema: basemap_data; Owner: wildlife_db
--

CREATE TABLE basemap_data.state (
    state_id integer DEFAULT nextval('basemap_data.state_seq'::regclass) NOT NULL,
    name character(100) NOT NULL,
    polygon public.geometry(MultiPolygon,4326)
);


ALTER TABLE basemap_data.state OWNER TO wildlife_db;

--
-- Name: state_park_seq; Type: SEQUENCE; Schema: basemap_data; Owner: wildlife_db
--

CREATE SEQUENCE basemap_data.state_park_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9999999999999999
    CACHE 1;


ALTER TABLE basemap_data.state_park_seq OWNER TO wildlife_db;

--
-- Name: state_park; Type: TABLE; Schema: basemap_data; Owner: wildlife_db
--

CREATE TABLE basemap_data.state_park (
    state_park_id integer DEFAULT nextval('basemap_data.state_park_seq'::regclass) NOT NULL,
    name character(100) NOT NULL,
    polygon public.geometry(MultiPolygon,4326)
);


ALTER TABLE basemap_data.state_park OWNER TO wildlife_db;

--
-- Name: anim_autocorrect_seq; Type: SEQUENCE; Schema: dev_data; Owner: wildlife_db
--

CREATE SEQUENCE dev_data.anim_autocorrect_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9999999999999999
    CACHE 1;


ALTER TABLE dev_data.anim_autocorrect_seq OWNER TO wildlife_db;

--
-- Name: animal_autocorrect; Type: TABLE; Schema: dev_data; Owner: wildlife_db
--

CREATE TABLE dev_data.animal_autocorrect (
    id integer DEFAULT nextval('dev_data.anim_autocorrect_seq'::regclass) NOT NULL,
    com_name character(50) NOT NULL,
    sci_name character(100) NOT NULL,
    state text NOT NULL
);


ALTER TABLE dev_data.animal_autocorrect OWNER TO wildlife_db;

--
-- Name: hab_inters_seq; Type: SEQUENCE; Schema: dev_data; Owner: wildlife_db
--

CREATE SEQUENCE dev_data.hab_inters_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9999999999999999
    CACHE 1;


ALTER TABLE dev_data.hab_inters_seq OWNER TO wildlife_db;

--
-- Name: habitat_intersections; Type: TABLE; Schema: dev_data; Owner: wildlife_db
--

CREATE TABLE dev_data.habitat_intersections (
    id integer DEFAULT nextval('dev_data.hab_inters_seq'::regclass) NOT NULL,
    com_name character(50) NOT NULL,
    type character(100) NOT NULL,
    state text NOT NULL
);


ALTER TABLE dev_data.habitat_intersections OWNER TO wildlife_db;

--
-- Name: wildlife_id_seq; Type: SEQUENCE; Schema: dev_data; Owner: wildlife_db
--

CREATE SEQUENCE dev_data.wildlife_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9999999999999999
    CACHE 1;


ALTER TABLE dev_data.wildlife_id_seq OWNER TO wildlife_db;

--
-- Name: wildlife_pt; Type: TABLE; Schema: dev_data; Owner: wildlife_db
--

CREATE TABLE dev_data.wildlife_pt (
    wildlife_id integer DEFAULT nextval('dev_data.wildlife_id_seq'::regclass) NOT NULL,
    gen_name character(50),
    com_name character(50) NOT NULL,
    sci_name character(100),
    gen_location character(40),
    spec_location character(40) NOT NULL,
    endangered boolean,
    photo_s3_url text,
    photo_blob bytea,
    username character(100) NOT NULL,
    comments character(400),
    lat double precision NOT NULL,
    long double precision NOT NULL,
    point public.geometry(Point,4326),
    created_date date DEFAULT now()
);


ALTER TABLE dev_data.wildlife_pt OWNER TO wildlife_db;

--
-- Name: anim_autocorrect_seq; Type: SEQUENCE; Schema: prod_data; Owner: wildlife_db
--

CREATE SEQUENCE prod_data.anim_autocorrect_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9999999999999999
    CACHE 1;


ALTER TABLE prod_data.anim_autocorrect_seq OWNER TO wildlife_db;

--
-- Name: animal_autocorrect; Type: TABLE; Schema: prod_data; Owner: wildlife_db
--

CREATE TABLE prod_data.animal_autocorrect (
    id integer DEFAULT nextval('prod_data.anim_autocorrect_seq'::regclass) NOT NULL,
    com_name character(50) NOT NULL,
    sci_name character(100) NOT NULL,
    state text NOT NULL
);


ALTER TABLE prod_data.animal_autocorrect OWNER TO wildlife_db;

--
-- Name: hab_inters_seq; Type: SEQUENCE; Schema: prod_data; Owner: wildlife_db
--

CREATE SEQUENCE prod_data.hab_inters_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9999999999999999
    CACHE 1;


ALTER TABLE prod_data.hab_inters_seq OWNER TO wildlife_db;

--
-- Name: habitat_intersections; Type: TABLE; Schema: prod_data; Owner: wildlife_db
--

CREATE TABLE prod_data.habitat_intersections (
    id integer DEFAULT nextval('prod_data.hab_inters_seq'::regclass) NOT NULL,
    com_name character(50) NOT NULL,
    type character(100) NOT NULL,
    state text NOT NULL
);


ALTER TABLE prod_data.habitat_intersections OWNER TO wildlife_db;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: prod_data; Owner: wildlife_db
--

CREATE SEQUENCE prod_data.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9999999999999999
    CACHE 1;


ALTER TABLE prod_data.users_id_seq OWNER TO wildlife_db;

--
-- Name: users; Type: TABLE; Schema: prod_data; Owner: wildlife_db
--

CREATE TABLE prod_data.users (
    user_id integer DEFAULT nextval('prod_data.users_id_seq'::regclass) NOT NULL,
    username character(200) NOT NULL,
    password text NOT NULL,
    salt text NOT NULL,
    email character(60) NOT NULL,
    city character(50) NOT NULL,
    state character(50),
    country character(50) NOT NULL
);


ALTER TABLE prod_data.users OWNER TO wildlife_db;

--
-- Name: wildlife_id_seq; Type: SEQUENCE; Schema: prod_data; Owner: wildlife_db
--

CREATE SEQUENCE prod_data.wildlife_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9999999999999999
    CACHE 1;


ALTER TABLE prod_data.wildlife_id_seq OWNER TO wildlife_db;

--
-- Name: wildlife_pt; Type: TABLE; Schema: prod_data; Owner: wildlife_db
--

CREATE TABLE prod_data.wildlife_pt (
    wildlife_id integer DEFAULT nextval('prod_data.wildlife_id_seq'::regclass) NOT NULL,
    gen_name character(50),
    com_name character(50) NOT NULL,
    sci_name character(100),
    gen_location character(40),
    spec_location character(40) NOT NULL,
    endangered boolean,
    photo_s3_url text,
    photo_blob bytea,
    username character(100) NOT NULL,
    comments character(400),
    lat double precision NOT NULL,
    long double precision NOT NULL,
    point public.geometry(Point,4326),
    created_date date DEFAULT now()
);


ALTER TABLE prod_data.wildlife_pt OWNER TO wildlife_db;

--
-- Data for Name: city; Type: TABLE DATA; Schema: basemap_data; Owner: wildlife_db
--

COPY basemap_data.city (city_id, name, polygon) FROM stdin;
\.


--
-- Data for Name: country; Type: TABLE DATA; Schema: basemap_data; Owner: wildlife_db
--

COPY basemap_data.country (country_id, name, polygon) FROM stdin;
\.


--
-- Data for Name: county; Type: TABLE DATA; Schema: basemap_data; Owner: wildlife_db
--

COPY basemap_data.county (county_id, name, polygon) FROM stdin;
\.


--
-- Data for Name: national_forest; Type: TABLE DATA; Schema: basemap_data; Owner: wildlife_db
--

COPY basemap_data.national_forest (national_forest_id, name, polygon) FROM stdin;
\.


--
-- Data for Name: national_mon; Type: TABLE DATA; Schema: basemap_data; Owner: wildlife_db
--

COPY basemap_data.national_mon (national_mon_id, name, polygon) FROM stdin;
\.


--
-- Data for Name: national_park; Type: TABLE DATA; Schema: basemap_data; Owner: wildlife_db
--

COPY basemap_data.national_park (national_park_id, name, polygon) FROM stdin;
\.


--
-- Data for Name: state; Type: TABLE DATA; Schema: basemap_data; Owner: wildlife_db
--

COPY basemap_data.state (state_id, name, polygon) FROM stdin;
\.


--
-- Data for Name: state_park; Type: TABLE DATA; Schema: basemap_data; Owner: wildlife_db
--

COPY basemap_data.state_park (state_park_id, name, polygon) FROM stdin;
\.


--
-- Data for Name: animal_autocorrect; Type: TABLE DATA; Schema: dev_data; Owner: wildlife_db
--

COPY dev_data.animal_autocorrect (id, com_name, sci_name, state) FROM stdin;
\.


--
-- Data for Name: habitat_intersections; Type: TABLE DATA; Schema: dev_data; Owner: wildlife_db
--

COPY dev_data.habitat_intersections (id, com_name, type, state) FROM stdin;
\.


--
-- Data for Name: wildlife_pt; Type: TABLE DATA; Schema: dev_data; Owner: wildlife_db
--

COPY dev_data.wildlife_pt (wildlife_id, gen_name, com_name, sci_name, gen_location, spec_location, endangered, photo_s3_url, photo_blob, username, comments, lat, long, point, created_date) FROM stdin;
\.


--
-- Data for Name: animal_autocorrect; Type: TABLE DATA; Schema: prod_data; Owner: wildlife_db
--

COPY prod_data.animal_autocorrect (id, com_name, sci_name, state) FROM stdin;
\.


--
-- Data for Name: habitat_intersections; Type: TABLE DATA; Schema: prod_data; Owner: wildlife_db
--

COPY prod_data.habitat_intersections (id, com_name, type, state) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: prod_data; Owner: wildlife_db
--

COPY prod_data.users (user_id, username, password, salt, email, city, state, country) FROM stdin;
\.


--
-- Data for Name: wildlife_pt; Type: TABLE DATA; Schema: prod_data; Owner: wildlife_db
--

COPY prod_data.wildlife_pt (wildlife_id, gen_name, com_name, sci_name, gen_location, spec_location, endangered, photo_s3_url, photo_blob, username, comments, lat, long, point, created_date) FROM stdin;
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: wildlife_db
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Name: city_seq; Type: SEQUENCE SET; Schema: basemap_data; Owner: wildlife_db
--

SELECT pg_catalog.setval('basemap_data.city_seq', 1, false);


--
-- Name: country_seq; Type: SEQUENCE SET; Schema: basemap_data; Owner: wildlife_db
--

SELECT pg_catalog.setval('basemap_data.country_seq', 1, false);


--
-- Name: county_seq; Type: SEQUENCE SET; Schema: basemap_data; Owner: wildlife_db
--

SELECT pg_catalog.setval('basemap_data.county_seq', 1, false);


--
-- Name: nat_for_seq; Type: SEQUENCE SET; Schema: basemap_data; Owner: wildlife_db
--

SELECT pg_catalog.setval('basemap_data.nat_for_seq', 1, false);


--
-- Name: nat_mon_seq; Type: SEQUENCE SET; Schema: basemap_data; Owner: wildlife_db
--

SELECT pg_catalog.setval('basemap_data.nat_mon_seq', 1, false);


--
-- Name: nat_park_seq; Type: SEQUENCE SET; Schema: basemap_data; Owner: wildlife_db
--

SELECT pg_catalog.setval('basemap_data.nat_park_seq', 1, false);


--
-- Name: state_park_seq; Type: SEQUENCE SET; Schema: basemap_data; Owner: wildlife_db
--

SELECT pg_catalog.setval('basemap_data.state_park_seq', 1, false);


--
-- Name: state_seq; Type: SEQUENCE SET; Schema: basemap_data; Owner: wildlife_db
--

SELECT pg_catalog.setval('basemap_data.state_seq', 1, false);


--
-- Name: anim_autocorrect_seq; Type: SEQUENCE SET; Schema: dev_data; Owner: wildlife_db
--

SELECT pg_catalog.setval('dev_data.anim_autocorrect_seq', 1, false);


--
-- Name: hab_inters_seq; Type: SEQUENCE SET; Schema: dev_data; Owner: wildlife_db
--

SELECT pg_catalog.setval('dev_data.hab_inters_seq', 1, false);


--
-- Name: wildlife_id_seq; Type: SEQUENCE SET; Schema: dev_data; Owner: wildlife_db
--

SELECT pg_catalog.setval('dev_data.wildlife_id_seq', 1, false);


--
-- Name: anim_autocorrect_seq; Type: SEQUENCE SET; Schema: prod_data; Owner: wildlife_db
--

SELECT pg_catalog.setval('prod_data.anim_autocorrect_seq', 1, false);


--
-- Name: hab_inters_seq; Type: SEQUENCE SET; Schema: prod_data; Owner: wildlife_db
--

SELECT pg_catalog.setval('prod_data.hab_inters_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: prod_data; Owner: wildlife_db
--

SELECT pg_catalog.setval('prod_data.users_id_seq', 1, false);


--
-- Name: wildlife_id_seq; Type: SEQUENCE SET; Schema: prod_data; Owner: wildlife_db
--

SELECT pg_catalog.setval('prod_data.wildlife_id_seq', 1, false);


--
-- Name: city city_pkey; Type: CONSTRAINT; Schema: basemap_data; Owner: wildlife_db
--

ALTER TABLE ONLY basemap_data.city
    ADD CONSTRAINT city_pkey PRIMARY KEY (city_id);


--
-- Name: country country_pkey; Type: CONSTRAINT; Schema: basemap_data; Owner: wildlife_db
--

ALTER TABLE ONLY basemap_data.country
    ADD CONSTRAINT country_pkey PRIMARY KEY (country_id);


--
-- Name: county county_pkey; Type: CONSTRAINT; Schema: basemap_data; Owner: wildlife_db
--

ALTER TABLE ONLY basemap_data.county
    ADD CONSTRAINT county_pkey PRIMARY KEY (county_id);


--
-- Name: national_forest national_forest_pkey; Type: CONSTRAINT; Schema: basemap_data; Owner: wildlife_db
--

ALTER TABLE ONLY basemap_data.national_forest
    ADD CONSTRAINT national_forest_pkey PRIMARY KEY (national_forest_id);


--
-- Name: national_mon national_mon_pkey; Type: CONSTRAINT; Schema: basemap_data; Owner: wildlife_db
--

ALTER TABLE ONLY basemap_data.national_mon
    ADD CONSTRAINT national_mon_pkey PRIMARY KEY (national_mon_id);


--
-- Name: national_park national_park_pkey; Type: CONSTRAINT; Schema: basemap_data; Owner: wildlife_db
--

ALTER TABLE ONLY basemap_data.national_park
    ADD CONSTRAINT national_park_pkey PRIMARY KEY (national_park_id);


--
-- Name: state_park state_park_pkey; Type: CONSTRAINT; Schema: basemap_data; Owner: wildlife_db
--

ALTER TABLE ONLY basemap_data.state_park
    ADD CONSTRAINT state_park_pkey PRIMARY KEY (state_park_id);


--
-- Name: state state_pkey; Type: CONSTRAINT; Schema: basemap_data; Owner: wildlife_db
--

ALTER TABLE ONLY basemap_data.state
    ADD CONSTRAINT state_pkey PRIMARY KEY (state_id);


--
-- Name: animal_autocorrect animal_autocorrect_pkey; Type: CONSTRAINT; Schema: dev_data; Owner: wildlife_db
--

ALTER TABLE ONLY dev_data.animal_autocorrect
    ADD CONSTRAINT animal_autocorrect_pkey PRIMARY KEY (id);


--
-- Name: habitat_intersections habitat_intersections_pkey; Type: CONSTRAINT; Schema: dev_data; Owner: wildlife_db
--

ALTER TABLE ONLY dev_data.habitat_intersections
    ADD CONSTRAINT habitat_intersections_pkey PRIMARY KEY (id);


--
-- Name: wildlife_pt wildlife_pt_pkey; Type: CONSTRAINT; Schema: dev_data; Owner: wildlife_db
--

ALTER TABLE ONLY dev_data.wildlife_pt
    ADD CONSTRAINT wildlife_pt_pkey PRIMARY KEY (wildlife_id);


--
-- Name: wildlife_pt wildlife_pt_user_uk; Type: CONSTRAINT; Schema: dev_data; Owner: wildlife_db
--

ALTER TABLE ONLY dev_data.wildlife_pt
    ADD CONSTRAINT wildlife_pt_user_uk UNIQUE (username);


--
-- Name: animal_autocorrect animal_autocorrect_pkey; Type: CONSTRAINT; Schema: prod_data; Owner: wildlife_db
--

ALTER TABLE ONLY prod_data.animal_autocorrect
    ADD CONSTRAINT animal_autocorrect_pkey PRIMARY KEY (id);


--
-- Name: habitat_intersections habitat_intersections_pkey; Type: CONSTRAINT; Schema: prod_data; Owner: wildlife_db
--

ALTER TABLE ONLY prod_data.habitat_intersections
    ADD CONSTRAINT habitat_intersections_pkey PRIMARY KEY (id);


--
-- Name: users users_email_uk; Type: CONSTRAINT; Schema: prod_data; Owner: wildlife_db
--

ALTER TABLE ONLY prod_data.users
    ADD CONSTRAINT users_email_uk UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: prod_data; Owner: wildlife_db
--

ALTER TABLE ONLY prod_data.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_user_uk; Type: CONSTRAINT; Schema: prod_data; Owner: wildlife_db
--

ALTER TABLE ONLY prod_data.users
    ADD CONSTRAINT users_user_uk UNIQUE (username);


--
-- Name: wildlife_pt wildlife_pt_pkey; Type: CONSTRAINT; Schema: prod_data; Owner: wildlife_db
--

ALTER TABLE ONLY prod_data.wildlife_pt
    ADD CONSTRAINT wildlife_pt_pkey PRIMARY KEY (wildlife_id);


--
-- Name: wildlife_pt wildlife_pt_user_uk; Type: CONSTRAINT; Schema: prod_data; Owner: wildlife_db
--

ALTER TABLE ONLY prod_data.wildlife_pt
    ADD CONSTRAINT wildlife_pt_user_uk UNIQUE (username);


--
-- Name: city_geom_index; Type: INDEX; Schema: basemap_data; Owner: wildlife_db
--

CREATE INDEX city_geom_index ON basemap_data.city USING gist (polygon);


--
-- Name: country_geom_index; Type: INDEX; Schema: basemap_data; Owner: wildlife_db
--

CREATE INDEX country_geom_index ON basemap_data.country USING gist (polygon);


--
-- Name: county_geom_index; Type: INDEX; Schema: basemap_data; Owner: wildlife_db
--

CREATE INDEX county_geom_index ON basemap_data.county USING gist (polygon);


--
-- Name: national_forest_geom_index; Type: INDEX; Schema: basemap_data; Owner: wildlife_db
--

CREATE INDEX national_forest_geom_index ON basemap_data.national_forest USING gist (polygon);


--
-- Name: national_mon_geom_index; Type: INDEX; Schema: basemap_data; Owner: wildlife_db
--

CREATE INDEX national_mon_geom_index ON basemap_data.national_mon USING gist (polygon);


--
-- Name: national_park_geom_index; Type: INDEX; Schema: basemap_data; Owner: wildlife_db
--

CREATE INDEX national_park_geom_index ON basemap_data.national_park USING gist (polygon);


--
-- Name: state_geom_index; Type: INDEX; Schema: basemap_data; Owner: wildlife_db
--

CREATE INDEX state_geom_index ON basemap_data.state USING gist (polygon);


--
-- Name: state_park_geom_index; Type: INDEX; Schema: basemap_data; Owner: wildlife_db
--

CREATE INDEX state_park_geom_index ON basemap_data.state_park USING gist (polygon);


--
-- Name: wildlife_pt_geom_index; Type: INDEX; Schema: dev_data; Owner: wildlife_db
--

CREATE INDEX wildlife_pt_geom_index ON dev_data.wildlife_pt USING gist (point);


--
-- Name: wildlife_pt_geom_index; Type: INDEX; Schema: prod_data; Owner: wildlife_db
--

CREATE INDEX wildlife_pt_geom_index ON prod_data.wildlife_pt USING gist (point);


--
-- Name: wildlife_pt wildlife_pt_user_fk; Type: FK CONSTRAINT; Schema: dev_data; Owner: wildlife_db
--

ALTER TABLE ONLY dev_data.wildlife_pt
    ADD CONSTRAINT wildlife_pt_user_fk FOREIGN KEY (username) REFERENCES prod_data.users(username);


--
-- Name: wildlife_pt wildlife_pt_user_fk; Type: FK CONSTRAINT; Schema: prod_data; Owner: wildlife_db
--

ALTER TABLE ONLY prod_data.wildlife_pt
    ADD CONSTRAINT wildlife_pt_user_fk FOREIGN KEY (username) REFERENCES prod_data.users(username);


--
-- Name: SCHEMA basemap_data; Type: ACL; Schema: -; Owner: wildlife_db
--

GRANT USAGE ON SCHEMA basemap_data TO bailey;
GRANT USAGE ON SCHEMA basemap_data TO basemap_user;


--
-- Name: SCHEMA dev_data; Type: ACL; Schema: -; Owner: wildlife_db
--

GRANT USAGE ON SCHEMA dev_data TO bailey;


--
-- Name: SCHEMA prod_data; Type: ACL; Schema: -; Owner: wildlife_db
--

GRANT USAGE ON SCHEMA prod_data TO bailey;


--
-- Name: TABLE city; Type: ACL; Schema: basemap_data; Owner: wildlife_db
--

GRANT ALL ON TABLE basemap_data.city TO bailey;
GRANT ALL ON TABLE basemap_data.city TO basemap_user;
GRANT SELECT ON TABLE basemap_data.city TO public_user;


--
-- Name: TABLE country; Type: ACL; Schema: basemap_data; Owner: wildlife_db
--

GRANT ALL ON TABLE basemap_data.country TO bailey;
GRANT ALL ON TABLE basemap_data.country TO basemap_user;
GRANT SELECT ON TABLE basemap_data.country TO public_user;


--
-- Name: TABLE county; Type: ACL; Schema: basemap_data; Owner: wildlife_db
--

GRANT ALL ON TABLE basemap_data.county TO basemap_user;
GRANT ALL ON TABLE basemap_data.county TO bailey;
GRANT SELECT ON TABLE basemap_data.county TO public_user;


--
-- Name: TABLE national_forest; Type: ACL; Schema: basemap_data; Owner: wildlife_db
--

GRANT ALL ON TABLE basemap_data.national_forest TO basemap_user;
GRANT ALL ON TABLE basemap_data.national_forest TO bailey;
GRANT SELECT ON TABLE basemap_data.national_forest TO public_user;


--
-- Name: TABLE national_mon; Type: ACL; Schema: basemap_data; Owner: wildlife_db
--

GRANT ALL ON TABLE basemap_data.national_mon TO bailey;
GRANT ALL ON TABLE basemap_data.national_mon TO basemap_user;
GRANT SELECT ON TABLE basemap_data.national_mon TO public_user;


--
-- Name: TABLE national_park; Type: ACL; Schema: basemap_data; Owner: wildlife_db
--

GRANT ALL ON TABLE basemap_data.national_park TO basemap_user;
GRANT ALL ON TABLE basemap_data.national_park TO bailey;
GRANT SELECT ON TABLE basemap_data.national_park TO public_user;


--
-- Name: TABLE state; Type: ACL; Schema: basemap_data; Owner: wildlife_db
--

GRANT ALL ON TABLE basemap_data.state TO basemap_user;
GRANT ALL ON TABLE basemap_data.state TO bailey;
GRANT SELECT ON TABLE basemap_data.state TO public_user;


--
-- Name: TABLE state_park; Type: ACL; Schema: basemap_data; Owner: wildlife_db
--

GRANT ALL ON TABLE basemap_data.state_park TO bailey;
GRANT ALL ON TABLE basemap_data.state_park TO basemap_user;
GRANT SELECT ON TABLE basemap_data.state_park TO public_user;


--
-- Name: TABLE animal_autocorrect; Type: ACL; Schema: dev_data; Owner: wildlife_db
--

GRANT ALL ON TABLE dev_data.animal_autocorrect TO bailey;


--
-- Name: TABLE habitat_intersections; Type: ACL; Schema: dev_data; Owner: wildlife_db
--

GRANT ALL ON TABLE dev_data.habitat_intersections TO bailey;


--
-- Name: TABLE wildlife_pt; Type: ACL; Schema: dev_data; Owner: wildlife_db
--

GRANT ALL ON TABLE dev_data.wildlife_pt TO bailey;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE dev_data.wildlife_pt TO public_user;


--
-- Name: TABLE animal_autocorrect; Type: ACL; Schema: prod_data; Owner: wildlife_db
--

GRANT ALL ON TABLE prod_data.animal_autocorrect TO bailey;


--
-- Name: TABLE habitat_intersections; Type: ACL; Schema: prod_data; Owner: wildlife_db
--

GRANT ALL ON TABLE prod_data.habitat_intersections TO bailey;


--
-- Name: TABLE users; Type: ACL; Schema: prod_data; Owner: wildlife_db
--

GRANT ALL ON TABLE prod_data.users TO bailey;
GRANT SELECT,INSERT,UPDATE ON TABLE prod_data.users TO public_user;


--
-- Name: TABLE wildlife_pt; Type: ACL; Schema: prod_data; Owner: wildlife_db
--

GRANT ALL ON TABLE prod_data.wildlife_pt TO bailey;
GRANT SELECT ON TABLE prod_data.wildlife_pt TO public_user;


--
-- PostgreSQL database dump complete
--
