# Author: Benjamin Leopold (cometsong)
# Created: 2015-01-13 11:05:06-0500
# Requirements: MySQL v5+

CREATE USER 'jaxlims'@'localhost' IDENTIFIED BY 'j@xL1m$';

-- single field for superfast data checking (of 60,466,176 possible values)
CREATE TABLE jaxid_master (
    jaxid CHAR(6) CHARACTER SET binary NOT NULL,
    CONSTRAINT PRIMARY KEY(jaxid),
    INDEX (jaxid ASC) USING BTREE
);

-- automate UPPERcase JAXid values for consistency
CREATE TRIGGER jaxid_upcase_ins BEFORE INSERT
    ON jaxid_master FOR EACH ROW
    SET NEW.jaxid = BINARY UPPER(CONVERT(NEW.jaxid USING utf8));

CREATE TRIGGER jaxid_upcase_upd BEFORE UPDATE
    ON jaxid_master FOR EACH ROW
    SET NEW.jaxid = BINARY UPPER(CONVERT(NEW.jaxid USING utf8));

GRANT INSERT, SELECT ON jaxid_db.* TO 'jaxlims;'
