from sqlalchemy import and_

from skeletor.core.compat import reduce


def rowdict(row):
    if row is None:
        return None
    return dict(row.items())


def rowdicts(rows):
    if rows is None:
        return None
    return [dict(r) for r in rows]


def fetchall(table):
    return table.select().execute().fetchall()


def fetchone(table, where_expr):
    """Select one row from a table filtered by a `where` expression"""
    expr = table.select().where(where_expr)
    return rowdict(expr.execute().fetchone())


def where_clause(table, operator=and_, **where):
    """Return a `where` expression to combine column=value criteria"""
    # Create a list of (column == value) filters and combine them using the
    # provided combinator.
    filters = [(getattr(table.c, k) == v) for k, v in where.items()]
    # If we have multiple filters then combine them using AND by default,
    # otherwise use the first one as-is.
    if len(filters) == 1:
        where_expr = filters[0]
    else:
        where_expr = reduce(operator, filters)
    return where_expr


def select_one(table, operator=and_, **where):
    """Select one row filtered by `where` column=value criteria"""
    where_expr = where_clause(table, operator=operator, **where)
    return fetchone(table, where_expr)


def select_all(table, operator=and_, **where):
    """Select all rows filtered by `where` column=value criteria"""
    where_expr = where_clause(table, operator=operator, **where)
    return table.select().where(where_expr).execute().fetchall()


def update_values(table, where_expr, **values):
    """Return an update().values(...) expression for the given table"""
    return table.update().values(**values).where(where_expr)


def update(table, table_id, **values):
    """Update a specific row's values by ID"""
    return update_values(table, table.c.id==table_id, **values).execute()
