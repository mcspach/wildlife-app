-- update prod_data.wildlife_pt with dev_data.wildlife_pt
INSERT INTO prod_data.wildlife_pt --specify columns if necessary
SELECT [DISTINCT] * FROM dev_data.wildlife_pt;
