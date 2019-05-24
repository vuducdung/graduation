pg_dump -U username -f backup.sql database_name
psql -d database_name -f backup.sql

./manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude sessions --indent 2 > db.json

CREATE DATABASE "graduation"
    ENCODING 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE template0;
    
CREATE OR REPLACE FUNCTION vn_unaccent(text)
  RETURNS text AS
$func$
SELECT lower(translate($1,
'¹²³ÀÁẢẠÂẤẦẨẬẪÃÄÅÆàáảạâấầẩẫậãäåæĀāĂẮẰẲẴẶăắằẳẵặĄąÇçĆćĈĉĊċČčĎďĐđÈÉẸÊẾỀỄỆËèéẹêềếễệëĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨÌÍỈỊÎÏìíỉịîïĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłÑñŃńŅņŇňŉŊŋÒÓỎỌÔỐỒỔỖỘỐỒỔỖỘƠỚỜỞỠỢÕÖòóỏọôốồổỗộơớờỡợởõöŌōŎŏŐőŒœØøŔŕŖŗŘřßŚśŜŝŞşŠšŢţŤťŦŧÙÚỦỤƯỪỨỬỮỰÛÜùúủụûưứừửữựüŨũŪūŬŭŮůŰűŲųŴŵÝýÿŶŷŸŹźŻżŽžёЁ',
'123AAAAAAAAAAAAAAaaaaaaaaaaaaaaAaAAAAAAaaaaaaAaCcCcCcCcCcDdDdEEEEEEEEEeeeeeeeeeEeEeEeEeEeGgGgGgGgHhHhIIIIIIIiiiiiiiIiIiIiIiIiJjKkkLlLlLlLlLlNnNnNnNnnNnOOOOOOOOOOOOOOOOOOOOOOOooooooooooooooooooOoOoOoEeOoRrRrRrSSsSsSsSsTtTtTtUUUUUUUUUUUUuuuuuuuuuuuuUuUuUuUuUuUuWwYyyYyYZzZzZzеЕ'));
$func$ LANGUAGE sql IMMUTABLE;

CREATE OR REPLACE FUNCTION news_tsv_trigger_func()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.news_tsv =
	setweight(to_tsvector(coalesce(vn_unaccent(NEW.name))),'A') ||
	setweight(to_tsvector(coalesce(vn_unaccent(NEW."keyWords"))), 'B') ||
	setweight(to_tsvector(coalesce(vn_unaccent(NEW.address))), 'D') ||;
RETURN NEW;
END $$;



CREATE TRIGGER news_tsv_trigger BEFORE INSERT OR UPDATE
OF name, "keyWords", address ON admin_locations FOR EACH ROW
EXECUTE PROCEDURE news_tsv_trigger_func();
CREATE INDEX admin_locations_idx ON admin_locations USING GIN(news_tsv);
create extension "cube";
create extension "earthdistance";

python manage.py loaddata /home/dungvd/db.json 
