--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: intarray; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS intarray WITH SCHEMA public;


--
-- Name: EXTENSION intarray; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION intarray IS 'functions, operators, and index support for 1-D arrays of integers';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: Access_Token; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Access_Token" (
    id integer NOT NULL,
    "time" timestamp without time zone DEFAULT now(),
    appid integer
);


ALTER TABLE public."Access_Token" OWNER TO yichun;

--
-- Name: Access_Token_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Access_Token_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Access_Token_id_seq" OWNER TO yichun;

--
-- Name: Access_Token_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Access_Token_id_seq" OWNED BY "Access_Token".id;


--
-- Name: Brand; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Brand" (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public."Brand" OWNER TO yichun;

--
-- Name: Brand_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Brand_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Brand_id_seq" OWNER TO yichun;

--
-- Name: Brand_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Brand_id_seq" OWNED BY "Brand".id;


--
-- Name: Category; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Category" (
    id integer NOT NULL,
    name text NOT NULL,
    parent_id integer
);


ALTER TABLE public."Category" OWNER TO yichun;

--
-- Name: Category_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Category_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Category_id_seq" OWNER TO yichun;

--
-- Name: Category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Category_id_seq" OWNED BY "Category".id;


--
-- Name: Cellar; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Cellar" (
    id integer NOT NULL,
    name text,
    description text,
    city_id integer,
    for_sale integer DEFAULT 0 NOT NULL,
    reservation integer DEFAULT 0 NOT NULL
);


ALTER TABLE public."Cellar" OWNER TO yichun;

--
-- Name: Cellar_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Cellar_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Cellar_id_seq" OWNER TO yichun;

--
-- Name: Cellar_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Cellar_id_seq" OWNED BY "Cellar".id;


--
-- Name: City; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "City" (
    id integer NOT NULL,
    name text
);


ALTER TABLE public."City" OWNER TO yichun;

--
-- Name: City_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "City_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."City_id_seq" OWNER TO yichun;

--
-- Name: City_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "City_id_seq" OWNED BY "City".id;


--
-- Name: Contact; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Contact" (
    id integer NOT NULL,
    name text NOT NULL,
    email text NOT NULL,
    address text NOT NULL,
    telephone text NOT NULL,
    type_id integer,
    zip_code text DEFAULT ''::text,
    additional_info text,
    lastname text,
    user_id integer,
    town text DEFAULT ''::text,
    country text DEFAULT ''::text,
    rut text DEFAULT ''::text NOT NULL,
    city_id integer
);


ALTER TABLE public."Contact" OWNER TO yichun;

--
-- Name: Contact_Types; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Contact_Types" (
    id integer NOT NULL,
    name text
);


ALTER TABLE public."Contact_Types" OWNER TO yichun;

--
-- Name: Contact_Types_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Contact_Types_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Contact_Types_id_seq" OWNER TO yichun;

--
-- Name: Contact_Types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Contact_Types_id_seq" OWNED BY "Contact_Types".id;


--
-- Name: Contact_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Contact_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Contact_id_seq" OWNER TO yichun;

--
-- Name: Contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Contact_id_seq" OWNED BY "Contact".id;


--
-- Name: Kardex; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Kardex" (
    id integer NOT NULL,
    product_sku text NOT NULL,
    units integer NOT NULL,
    price double precision NOT NULL,
    sell_price double precision NOT NULL,
    cellar_id integer NOT NULL,
    total double precision NOT NULL,
    balance_units integer NOT NULL,
    balance_price double precision NOT NULL,
    balance_total double precision DEFAULT 0,
    date timestamp without time zone NOT NULL,
    "user" text,
    operation_type text,
    color text,
    size text
);


ALTER TABLE public."Kardex" OWNER TO yichun;

--
-- Name: Kardex_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Kardex_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Kardex_id_seq" OWNER TO yichun;

--
-- Name: Kardex_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Kardex_id_seq" OWNED BY "Kardex".id;


--
-- Name: Order; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Order" (
    id integer NOT NULL,
    date timestamp without time zone NOT NULL,
    type integer NOT NULL,
    subtotal double precision NOT NULL,
    shipping integer NOT NULL,
    tax double precision NOT NULL,
    total double precision NOT NULL,
    items_quantity integer NOT NULL,
    products_quantity integer NOT NULL,
    user_id integer NOT NULL,
    billing_id integer NOT NULL,
    shipping_id integer,
    payment_type integer DEFAULT 1 NOT NULL,
    source text DEFAULT 'web'::text,
    voucher text DEFAULT ''::text,
    state integer DEFAULT 1,
    tracking_code text,
    provider_id integer
);


ALTER TABLE public."Order" OWNER TO yichun;

--
-- Name: Order_Detail; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Order_Detail" (
    id integer NOT NULL,
    quantity integer NOT NULL,
    subtotal double precision NOT NULL,
    order_id integer NOT NULL,
    product_id integer NOT NULL,
    size text DEFAULT ''::text NOT NULL
);


ALTER TABLE public."Order_Detail" OWNER TO yichun;

--
-- Name: Order_Detail_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Order_Detail_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Order_Detail_id_seq" OWNER TO yichun;

--
-- Name: Order_Detail_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Order_Detail_id_seq" OWNED BY "Order_Detail".id;


--
-- Name: Order_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Order_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Order_id_seq" OWNER TO yichun;

--
-- Name: Order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Order_id_seq" OWNED BY "Order".id;


--
-- Name: Payment_Types; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Payment_Types" (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public."Payment_Types" OWNER TO yichun;

--
-- Name: Payment_Types_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Payment_Types_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Payment_Types_id_seq" OWNER TO yichun;

--
-- Name: Payment_Types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Payment_Types_id_seq" OWNED BY "Payment_Types".id;


--
-- Name: Payment_Types_name_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Payment_Types_name_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Payment_Types_name_seq" OWNER TO yichun;

--
-- Name: Payment_Types_name_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Payment_Types_name_seq" OWNED BY "Payment_Types".name;


--
-- Name: Permission; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Permission" (
    id integer NOT NULL,
    name text
);


ALTER TABLE public."Permission" OWNER TO yichun;

--
-- Name: Permission_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Permission_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Permission_id_seq" OWNER TO yichun;

--
-- Name: Permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Permission_id_seq" OWNED BY "Permission".id;


--
-- Name: Product; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Product" (
    id integer NOT NULL,
    sku text NOT NULL,
    description text,
    brand text NOT NULL,
    size text[] NOT NULL,
    material text NOT NULL,
    bullet_1 text,
    bullet_2 text,
    currency character varying(10),
    images text[],
    image text,
    image_2 text,
    image_3 text,
    price integer DEFAULT 0 NOT NULL,
    category_id integer NOT NULL,
    bullet_3 text,
    manufacturer text,
    name text NOT NULL,
    color text,
    upc text,
    sell_price integer DEFAULT 0,
    which_size text DEFAULT ''::text NOT NULL,
    delivery text DEFAULT ''::text NOT NULL,
    for_sale integer DEFAULT 0 NOT NULL,
    image_4 text DEFAULT ''::text,
    image_5 text DEFAULT ''::text,
    image_6 text DEFAULT ''::text
);


ALTER TABLE public."Product" OWNER TO yichun;

--
-- Name: Product_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Product_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Product_id_seq" OWNER TO yichun;

--
-- Name: Product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Product_id_seq" OWNED BY "Product".id;


--
-- Name: Shipping; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Shipping" (
    id integer NOT NULL,
    from_city_id integer NOT NULL,
    to_city_id integer NOT NULL,
    correos_price integer,
    chilexpress_price integer,
    price integer NOT NULL,
    edited boolean DEFAULT false,
    charge_type integer DEFAULT 1 NOT NULL
);


ALTER TABLE public."Shipping" OWNER TO yichun;

--
-- Name: Shipping_Provider; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Shipping_Provider" (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public."Shipping_Provider" OWNER TO yichun;

--
-- Name: Shipping_Provider_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Shipping_Provider_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Shipping_Provider_id_seq" OWNER TO yichun;

--
-- Name: Shipping_Provider_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Shipping_Provider_id_seq" OWNED BY "Shipping_Provider".id;


--
-- Name: Shipping_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Shipping_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Shipping_id_seq" OWNER TO yichun;

--
-- Name: Shipping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Shipping_id_seq" OWNED BY "Shipping".id;


--
-- Name: State; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "State" (
    id integer NOT NULL,
    name text
);


ALTER TABLE public."State" OWNER TO yichun;

--
-- Name: State_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "State_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."State_id_seq" OWNER TO yichun;

--
-- Name: State_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "State_id_seq" OWNED BY "State".id;


--
-- Name: Tag; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Tag" (
    id integer NOT NULL,
    name text NOT NULL,
    visible integer DEFAULT 0 NOT NULL
);


ALTER TABLE public."Tag" OWNER TO yichun;

--
-- Name: Tag_Product; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Tag_Product" (
    id integer NOT NULL,
    product_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public."Tag_Product" OWNER TO yichun;

--
-- Name: Tag_Product_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Tag_Product_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Tag_Product_id_seq" OWNER TO yichun;

--
-- Name: Tag_Product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Tag_Product_id_seq" OWNED BY "Tag_Product".id;


--
-- Name: Tag_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Tag_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Tag_id_seq" OWNER TO yichun;

--
-- Name: Tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Tag_id_seq" OWNED BY "Tag".id;


--
-- Name: Tag_name_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Tag_name_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Tag_name_seq" OWNER TO yichun;

--
-- Name: Tag_name_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Tag_name_seq" OWNED BY "Tag".name;


--
-- Name: Temp_Cart; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Temp_Cart" (
    id integer NOT NULL,
    product_id integer,
    date timestamp without time zone,
    quantity integer,
    subtotal integer,
    user_id integer,
    size text,
    shipping_id integer,
    billing_id integer,
    payment_type integer,
    shipping_type integer DEFAULT 1,
    bought integer DEFAULT 0
);


ALTER TABLE public."Temp_Cart" OWNER TO yichun;

--
-- Name: Temp_Cart_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Temp_Cart_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Temp_Cart_id_seq" OWNER TO yichun;

--
-- Name: Temp_Cart_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Temp_Cart_id_seq" OWNED BY "Temp_Cart".id;


--
-- Name: User; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "User" (
    id integer NOT NULL,
    permissions integer[] DEFAULT ARRAY[]::integer[] NOT NULL,
    type_id integer NOT NULL,
    name text,
    email text NOT NULL,
    password text DEFAULT ''::text NOT NULL,
    cellar_permissions integer[] DEFAULT ARRAY[]::integer[],
    lastname text DEFAULT ''::text NOT NULL,
    rut text DEFAULT ''::text,
    bussiness text DEFAULT ''::text,
    approval_date timestamp without time zone,
    registration_date timestamp without time zone DEFAULT now() NOT NULL,
    status integer DEFAULT 1 NOT NULL,
    first_view timestamp without time zone DEFAULT now() NOT NULL,
    last_view timestamp without time zone DEFAULT now() NOT NULL,
    deleted integer DEFAULT 0
);


ALTER TABLE public."User" OWNER TO yichun;

--
-- Name: User_Types; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "User_Types" (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public."User_Types" OWNER TO yichun;

--
-- Name: User_Types_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "User_Types_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."User_Types_id_seq" OWNER TO yichun;

--
-- Name: User_Types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "User_Types_id_seq" OWNED BY "User_Types".id;


--
-- Name: User_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "User_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."User_id_seq" OWNER TO yichun;

--
-- Name: User_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "User_id_seq" OWNED BY "User".id;


--
-- Name: Voto; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Voto" (
    id integer NOT NULL,
    user_id integer,
    product_id integer
);


ALTER TABLE public."Voto" OWNER TO yichun;

--
-- Name: Votos_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Votos_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Votos_id_seq" OWNER TO yichun;

--
-- Name: Votos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Votos_id_seq" OWNED BY "Voto".id;


--
-- Name: Webpay; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Webpay" (
    id integer NOT NULL,
    "TBK_MONTO" integer,
    "TBK_CODIGO_AUTORIZACION" integer,
    "TBK_FINAL_NUMERO_TARJETA" integer,
    "TBK_FECHA_CONTABLE" integer,
    "TBK_FECHA_TRANSACCION" integer,
    "TBK_HORA_TRANSACCION" integer,
    "TBK_ID_TRANSACCION" integer,
    "TBK_TIPO_PAGO" text,
    "TBK_NUMERO_CUOTAS" integer,
    "TBK_ID_SESION" text NOT NULL,
    "TBK_ORDEN_COMPRA" integer NOT NULL,
    "ORDER_ID" integer NOT NULL
);


ALTER TABLE public."Webpay" OWNER TO yichun;

--
-- Name: Webpay_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Webpay_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Webpay_id_seq" OWNER TO yichun;

