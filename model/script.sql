CREATE TABLE "Size"
(
  name text,
  id serial NOT NULL,
  CONSTRAINT "Size_pkey" PRIMARY KEY (id )
);

ALTER TABLE "Kardex" ADD COLUMN size_id integer;
ALTER TABLE "Kardex" DROP CONSTRAINT kardex_cellar;
ALTER TABLE "Kardex" ADD CONSTRAINT kardex_cellar FOREIGN KEY (cellar_id)
      REFERENCES "Cellar" (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Kardex" ADD CONSTRAINT kardex_size FOREIGN KEY (size_id) REFERENCES "Size" (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

INSERT INTO "Size" VALUES ('35.0', 1);
INSERT INTO "Size" VALUES ('36.0', 2);
INSERT INTO "Size" VALUES ('37.0', 3);
INSERT INTO "Size" VALUES ('38.0', 4);
INSERT INTO "Size" VALUES ('39.0', 5);
INSERT INTO "Size" VALUES ('40.0', 6);

UPDATE "Kardex" t1
SET size_id = t2.id
FROM "Size" t2
where t2.name = t1.size;

ALTER TABLE "Kardex" DROP COLUMN size;

alter table "Product" drop column "size";

CREATE OR REPLACE VIEW sizes AS 
 SELECT DISTINCT ON (k.product_sku, k.size_id) k.product_sku, k.size_id, s.name
   FROM "Kardex" k
   JOIN "Size" s ON s.id = k.size_id
  ORDER BY k.product_sku, k.size_id DESC;

alter table "Product" add column "bulk_price" integer not null default 0;