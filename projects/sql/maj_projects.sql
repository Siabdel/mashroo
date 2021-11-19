--  exec sp_columns projects_ticket_categories

-- SELECT * FROM projects_ticket_categories
-- SELECT * FROM projects_project_categories

SELECT * FROM projects_project

SELECT
    tab.name AS [Table]
    ,tab.id AS [Table Id]
    ,constr.name AS [Constraint Name]
    ,constr.xtype AS [Constraint Type]
    ,CASE constr.xtype WHEN 'PK' THEN 'Primary Key' WHEN 'UQ' THEN 'Unique' ELSE '' END AS [Constraint Name2]
    ,i.index_id AS [Index ID]
    ,ic.column_id AS [Column ID]
    ,clmns.name AS [Column Name]
    ,clmns.max_length AS [Column Max Length]
    ,clmns.precision AS [Column Precision]
    ,CASE WHEN clmns.is_nullable = 0 THEN 'NO' ELSE 'YES' END AS [Column Nullable]
    ,CASE WHEN clmns.is_identity = 0 THEN 'NO' ELSE 'YES' END AS [Column IS IDENTITY]
FROM sysobjects AS tab
INNER JOIN sysobjects AS constr ON(constr.parent_obj = tab.id AND constr.type = 'K')
INNER JOIN sys.indexes AS i ON( (i.index_id > 0 and i.is_hypothetical = 0) AND (i.object_id=tab.id) AND i.name = constr.name )
INNER JOIN sys.index_columns AS ic ON (ic.column_id > 0 and (ic.key_ordinal > 0 or ic.partition_ordinal = 0 or ic.is_included_column != 0))
                                    AND (ic.index_id=CAST(i.index_id AS int)
                                    AND ic.object_id=i.object_id)
INNER JOIN sys.columns AS clmns ON clmns.object_id = ic.object_id and clmns.column_id = ic.column_id
WHERE   tab.name like '%projects_project%'
ORDER BY tab.name
# Supprimer des constarints persistantes
##
alter table projects_project drop constraint   UQ__projects__9DD95BAF7D92D2E1
alter table projects_ticket drop constraint   UQ__projects__9DD95BAF1643E3EC


"""
--exec sp_columns projects_project_participants
--exec sp_columns projects_project

-- exec sp_columns projects_profileuser
-- exec sp_columns django_migrations

-- SELECT * FROM django_migrations
-- WHERE app='PROFILE'
"""
