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
    size_id integer
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
    size text DEFAULT ''::text NOT NULL,
    price integer
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
    image_6 text DEFAULT ''::text,
    promotion_price integer DEFAULT 0,
    bulk_price integer DEFAULT 0 NOT NULL
);


ALTER TABLE public."Product" OWNER TO yichun;

--
-- Name: Product_Size; Type: TABLE; Schema: public; Owner: yichun; Tablespace: 
--

CREATE TABLE "Product_Size" (
    id integer NOT NULL,
    size_id integer NOT NULL,
    product_sku text NOT NULL
);


ALTER TABLE public."Product_Size" OWNER TO yichun;

--
-- Name: Product_Size_id_seq; Type: SEQUENCE; Schema: public; Owner: yichun
--

CREATE SEQUENCE "Product_Size_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Product_Size_id_seq" OWNER TO yichun;

--
-- Name: Product_Size_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yichun
--

ALTER SEQUENCE "Product_Size_id_seq" OWNED BY "Product_Size".id;


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
-- Name: Size; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "Size" (
    name text,
    id integer NOT NULL
);


ALTER TABLE public."Size" OWNER TO postgres;

--
-- Name: Size_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "Size_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Size_id_seq" OWNER TO postgres;

--
-- Name: Size_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE "Size_id_seq" OWNED BY "Size".id;


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
    bought integer DEFAULT 0,
    price integer
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
-- Name: sizes; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW sizes AS
    SELECT DISTINCT ON (k.product_sku, k.size_id) k.product_sku, k.size_id, s.name FROM ("Kardex" k JOIN "Size" s ON ((s.id = k.size_id))) ORDER BY k.product_sku, k.size_id DESC;


ALTER TABLE public.sizes OWNER TO postgres;

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

ALTER TABLE ONLY "Product_Size" ALTER COLUMN id SET DEFAULT nextval('"Product_Size_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Shipping" ALTER COLUMN id SET DEFAULT nextval('"Shipping_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Shipping_Provider" ALTER COLUMN id SET DEFAULT nextval('"Shipping_Provider_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "Size" ALTER COLUMN id SET DEFAULT nextval('"Size_id_seq"'::regclass);


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
-- Name: Size_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "Size"
    ADD CONSTRAINT "Size_pkey" PRIMARY KEY (id);


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
-- Name: pk_product_size; Type: CONSTRAINT; Schema: public; Owner: yichun; Tablespace: 
--

ALTER TABLE ONLY "Product_Size"
    ADD CONSTRAINT pk_product_size PRIMARY KEY (size_id, product_sku);


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
-- Name: Kardex_product_sku_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Kardex"
    ADD CONSTRAINT "Kardex_product_sku_fkey" FOREIGN KEY (product_sku, size_id) REFERENCES "Product_Size"(product_sku, size_id);


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
-- Name: kardex_size; Type: FK CONSTRAINT; Schema: public; Owner: yichun
--

ALTER TABLE ONLY "Kardex"
    ADD CONSTRAINT kardex_size FOREIGN KEY (size_id) REFERENCES "Size"(id);


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