--
-- Name: Webpay_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Webpay_id_seq" OWNED BY "Webpay".id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Access_Token" ALTER COLUMN id SET DEFAULT nextval('"Access_Token_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Brand" ALTER COLUMN id SET DEFAULT nextval('"Brand_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Category" ALTER COLUMN id SET DEFAULT nextval('"Category_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Cellar" ALTER COLUMN id SET DEFAULT nextval('"Cellar_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "City" ALTER COLUMN id SET DEFAULT nextval('"City_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Contact" ALTER COLUMN id SET DEFAULT nextval('"Contact_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Contact_Types" ALTER COLUMN id SET DEFAULT nextval('"Contact_Types_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Kardex" ALTER COLUMN id SET DEFAULT nextval('"Kardex_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Order" ALTER COLUMN id SET DEFAULT nextval('"Order_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Order_Detail" ALTER COLUMN id SET DEFAULT nextval('"Order_Detail_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Payment_Types" ALTER COLUMN id SET DEFAULT nextval('"Payment_Types_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Permission" ALTER COLUMN id SET DEFAULT nextval('"Permission_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Product" ALTER COLUMN id SET DEFAULT nextval('"Product_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Shipping" ALTER COLUMN id SET DEFAULT nextval('"Shipping_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Shipping_Provider" ALTER COLUMN id SET DEFAULT nextval('"Shipping_Provider_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "State" ALTER COLUMN id SET DEFAULT nextval('"State_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Tag" ALTER COLUMN id SET DEFAULT nextval('"Tag_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Tag_Product" ALTER COLUMN id SET DEFAULT nextval('"Tag_Product_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Temp_Cart" ALTER COLUMN id SET DEFAULT nextval('"Temp_Cart_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "User" ALTER COLUMN id SET DEFAULT nextval('"User_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "User_Types" ALTER COLUMN id SET DEFAULT nextval('"User_Types_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Voto" ALTER COLUMN id SET DEFAULT nextval('"Votos_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Webpay" ALTER COLUMN id SET DEFAULT nextval('"Webpay_id_seq"'::regclass);


--
-- Data for Name: Access_Token; Type: TABLE DATA; Schema: public; Owner: yichun
--



--
-- Name: Access_Token_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Access_Token_id_seq"', 12536, true);


--
-- Data for Name: Brand; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Brand" VALUES (1, 'Giani Da Firenze');
INSERT INTO "Brand" VALUES (2, '1');


--
-- Name: Brand_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Brand_id_seq"', 2, true);


--
-- Data for Name: Category; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Category" VALUES (4, 'Bota', NULL);
INSERT INTO "Category" VALUES (5, 'categoria', NULL);
INSERT INTO "Category" VALUES (6, 'producto 1', NULL);
INSERT INTO "Category" VALUES (7, 'zapatos', NULL);
INSERT INTO "Category" VALUES (1, 'Botin', NULL);


--
-- Name: Category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Category_id_seq"', 7, true);


--
-- Data for Name: Cellar; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Cellar" VALUES (5, 'Bodega Central', 'asadadas', 3, 1, 0);
INSERT INTO "Cellar" VALUES (12, 'bodega reserva', 'aqui quedan los productos reservados desde la web', 3, 0, 1);


--
-- Name: Cellar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Cellar_id_seq"', 12, true);


--
-- Data for Name: City; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "City" VALUES (1, 'Arica');
INSERT INTO "City" VALUES (2, 'Iquique');
INSERT INTO "City" VALUES (3, 'Santiago');
INSERT INTO "City" VALUES (4, 'Valdivia');
INSERT INTO "City" VALUES (5, 'Antofagasta');
INSERT INTO "City" VALUES (6, 'Talca');
INSERT INTO "City" VALUES (9, 'ConcepciÃ³n');
INSERT INTO "City" VALUES (10, 'Temuco');
INSERT INTO "City" VALUES (11, 'Punta Arenas');
INSERT INTO "City" VALUES (12, 'La Serena');
INSERT INTO "City" VALUES (13, 'Rancagua');
INSERT INTO "City" VALUES (14, 'Coquimbo');
INSERT INTO "City" VALUES (15, 'CopiapÃ³');
INSERT INTO "City" VALUES (16, 'ValparaÃ­so');
INSERT INTO "City" VALUES (19, 'TarapacÃ¡');
INSERT INTO "City" VALUES (20, 'ChillÃ¡n');
INSERT INTO "City" VALUES (21, 'CuricÃ³');
INSERT INTO "City" VALUES (22, '');
INSERT INTO "City" VALUES (23, 'Arica DHSS');
INSERT INTO "City" VALUES (24, 'Arica DHS');
INSERT INTO "City" VALUES (25, 'Antofagasta DÃ­a HÃ¡bil Siguiente');
INSERT INTO "City" VALUES (26, 'Antofagasta DÃ­a HÃ¡bil Sub Siguiente');
INSERT INTO "City" VALUES (27, 'Arica DÃ­a HÃ¡bil Siguente');
INSERT INTO "City" VALUES (28, 'Arica DÃ­a HÃ¡bil Sub Siguiente');
INSERT INTO "City" VALUES (29, 'Copiapo');
INSERT INTO "City" VALUES (30, 'Ovalle');
INSERT INTO "City" VALUES (31, 'Valparaiso');
INSERT INTO "City" VALUES (32, 'San Antonio');
INSERT INTO "City" VALUES (33, 'ViÃ±a del Mar');
INSERT INTO "City" VALUES (34, 'San Fernando');
INSERT INTO "City" VALUES (35, 'Los Angeles');
INSERT INTO "City" VALUES (36, 'Osorno');
INSERT INTO "City" VALUES (37, 'Puerto Montt');
INSERT INTO "City" VALUES (38, 'Coyhaique');


--
-- Name: City_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"City_id_seq"', 38, true);


--
-- Data for Name: Contact; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Contact" VALUES (28, 'Ricardo', 'ricardo@loadingplay.com', 'santa rosa 326', '97855603', 3, '8330341', '', 'Silva', 8, '', '', '', NULL);
INSERT INTO "Contact" VALUES (23, 'Ricardo', 'ricardo@loadingplay.com', 'santa rosa 326', '97855603', 3, '8330341', '', 'Silva', 8, '', '', '', NULL);
INSERT INTO "Contact" VALUES (25, 'Ricardo', 'ricardo@loadingplay.com', 'santa rosa 326', '97855603', 3, '8330341', '', 'Silva', 8, '', '', '', NULL);
INSERT INTO "Contact" VALUES (26, 'Ricardo', 'ricardo@loadingplay.com', 'santa rosa 326', '97855603', 3, '8330341', '', 'Silva', 8, '', '', '', NULL);
INSERT INTO "Contact" VALUES (27, 'Ricardo', 'ricardo@loadingplay.com', 'santa rosa 326', '97855603', 3, '8330341', '', 'Silva', 8, '', '', '', NULL);
INSERT INTO "Contact" VALUES (21, 'Ricardo', 'ricardo@loadingplay.com', 'santa rosa 326', '97855603', 3, '8330341', '', 'Silva', 8, '', '', '', NULL);
INSERT INTO "Contact" VALUES (29, 'Ricardo', 'ricardo@loadingplay.com', 'santa rosa 326', '93538018', 3, '7804385', '', 'Silva', 39, '', '', '', NULL);
INSERT INTO "Contact" VALUES (58, 'Yi Chun', 'yichun212@gmail.com', 'alonso de cÃ³rdova 5870', '97855603', 3, '984152515', '', 'Lin', 15, 'santiago', '', '14.645.855-6', 5);
INSERT INTO "Contact" VALUES (38, 'Ricardo', 'ricardo@loadingplay.com', 'santa rosa 2', '912345678', 3, '7804385', '', 'Silva', 16, 'santiago', '', '167618979', 5);
INSERT INTO "Contact" VALUES (50, 'Yi Chun', 'yi.neko@gmail.com', 'santa rosa 326 dpto 1703', '97855603', 3, '8330341', '', 'Lin', 403, 'santiago', '', '14.645.855-6', NULL);
INSERT INTO "Contact" VALUES (65, 'CERTIFICACION', 'certificacion2@transbank.cl', 'HUERFANOS 770', '99999999', 3, '99999999', '', 'WEBPAY', 592, 'SANTIAGO', '', '1-9', 3);
INSERT INTO "Contact" VALUES (32, 'jose', 'jarenasmuller@gmail.com', 'av. americo vespucio', '8251951', 3, '8251951', '', 'Arenas MÃ¼ller', 22, 'la florida', '', '16323861-6', NULL);
INSERT INTO "Contact" VALUES (49, 'soporte tbk', 'soporte9@tbk.cl', 'portugal', '1234567', 3, '6247344', '', 'tbk', 450, 'santiago', '', '111111111', NULL);
INSERT INTO "Contact" VALUES (60, 'Soporte', 'soporte11@transbank.cl', 'Laguna', '800441144', 3, '6247344', '', 'WP', 462, 'santiago', '', '18.455.334-1', 9);
INSERT INTO "Contact" VALUES (61, 'soporte tbk', 'soporte11@transbank.cl', 'Laguna', '800441144', 3, '6247344', '', 'WP', 462, 'santiago', '', '18.455.334-1', 3);
INSERT INTO "Contact" VALUES (59, 'soporte tbk', 'AA@AA.CL', 'prueba', '800441144', 3, '6247344', '', 'X', 462, 'santiago', '', '3-5', 3);
INSERT INTO "Contact" VALUES (55, 'Pruebas', 'aa@aa.com', 'calle pruebas', '999999778', 3, '111', '', 'TBK', 507, 'santiago', '', '999999999', 9);
INSERT INTO "Contact" VALUES (70, 'jose', 'jose@loadingplay.com', 'avenida americo vespucio', '2825473', 3, '8251951', 'uieuriuer', 'arenas', 22, 'Santiago', '', '163238616', 11);
INSERT INTO "Contact" VALUES (52, 'jose', 'jarenasmuller@gmail.com', 'avenida americo vespucio', '11111111', 3, '8251951', '', 'arenas', 22, 'Santiago', '', '11111111-1', 29);
INSERT INTO "Contact" VALUES (69, 'Yi Chun', 'yichun212@gmail.com', 'santa rosa 326 dpto 1703', '84152515', 3, '7550000', '', 'Lin', 733, 'santiago', '', '146458556', 3);
INSERT INTO "Contact" VALUES (63, 'transbank', 'Soporte11@Transbank.cl', 'Portugal 1189', '800441144', 3, '6421215', '', 'WP', 573, 'cxcxccc', '', '1-9', 3);
INSERT INTO "Contact" VALUES (62, 'SOPORTE', 'soporte11@transbank.cl', 'PRUEBAS 1234', '800441144', 3, '6421212', '', 'WP', 573, 'HUECHURABA', '', '11.111.111-1', 3);
INSERT INTO "Contact" VALUES (57, 'TRANSBANK', 'soporte11@transbank.cl', 'prueba', '800441144', 3, '6247344', '', 'Pruebas', 462, 'santiago', '', '15708358-9', 9);
INSERT INTO "Contact" VALUES (56, 'TRANSBANK', 'AA@AA.CL', 'prueba', '800441144', 3, '6247344', '', 'X', 462, 'santiago', '', '3-5', 3);
INSERT INTO "Contact" VALUES (64, 'Soporte WP', 'AA@AA.CL', 'prueba', '800441144', 3, 'sdsds', '', 'WP', 462, 'santiago', '', '208663996', 9);
INSERT INTO "Contact" VALUES (31, 'julian', 'julian@larrea.cl', 'martin de zamora 4381', '348734', 3, '7770008', '', 'larrea', 27, 'las condes', '', '13882457-8', 3);


--
-- Data for Name: Contact_Types; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Contact_Types" VALUES (1, 'Despacho');
INSERT INTO "Contact_Types" VALUES (2, 'Facturacion');
INSERT INTO "Contact_Types" VALUES (3, 'Default');


--
-- Name: Contact_Types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Contact_Types_id_seq"', 3, true);


--
-- Name: Contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Contact_id_seq"', 70, true);


--
-- Data for Name: Kardex; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Kardex" VALUES (2226, 'GDF-PV14-Kereu-C6', 1, 34391, 0, 5, 34391, 0, 0, 0, '2015-02-14 03:45:34.258592', 'ricardo@loadingplay.com', 'mov_out', 'azul', '36.0');
INSERT INTO "Kardex" VALUES (2232, 'GDF-OI14-Queltehue-C39', 1, 33558, 1, 5, 33558, 1, 33558, 33558, '2015-02-19 20:51:12.030994', 'julian@larrea.cl', 'mov_out', '', '37.0');
INSERT INTO "Kardex" VALUES (2233, 'GDF-OI14-Queltehue-C39', 1, 33558, 0, 12, 33558, 1, 33558, 33558, '2015-02-19 20:51:12.030994', 'julian@larrea.cl', 'mov_in', '', '37.0');
INSERT INTO "Kardex" VALUES (2227, 'GDF-PV14-Kereu-C6', 1, 34391, 0, 12, 34391, 1, 34391, 34391, '2015-02-14 03:45:34.506058', 'ricardo@loadingplay.com', 'mov_in', 'azul', '36.0');
INSERT INTO "Kardex" VALUES (2234, 'GDF-OI14-Queltehue-C39', 1, 33558, 1, 12, 33558, 0, 0, 0, '2015-02-19 21:10:42.979633', 'Sistema', 'sell', 'negro camel', '37.0');
INSERT INTO "Kardex" VALUES (2228, 'GDF-PV14-Kereu-C6', 1, 34391, 69900, 12, 34391, 0, 0, 0, '2015-02-14 03:46:17.966984', 'Sistema', 'sell', 'azul', '36.0');
INSERT INTO "Kardex" VALUES (2235, 'GDF-OI14-Queltehue-C39', 1, 33558, 1, 5, 33558, 0, 0, 0, '2015-02-19 21:54:04.337614', 'julian@larrea.cl', 'mov_out', '', '37.0');
INSERT INTO "Kardex" VALUES (2236, 'GDF-OI14-Queltehue-C39', 1, 33558, 0, 12, 33558, 1, 33558, 33558, '2015-02-19 21:54:04.337614', 'julian@larrea.cl', 'mov_in', '', '37.0');
INSERT INTO "Kardex" VALUES (2229, 'GDF-OI14-Queltehue-C39', 1, 33558, 0, 5, 33558, 2, 33558, 67116, '2015-02-14 03:48:36.906395', 'ricardo@loadingplay.com', 'mov_out', 'negro camel', '37.0');
INSERT INTO "Kardex" VALUES (2237, 'GDF-OI14-Queltehue-C39', 1, 33558, 1, 5, 33558, 3, 33558, 100674, '2015-02-19 22:33:33.913606', 'julian@larrea.cl', 'mov_out', '', '38.0');
INSERT INTO "Kardex" VALUES (2238, 'GDF-OI14-Queltehue-C39', 1, 33558, 0, 12, 33558, 1, 33558, 33558, '2015-02-19 22:33:33.913606', 'julian@larrea.cl', 'mov_in', '', '38.0');
INSERT INTO "Kardex" VALUES (2230, 'GDF-OI14-Queltehue-C39', 1, 33558, 0, 12, 33558, 1, 33558, 33558, '2015-02-14 03:48:37.17762', 'ricardo@loadingplay.com', 'mov_in', 'negro camel', '37.0');
INSERT INTO "Kardex" VALUES (2239, 'GDF-OI14-Queltehue-C39', 1, 33558, 1, 12, 33558, 0, 0, 0, '2015-02-19 22:46:40.19236', 'Sistema', 'sell', 'negro camel', '38.0');
INSERT INTO "Kardex" VALUES (2231, 'GDF-OI14-Queltehue-C39', 1, 33558, 1, 12, 33558, 0, 0, 0, '2015-02-14 03:49:15.746875', 'Sistema', 'sell', 'negro camel', '37.0');
INSERT INTO "Kardex" VALUES (2085, 'GDF-OI14-Queltehue-C35', 2, 33558, 0, 5, 67116, 2, 33558, 67116, '2015-01-26 22:52:15.94864', 'ricardo@loadingplay.com', 'buy', 'azul cafÃ©', '35.0');
INSERT INTO "Kardex" VALUES (2086, 'GDF-OI14-Queltehue-C35', 4, 33558, 0, 5, 134232, 4, 33558, 134232, '2015-01-26 22:52:16.05246', 'ricardo@loadingplay.com', 'buy', 'azul cafÃ©', '36.0');
INSERT INTO "Kardex" VALUES (2087, 'GDF-OI14-Queltehue-C35', 12, 33558, 0, 5, 402696, 12, 33558, 402696, '2015-01-26 22:52:16.154327', 'ricardo@loadingplay.com', 'buy', 'azul cafÃ©', '37.0');
INSERT INTO "Kardex" VALUES (2088, 'GDF-OI14-Queltehue-C35', 6, 33558, 0, 5, 201348, 6, 33558, 201348, '2015-01-26 22:52:16.25884', 'ricardo@loadingplay.com', 'buy', 'azul cafÃ©', '38.0');
INSERT INTO "Kardex" VALUES (2089, 'GDF-OI14-Queltehue-C35', 2, 33558, 0, 5, 67116, 2, 33558, 67116, '2015-01-26 22:52:16.366565', 'ricardo@loadingplay.com', 'buy', 'azul cafÃ©', '39.0');
INSERT INTO "Kardex" VALUES (2090, 'GDF-OI14-Queltehue-C35', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:16.47299', 'ricardo@loadingplay.com', 'buy', 'azul cafÃ©', '40.0');
INSERT INTO "Kardex" VALUES (2091, 'GDF-OI14-Queltehue-C19', 3, 33558, 0, 5, 100674, 3, 33558, 100674, '2015-01-26 22:52:17.119818', 'ricardo@loadingplay.com', 'buy', 'cafÃ© moro', '35.0');
INSERT INTO "Kardex" VALUES (2092, 'GDF-OI14-Queltehue-C19', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:17.222992', 'ricardo@loadingplay.com', 'buy', 'cafÃ© moro', '37.0');
INSERT INTO "Kardex" VALUES (2093, 'GDF-OI14-Queltehue-C19', 2, 33558, 0, 5, 67116, 2, 33558, 67116, '2015-01-26 22:52:17.334229', 'ricardo@loadingplay.com', 'buy', 'cafÃ© moro', '39.0');
INSERT INTO "Kardex" VALUES (2094, 'GDF-OI14-Queltehue-C38', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:17.983549', 'ricardo@loadingplay.com', 'buy', 'cafÃ© ocre', '36.0');
INSERT INTO "Kardex" VALUES (2095, 'GDF-OI14-Queltehue-C38', 3, 33558, 0, 5, 100674, 3, 33558, 100674, '2015-01-26 22:52:18.083438', 'ricardo@loadingplay.com', 'buy', 'cafÃ© ocre', '37.0');
INSERT INTO "Kardex" VALUES (2096, 'GDF-OI14-Queltehue-C38', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:18.186152', 'ricardo@loadingplay.com', 'buy', 'cafÃ© ocre', '38.0');
INSERT INTO "Kardex" VALUES (2097, 'GDF-OI14-Queltehue-C38', 3, 33558, 0, 5, 100674, 3, 33558, 100674, '2015-01-26 22:52:18.299221', 'ricardo@loadingplay.com', 'buy', 'cafÃ© ocre', '39.0');
INSERT INTO "Kardex" VALUES (2098, 'GDF-OI14-Queltehue-C38', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:18.421645', 'ricardo@loadingplay.com', 'buy', 'cafÃ© ocre', '40.0');
INSERT INTO "Kardex" VALUES (2099, 'GDF-OI14-Queltehue-C16', 2, 33558, 0, 5, 67116, 2, 33558, 67116, '2015-01-26 22:52:19.089545', 'ricardo@loadingplay.com', 'buy', 'beige taupe', '35.0');
INSERT INTO "Kardex" VALUES (2100, 'GDF-OI14-Queltehue-C39', 3, 33558, 0, 5, 100674, 3, 33558, 100674, '2015-01-26 22:52:19.743586', 'ricardo@loadingplay.com', 'buy', 'negro camel', '37.0');
INSERT INTO "Kardex" VALUES (2101, 'GDF-OI14-Queltehue-C39', 4, 33558, 0, 5, 134232, 4, 33558, 134232, '2015-01-26 22:52:19.851348', 'ricardo@loadingplay.com', 'buy', 'negro camel', '38.0');
INSERT INTO "Kardex" VALUES (2102, 'GDF-OI14-Queltehue-C39', 2, 33558, 0, 5, 67116, 2, 33558, 67116, '2015-01-26 22:52:19.96043', 'ricardo@loadingplay.com', 'buy', 'negro camel', '39.0');
INSERT INTO "Kardex" VALUES (2103, 'GDF-OI14-Queltehue-C30', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:20.621924', 'ricardo@loadingplay.com', 'buy', 'camel azul', '35.0');
INSERT INTO "Kardex" VALUES (2104, 'GDF-OI14-Queltehue-C30', 2, 33558, 0, 5, 67116, 2, 33558, 67116, '2015-01-26 22:52:20.72481', 'ricardo@loadingplay.com', 'buy', 'camel azul', '36.0');
INSERT INTO "Kardex" VALUES (2105, 'GDF-OI14-Queltehue-C30', 3, 33558, 0, 5, 100674, 3, 33558, 100674, '2015-01-26 22:52:20.833103', 'ricardo@loadingplay.com', 'buy', 'camel azul', '37.0');
INSERT INTO "Kardex" VALUES (2106, 'GDF-OI14-Queltehue-C30', 3, 33558, 0, 5, 100674, 3, 33558, 100674, '2015-01-26 22:52:20.94126', 'ricardo@loadingplay.com', 'buy', 'camel azul', '38.0');
INSERT INTO "Kardex" VALUES (2107, 'GDF-OI14-Queltehue-C30', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:21.045222', 'ricardo@loadingplay.com', 'buy', 'camel azul', '39.0');
INSERT INTO "Kardex" VALUES (2108, 'GDF-OI14-Queltehue-C33', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:21.717564', 'ricardo@loadingplay.com', 'buy', 'cafÃ© beige', '35.0');
INSERT INTO "Kardex" VALUES (2109, 'GDF-OI14-Queltehue-C33', 2, 33558, 0, 5, 67116, 2, 33558, 67116, '2015-01-26 22:52:21.83047', 'ricardo@loadingplay.com', 'buy', 'cafÃ© beige', '40.0');
INSERT INTO "Kardex" VALUES (2110, 'GDF-OI14-Queltehue-C26', 2, 33558, 0, 5, 67116, 2, 33558, 67116, '2015-01-26 22:52:22.515703', 'ricardo@loadingplay.com', 'buy', 'camel cafÃ©', '35.0');
INSERT INTO "Kardex" VALUES (2111, 'GDF-OI14-Queltehue-C26', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:22.621056', 'ricardo@loadingplay.com', 'buy', 'camel cafÃ©', '37.0');
INSERT INTO "Kardex" VALUES (2112, 'GDF-OI14-Gavilan-C13', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:23.308609', 'ricardo@loadingplay.com', 'buy', 'cafÃ© beige', '35.0');
INSERT INTO "Kardex" VALUES (2113, 'GDF-OI14-Gavilan-C13', 2, 33558, 0, 5, 67116, 2, 33558, 67116, '2015-01-26 22:52:23.413929', 'ricardo@loadingplay.com', 'buy', 'cafÃ© beige', '36.0');
INSERT INTO "Kardex" VALUES (2114, 'GDF-OI14-Gavilan-C13', 2, 33558, 0, 5, 67116, 2, 33558, 67116, '2015-01-26 22:52:23.521', 'ricardo@loadingplay.com', 'buy', 'cafÃ© beige', '37.0');
INSERT INTO "Kardex" VALUES (2115, 'GDF-OI14-Gavilan-C13', 3, 33558, 0, 5, 100674, 3, 33558, 100674, '2015-01-26 22:52:23.626171', 'ricardo@loadingplay.com', 'buy', 'cafÃ© beige', '38.0');
INSERT INTO "Kardex" VALUES (2116, 'GDF-OI14-Gavilan-C13', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:23.73097', 'ricardo@loadingplay.com', 'buy', 'cafÃ© beige', '39.0');
INSERT INTO "Kardex" VALUES (2117, 'GDF-OI14-Gavilan-C13', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:23.858055', 'ricardo@loadingplay.com', 'buy', 'cafÃ© beige', '40.0');
INSERT INTO "Kardex" VALUES (2118, 'GDF-OI14-Gavilan-C11', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:24.585898', 'ricardo@loadingplay.com', 'buy', 'cafÃ© beige', '39.0');
INSERT INTO "Kardex" VALUES (2119, 'GDF-OI14-Gavilan-C11', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:24.692382', 'ricardo@loadingplay.com', 'buy', 'cafÃ© beige', '40.0');
INSERT INTO "Kardex" VALUES (2120, 'GDF-OI14-Gavilan-C10', 2, 33558, 0, 5, 67116, 2, 33558, 67116, '2015-01-26 22:52:25.415447', 'ricardo@loadingplay.com', 'buy', 'cafÃ© gris', '37.0');
INSERT INTO "Kardex" VALUES (2121, 'GDF-OI14-Gavilan-C10', 3, 33558, 0, 5, 100674, 3, 33558, 100674, '2015-01-26 22:52:25.523429', 'ricardo@loadingplay.com', 'buy', 'cafÃ© gris', '38.0');
INSERT INTO "Kardex" VALUES (2122, 'GDF-OI14-Gavilan-C10', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:25.625407', 'ricardo@loadingplay.com', 'buy', 'cafÃ© gris', '39.0');
INSERT INTO "Kardex" VALUES (2123, 'GDF-OI14-Gavilan-C10', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:25.727822', 'ricardo@loadingplay.com', 'buy', 'cafÃ© gris', '40.0');
INSERT INTO "Kardex" VALUES (2124, 'GDF-OI14-Gavilan-C12', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:26.425217', 'ricardo@loadingplay.com', 'buy', 'verde beige', '35.0');
INSERT INTO "Kardex" VALUES (2125, 'GDF-OI14-Gavilan-C12', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:26.529751', 'ricardo@loadingplay.com', 'buy', 'verde beige', '36.0');
INSERT INTO "Kardex" VALUES (2126, 'GDF-OI14-Gavilan-C12', 6, 33558, 0, 5, 201348, 6, 33558, 201348, '2015-01-26 22:52:26.632282', 'ricardo@loadingplay.com', 'buy', 'verde beige', '37.0');
INSERT INTO "Kardex" VALUES (2127, 'GDF-OI14-Gavilan-C12', 2, 33558, 0, 5, 67116, 2, 33558, 67116, '2015-01-26 22:52:26.737122', 'ricardo@loadingplay.com', 'buy', 'verde beige', '38.0');
INSERT INTO "Kardex" VALUES (2128, 'GDF-OI14-Gavilan-C12', 2, 33558, 0, 5, 67116, 2, 33558, 67116, '2015-01-26 22:52:26.849902', 'ricardo@loadingplay.com', 'buy', 'verde beige', '39.0');
INSERT INTO "Kardex" VALUES (2129, 'GDF-OI14-Gavilan-C12', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:26.960801', 'ricardo@loadingplay.com', 'buy', 'verde beige', '40.0');
INSERT INTO "Kardex" VALUES (2130, 'GDF-OI14-Gavilan-C6', 4, 33558, 0, 5, 134232, 4, 33558, 134232, '2015-01-26 22:52:27.659893', 'ricardo@loadingplay.com', 'buy', 'cafÃ©', '37.0');
INSERT INTO "Kardex" VALUES (2131, 'GDF-OI14-Gavilan-C2', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:28.376515', 'ricardo@loadingplay.com', 'buy', 'negro', '35.0');
INSERT INTO "Kardex" VALUES (2132, 'GDF-OI14-Gavilan-C2', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-01-26 22:52:28.483563', 'ricardo@loadingplay.com', 'buy', 'negro', '40.0');
INSERT INTO "Kardex" VALUES (2133, 'GDF-OI14-Gavilan-C5', 3, 33558, 0, 5, 100674, 3, 33558, 100674, '2015-01-26 22:52:29.199209', 'ricardo@loadingplay.com', 'buy', 'verde gris', '37.0');
INSERT INTO "Kardex" VALUES (2134, 'GDF-PV14-Lile-C8', 2, 34510, 0, 5, 69020, 2, 34510, 69020, '2015-01-26 22:52:29.929147', 'ricardo@loadingplay.com', 'buy', 'azul', '36.0');
INSERT INTO "Kardex" VALUES (2135, 'GDF-PV14-Lile-C8', 5, 34510, 0, 5, 172550, 5, 34510, 172550, '2015-01-26 22:52:30.034302', 'ricardo@loadingplay.com', 'buy', 'azul', '37.0');
INSERT INTO "Kardex" VALUES (2136, 'GDF-PV14-Lile-C8', 4, 34510, 0, 5, 138040, 4, 34510, 138040, '2015-01-26 22:52:30.137576', 'ricardo@loadingplay.com', 'buy', 'azul', '38.0');
INSERT INTO "Kardex" VALUES (2137, 'GDF-PV14-Lile-C9', 2, 34510, 0, 5, 69020, 2, 34510, 69020, '2015-01-26 22:52:30.877623', 'ricardo@loadingplay.com', 'buy', 'azul', '36.0');
INSERT INTO "Kardex" VALUES (2138, 'GDF-PV14-Lile-C9', 7, 34510, 0, 5, 241570, 7, 34510, 241570, '2015-01-26 22:52:30.988294', 'ricardo@loadingplay.com', 'buy', 'azul', '37.0');
INSERT INTO "Kardex" VALUES (2139, 'GDF-PV14-Lile-C9', 2, 34510, 0, 5, 69020, 2, 34510, 69020, '2015-01-26 22:52:31.088304', 'ricardo@loadingplay.com', 'buy', 'azul', '38.0');
INSERT INTO "Kardex" VALUES (2140, 'GDF-PV14-Lile-C9', 2, 34510, 0, 5, 69020, 2, 34510, 69020, '2015-01-26 22:52:31.190072', 'ricardo@loadingplay.com', 'buy', 'azul', '39.0');
INSERT INTO "Kardex" VALUES (2141, 'GDF-PV14-Lile-C2', 2, 34510, 0, 5, 69020, 2, 34510, 69020, '2015-01-26 22:52:31.919045', 'ricardo@loadingplay.com', 'buy', 'rojo', '37.0');
INSERT INTO "Kardex" VALUES (2142, 'GDF-PV14-Lile-C1', 3, 34510, 0, 5, 103530, 3, 34510, 103530, '2015-01-26 22:52:32.636422', 'ricardo@loadingplay.com', 'buy', 'camel', '37.0');
INSERT INTO "Kardex" VALUES (2143, 'GDF-PV14-Lile-C10', 1, 34510, 0, 5, 34510, 1, 34510, 34510, '2015-01-26 22:52:33.366897', 'ricardo@loadingplay.com', 'buy', 'camel', '35.0');
INSERT INTO "Kardex" VALUES (2144, 'GDF-PV14-Lile-C10', 2, 34510, 0, 5, 69020, 2, 34510, 69020, '2015-01-26 22:52:33.477898', 'ricardo@loadingplay.com', 'buy', 'camel', '36.0');
INSERT INTO "Kardex" VALUES (2145, 'GDF-PV14-Lile-C10', 2, 34510, 0, 5, 69020, 2, 34510, 69020, '2015-01-26 22:52:33.579038', 'ricardo@loadingplay.com', 'buy', 'camel', '37.0');
INSERT INTO "Kardex" VALUES (2146, 'GDF-PV14-Lile-C10', 1, 34510, 0, 5, 34510, 1, 34510, 34510, '2015-01-26 22:52:33.680848', 'ricardo@loadingplay.com', 'buy', 'camel', '39.0');
INSERT INTO "Kardex" VALUES (2147, 'GDF-PV14-Lile-C10', 2, 34510, 0, 5, 69020, 2, 34510, 69020, '2015-01-26 22:52:33.792759', 'ricardo@loadingplay.com', 'buy', 'camel', '40.0');
INSERT INTO "Kardex" VALUES (2148, 'GDF-PV14-Kereu-C6', 1, 34391, 0, 5, 34391, 1, 34391, 34391, '2015-01-26 22:52:34.522234', 'ricardo@loadingplay.com', 'buy', 'azul', '36.0');
INSERT INTO "Kardex" VALUES (2149, 'GDF-PV14-Kereu-C6', 2, 34391, 0, 5, 68782, 2, 34391, 68782, '2015-01-26 22:52:34.624203', 'ricardo@loadingplay.com', 'buy', 'azul', '37.0');
INSERT INTO "Kardex" VALUES (2150, 'GDF-PV14-Kereu-C6', 1, 34391, 0, 5, 34391, 1, 34391, 34391, '2015-01-26 22:52:34.725458', 'ricardo@loadingplay.com', 'buy', 'azul', '40.0');
INSERT INTO "Kardex" VALUES (2151, 'GDF-PV14-Kereu-C11', 2, 34391, 0, 5, 68782, 2, 34391, 68782, '2015-01-26 22:52:35.464931', 'ricardo@loadingplay.com', 'buy', 'cafÃ©', '38.0');
INSERT INTO "Kardex" VALUES (2152, 'GDF-PV14-Kereu-C11', 2, 34391, 0, 5, 68782, 2, 34391, 68782, '2015-01-26 22:52:35.564923', 'ricardo@loadingplay.com', 'buy', 'cafÃ©', '40.0');
INSERT INTO "Kardex" VALUES (2153, 'GDF-PV14-Kereu-C12', 1, 34391, 0, 5, 34391, 1, 34391, 34391, '2015-01-26 22:52:36.305889', 'ricardo@loadingplay.com', 'buy', 'beige', '36.0');
INSERT INTO "Kardex" VALUES (2154, 'GDF-PV14-Kereu-C12', 1, 34391, 0, 5, 34391, 1, 34391, 34391, '2015-01-26 22:52:36.410286', 'ricardo@loadingplay.com', 'buy', 'beige', '37.0');
INSERT INTO "Kardex" VALUES (2155, 'GDF-PV14-Kereu-C12', 2, 34391, 0, 5, 68782, 2, 34391, 68782, '2015-01-26 22:52:36.514822', 'ricardo@loadingplay.com', 'buy', 'beige', '40.0');
INSERT INTO "Kardex" VALUES (2156, 'GDF-PV14-Kereu-C5', 1, 34391, 0, 5, 34391, 1, 34391, 34391, '2015-01-26 22:52:37.248778', 'ricardo@loadingplay.com', 'buy', 'cafÃ© verde', '35.0');
INSERT INTO "Kardex" VALUES (2157, 'GDF-PV14-Kereu-C5', 1, 34391, 0, 5, 34391, 1, 34391, 34391, '2015-01-26 22:52:37.358286', 'ricardo@loadingplay.com', 'buy', 'cafÃ© verde', '37.0');
INSERT INTO "Kardex" VALUES (2158, 'GDF-PV14-Kereu-C5', 2, 34391, 0, 5, 68782, 2, 34391, 68782, '2015-01-26 22:52:37.549534', 'ricardo@loadingplay.com', 'buy', 'cafÃ© verde', '38.0');
INSERT INTO "Kardex" VALUES (2159, 'GDF-PV14-Kereu-C5', 1, 34391, 0, 5, 34391, 1, 34391, 34391, '2015-01-26 22:52:37.652283', 'ricardo@loadingplay.com', 'buy', 'cafÃ© verde', '39.0');
INSERT INTO "Kardex" VALUES (2160, 'GDF-PV14-Kereu-C1', 1, 34391, 0, 5, 34391, 1, 34391, 34391, '2015-01-26 22:52:38.426087', 'ricardo@loadingplay.com', 'buy', 'negro', '36.0');
INSERT INTO "Kardex" VALUES (2161, 'GDF-PV14-Kereu-C1', 1, 34391, 0, 5, 34391, 1, 34391, 34391, '2015-01-26 22:52:38.530282', 'ricardo@loadingplay.com', 'buy', 'negro', '40.0');
INSERT INTO "Kardex" VALUES (2162, 'GDF-PV14-Kereu-C3', 1, 34391, 0, 5, 34391, 1, 34391, 34391, '2015-01-26 22:52:39.282159', 'ricardo@loadingplay.com', 'buy', 'cafÃ© negro', '35.0');
INSERT INTO "Kardex" VALUES (2163, 'GDF-PV14-Kereu-C3', 1, 34391, 0, 5, 34391, 1, 34391, 34391, '2015-01-26 22:52:39.386481', 'ricardo@loadingplay.com', 'buy', 'cafÃ© negro', '36.0');
INSERT INTO "Kardex" VALUES (2164, 'GDF-PV14-Lile-C13', 1, 34510, 0, 5, 34510, 1, 34510, 34510, '2015-01-26 22:52:40.137329', 'ricardo@loadingplay.com', 'buy', 'Beige', '35.0');
INSERT INTO "Kardex" VALUES (2165, 'GDF-PV14-Lile-C13', 3, 34510, 0, 5, 103530, 3, 34510, 103530, '2015-01-26 22:52:40.238498', 'ricardo@loadingplay.com', 'buy', 'Beige', '37.0');
INSERT INTO "Kardex" VALUES (2166, 'GDF-OI14-Queltehue-C31', 2, 33558, 0, 5, 67116, 2, 33558, 67116, '2015-01-26 22:52:41.002267', 'ricardo@loadingplay.com', 'buy', 'camel rojo', '35.0');
INSERT INTO "Kardex" VALUES (2167, 'GDF-OI14-Queltehue-C31', 2, 33558, 0, 5, 67116, 2, 33558, 67116, '2015-01-26 22:52:41.104656', 'ricardo@loadingplay.com', 'buy', 'camel rojo', '37.0');
INSERT INTO "Kardex" VALUES (2168, 'GDF-PV14-Sirisi-C8', 1, 32011, 0, 5, 32011, 1, 32011, 32011, '2015-01-26 22:52:41.865022', 'ricardo@loadingplay.com', 'buy', 'croco rojo', '36.0');
INSERT INTO "Kardex" VALUES (2169, 'GDF-PV14-Sirisi-C8', 3, 32011, 0, 5, 96033, 3, 32011, 96033, '2015-01-26 22:52:41.972153', 'ricardo@loadingplay.com', 'buy', 'croco rojo', '37.0');
INSERT INTO "Kardex" VALUES (2170, 'GDF-PV14-Sirisi-C8', 2, 32011, 0, 5, 64022, 2, 32011, 64022, '2015-01-26 22:52:42.071887', 'ricardo@loadingplay.com', 'buy', 'croco rojo', '38.0');
INSERT INTO "Kardex" VALUES (2171, 'GDF-PV14-Sirisi-C8', 1, 32011, 0, 5, 32011, 1, 32011, 32011, '2015-01-26 22:52:42.175488', 'ricardo@loadingplay.com', 'buy', 'croco rojo', '40.0');
INSERT INTO "Kardex" VALUES (2172, 'GDF-PV14-Sirisi-C9', 1, 32011, 0, 5, 32011, 1, 32011, 32011, '2015-01-26 22:52:42.953116', 'ricardo@loadingplay.com', 'buy', 'croco beige', '35.0');
INSERT INTO "Kardex" VALUES (2173, 'GDF-PV14-Sirisi-C9', 2, 32011, 0, 5, 64022, 2, 32011, 64022, '2015-01-26 22:52:43.05209', 'ricardo@loadingplay.com', 'buy', 'croco beige', '36.0');
INSERT INTO "Kardex" VALUES (2174, 'GDF-PV14-Sirisi-C9', 3, 32011, 0, 5, 96033, 3, 32011, 96033, '2015-01-26 22:52:43.153654', 'ricardo@loadingplay.com', 'buy', 'croco beige', '37.0');
INSERT INTO "Kardex" VALUES (2175, 'GDF-PV14-Sirisi-C9', 2, 32011, 0, 5, 64022, 2, 32011, 64022, '2015-01-26 22:52:43.254623', 'ricardo@loadingplay.com', 'buy', 'croco beige', '38.0');
INSERT INTO "Kardex" VALUES (2176, 'GDF-PV14-Sirisi-C9', 1, 32011, 0, 5, 32011, 1, 32011, 32011, '2015-01-26 22:52:43.364026', 'ricardo@loadingplay.com', 'buy', 'croco beige', '39.0');
INSERT INTO "Kardex" VALUES (2177, 'GDF-PV14-Sirisi-C9', 1, 32011, 0, 5, 32011, 1, 32011, 32011, '2015-01-26 22:52:43.470001', 'ricardo@loadingplay.com', 'buy', 'croco beige', '40.0');
INSERT INTO "Kardex" VALUES (2178, 'GDF-PV14-Sirisi-C5', 1, 32011, 0, 5, 32011, 1, 32011, 32011, '2015-01-26 22:52:44.237899', 'ricardo@loadingplay.com', 'buy', 'beige', '37.0');
INSERT INTO "Kardex" VALUES (2179, 'GDF-PV14-Sirisi-C5', 1, 32011, 0, 5, 32011, 1, 32011, 32011, '2015-01-26 22:52:44.351081', 'ricardo@loadingplay.com', 'buy', 'beige', '38.0');
INSERT INTO "Kardex" VALUES (2180, 'GDF-PV14-Sirisi-C7', 3, 32011, 0, 5, 96033, 3, 32011, 96033, '2015-01-26 22:52:45.163893', 'ricardo@loadingplay.com', 'buy', 'croco negro gris', '37.0');
INSERT INTO "Kardex" VALUES (2181, 'GDF-PV14-Sirisi-C7', 2, 32011, 0, 5, 64022, 2, 32011, 64022, '2015-01-26 22:52:45.271654', 'ricardo@loadingplay.com', 'buy', 'croco negro gris', '38.0');
INSERT INTO "Kardex" VALUES (2182, 'GDF-PV14-Sirisi-C7', 2, 32011, 0, 5, 64022, 2, 32011, 64022, '2015-01-26 22:52:45.375849', 'ricardo@loadingplay.com', 'buy', 'croco negro gris', '39.0');
INSERT INTO "Kardex" VALUES (2183, 'GDF-PV14-Sirisi-C7', 1, 32011, 0, 5, 32011, 1, 32011, 32011, '2015-01-26 22:52:45.482411', 'ricardo@loadingplay.com', 'buy', 'croco negro gris', '40.0');
INSERT INTO "Kardex" VALUES (2184, 'GDF-PV14-Sirisi-C3', 1, 32011, 0, 5, 32011, 1, 32011, 32011, '2015-01-26 22:52:46.262756', 'ricardo@loadingplay.com', 'buy', 'verde', '36.0');
INSERT INTO "Kardex" VALUES (2185, 'GDF-PV14-Sirisi-C3', 1, 32011, 0, 5, 32011, 1, 32011, 32011, '2015-01-26 22:52:46.369583', 'ricardo@loadingplay.com', 'buy', 'verde', '40.0');
INSERT INTO "Kardex" VALUES (2186, 'GDF-PV14-Sirisi-C1', 4, 32011, 0, 5, 128044, 4, 32011, 128044, '2015-01-26 22:52:47.153432', 'ricardo@loadingplay.com', 'buy', 'musgo', '37.0');
INSERT INTO "Kardex" VALUES (2187, 'GDF-PV14-Sirisi-C1', 1, 32011, 0, 5, 32011, 1, 32011, 32011, '2015-01-26 22:52:47.255103', 'ricardo@loadingplay.com', 'buy', 'musgo', '38.0');
INSERT INTO "Kardex" VALUES (2188, 'GDF-PV14-Sirisi-C2', 3, 32011, 0, 5, 96033, 3, 32011, 96033, '2015-01-26 22:52:48.058092', 'ricardo@loadingplay.com', 'buy', 'rosa viejo', '37.0');
INSERT INTO "Kardex" VALUES (2189, 'GDF-PV14-Sirisi-C2', 3, 32011, 0, 5, 96033, 3, 32011, 96033, '2015-01-26 22:52:48.161066', 'ricardo@loadingplay.com', 'buy', 'rosa viejo', '38.0');
INSERT INTO "Kardex" VALUES (2190, 'GDF-PV14-Sirisi-C2', 1, 32011, 0, 5, 32011, 1, 32011, 32011, '2015-01-26 22:52:48.270603', 'ricardo@loadingplay.com', 'buy', 'rosa viejo', '39.0');
INSERT INTO "Kardex" VALUES (2191, 'GDF-PV14-Sirisi-C2', 1, 32011, 0, 5, 32011, 1, 32011, 32011, '2015-01-26 22:52:48.376499', 'ricardo@loadingplay.com', 'buy', 'rosa viejo', '40.0');
INSERT INTO "Kardex" VALUES (2192, 'GDF-PV14-Sirisi-C4', 1, 32011, 0, 5, 32011, 1, 32011, 32011, '2015-01-26 22:52:49.182611', 'ricardo@loadingplay.com', 'buy', 'mostaza', '36.0');
INSERT INTO "Kardex" VALUES (2193, 'GDF-PV14-Sirisi-C4', 4, 32011, 0, 5, 128044, 4, 32011, 128044, '2015-01-26 22:52:49.295452', 'ricardo@loadingplay.com', 'buy', 'mostaza', '37.0');
INSERT INTO "Kardex" VALUES (2194, 'GDF-PV14-Sirisi-C4', 3, 32011, 0, 5, 96033, 3, 32011, 96033, '2015-01-26 22:52:49.402402', 'ricardo@loadingplay.com', 'buy', 'mostaza', '38.0');
INSERT INTO "Kardex" VALUES (2195, 'GDF-PV14-Sirisi-C4', 2, 32011, 0, 5, 64022, 2, 32011, 64022, '2015-01-26 22:52:49.508685', 'ricardo@loadingplay.com', 'buy', 'mostaza', '39.0');
INSERT INTO "Kardex" VALUES (2196, 'GDF-OI14-Queltehue-C19', 1, 33558, 69900, 5, 33558, 2, 33558, 67116, '2015-02-04 14:19:28.314', 'yi.neko@gmail.com', 'sell', '', '35.0');
INSERT INTO "Kardex" VALUES (2197, 'GDF-OI14-Queltehue-C19', 1, 33558, 0, 5, 33558, 3, 33558, 100674, '2015-02-04 14:19:28.314', 'yi.neko@gmail.com', 'buy', '', '35.0');
INSERT INTO "Kardex" VALUES (2198, 'GDF-OI14-Gavilan-C11', 1, 33558, 69900, 5, 33558, 0, 0, 0, '2015-02-04 14:19:36.233', 'yi.neko@gmail.com', 'sell', '', '39.0');
INSERT INTO "Kardex" VALUES (2199, 'GDF-OI14-Gavilan-C11', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-02-04 14:19:36.233', 'yi.neko@gmail.com', 'buy', '', '39.0');
INSERT INTO "Kardex" VALUES (2200, 'GDF-OI14-Queltehue-C19', 1, 33558, 69900, 5, 33558, 2, 33558, 67116, '2015-02-04 14:20:16.815', 'yi.neko@gmail.com', 'sell', '', '35.0');
INSERT INTO "Kardex" VALUES (2201, 'GDF-OI14-Queltehue-C19', 1, 33558, 0, 5, 33558, 3, 33558, 100674, '2015-02-04 14:20:16.815', 'yi.neko@gmail.com', 'buy', '', '35.0');
INSERT INTO "Kardex" VALUES (2202, 'GDF-OI14-Gavilan-C11', 1, 33558, 69900, 5, 33558, 0, 0, 0, '2015-02-04 14:20:24.522', 'yi.neko@gmail.com', 'sell', '', '39.0');
INSERT INTO "Kardex" VALUES (2203, 'GDF-OI14-Gavilan-C11', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-02-04 14:20:24.522', 'yi.neko@gmail.com', 'buy', '', '39.0');
INSERT INTO "Kardex" VALUES (2204, 'GDF-OI14-Queltehue-C19', 1, 33558, 69900, 5, 33558, 2, 33558, 67116, '2015-02-04 14:21:43.56', 'yi.neko@gmail.com', 'sell', '', '35.0');
INSERT INTO "Kardex" VALUES (2205, 'GDF-OI14-Queltehue-C19', 1, 33558, 0, 5, 33558, 3, 33558, 100674, '2015-02-04 14:21:43.56', 'yi.neko@gmail.com', 'buy', '', '35.0');
INSERT INTO "Kardex" VALUES (2206, 'GDF-OI14-Gavilan-C11', 1, 33558, 69900, 5, 33558, 0, 0, 0, '2015-02-04 14:21:51.382', 'yi.neko@gmail.com', 'sell', '', '39.0');
INSERT INTO "Kardex" VALUES (2207, 'GDF-OI14-Gavilan-C11', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-02-04 14:21:51.382', 'yi.neko@gmail.com', 'buy', '', '39.0');
INSERT INTO "Kardex" VALUES (2208, 'GDF-OI14-Queltehue-C19', 1, 33558, 69900, 5, 33558, 2, 33558, 67116, '2015-02-04 14:22:33.885', 'yi.neko@gmail.com', 'sell', '', '35.0');
INSERT INTO "Kardex" VALUES (2209, 'GDF-OI14-Queltehue-C19', 1, 33558, 0, 5, 33558, 3, 33558, 100674, '2015-02-04 14:22:33.885', 'yi.neko@gmail.com', 'buy', '', '35.0');
INSERT INTO "Kardex" VALUES (2210, 'GDF-OI14-Gavilan-C11', 1, 33558, 69900, 5, 33558, 0, 0, 0, '2015-02-04 14:22:41.805', 'yi.neko@gmail.com', 'sell', '', '39.0');
INSERT INTO "Kardex" VALUES (2211, 'GDF-OI14-Gavilan-C11', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-02-04 14:22:41.805', 'yi.neko@gmail.com', 'buy', '', '39.0');
INSERT INTO "Kardex" VALUES (2212, 'GDF-OI14-Queltehue-C19', 1, 33558, 69900, 5, 33558, 2, 33558, 67116, '2015-02-04 14:23:51.91', 'yi.neko@gmail.com', 'sell', '', '35.0');
INSERT INTO "Kardex" VALUES (2213, 'GDF-OI14-Queltehue-C19', 1, 33558, 0, 5, 33558, 3, 33558, 100674, '2015-02-04 14:23:51.91', 'yi.neko@gmail.com', 'buy', '', '35.0');
INSERT INTO "Kardex" VALUES (2214, 'GDF-OI14-Gavilan-C11', 1, 33558, 69900, 5, 33558, 0, 0, 0, '2015-02-04 14:23:59.866', 'yi.neko@gmail.com', 'sell', '', '39.0');
INSERT INTO "Kardex" VALUES (2215, 'GDF-OI14-Gavilan-C11', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-02-04 14:23:59.866', 'yi.neko@gmail.com', 'buy', '', '39.0');
INSERT INTO "Kardex" VALUES (2216, 'GDF-OI14-Queltehue-C39', 1, 33558, 1, 5, 33558, 2, 33558, 67116, '2015-02-04 18:49:57.772213', 'yichun212@gmail.com', 'sell', '', '37.0');
INSERT INTO "Kardex" VALUES (2217, 'GDF-OI14-Queltehue-C39', 1, 33558, 0, 5, 33558, 3, 33558, 100674, '2015-02-04 18:49:57.772213', 'yichun212@gmail.com', 'buy', '', '37.0');
INSERT INTO "Kardex" VALUES (2218, 'GDF-OI14-Queltehue-C16', 1, 33558, 69900, 5, 33558, 1, 33558, 33558, '2015-02-04 23:22:48.885762', 'yichun212@gmail.com', 'sell', '', '35.0');
INSERT INTO "Kardex" VALUES (2219, 'GDF-OI14-Queltehue-C16', 1, 33558, 0, 5, 33558, 2, 33558, 67116, '2015-02-04 23:22:48.885762', 'yichun212@gmail.com', 'buy', '', '35.0');
INSERT INTO "Kardex" VALUES (2220, 'GDF-OI14-Queltehue-C39', 1, 33558, 1, 5, 33558, 2, 33558, 67116, '2015-02-05 00:34:26.653479', 'julian@larrea.cl', 'sell', '', '37.0');
INSERT INTO "Kardex" VALUES (2221, 'GDF-OI14-Queltehue-C39', 1, 33558, 0, 5, 33558, 3, 33558, 100674, '2015-02-05 00:34:26.653479', 'julian@larrea.cl', 'buy', '', '37.0');
INSERT INTO "Kardex" VALUES (2222, 'GDF-OI14-Queltehue-C39', 1, 33558, 1, 5, 33558, 2, 33558, 67116, '2015-02-05 00:34:27.975298', 'julian@larrea.cl', 'sell', '', '37.0');
INSERT INTO "Kardex" VALUES (2223, 'GDF-OI14-Queltehue-C39', 1, 33558, 0, 5, 33558, 3, 33558, 100674, '2015-02-05 00:34:27.975298', 'julian@larrea.cl', 'buy', '', '37.0');
INSERT INTO "Kardex" VALUES (2224, 'GDF-OI14-Queltehue-C38', 1, 33558, 69900, 5, 33558, 0, 0, 0, '2015-02-05 01:14:42.763499', 'julian@larrea.cl', 'sell', '', '36.0');
INSERT INTO "Kardex" VALUES (2225, 'GDF-OI14-Queltehue-C38', 1, 33558, 0, 5, 33558, 1, 33558, 33558, '2015-02-05 01:14:42.763499', 'julian@larrea.cl', 'buy', '', '36.0');


--
-- Name: Kardex_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Kardex_id_seq"', 2239, true);


--
-- Data for Name: Order; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Order" VALUES (262, '2015-02-04 23:22:48.531058', 1, 69900, 2450, 0, 69900, 1, 1, 733, 69, 69, 1, 'web', '', 2, NULL, NULL);
INSERT INTO "Order" VALUES (263, '2015-02-05 00:01:23.462434', 1, 489300, 26040, 0, 489300, 7, 5, 27, 31, 31, 1, 'web', '', 2, NULL, NULL);
INSERT INTO "Order" VALUES (265, '2015-02-05 01:14:42.658658', 1, 69900, 0, 0, 69900, 1, 1, 27, 31, 31, 1, 'web', '', 1, NULL, NULL);
INSERT INTO "Order" VALUES (266, '2015-02-06 14:01:04.939812', 1, 209701, 0, 0, 209701, 4, 3, 27, 31, 31, 1, 'web', '', 1, NULL, NULL);
INSERT INTO "Order" VALUES (267, '2015-02-06 18:53:26.587566', 1, 139800, 14260, 0, 139800, 2, 1, 22, 70, 70, 1, 'web', '', 1, NULL, NULL);
INSERT INTO "Order" VALUES (268, '2015-02-06 18:55:37.414273', 1, 139800, 14260, 0, 139800, 2, 1, 22, 70, 70, 1, 'web', '', 1, NULL, NULL);
INSERT INTO "Order" VALUES (270, '2015-02-09 17:26:56.040902', 1, 69900, 0, 0, 69900, 1, 1, 733, 69, 69, 1, 'web', '', 4, 'RE123Correo', 2);
INSERT INTO "Order" VALUES (264, '2015-02-05 00:31:50.251498', 1, 1, 0, 0, 1, 1, 1, 27, 31, 31, 2, 'web', '', 4, 'Orden264Chilexpress', 1);
INSERT INTO "Order" VALUES (271, '2015-02-17 20:08:42.30893', 1, 279601, 0, 0, 279601, 5, 4, 27, 31, 31, 2, 'web', '', 1, NULL, NULL);
INSERT INTO "Order" VALUES (273, '2015-02-17 20:18:19.428209', 1, 349501, 0, 0, 349501, 6, 5, 27, 31, 31, 2, 'web', '', 1, NULL, NULL);
INSERT INTO "Order" VALUES (260, '2015-01-31 00:56:15.151287', 1, 139800, 7780, 0, 139800, 2, 2, 27, 31, 31, 1, 'web', '', 5, NULL, NULL);
INSERT INTO "Order" VALUES (261, '2015-02-04 18:49:09.001374', 1, 1, 0, 0, 1, 1, 1, 733, 69, 69, 2, 'web', '', 5, NULL, NULL);
INSERT INTO "Order" VALUES (275, '2015-02-19 21:00:47.11141', 1, 69900, 0, 0, 69900, 1, 1, 27, 31, 31, 1, 'web', '', 3, NULL, NULL);
INSERT INTO "Order" VALUES (274, '2015-02-19 20:49:28.721892', 1, 1, 0, 0, 1, 1, 1, 27, 31, 31, 2, 'web', '', 4, '1234', 1);
INSERT INTO "Order" VALUES (276, '2015-02-19 21:01:17.279996', 1, 69900, 0, 0, 69900, 1, 1, 27, 31, 31, 1, 'web', '', 2, NULL, NULL);
INSERT INTO "Order" VALUES (278, '2015-02-19 21:52:57.235429', 1, 1, 0, 0, 1, 1, 1, 27, 31, 31, 2, 'web', '', 3, NULL, NULL);
INSERT INTO "Order" VALUES (280, '2015-02-19 22:32:16.243885', 1, 1, 0, 0, 1, 1, 1, 27, 31, 31, 2, 'web', '', 4, '1234', 1);


--
-- Data for Name: Order_Detail; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Order_Detail" VALUES (291, 1, 69900, 260, 114, '35.0');
INSERT INTO "Order_Detail" VALUES (292, 1, 69900, 260, 122, '39.0');
INSERT INTO "Order_Detail" VALUES (293, 1, 1, 261, 117, '37.0');
INSERT INTO "Order_Detail" VALUES (294, 1, 69900, 262, 116, '35.0');
INSERT INTO "Order_Detail" VALUES (295, 2, 139800, 263, 117, '37.0');
INSERT INTO "Order_Detail" VALUES (296, 1, 69900, 263, 117, '37.0');
INSERT INTO "Order_Detail" VALUES (297, 1, 69900, 263, 116, '35.0');
INSERT INTO "Order_Detail" VALUES (298, 1, 69900, 263, 114, '35.0');
INSERT INTO "Order_Detail" VALUES (299, 2, 139800, 263, 114, '35.0');
INSERT INTO "Order_Detail" VALUES (300, 1, 1, 264, 117, '37.0');
INSERT INTO "Order_Detail" VALUES (301, 1, 69900, 265, 115, '36.0');
INSERT INTO "Order_Detail" VALUES (302, 1, 69900, 266, 114, '35.0');
INSERT INTO "Order_Detail" VALUES (303, 2, 139800, 266, 116, '35.0');
INSERT INTO "Order_Detail" VALUES (304, 1, 1, 266, 117, '37.0');
INSERT INTO "Order_Detail" VALUES (305, 2, 139800, 267, 116, '35.0');
INSERT INTO "Order_Detail" VALUES (306, 2, 139800, 268, 116, '35.0');
INSERT INTO "Order_Detail" VALUES (307, 1, 69900, 270, 133, '36.0');
INSERT INTO "Order_Detail" VALUES (308, 2, 139800, 271, 116, '35.0');
INSERT INTO "Order_Detail" VALUES (309, 1, 69900, 271, 114, '35.0');
INSERT INTO "Order_Detail" VALUES (310, 1, 69900, 271, 114, '35.0');
INSERT INTO "Order_Detail" VALUES (311, 1, 1, 271, 117, '37.0');
INSERT INTO "Order_Detail" VALUES (312, 2, 139800, 273, 116, '35.0');
INSERT INTO "Order_Detail" VALUES (313, 1, 69900, 273, 114, '35.0');
INSERT INTO "Order_Detail" VALUES (314, 1, 69900, 273, 114, '35.0');
INSERT INTO "Order_Detail" VALUES (315, 1, 1, 273, 117, '37.0');
INSERT INTO "Order_Detail" VALUES (316, 1, 69900, 273, 122, '39.0');
INSERT INTO "Order_Detail" VALUES (317, 1, 1, 274, 117, '37.0');
INSERT INTO "Order_Detail" VALUES (318, 1, 69900, 275, 116, '35.0');
INSERT INTO "Order_Detail" VALUES (319, 1, 69900, 276, 116, '35.0');
INSERT INTO "Order_Detail" VALUES (320, 1, 1, 278, 117, '37.0');
INSERT INTO "Order_Detail" VALUES (321, 1, 1, 280, 117, '38.0');


--
-- Name: Order_Detail_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Order_Detail_id_seq"', 321, true);


--
-- Name: Order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Order_id_seq"', 280, true);


--
-- Data for Name: Payment_Types; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Payment_Types" VALUES (1, 'Transferencia');
INSERT INTO "Payment_Types" VALUES (2, 'Webpay');


--
-- Name: Payment_Types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Payment_Types_id_seq"', 2, true);


--
-- Name: Payment_Types_name_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Payment_Types_name_seq"', 1, false);


--
-- Data for Name: Permission; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Permission" VALUES (1, 'acceso a api');
INSERT INTO "Permission" VALUES (2, 'cargar productos nuevos');
INSERT INTO "Permission" VALUES (3, 'vender');
INSERT INTO "Permission" VALUES (4, 'modificar bodegas');
INSERT INTO "Permission" VALUES (5, 'administrar usuarios');
INSERT INTO "Permission" VALUES (6, 'ver informes');


--
-- Name: Permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Permission_id_seq"', 6, true);


--
-- Data for Name: Product; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Product" VALUES (141, 'GDF-PV14-Sirisi-C8', '<ul><li>Color:  croco rojo&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{36.0,37.0,38.0,40.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Sirisi-C8.png', '1_GDF-PV14-Sirisi-C8.png', '2_GDF-PV14-Sirisi-C8.png', 32011, 1, '', 'Calzur Ltda.', 'Sirisi C8', 'croco rojo', '.', 67900, '', '', 1, '3_GDF-PV14-Sirisi-C8.png', '4_GDF-PV14-Sirisi-C8.png', '5_GDF-PV14-Sirisi-C8.png');
INSERT INTO "Product" VALUES (116, 'GDF-OI14-Queltehue-C16', '<ul><li>Color: beige taupe&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{35.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Queltehue-C16.png', '1_GDF-OI14-Queltehue-C16.png', '2_GDF-OI14-Queltehue-C16.png', 33558, 1, '', 'Calzur Ltda.', 'Queltehue C16', 'beige taupe', '.', 69900, '', '', 1, '3_GDF-OI14-Queltehue-C16.png', '4_GDF-OI14-Queltehue-C16.png', '5_GDF-OI14-Queltehue-C16.png');
INSERT INTO "Product" VALUES (113, 'GDF-OI14-Queltehue-C35', '<ul><li>Color: azul cafÃ©&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{35.0,36.0,37.0,38.0,39.0,40.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Queltehue-C35.png', '1_GDF-OI14-Queltehue-C35.png', '2_GDF-OI14-Queltehue-C35.png', 33558, 1, '', 'Calzur Ltda.', 'Queltehue C35', 'azul cafÃ©', '.', 69900, '', '', 1, '3_GDF-OI14-Queltehue-C35.png', '4_GDF-OI14-Queltehue-C35.png', '5_GDF-OI14-Queltehue-C35.png');
INSERT INTO "Product" VALUES (114, 'GDF-OI14-Queltehue-C19', '<ul><li>Color: cafÃ© moro&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{35.0,37.0,39.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Queltehue-C19.png', '1_GDF-OI14-Queltehue-C19.png', '2_GDF-OI14-Queltehue-C19.png', 33558, 1, '', 'Calzur Ltda.', 'Queltehue C19', 'cafÃ© moro', '.', 69900, '', '', 1, '3_GDF-OI14-Queltehue-C19.png', '4_GDF-OI14-Queltehue-C19.png', '5_GDF-OI14-Queltehue-C19.png');
INSERT INTO "Product" VALUES (118, 'GDF-OI14-Queltehue-C30', '<ul><li>Color: camel azul&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{35.0,36.0,37.0,38.0,39.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Queltehue-C30.png', '1_GDF-OI14-Queltehue-C30.png', '2_GDF-OI14-Queltehue-C30.png', 33558, 1, '', 'Calzur Ltda.', 'Queltehue C30', 'camel azul', '.', 69900, '', '', 1, '3_GDF-OI14-Queltehue-C30.png', '4_GDF-OI14-Queltehue-C30.png', '5_GDF-OI14-Queltehue-C30.png');
INSERT INTO "Product" VALUES (115, 'GDF-OI14-Queltehue-C38', '<ul><li>Color: cafÃ© ocre&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{36.0,37.0,38.0,39.0,40.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Queltehue-C38.png', '1_GDF-OI14-Queltehue-C38.png', '2_GDF-OI14-Queltehue-C38.png', 33558, 1, '', 'Calzur Ltda.', 'Queltehue C38', 'cafÃ© ocre', '.', 69900, '', '', 1, '3_GDF-OI14-Queltehue-C38.png', '4_GDF-OI14-Queltehue-C38.png', '5_GDF-OI14-Queltehue-C38.png');
INSERT INTO "Product" VALUES (117, 'GDF-OI14-Queltehue-C39', '<ul><li>Color: negro camel&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{37.0,38.0,39.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Queltehue-C39.png', '1_GDF-OI14-Queltehue-C39.png', '2_GDF-OI14-Queltehue-C39.png', 33558, 1, '', 'Calzur Ltda.', 'Queltehue C39', 'negro camel', '.', 1, '', '', 1, '3_GDF-OI14-Queltehue-C39.png', '4_GDF-OI14-Queltehue-C39.png', '5_GDF-OI14-Queltehue-C39.png');
INSERT INTO "Product" VALUES (122, 'GDF-OI14-Gavilan-C11', '<ul><li>Color: CafÃ© Beige&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{39.0,40.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Gavilan-C11.png', '1_GDF-OI14-Gavilan-C11.png', '2_GDF-OI14-Gavilan-C11.png', 33558, 1, '', 'Calzur Ltda.', 'Gavilan C11', 'cafÃ© beige', '.', 69900, '', '', 1, '3_GDF-OI14-Gavilan-C11.png', '4_GDF-OI14-Gavilan-C11.png', '5_GDF-OI14-Gavilan-C11.png');
INSERT INTO "Product" VALUES (121, 'GDF-OI14-Gavilan-C13', '<ul><li>Color: CafÃ© Beige</li><li>Capellada (material exterior): Cuero</li><li>Forro (material interior): Cuero</li><li>Plantilla: Cuero</li><li>Planta: (suela) Goma</li><li>Taco: Goma</li><li>Altura del Taco: 4,5 cm</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{35.0,36.0,37.0,38.0,39.0,40.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Gavilan-C13.png', '1_GDF-OI14-Gavilan-C13.png', '2_GDF-OI14-Gavilan-C13.png', 33558, 1, '', 'Calzur Ltda.', 'Gavilan C13', 'cafÃ© beige', '.', 69900, '', '', 1, '3_GDF-OI14-Gavilan-C13.png', '4_GDF-OI14-Gavilan-C13.png', '5_GDF-OI14-Gavilan-C13.png');
INSERT INTO "Product" VALUES (127, 'GDF-OI14-Gavilan-C5', '<ul><li>Color: verde gris&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{37.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Gavilan-C5.png', '1_GDF-OI14-Gavilan-C5.png', '2_GDF-OI14-Gavilan-C5.png', 33558, 1, '', 'Calzur Ltda.', 'Gavilan C5', 'verde gris', '.', 69900, '', '', 1, '3_GDF-OI14-Gavilan-C5.png', '4_GDF-OI14-Gavilan-C5.png', '5_GDF-OI14-Gavilan-C5.png');
INSERT INTO "Product" VALUES (120, 'GDF-OI14-Queltehue-C26', '<ul><li>Color: camel cafÃ©&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{35.0,37.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Queltehue-C26.png', '1_GDF-OI14-Queltehue-C26.png', '2_GDF-OI14-Queltehue-C26.png', 33558, 1, '', 'Calzur Ltda.', 'Queltehue C26', 'camel cafÃ©', '.', 69900, '', '', 1, '3_GDF-OI14-Queltehue-C26.png', '4_GDF-OI14-Queltehue-C26.png', '5_GDF-OI14-Queltehue-C26.png');
INSERT INTO "Product" VALUES (119, 'GDF-OI14-Queltehue-C33', '<ul><li>Color: cafÃ© beige&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{35.0,40.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Queltehue-C33.png', '1_GDF-OI14-Queltehue-C33.png', '2_GDF-OI14-Queltehue-C33.png', 33558, 1, '', 'Calzur Ltda.', 'Queltehue C33', 'cafÃ© beige', '.', 69900, '', '', 1, '3_GDF-OI14-Queltehue-C33.png', '4_GDF-OI14-Queltehue-C33.png', '5_GDF-OI14-Queltehue-C33.png');
INSERT INTO "Product" VALUES (135, 'GDF-PV14-Kereu-C12', '<ul><li>Color: beige&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 6 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{36.0,37.0,40.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Kereu-C12.png', '1_GDF-PV14-Kereu-C12.png', '2_GDF-PV14-Kereu-C12.png', 34391, 1, '', 'Calzur Ltda.', 'Kereu C12', 'beige', '.', 69900, '', '', 1, '3_GDF-PV14-Kereu-C12.png', '4_GDF-PV14-Kereu-C12.png', '5_GDF-PV14-Kereu-C12.png');
INSERT INTO "Product" VALUES (132, 'GDF-PV14-Lile-C10', '<ul><li>Color: camel&nbsp;</li><li>Capellada (material exterior): Reno&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 6 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{35.0,36.0,37.0,39.0,40.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Lile-C10.png', '1_GDF-PV14-Lile-C10.png', '2_GDF-PV14-Lile-C10.png', 34510, 1, '', 'Calzur Ltda.', 'Lile C10', 'camel', '.', 69900, '', '', 1, '3_GDF-PV14-Lile-C10.png', '4_GDF-PV14-Lile-C10.png', '5_GDF-PV14-Lile-C10.png');
INSERT INTO "Product" VALUES (137, 'GDF-PV14-Kereu-C1', '<ul><li>Color: negro&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Madera&nbsp;</li><li>Taco: Madera&nbsp;</li><li>Altura del Taco: 7 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{36.0,40.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Kereu-C1.png', '1_GDF-PV14-Kereu-C1.png', '2_GDF-PV14-Kereu-C1.png', 34391, 1, '', 'Calzur Ltda.', 'Kereu C1', 'negro', '.', 69900, '', '', 1, '3_GDF-PV14-Kereu-C1.png', '4_GDF-PV14-Kereu-C1.png', '5_GDF-PV14-Kereu-C1.png');
INSERT INTO "Product" VALUES (131, 'GDF-PV14-Lile-C1', '<ul><li>Color: Camel&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 6 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{37.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Lile-C1.png', '1_GDF-PV14-Lile-C1.png', '2_GDF-PV14-Lile-C1.png', 34510, 1, '', 'Calzur Ltda.', 'Lile C1', 'camel', '.', 69900, '', '', 1, '3_GDF-PV14-Lile-C1.png', '4_GDF-PV14-Lile-C1.png', '5_GDF-PV14-Lile-C1.png');
INSERT INTO "Product" VALUES (139, 'GDF-PV14-Lile-C13', '<ul><li>Color: beige&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 6 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{35.0,37.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Lile-C13.png', '1_GDF-PV14-Lile-C13.png', '2_GDF-PV14-Lile-C13.png', 34510, 1, '', 'Calzur Ltda.', 'Lile C13', 'Beige', '.', 69900, '', '', 1, '3_GDF-PV14-Lile-C13.png', '4_GDF-PV14-Lile-C13.png', '5_GDF-PV14-Lile-C13.png');
INSERT INTO "Product" VALUES (130, 'GDF-PV14-Lile-C2', '<ul><li>Color: rojo&nbsp;</li><li>Capellada (material exterior): Reno&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Madera&nbsp;</li><li>Taco: Madera&nbsp;</li><li>Altura del Taco: 7 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{37.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Lile-C2.png', '1_GDF-PV14-Lile-C2.png', '2_GDF-PV14-Lile-C2.png', 34510, 1, '', 'Calzur Ltda.', 'Lile C2', 'rojo', '.', 69900, '', '', 1, '3_GDF-PV14-Lile-C2.png', '4_GDF-PV14-Lile-C2.png', '5_GDF-PV14-Lile-C2.png');
INSERT INTO "Product" VALUES (145, 'GDF-PV14-Sirisi-C3', '<ul><li>Color: verde&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{36.0,40.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Sirisi-C3.png', '1_GDF-PV14-Sirisi-C3.png', '2_GDF-PV14-Sirisi-C3.png', 32011, 1, '', 'Calzur Ltda.', 'Sirisi C3', 'verde', '.', 67900, '', '', 1, '3_GDF-PV14-Sirisi-C3.png', '4_GDF-PV14-Sirisi-C3.png', '5_GDF-PV14-Sirisi-C3.png');
INSERT INTO "Product" VALUES (148, 'GDF-PV14-Sirisi-C4', '<ul><li>Color: mostaza&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{36.0,37.0,38.0,39.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Sirisi-C4.png', '1_GDF-PV14-Sirisi-C4.png', '2_GDF-PV14-Sirisi-C4.png', 32011, 1, '', 'Calzur Ltda.', 'Sirisi C4', 'mostaza', '.', 67900, '', '', 1, '3_GDF-PV14-Sirisi-C4.png', '4_GDF-PV14-Sirisi-C4.png', '5_GDF-PV14-Sirisi-C4.png');
INSERT INTO "Product" VALUES (144, 'GDF-PV14-Sirisi-C7', '<ul><li>Color: croco negro gris&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{37.0,38.0,39.0,40.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Sirisi-C7.png', '1_GDF-PV14-Sirisi-C7.png', '2_GDF-PV14-Sirisi-C7.png', 32011, 1, '', 'Calzur Ltda.', 'Sirisi C7', 'croco negro gris', '.', 67900, '', '', 1, '3_GDF-PV14-Sirisi-C7.png', '4_GDF-PV14-Sirisi-C7.png', '5_GDF-PV14-Sirisi-C7.png');
INSERT INTO "Product" VALUES (125, 'GDF-OI14-Gavilan-C6', '<ul><li>Color: cafÃ©&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{37.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Gavilan-C6.png', '1_GDF-OI14-Gavilan-C6.png', '2_GDF-OI14-Gavilan-C6.png', 33558, 1, '', 'Calzur Ltda.', 'Gavilan C6', 'cafÃ©', '.', 69900, '', '', 1, '3_GDF-OI14-Gavilan-C6.png', '4_GDF-OI14-Gavilan-C6.png', '5_GDF-OI14-Gavilan-C6.png');
INSERT INTO "Product" VALUES (142, 'GDF-PV14-Sirisi-C9', '<ul><li>Color: croco beige&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{35.0,36.0,37.0,38.0,39.0,40.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Sirisi-C9.png', '1_GDF-PV14-Sirisi-C9.png', '2_GDF-PV14-Sirisi-C9.png', 32011, 1, '', 'Calzur Ltda.', 'Sirisi C9', 'croco beige', '.', 67900, '', '', 1, '3_GDF-PV14-Sirisi-C9.png', '4_GDF-PV14-Sirisi-C9.png', '5_GDF-PV14-Sirisi-C9.png');
INSERT INTO "Product" VALUES (124, 'GDF-OI14-Gavilan-C12', '<ul><li>Color: verde beige&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{35.0,36.0,37.0,38.0,39.0,40.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Gavilan-C12.png', '1_GDF-OI14-Gavilan-C12.png', '2_GDF-OI14-Gavilan-C12.png', 33558, 1, '', 'Calzur Ltda.', 'Gavilan C12', 'verde beige', '.', 69900, '', '', 1, '3_GDF-OI14-Gavilan-C12.png', '4_GDF-OI14-Gavilan-C12.png', '5_GDF-OI14-Gavilan-C12.png');
INSERT INTO "Product" VALUES (140, 'GDF-OI14-Queltehue-C31', '<ul><li>Color: Camel Rojo&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{35.0,37.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Queltehue-C31.png', '1_GDF-OI14-Queltehue-C31.png', '2_GDF-OI14-Queltehue-C31.png', 33558, 1, '', 'Calzur Ltda.', 'Queltehue C31', 'camel rojo', '.', 69900, '', '', 1, '3_GDF-OI14-Queltehue-C31.png', '4_GDF-OI14-Queltehue-C31.png', '5_GDF-OI14-Queltehue-C31.png');
INSERT INTO "Product" VALUES (138, 'GDF-PV14-Kereu-C3', '<ul><li>Color: cafÃ© negro&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 6 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{35.0,36.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Kereu-C3.png', '1_GDF-PV14-Kereu-C3.png', '2_GDF-PV14-Kereu-C3.png', 34391, 1, '', 'Calzur Ltda.', 'Kereu C3', 'cafÃ© negro', '.', 69900, '', '', 1, '3_GDF-PV14-Kereu-C3.png', '4_GDF-PV14-Kereu-C3.png', '5_GDF-PV14-Kereu-C3.png');
INSERT INTO "Product" VALUES (134, 'GDF-PV14-Kereu-C11', '<ul><li>Color: cafÃ©&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 6 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{38.0,40.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Kereu-C11.png', '1_GDF-PV14-Kereu-C11.png', '2_GDF-PV14-Kereu-C11.png', 34391, 1, '', 'Calzur Ltda.', 'Kereu C11', 'cafÃ©', '.', 69900, '', '', 1, '3_GDF-PV14-Kereu-C11.png', '4_GDF-PV14-Kereu-C11.png', '5_GDF-PV14-Kereu-C11.png');
INSERT INTO "Product" VALUES (133, 'GDF-PV14-Kereu-C6', '<ul><li>Color: azul&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 6 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{36.0,37.0,40.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Kereu-C6.png', '1_GDF-PV14-Kereu-C6.png', '2_GDF-PV14-Kereu-C6.png', 34391, 1, '', 'Calzur Ltda.', 'Kereu C6', 'azul', '.', 69900, '', '', 1, '3_GDF-PV14-Kereu-C6.png', '4_GDF-PV14-Kereu-C6.png', '5_GDF-PV14-Kereu-C6.png');
INSERT INTO "Product" VALUES (147, 'GDF-PV14-Sirisi-C2', '<ul><li>Color: Rosa viejo&nbsp;</li><li>Capellada (material exterior): Reno&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Madera&nbsp;</li><li>Taco: Madera&nbsp;</li><li>Altura del Taco: 7 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{37.0,38.0,39.0,40.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Sirisi-C2.png', '1_GDF-PV14-Sirisi-C2.png', '2_GDF-PV14-Sirisi-C2.png', 32011, 1, '', 'Calzur Ltda.', 'Sirisi C2', 'rosa viejo', '.', 67900, '', '', 1, '3_GDF-PV14-Sirisi-C2.png', '4_GDF-PV14-Sirisi-C2.png', '5_GDF-PV14-Sirisi-C2.png');
INSERT INTO "Product" VALUES (123, 'GDF-OI14-Gavilan-C10', '<ul><li>Color: cafÃ© gris&nbsp;<br></li><li>Capellada (material exterior): Cuero&nbsp;<br></li><li>Forro (material interior): Cuero&nbsp;<br></li><li>Plantilla: Cuero&nbsp;<br></li><li>Planta (suela): Goma&nbsp;<br></li><li>Taco: Goma&nbsp;<br></li><li>Altura del Taco: 4,5 cm&nbsp;<br></li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{37.0,38.0,39.0,40.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Gavilan-C10.png', '1_GDF-OI14-Gavilan-C10.png', '2_GDF-OI14-Gavilan-C10.png', 33558, 1, '', 'Calzur Ltda.', 'Gavilan C10', 'cafÃ© gris', '.', 69900, '', '', 1, '3_GDF-OI14-Gavilan-C10.png', '4_GDF-OI14-Gavilan-C10.png', '5_GDF-OI14-Gavilan-C10.png');
INSERT INTO "Product" VALUES (126, 'GDF-OI14-Gavilan-C2', '<ul><li>Color: negro&nbsp;</li><li>&nbsp;Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 4,5 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{35.0,40.0}', '', '', '', NULL, NULL, '0_GDF-OI14-Gavilan-C2.png', '1_GDF-OI14-Gavilan-C2.png', '2_GDF-OI14-Gavilan-C2.png', 33558, 1, '', 'Calzur Ltda.', 'Gavilan C2', 'negro', '.', 69900, '', '', 1, '3_GDF-OI14-Gavilan-C2.png', '4_GDF-OI14-Gavilan-C2.png', '5_GDF-OI14-Gavilan-C2.png');
INSERT INTO "Product" VALUES (136, 'GDF-PV14-Kereu-C5', '<ul><li>Color: cafÃ© verde&nbsp;</li><li>Capellada (material exterior): Reno&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 6 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{35.0,37.0,38.0,39.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Kereu-C5.png', '1_GDF-PV14-Kereu-C5.png', '2_GDF-PV14-Kereu-C5.png', 34391, 1, '', 'Calzur Ltda.', 'Kereu C5', 'cafÃ© verde', '.', 69900, '', '', 1, '3_GDF-PV14-Kereu-C5.png', '4_GDF-PV14-Kereu-C5.png', '5_GDF-PV14-Kereu-C5.png');
INSERT INTO "Product" VALUES (128, 'GDF-PV14-Lile-C8', '<ul><li>Color: azul&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 6 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{36.0,37.0,38.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Lile-C8.png', '1_GDF-PV14-Lile-C8.png', '2_GDF-PV14-Lile-C8.png', 34510, 1, '', 'Calzur Ltda.', 'Lile C8', 'azul', '.', 69900, '', '', 1, '3_GDF-PV14-Lile-C8.png', '4_GDF-PV14-Lile-C8.png', '5_GDF-PV14-Lile-C8.png');
INSERT INTO "Product" VALUES (129, 'GDF-PV14-Lile-C9', '<ul><li>Color: azul&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Goma&nbsp;</li><li>Taco: Goma&nbsp;</li><li>Altura del Taco: 6 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{36.0,37.0,38.0,39.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Lile-C9.png', '1_GDF-PV14-Lile-C9.png', '2_GDF-PV14-Lile-C9.png', 34510, 1, '', 'Calzur Ltda.', 'Lile C9', 'azul', '.', 69900, '', '', 1, '3_GDF-PV14-Lile-C9.png', '4_GDF-PV14-Lile-C9.png', '5_GDF-PV14-Lile-C9.png');
INSERT INTO "Product" VALUES (143, 'GDF-PV14-Sirisi-C5', '<ul><li>Color: beige&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Madera&nbsp;</li><li>Taco: Madera&nbsp;</li><li>Altura del Taco: 7 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{37.0,38.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Sirisi-C5.png', '1_GDF-PV14-Sirisi-C5.png', '2_GDF-PV14-Sirisi-C5.png', 32011, 1, '', 'Calzur Ltda.', 'Sirisi C5', 'beige', '.', 67900, '', '', 1, '3_GDF-PV14-Sirisi-C5.png', '4_GDF-PV14-Sirisi-C5.png', '5_GDF-PV14-Sirisi-C5.png');
INSERT INTO "Product" VALUES (146, 'GDF-PV14-Sirisi-C1', '<ul><li>Color: musgo&nbsp;</li><li>Capellada (material exterior): Cuero&nbsp;</li><li>Forro (material interior): Cuero&nbsp;</li><li>Plantilla: Cuero&nbsp;</li><li>Planta (suela): Madera&nbsp;</li><li>Taco: Madera&nbsp;</li><li>Altura del Taco: 7 cm&nbsp;</li><li>Estilo: BotÃ­n<br></li></ul>', 'Giani Da Firenze', '{37.0,38.0}', '', '', '', NULL, NULL, '0_GDF-PV14-Sirisi-C1.png', '1_GDF-PV14-Sirisi-C1.png', '2_GDF-PV14-Sirisi-C1.png', 32011, 1, '', 'Calzur Ltda.', 'Sirisi C1', 'musgo', '.', 67900, '', '', 1, '3_GDF-PV14-Sirisi-C1.png', '4_GDF-PV14-Sirisi-C1.png', '5_GDF-PV14-Sirisi-C1.png');


--
-- Name: Product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Product_id_seq"', 148, true);


--
-- Data for Name: Shipping; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Shipping" VALUES (11, 5, 25, 0, 6690, 6690, false, 1);
INSERT INTO "Shipping" VALUES (12, 5, 26, 0, 4010, 4010, false, 1);
INSERT INTO "Shipping" VALUES (9, 5, 28, 0, 4480, 4480, true, 1);
INSERT INTO "Shipping" VALUES (10, 5, 27, 0, 7420, 7420, true, 1);
INSERT INTO "Shipping" VALUES (13, 5, 29, 0, 3890, 3890, false, 1);
INSERT INTO "Shipping" VALUES (14, 5, 12, 0, 3890, 3890, false, 1);
INSERT INTO "Shipping" VALUES (15, 5, 14, 0, 3890, 3890, false, 1);
INSERT INTO "Shipping" VALUES (16, 5, 30, 0, 3890, 3890, false, 1);
INSERT INTO "Shipping" VALUES (17, 5, 31, 0, 3720, 3720, false, 1);
INSERT INTO "Shipping" VALUES (18, 5, 33, 0, 3720, 3720, false, 1);
INSERT INTO "Shipping" VALUES (19, 5, 32, 0, 3720, 3720, true, 1);
INSERT INTO "Shipping" VALUES (21, 5, 13, 0, 3780, 3780, false, 1);
INSERT INTO "Shipping" VALUES (22, 5, 34, 0, 3780, 3780, false, 1);
INSERT INTO "Shipping" VALUES (23, 5, 21, 0, 3780, 3780, false, 1);
INSERT INTO "Shipping" VALUES (24, 5, 6, 0, 3780, 3780, false, 1);
INSERT INTO "Shipping" VALUES (25, 5, 20, 0, 3780, 3780, false, 1);
INSERT INTO "Shipping" VALUES (26, 5, 9, 0, 3780, 3780, false, 1);
INSERT INTO "Shipping" VALUES (27, 5, 35, 0, 3780, 3780, false, 1);
INSERT INTO "Shipping" VALUES (28, 5, 10, 0, 3900, 3900, false, 1);
INSERT INTO "Shipping" VALUES (29, 5, 4, 0, 3900, 3900, false, 1);
INSERT INTO "Shipping" VALUES (30, 5, 36, 0, 3900, 3900, true, 1);
INSERT INTO "Shipping" VALUES (32, 5, 37, 0, 4250, 4250, false, 1);
INSERT INTO "Shipping" VALUES (33, 5, 38, 0, 7130, 7130, false, 1);
INSERT INTO "Shipping" VALUES (34, 5, 11, 0, 7130, 7130, false, 1);
INSERT INTO "Shipping" VALUES (20, 5, 3, 0, 2450, 0, true, 1);


--
-- Data for Name: Shipping_Provider; Type: TABLE DATA; Schema: public; Owner: yichun
--



--
-- Name: Shipping_Provider_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Shipping_Provider_id_seq"', 1, false);


--
-- Name: Shipping_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Shipping_id_seq"', 34, true);


--
-- Data for Name: State; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "State" VALUES (2, 'Pagada');
INSERT INTO "State" VALUES (3, 'Despachada');
INSERT INTO "State" VALUES (4, 'Recibida');
INSERT INTO "State" VALUES (5, 'Completada');
INSERT INTO "State" VALUES (1, 'Pendiente');


--
-- Name: State_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"State_id_seq"', 5, true);


--
-- Data for Name: Tag; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Tag" VALUES (2, 'botines', 1);
INSERT INTO "Tag" VALUES (8, 'Autoctono', 0);
INSERT INTO "Tag" VALUES (14, 'Categoria nueva', 0);
INSERT INTO "Tag" VALUES (1, 'lo nuevo', 1);
INSERT INTO "Tag" VALUES (56, 'Gavilan', 1);
INSERT INTO "Tag" VALUES (58, 'Kereu', 1);
INSERT INTO "Tag" VALUES (60, 'Sirisi', 1);
INSERT INTO "Tag" VALUES (59, 'Lile', 1);
INSERT INTO "Tag" VALUES (57, 'Queltehue', 1);
INSERT INTO "Tag" VALUES (7, 'zapatos', 0);


--
-- Data for Name: Tag_Product; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Tag_Product" VALUES (540, 15, 8);
INSERT INTO "Tag_Product" VALUES (541, 9, 8);
INSERT INTO "Tag_Product" VALUES (542, 6, 8);
INSERT INTO "Tag_Product" VALUES (543, 7, 8);
INSERT INTO "Tag_Product" VALUES (544, 28, 8);
INSERT INTO "Tag_Product" VALUES (545, 29, 8);
INSERT INTO "Tag_Product" VALUES (546, 19, 8);
INSERT INTO "Tag_Product" VALUES (547, 17, 8);
INSERT INTO "Tag_Product" VALUES (548, 18, 8);
INSERT INTO "Tag_Product" VALUES (434, 15, 7);
INSERT INTO "Tag_Product" VALUES (549, 12, 8);
INSERT INTO "Tag_Product" VALUES (436, 7, 7);
INSERT INTO "Tag_Product" VALUES (437, 29, 7);
INSERT INTO "Tag_Product" VALUES (438, 19, 7);
INSERT INTO "Tag_Product" VALUES (439, 8, 7);
INSERT INTO "Tag_Product" VALUES (440, 13, 7);
INSERT INTO "Tag_Product" VALUES (550, 16, 8);
INSERT INTO "Tag_Product" VALUES (551, 30, 8);
INSERT INTO "Tag_Product" VALUES (641, 123, 2);
INSERT INTO "Tag_Product" VALUES (642, 122, 2);
INSERT INTO "Tag_Product" VALUES (643, 124, 2);
INSERT INTO "Tag_Product" VALUES (644, 121, 2);
INSERT INTO "Tag_Product" VALUES (645, 126, 2);
INSERT INTO "Tag_Product" VALUES (558, 34, 7);
INSERT INTO "Tag_Product" VALUES (559, 35, 7);
INSERT INTO "Tag_Product" VALUES (646, 127, 2);
INSERT INTO "Tag_Product" VALUES (647, 125, 2);
INSERT INTO "Tag_Product" VALUES (648, 116, 2);
INSERT INTO "Tag_Product" VALUES (649, 114, 2);
INSERT INTO "Tag_Product" VALUES (561, 38, 7);
INSERT INTO "Tag_Product" VALUES (650, 120, 2);
INSERT INTO "Tag_Product" VALUES (651, 118, 2);
INSERT INTO "Tag_Product" VALUES (652, 140, 2);
INSERT INTO "Tag_Product" VALUES (653, 119, 2);
INSERT INTO "Tag_Product" VALUES (654, 113, 2);
INSERT INTO "Tag_Product" VALUES (655, 115, 2);
INSERT INTO "Tag_Product" VALUES (656, 117, 2);
INSERT INTO "Tag_Product" VALUES (657, 137, 2);
INSERT INTO "Tag_Product" VALUES (658, 134, 2);
INSERT INTO "Tag_Product" VALUES (659, 135, 2);
INSERT INTO "Tag_Product" VALUES (660, 138, 2);
INSERT INTO "Tag_Product" VALUES (661, 136, 2);
INSERT INTO "Tag_Product" VALUES (662, 133, 2);
INSERT INTO "Tag_Product" VALUES (663, 131, 2);
INSERT INTO "Tag_Product" VALUES (664, 132, 2);
INSERT INTO "Tag_Product" VALUES (665, 139, 2);
INSERT INTO "Tag_Product" VALUES (666, 130, 2);
INSERT INTO "Tag_Product" VALUES (667, 128, 2);
INSERT INTO "Tag_Product" VALUES (668, 129, 2);
INSERT INTO "Tag_Product" VALUES (669, 146, 2);
INSERT INTO "Tag_Product" VALUES (670, 147, 2);
INSERT INTO "Tag_Product" VALUES (671, 145, 2);
INSERT INTO "Tag_Product" VALUES (672, 148, 2);
INSERT INTO "Tag_Product" VALUES (673, 143, 2);
INSERT INTO "Tag_Product" VALUES (674, 144, 2);
INSERT INTO "Tag_Product" VALUES (675, 141, 2);
INSERT INTO "Tag_Product" VALUES (676, 142, 2);
INSERT INTO "Tag_Product" VALUES (677, 123, 56);
INSERT INTO "Tag_Product" VALUES (678, 122, 56);
INSERT INTO "Tag_Product" VALUES (679, 124, 56);
INSERT INTO "Tag_Product" VALUES (680, 121, 56);
INSERT INTO "Tag_Product" VALUES (681, 126, 56);
INSERT INTO "Tag_Product" VALUES (682, 127, 56);
INSERT INTO "Tag_Product" VALUES (683, 125, 56);
INSERT INTO "Tag_Product" VALUES (684, 116, 57);
INSERT INTO "Tag_Product" VALUES (685, 114, 57);
INSERT INTO "Tag_Product" VALUES (686, 120, 57);
INSERT INTO "Tag_Product" VALUES (687, 118, 57);
INSERT INTO "Tag_Product" VALUES (688, 140, 57);
INSERT INTO "Tag_Product" VALUES (493, 33, 7);
INSERT INTO "Tag_Product" VALUES (689, 119, 57);
INSERT INTO "Tag_Product" VALUES (690, 113, 57);
INSERT INTO "Tag_Product" VALUES (498, 6, 7);
INSERT INTO "Tag_Product" VALUES (691, 115, 57);
INSERT INTO "Tag_Product" VALUES (692, 117, 57);
INSERT INTO "Tag_Product" VALUES (693, 137, 58);
INSERT INTO "Tag_Product" VALUES (694, 134, 58);
INSERT INTO "Tag_Product" VALUES (517, 11, 7);
INSERT INTO "Tag_Product" VALUES (695, 135, 58);
INSERT INTO "Tag_Product" VALUES (696, 138, 58);
INSERT INTO "Tag_Product" VALUES (697, 136, 58);
INSERT INTO "Tag_Product" VALUES (698, 133, 58);
INSERT INTO "Tag_Product" VALUES (699, 131, 59);
INSERT INTO "Tag_Product" VALUES (700, 132, 59);
INSERT INTO "Tag_Product" VALUES (701, 139, 59);
INSERT INTO "Tag_Product" VALUES (702, 130, 59);
INSERT INTO "Tag_Product" VALUES (703, 128, 59);
INSERT INTO "Tag_Product" VALUES (704, 129, 59);
INSERT INTO "Tag_Product" VALUES (705, 146, 60);
INSERT INTO "Tag_Product" VALUES (706, 147, 60);
INSERT INTO "Tag_Product" VALUES (707, 145, 60);
INSERT INTO "Tag_Product" VALUES (708, 148, 60);
INSERT INTO "Tag_Product" VALUES (709, 143, 60);
INSERT INTO "Tag_Product" VALUES (710, 144, 60);
INSERT INTO "Tag_Product" VALUES (711, 141, 60);
INSERT INTO "Tag_Product" VALUES (712, 142, 60);
INSERT INTO "Tag_Product" VALUES (713, 122, 1);
INSERT INTO "Tag_Product" VALUES (714, 125, 1);
INSERT INTO "Tag_Product" VALUES (715, 116, 1);
INSERT INTO "Tag_Product" VALUES (716, 114, 1);
INSERT INTO "Tag_Product" VALUES (717, 118, 1);
INSERT INTO "Tag_Product" VALUES (718, 140, 1);
INSERT INTO "Tag_Product" VALUES (719, 115, 1);
INSERT INTO "Tag_Product" VALUES (720, 117, 1);
INSERT INTO "Tag_Product" VALUES (721, 137, 1);
INSERT INTO "Tag_Product" VALUES (722, 134, 1);
INSERT INTO "Tag_Product" VALUES (723, 138, 1);
INSERT INTO "Tag_Product" VALUES (724, 148, 1);


--
-- Name: Tag_Product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Tag_Product_id_seq"', 724, true);


--
-- Name: Tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Tag_id_seq"', 60, true);


--
-- Name: Tag_name_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Tag_name_seq"', 1, false);


--
-- Data for Name: Temp_Cart; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Temp_Cart" VALUES (423, 113, '2015-02-02 21:15:02.805997', 1, 69900, 696, '35.0', NULL, NULL, NULL, 1, 0);
INSERT INTO "Temp_Cart" VALUES (448, 117, '2015-02-05 21:48:01.272925', 1, 1, 16, '37.0', NULL, NULL, NULL, 1, 0);
INSERT INTO "Temp_Cart" VALUES (452, 116, '2015-02-06 15:50:15.419248', 2, 139800, 22, '35.0', 52, 52, 2, 1, 0);
INSERT INTO "Temp_Cart" VALUES (400, 117, '2015-01-30 22:09:31.10427', 1, 69900, 656, '37.0', NULL, NULL, NULL, 1, 0);
INSERT INTO "Temp_Cart" VALUES (432, 117, '2015-02-04 18:44:57.990051', 1, 1, 695, '37.0', NULL, NULL, NULL, 1, 0);
INSERT INTO "Temp_Cart" VALUES (444, 116, '2015-02-05 03:23:09.096344', 1, 69900, 752, '35.0', NULL, NULL, NULL, 1, 0);
INSERT INTO "Temp_Cart" VALUES (445, 117, '2015-02-05 03:23:36.498089', 2, 2, 752, '37.0', NULL, NULL, NULL, 1, 0);
INSERT INTO "Temp_Cart" VALUES (411, 114, '2015-01-31 01:34:58.532858', 1, 69900, 671, '35.0', NULL, NULL, NULL, 1, 0);
INSERT INTO "Temp_Cart" VALUES (446, 122, '2015-02-05 03:24:06.322866', 1, 69900, 752, '39.0', NULL, NULL, NULL, 1, 0);
INSERT INTO "Temp_Cart" VALUES (412, 116, '2015-01-31 01:37:23.932123', 2, 139800, 671, '35.0', NULL, NULL, NULL, 1, 0);
INSERT INTO "Temp_Cart" VALUES (406, 117, '2015-01-31 00:35:53.423264', 6, 419400, 671, '37.0', NULL, NULL, NULL, 1, 0);
INSERT INTO "Temp_Cart" VALUES (415, 118, '2015-01-31 13:48:42.004064', 1, 69900, 682, '35.0', NULL, NULL, NULL, 1, 0);
INSERT INTO "Temp_Cart" VALUES (417, 116, '2015-02-02 20:23:34.586908', 1, 69900, 688, '35.0', NULL, NULL, NULL, 1, 0);
INSERT INTO "Temp_Cart" VALUES (421, 116, '2015-02-02 21:07:59.12567', 1, 69900, 694, '35.0', NULL, NULL, NULL, 1, 0);
INSERT INTO "Temp_Cart" VALUES (422, 116, '2015-02-02 21:14:45.467483', 1, 69900, 696, '35.0', NULL, NULL, NULL, 1, 0);


--
-- Name: Temp_Cart_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Temp_Cart_id_seq"', 463, true);


--
-- Data for Name: User; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "User" VALUES (735, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-04 16:33:43.719657', 1, '2015-02-04 16:33:43.719657', '2015-02-04 16:33:43.719657', 0);
INSERT INTO "User" VALUES (632, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-11 15:00:35.416644', 1, '2015-01-11 15:00:35.416644', '2015-01-11 15:00:35.416644', 0);
INSERT INTO "User" VALUES (633, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-18 00:17:00.787541', 1, '2015-01-18 00:17:00.787541', '2015-01-18 00:17:00.787541', 0);
INSERT INTO "User" VALUES (690, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-02-02 19:16:37.747458', 1, '2015-02-02 19:16:37.747458', '2015-02-02 19:16:37.747458', 0);
INSERT INTO "User" VALUES (742, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-04 20:35:56.693903', 1, '2015-02-04 20:35:56.693903', '2015-02-04 20:35:56.693903', 0);
INSERT INTO "User" VALUES (647, '{}', 3, 'jjj', 'jjj@jjj.cl', 'j', '{}', '', '', '', NULL, '2015-01-29 22:37:45.127367', 1, '2015-01-29 22:37:45.127367', '2015-01-29 22:37:45.127367', 0);
INSERT INTO "User" VALUES (698, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-02-02 23:03:47.030236', 1, '2015-02-02 23:03:47.030236', '2015-02-02 23:03:47.030236', 0);
INSERT INTO "User" VALUES (780, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-19 16:56:41.681998', 1, '2015-02-19 16:56:41.681998', '2015-02-19 16:56:41.681998', 0);
INSERT INTO "User" VALUES (712, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-04 14:23:51.227575', 1, '2015-02-04 14:23:51.227575', '2015-02-04 14:23:51.227575', 0);
INSERT INTO "User" VALUES (482, '{}', 3, 'julian', 'julian@gianidafirenze.cl', 'juliano9', '{}', '', '', '', NULL, '2014-10-21 21:15:54.506648', 1, '2014-10-21 21:15:54.506648', '2014-10-21 21:15:54.506648', 0);
INSERT INTO "User" VALUES (671, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-31 00:25:46.542471', 1, '2015-01-31 00:25:46.542471', '2015-01-31 00:25:46.542471', 0);
INSERT INTO "User" VALUES (634, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-19 19:49:27.600905', 1, '2015-01-19 19:49:27.600905', '2015-01-19 19:49:27.600905', 0);
INSERT INTO "User" VALUES (641, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-29 02:21:04.370691', 1, '2015-01-29 02:21:04.370691', '2015-01-29 02:21:04.370691', 0);
INSERT INTO "User" VALUES (684, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-02-01 14:36:36.151636', 1, '2015-02-01 14:36:36.151636', '2015-02-01 14:36:36.151636', 0);
INSERT INTO "User" VALUES (648, '{}', 3, 'aa', 'aa@aac.cl', 'aa', '{}', '', '', '', NULL, '2015-01-29 22:38:17.003275', 1, '2015-01-29 22:38:17.003275', '2015-01-29 22:38:17.003275', 0);
INSERT INTO "User" VALUES (655, '{}', 3, 'm', 'm@m.cl', '1234', '{}', '', '', '', NULL, '2015-01-29 22:54:30.629855', 1, '2015-01-29 22:54:30.629855', '2015-01-29 22:54:30.629855', 0);
INSERT INTO "User" VALUES (699, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-02-02 23:32:30.91811', 1, '2015-02-02 23:32:30.91811', '2015-02-02 23:32:30.91811', 0);
INSERT INTO "User" VALUES (750, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-05 00:04:09.884078', 1, '2015-02-05 00:04:09.884078', '2015-02-05 00:04:09.884078', 0);
INSERT INTO "User" VALUES (757, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-05 19:12:39.23515', 1, '2015-02-05 19:12:39.23515', '2015-02-05 19:12:39.23515', 0);
INSERT INTO "User" VALUES (769, '{}', 3, 'Chien-Hung Lin', 'chienhung.lin@usach.cl', '90a8db953336c8dabbcf48b1592a8c06', '{}', '', '', '', NULL, '2015-02-09 15:36:11.481926', 1, '2015-02-09 15:36:11.481926', '2015-02-09 15:36:11.481926', 0);
INSERT INTO "User" VALUES (781, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-19 16:57:56.671014', 1, '2015-02-19 16:57:56.671014', '2015-02-19 16:57:56.671014', 0);
INSERT INTO "User" VALUES (667, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-30 20:17:15.021588', 1, '2015-01-30 20:17:15.021588', '2015-01-30 20:17:15.021588', 0);
INSERT INTO "User" VALUES (8, '{1,2,3,4,5,6}', 1, 'Ricardo', 'ricardo@loadingplay.com', 'escuela16761', '{5}', 'silva', '', '', '2014-09-21 00:00:00', '2014-09-16 14:58:36.87965', 1, '2014-09-16 14:59:30.2947', '2014-09-16 14:59:46.468531', 0);
INSERT INTO "User" VALUES (635, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-20 21:31:34.442978', 1, '2015-01-20 21:31:34.442978', '2015-01-20 21:31:34.442978', 0);
INSERT INTO "User" VALUES (679, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-31 01:59:42.426236', 1, '2015-01-31 01:59:42.426236', '2015-01-31 01:59:42.426236', 0);
INSERT INTO "User" VALUES (685, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-02-01 15:55:17.371044', 1, '2015-02-01 15:55:17.371044', '2015-02-01 15:55:17.371044', 0);
INSERT INTO "User" VALUES (642, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-29 22:16:46.529291', 1, '2015-01-29 22:16:46.529291', '2015-01-29 22:16:46.529291', 0);
INSERT INTO "User" VALUES (737, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-04 16:40:02.159489', 1, '2015-02-04 16:40:02.159489', '2015-02-04 16:40:02.159489', 0);
INSERT INTO "User" VALUES (656, '{}', 3, 'luisa', 'luisa@gmail.com', 'kika', '{}', '', '', '', NULL, '2015-01-29 22:54:58.042848', 1, '2015-01-29 22:54:58.042848', '2015-01-29 22:54:58.042848', 0);
INSERT INTO "User" VALUES (744, '{}', 3, 'oscarito', 'master_egg@hotmail.com', '942d37c245cc6de02d159b3fa2986990', '{}', '', '', '', NULL, '2015-02-04 20:53:38.139672', 1, '2015-02-04 20:53:38.139672', '2015-02-04 20:53:38.139672', 0);
INSERT INTO "User" VALUES (773, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-16 01:00:11.617801', 1, '2015-02-16 01:00:11.617801', '2015-02-16 01:00:11.617801', 0);
INSERT INTO "User" VALUES (782, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-19 17:03:03.154813', 1, '2015-02-19 17:03:03.154813', '2015-02-19 17:03:03.154813', 0);
INSERT INTO "User" VALUES (592, '{}', 3, 'CERTIFICACION', 'certificacion2@transbank.cl', '123456', '{}', '', '', '', NULL, '2014-12-05 20:16:08.91959', 1, '2014-12-05 20:16:08.91959', '2014-12-05 20:16:08.91959', 0);
INSERT INTO "User" VALUES (621, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-04 04:33:39.318339', 1, '2015-01-04 04:33:39.318339', '2015-01-04 04:33:39.318339', 0);
INSERT INTO "User" VALUES (643, '{}', 3, 'yichun', 'yi@sa.cl', '1234', '{}', '', '', '', NULL, '2015-01-29 22:25:02.020935', 1, '2015-01-29 22:25:02.020935', '2015-01-29 22:25:02.020935', 0);
INSERT INTO "User" VALUES (745, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-04 23:12:07.796096', 1, '2015-02-04 23:12:07.796096', '2015-02-04 23:12:07.796096', 0);
INSERT INTO "User" VALUES (694, '{}', 3, 'Rumy', 'aa@cl.cl', 'escuela', '{}', '', '', '', NULL, '2015-02-02 21:07:35.123216', 1, '2015-02-02 21:07:35.123216', '2015-02-02 21:07:35.123216', 0);
INSERT INTO "User" VALUES (752, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-05 03:22:54.4468', 1, '2015-02-05 03:22:54.4468', '2015-02-05 03:22:54.4468', 0);
INSERT INTO "User" VALUES (708, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-02-04 13:00:49.560349', 1, '2015-02-04 13:00:49.560349', '2015-02-04 13:00:49.560349', 0);
INSERT INTO "User" VALUES (715, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-04 14:55:41.750423', 1, '2015-02-04 14:55:41.750423', '2015-02-04 14:55:41.750423', 0);
INSERT INTO "User" VALUES (759, '{}', 3, 'cxzczx', 'cxzcxz@gmail.com', '35188f6c9a2638ec9685082515fd0581', '{}', '', '', '', NULL, '2015-02-05 20:04:35.16932', 1, '2015-02-05 20:04:35.16932', '2015-02-05 20:04:35.16932', 0);
INSERT INTO "User" VALUES (776, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-17 20:18:36.731537', 1, '2015-02-17 20:18:36.731537', '2015-02-17 20:18:36.731537', 0);
INSERT INTO "User" VALUES (15, '{}', 3, 'maria', 'maomao@gl.cl', '1234', '{5}', 'Larrea', '', 'Imprenta', NULL, '2014-09-16 14:58:36.87965', 1, '2014-09-16 14:59:30.2947', '2014-09-16 14:59:46.468531', 0);
INSERT INTO "User" VALUES (644, '{}', 3, 'user', 'user@user.com', '1234', '{}', '', '', '', NULL, '2015-01-29 22:29:40.818581', 1, '2015-01-29 22:29:40.818581', '2015-01-29 22:29:40.818581', 0);
INSERT INTO "User" VALUES (658, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-30 14:53:06.914677', 1, '2015-01-30 14:53:06.914677', '2015-01-30 14:53:06.914677', 0);
INSERT INTO "User" VALUES (674, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-31 00:54:07.822459', 1, '2015-01-31 00:54:07.822459', '2015-01-31 00:54:07.822459', 0);
INSERT INTO "User" VALUES (681, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-31 02:36:39.124585', 1, '2015-01-31 02:36:39.124585', '2015-01-31 02:36:39.124585', 0);
INSERT INTO "User" VALUES (687, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-02-02 16:06:05.377887', 1, '2015-02-02 16:06:05.377887', '2015-02-02 16:06:05.377887', 0);
INSERT INTO "User" VALUES (695, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-02-02 21:08:56.624748', 1, '2015-02-02 21:08:56.624748', '2015-02-02 21:08:56.624748', 0);
INSERT INTO "User" VALUES (573, '{}', 3, 'SOPORTE WP', 'SOPORTE11@TRANSBANK.CL', '123456', '{}', '', '', '', NULL, '2014-11-29 02:12:28.175539', 1, '2014-11-29 02:12:28.175539', '2014-11-29 02:12:28.175539', 0);
INSERT INTO "User" VALUES (27, '{}', 3, 'Julian Larrea', 'julian@larrea.cl', '', '{}', '', '', '', NULL, '2014-09-16 14:58:36.87965', 1, '2014-09-16 14:59:30.2947', '2014-09-16 14:59:46.468531', 0);
INSERT INTO "User" VALUES (39, '{}', 3, 'Ricardo Silva', 'ricardo.silva.16761@gmail.com', 'escuela', '{}', '', '', '', NULL, '2014-09-16 16:20:38.450674', 1, '2014-09-16 16:20:38.450674', '2014-09-16 16:20:38.450674', 0);
INSERT INTO "User" VALUES (22, '{}', 3, 'Philippe Snow', 'jarenasmuller@gmail.com', '01750bc4d244cb69bfbfbed7498986c1', '{}', '', '', '', NULL, '2014-09-16 14:58:36.87965', 1, '2014-09-16 14:59:30.2947', '2014-09-16 14:59:46.468531', 0);
INSERT INTO "User" VALUES (403, '{}', 3, 'Rumy', 'rumy@test.com', '123456', '{}', '', '', '', NULL, '2014-09-25 16:47:39.889639', 1, '2014-09-25 16:47:39.889639', '2014-09-25 16:47:39.889639', 0);
INSERT INTO "User" VALUES (16, '{}', 3, 'Ricardo Silva', 'elp3rr0@hotmail.com', '', '{}', '', '', '', NULL, '2014-09-16 14:58:36.87965', 1, '2014-09-16 14:59:30.2947', '2014-09-16 14:59:46.468531', 0);
INSERT INTO "User" VALUES (473, '{}', 3, 'julian', 'nailuj41@gmail.com', 'juliano9', '{}', '', '', '', NULL, '2014-10-20 16:58:18.731775', 1, '2014-10-20 16:58:18.731775', '2014-10-20 16:58:18.731775', 0);
INSERT INTO "User" VALUES (746, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-04 23:14:44.983368', 1, '2015-02-04 23:14:44.983368', '2015-02-04 23:14:44.983368', 0);
INSERT INTO "User" VALUES (507, '{}', 3, 'PruebaTBK', 'aa@aa.com', '123456', '{}', '', '', '', NULL, '2014-10-25 23:07:54.297767', 1, '2014-10-25 23:07:54.297767', '2014-10-25 23:07:54.297767', 0);
INSERT INTO "User" VALUES (622, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-05 08:25:22.138865', 1, '2015-01-05 08:25:22.138865', '2015-01-05 08:25:22.138865', 0);
INSERT INTO "User" VALUES (629, '{2,3,6}', 1, 'Javiera', 'javiera@gianidafirenze.cl', '2327', '{5}', 'Soto Gonzales', '', '', NULL, '2015-01-07 13:41:59.018865', 1, '2015-01-07 13:41:59.018865', '2015-01-07 13:41:59.018865', 0);
INSERT INTO "User" VALUES (760, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-06 18:30:40.842224', 1, '2015-02-06 18:30:40.842224', '2015-02-06 18:30:40.842224', 0);
INSERT INTO "User" VALUES (777, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-17 20:18:46.014057', 1, '2015-02-17 20:18:46.014057', '2015-02-17 20:18:46.014057', 0);
INSERT INTO "User" VALUES (675, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-31 01:26:51.733642', 1, '2015-01-31 01:26:51.733642', '2015-01-31 01:26:51.733642', 0);
INSERT INTO "User" VALUES (682, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-31 13:46:40.459838', 1, '2015-01-31 13:46:40.459838', '2015-01-31 13:46:40.459838', 0);
INSERT INTO "User" VALUES (432, '{}', 3, 'Ricardo Silva', 'contact@loadingplay.com', 'escuela16761', '{}', '', '', '', NULL, '2014-09-30 21:02:37.023855', 1, '2014-09-30 21:02:37.023855', '2014-09-30 21:02:37.023855', 0);
INSERT INTO "User" VALUES (450, '{}', 3, 'soporte tbk', 'soporte9@tbk.cl', '12345', '{}', '', '', '', NULL, '2014-10-15 17:12:31.674706', 1, '2014-10-15 17:12:31.674706', '2014-10-15 17:12:31.674706', 0);
INSERT INTO "User" VALUES (462, '{}', 3, 'TRANSBANK', 'soporte8@transbank.cl', '123456', '{}', '', '', '', NULL, '2014-10-19 02:17:37.519394', 1, '2014-10-19 02:17:37.519394', '2014-10-19 02:17:37.519394', 0);
INSERT INTO "User" VALUES (688, '{}', 3, 'Wan Yu', 'wanxulina@gmail.com', '141192', '{}', '', '', '', NULL, '2015-02-02 16:18:12.153975', 1, '2015-02-02 16:18:12.153975', '2015-02-02 16:18:12.153975', 0);
INSERT INTO "User" VALUES (696, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-02-02 21:12:53.405441', 1, '2015-02-02 21:12:53.405441', '2015-02-02 21:12:53.405441', 0);
INSERT INTO "User" VALUES (630, '{1,2,3,6}', 1, 'Giani', 'giani@gianidafirenze.cl', '6982', '{5}', 'Rodriguez Grunert', '', '', NULL, '2015-01-07 14:03:57.730608', 1, '2015-01-07 14:03:57.730608', '2015-01-07 14:03:57.730608', 0);
INSERT INTO "User" VALUES (638, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-23 18:01:45.097298', 1, '2015-01-23 18:01:45.097298', '2015-01-23 18:01:45.097298', 0);
INSERT INTO "User" VALUES (645, '{}', 3, 'qwer', 'qwer@akdhajshd.com', '1234', '{}', '', '', '', NULL, '2015-01-29 22:31:15.714694', 1, '2015-01-29 22:31:15.714694', '2015-01-29 22:31:15.714694', 0);
INSERT INTO "User" VALUES (652, '{}', 3, 'q', 'q@q.cl', 'q', '{}', '', '', '', NULL, '2015-01-29 22:50:55.621207', 1, '2015-01-29 22:50:55.621207', '2015-01-29 22:50:55.621207', 0);
INSERT INTO "User" VALUES (710, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-04 14:16:37.619744', 1, '2015-02-04 14:16:37.619744', '2015-02-04 14:16:37.619744', 0);
INSERT INTO "User" VALUES (733, '{}', 3, 'Yi Chun Lin', 'yichun212@gmail.com', '7423be50e9bd33a1edba6be478f3efc7', '{}', '', '', '', NULL, '2015-02-04 16:33:07.141029', 1, '2015-02-04 16:33:07.141029', '2015-02-04 16:33:07.141029', 0);
INSERT INTO "User" VALUES (761, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-06 18:32:38.514672', 1, '2015-02-06 18:32:38.514672', '2015-02-06 18:32:38.514672', 0);
INSERT INTO "User" VALUES (768, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-09 01:26:50.096219', 1, '2015-02-09 01:26:50.096219', '2015-02-09 01:26:50.096219', 0);
INSERT INTO "User" VALUES (676, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-31 01:36:41.935487', 1, '2015-01-31 01:36:41.935487', '2015-01-31 01:36:41.935487', 0);
INSERT INTO "User" VALUES (689, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-02-02 17:44:38.412614', 1, '2015-02-02 17:44:38.412614', '2015-02-02 17:44:38.412614', 0);
INSERT INTO "User" VALUES (697, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-02-02 22:33:24.690065', 1, '2015-02-02 22:33:24.690065', '2015-02-02 22:33:24.690065', 0);
INSERT INTO "User" VALUES (250, '{1,2,3,4,5,6}', 1, 'Miguel Angel', 'masg@gianidafirenze.cl', '2327', '{5}', 'Soto', '', '', NULL, '2014-09-22 03:21:21.901746', 1, '2014-09-22 03:21:21.901746', '2014-09-22 03:21:21.901746', 0);
INSERT INTO "User" VALUES (704, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-03 22:20:09.928305', 1, '2015-02-03 22:20:09.928305', '2015-02-03 22:20:09.928305', 0);
INSERT INTO "User" VALUES (631, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-07 17:25:36.717328', 1, '2015-01-07 17:25:36.717328', '2015-01-07 17:25:36.717328', 0);
INSERT INTO "User" VALUES (639, '{}', 5, '', '', '', '{}', '', '', '', NULL, '2015-01-23 23:27:26.780254', 1, '2015-01-23 23:27:26.780254', '2015-01-23 23:27:26.780254', 0);
INSERT INTO "User" VALUES (646, '{}', 3, 'asAS', 'asd@lp.cl', '123', '{}', '', '', '', NULL, '2015-01-29 22:34:27.070167', 1, '2015-01-29 22:34:27.070167', '2015-01-29 22:34:27.070167', 0);
INSERT INTO "User" VALUES (734, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-04 16:33:36.935674', 1, '2015-02-04 16:33:36.935674', '2015-02-04 16:33:36.935674', 0);
INSERT INTO "User" VALUES (779, '{}', 5, '', '', 'd41d8cd98f00b204e9800998ecf8427e', '{}', '', '', '', NULL, '2015-02-19 16:23:56.148318', 1, '2015-02-19 16:23:56.148318', '2015-02-19 16:23:56.148318', 0);
INSERT INTO "User" VALUES (741, '{1,2,3,4,5,6}', 3, 'test', 'yi.neko@gmail.com', '0f193d2f1d94ef6fde97072eff98a6b7', '{5,12}', '', '', '', NULL, '2015-02-04 20:34:48.478421', 1, '2015-02-04 20:34:48.478421', '2015-02-04 20:34:48.478421', 0);


--
-- Data for Name: User_Types; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "User_Types" VALUES (1, 'Vendedor');
INSERT INTO "User_Types" VALUES (2, 'Administrador');
INSERT INTO "User_Types" VALUES (3, 'Cliente');
INSERT INTO "User_Types" VALUES (4, 'Cliente Mayorista');
INSERT INTO "User_Types" VALUES (5, 'Visita');


--
-- Name: User_Types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"User_Types_id_seq"', 4, true);


--
-- Name: User_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"User_id_seq"', 791, true);


--
-- Data for Name: Voto; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Voto" VALUES (1, 6, 1);
INSERT INTO "Voto" VALUES (2, 13, 1);
INSERT INTO "Voto" VALUES (3, 1, 13);
INSERT INTO "Voto" VALUES (4, 253, 6);
INSERT INTO "Voto" VALUES (5, 282, 6);
INSERT INTO "Voto" VALUES (6, 312, 6);
INSERT INTO "Voto" VALUES (7, 22, 22);
INSERT INTO "Voto" VALUES (8, 412, 20);
INSERT INTO "Voto" VALUES (9, 422, 11);
INSERT INTO "Voto" VALUES (10, 22, 6);
INSERT INTO "Voto" VALUES (11, 16, 24);
INSERT INTO "Voto" VALUES (12, 436, 10);
INSERT INTO "Voto" VALUES (13, 16, 11);
INSERT INTO "Voto" VALUES (14, 16, 16);
INSERT INTO "Voto" VALUES (15, 22, 18);
INSERT INTO "Voto" VALUES (16, 450, 16);
INSERT INTO "Voto" VALUES (17, 458, 8);
INSERT INTO "Voto" VALUES (18, 22, 8);
INSERT INTO "Voto" VALUES (19, 469, 12);
INSERT INTO "Voto" VALUES (20, 28, 32);
INSERT INTO "Voto" VALUES (21, 28, 27);
INSERT INTO "Voto" VALUES (22, 28, 28);
INSERT INTO "Voto" VALUES (23, 0, 116);
INSERT INTO "Voto" VALUES (24, 769, 116);


--
-- Name: Votos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Votos_id_seq"', 24, true);


--
-- Data for Name: Webpay; Type: TABLE DATA; Schema: public; Owner: yichun
--

INSERT INTO "Webpay" VALUES (1, 3140000, 116333, 6623, 1109, 1109, 13327, 550763457, 'VN', 0, '20141109043347', 189, 189);
INSERT INTO "Webpay" VALUES (2, 3140000, 202944, 6623, 1109, 1109, 14201, 550814847, 'VN', 0, '20141109044221', 190, 190);
INSERT INTO "Webpay" VALUES (3, 5290000, 143015, 6623, 1109, 1109, 14703, 550844976, 'VN', 0, '20141109044723', 192, 192);
INSERT INTO "Webpay" VALUES (4, 10730000, 101933, 6623, 1123, 1123, 71502, 673771019, 'VD', 0, '20141123101501', 194, 194);
INSERT INTO "Webpay" VALUES (5, 9570000, 154569, 6623, 1123, 1123, 73233, 673876144, 'SI', 3, '20141123103234', 197, 197);
INSERT INTO "Webpay" VALUES (6, 3140000, 957013, 6623, 1123, 1123, 73748, 673907631, 'VC', 40, '20141123103749', 198, 198);
INSERT INTO "Webpay" VALUES (7, 3190000, 207100, 6623, 1123, 1123, 73947, 673919565, 'VN', 0, '20141123103950', 199, 199);
INSERT INTO "Webpay" VALUES (8, 5760000, 155856, 6623, 1123, 1123, 74334, 673942264, 'VN', 0, '20141123104336', 201, 201);
INSERT INTO "Webpay" VALUES (9, 8720000, 570745, 6623, 1128, 1128, 231859, 722754960, 'VD', 0, '20141129021902', 203, 203);
INSERT INTO "Webpay" VALUES (10, 5630000, 634928, 6623, 1128, 1128, 232142, 722771553, 'VN', 0, '20141129022150', 205, 205);
INSERT INTO "Webpay" VALUES (11, 2940000, 154008, 6623, 1128, 1128, 232357, 722785026, 'SI', 3, '20141129022352', 206, 206);
INSERT INTO "Webpay" VALUES (12, 8320000, 188532, 6623, 1128, 1128, 233554, 722856745, 'VC', 40, '20141129023600', 210, 210);
INSERT INTO "Webpay" VALUES (13, 9450000, 114413, 6623, 1202, 1202, 141140, 754031556, 'VN', 0, '20141202171148', 211, 211);
INSERT INTO "Webpay" VALUES (14, 6030000, 953715, 6623, 1205, 1205, 172020, 781083350, 'SI', 3, '20141205202021', 212, 212);
INSERT INTO "Webpay" VALUES (15, 4950000, 111446, 6623, 1206, 1206, 81058, 786427100, 'VN', 0, '20141206110957', 215, 215);
INSERT INTO "Webpay" VALUES (16, 4950000, 639264, 6623, 1206, 1206, 82234, 786497030, 'SI', 3, '20141206112243', 216, 216);
INSERT INTO "Webpay" VALUES (17, 4950000, 174390, 6623, 1206, 1206, 82842, 786533863, 'VC', 40, '20141206112824', 217, 217);
INSERT INTO "Webpay" VALUES (18, 4950000, 173608, 6623, 1206, 1206, 91203, 786794142, 'VD', 0, '20141206121209', 218, 218);
INSERT INTO "Webpay" VALUES (19, 100, 408091, 27, 204, 204, 154848, 307575102, 'VD', 0, '20150204184905', 261, 261);
INSERT INTO "Webpay" VALUES (20, 100, 597203, 8214, 204, 204, 213101, 309631139, 'VN', 0, '20150205003143', 264, 264);
INSERT INTO "Webpay" VALUES (21, 100, 127387, 8214, 219, 219, 174925, 437897015, 'VN', 0, '20150219204917', 274, 274);
INSERT INTO "Webpay" VALUES (22, 100, 336015, 8214, 219, 219, 184204, 438277851, 'VN', 0, '20150219215240', 278, 278);
INSERT INTO "Webpay" VALUES (23, 100, 811174, 8214, 219, 219, 193211, 438513692, 'VN', 0, '20150219223151', 280, 280);


--
-- Name: Webpay_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yichun
--

SELECT pg_catalog.setval('"Webpay_id_seq"', 23, true);


--
-- Name: Access_Token_pkey; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Access_Token"
    ADD CONSTRAINT "Access_Token_pkey" PRIMARY KEY (id);


--
-- Name: Brand_pkey; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Brand"
    ADD CONSTRAINT "Brand_pkey" PRIMARY KEY (id);


--
-- Name: City_pkey; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "City"
    ADD CONSTRAINT "City_pkey" PRIMARY KEY (id);


--
-- Name: Contact_Types_pkey; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Contact_Types"
    ADD CONSTRAINT "Contact_Types_pkey" PRIMARY KEY (id);


--
-- Name: Payment_Types_pkey; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Payment_Types"
    ADD CONSTRAINT "Payment_Types_pkey" PRIMARY KEY (id);


--
-- Name: Shipping_Provider_name_key; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Shipping_Provider"
    ADD CONSTRAINT "Shipping_Provider_name_key" UNIQUE (name);


--
-- Name: Shipping_Provider_pkey; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Shipping_Provider"
    ADD CONSTRAINT "Shipping_Provider_pkey" PRIMARY KEY (id);


--
-- Name: Shipping_pkey; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Shipping"
    ADD CONSTRAINT "Shipping_pkey" PRIMARY KEY (id);


--
-- Name: State_pkey; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "State"
    ADD CONSTRAINT "State_pkey" PRIMARY KEY (id);


--
-- Name: Tag_Product_pkey; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Tag_Product"
    ADD CONSTRAINT "Tag_Product_pkey" PRIMARY KEY (id);


--
-- Name: Tag_pkey; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Tag"
    ADD CONSTRAINT "Tag_pkey" PRIMARY KEY (id);


--
-- Name: Temp_Cart_pkey; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Temp_Cart"
    ADD CONSTRAINT "Temp_Cart_pkey" PRIMARY KEY (id);


--
-- Name: Votos_pkey; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Voto"
    ADD CONSTRAINT "Votos_pkey" PRIMARY KEY (id);


--
-- Name: Webpay_pkey; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Webpay"
    ADD CONSTRAINT "Webpay_pkey" PRIMARY KEY (id);


--
-- Name: category_pk; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Category"
    ADD CONSTRAINT category_pk PRIMARY KEY (id);


--
-- Name: cellar_pk; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Cellar"
    ADD CONSTRAINT cellar_pk PRIMARY KEY (id);


--
-- Name: contact_pk; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Contact"
    ADD CONSTRAINT contact_pk PRIMARY KEY (id);


--
-- Name: kardex_pk; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Kardex"
    ADD CONSTRAINT kardex_pk PRIMARY KEY (id);


--
-- Name: order_detail_pk; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Order_Detail"
    ADD CONSTRAINT order_detail_pk PRIMARY KEY (id);


--
-- Name: order_pk; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Order"
    ADD CONSTRAINT order_pk PRIMARY KEY (id);


--
-- Name: permission_pk; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Permission"
    ADD CONSTRAINT permission_pk PRIMARY KEY (id);


--
-- Name: product_pk; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Product"
    ADD CONSTRAINT product_pk PRIMARY KEY (id);


--
-- Name: user_pk; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "User"
    ADD CONSTRAINT user_pk PRIMARY KEY (id);


--
-- Name: user_types_pk; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "User_Types"
    ADD CONSTRAINT user_types_pk PRIMARY KEY (id);


--
-- Name: Order_billing_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Order"
    ADD CONSTRAINT "Order_billing_id_fkey" FOREIGN KEY (billing_id) REFERENCES "Contact"(id);


--
-- Name: Order_shipping_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Order"
    ADD CONSTRAINT "Order_shipping_id_fkey" FOREIGN KEY (shipping_id) REFERENCES "Contact"(id);


--
-- Name: Order_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Order"
    ADD CONSTRAINT "Order_user_id_fkey" FOREIGN KEY (user_id) REFERENCES "User"(id);


--
-- Name: TempCart_User; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Temp_Cart"
    ADD CONSTRAINT "TempCart_User" FOREIGN KEY (user_id) REFERENCES "User"(id) ON DELETE CASCADE;


--
-- Name: Temp_Cart_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Temp_Cart"
    ADD CONSTRAINT "Temp_Cart_product_id_fkey" FOREIGN KEY (product_id) REFERENCES "Product"(id);


--
-- Name: category_category; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Category"
    ADD CONSTRAINT category_category FOREIGN KEY (parent_id) REFERENCES "Category"(id);


--
-- Name: cellar_city; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Cellar"
    ADD CONSTRAINT cellar_city FOREIGN KEY (city_id) REFERENCES "City"(id);


--
-- Name: contact_contact_type; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Contact"
    ADD CONSTRAINT contact_contact_type FOREIGN KEY (type_id) REFERENCES "Contact_Types"(id);


--
-- Name: contact_user; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Contact"
    ADD CONSTRAINT contact_user FOREIGN KEY (user_id) REFERENCES "User"(id);


--
-- Name: kardex_cellar; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Kardex"
    ADD CONSTRAINT kardex_cellar FOREIGN KEY (cellar_id) REFERENCES "Cellar"(id);


--
-- Name: order_detail_order; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Order_Detail"
    ADD CONSTRAINT order_detail_order FOREIGN KEY (order_id) REFERENCES "Order"(id);


--
-- Name: order_detail_product; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Order_Detail"
    ADD CONSTRAINT order_detail_product FOREIGN KEY (product_id) REFERENCES "Product"(id);


--
-- Name: product_category; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Product"
    ADD CONSTRAINT product_category FOREIGN KEY (category_id) REFERENCES "Category"(id);


--
-- Name: user_user_types; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "User"
    ADD CONSTRAINT user_user_types FOREIGN KEY (type_id) REFERENCES "User_Types"(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--
