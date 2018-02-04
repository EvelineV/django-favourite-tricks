def get_family_tree():
    return '''
    WITH RECURSIVE family_tree (id, name, path, level, mother_id) AS (
        SELECT
            id,
            name,
            ARRAY[]::varchar(255)[] || name AS path,
            0,
            mother_id
        FROM zoo_animal
        WHERE mother_id is NULL
        UNION ALL
        SELECT
            animal.id,
            animal.name,
            tree.path || animal.name,
            tree.level + 1,
            tree.id
        FROM zoo_animal AS animal, family_tree AS tree
        WHERE animal.mother_id = tree.id
    )
    '''


def get_list_of_ancestors():
    return '''
        {recursive}
        SELECT
            path
        FROM family_tree WHERE name=%s
    '''.format(recursive=get_family_tree())


def get_list_of_descendants(name):
    return '''
    {recursive}
    SELECT
        id, name
    FROM family_tree
    WHERE '{name}' = ANY(family_tree.path)
    ORDER BY id
    '''.format(recursive=get_family_tree(), name=name)
