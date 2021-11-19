LOAD DATA [LOCAL] INFILE 'nom_fichier' IGNORE
-- IGNORE se place juste avant INTO, comme dans INSERT
INTO TABLE nom_table
[FIELDS
    [TERMINATED BY '\t']
    [ENCLOSED BY '']
    [ESCAPED BY '\\' ]
]
[LINES
    [STARTING BY '']
    [TERMINATED BY '\n']
]
[IGNORE nombre LINES]
[(nom_colonne,...)];
