--
-- PostgreSQL database dump
--

-- Dumped from database version 14.2
-- Dumped by pg_dump version 14.2

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

--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: music_list; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.music_list (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    genre character varying(20) NOT NULL,
    bytes bytea NOT NULL,
    artist character varying(150) NOT NULL
);


ALTER TABLE public.music_list OWNER TO postgres;

--
-- Name: music_list_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.music_list_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.music_list_id_seq OWNER TO postgres;

--
-- Name: music_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.music_list_id_seq OWNED BY public.music_list.id;


--
-- Name: music_list id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.music_list ALTER COLUMN id SET DEFAULT nextval('public.music_list_id_seq'::regclass);


--
-- Name: music_list music_list_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.music_list
    ADD CONSTRAINT music_list_pkey PRIMARY KEY (id);


--
-- Name: music_list unique_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.music_list
    ADD CONSTRAINT unique_name UNIQUE (name, artist);


--
-- PostgreSQL database dump complete
--

