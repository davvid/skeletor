from functools import reduce

from sqlalchemy import and_


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


def where(table, operator=and_, **values):
    """Return a `where` expression to combine column=value criteria"""
    # Create a list of (column == value) filters and combine them
    return reduce_filters(table, eq_column, operator=operator, **values)


def iwhere(table, operator=and_, **values):
    """Return a `where` expression to combine column ILIKE value criteria"""
    # Create a list of (column ILIKE value) filters and combine them
    return reduce_filters(table, ilike_column, operator=operator, **values)


def eq_column(table, column, value):
    """column == value"""
    return getattr(table.c, column) == value


def ilike_column(table, column, value):
    """column ILIKE value"""
    return getattr(table.c, column).ilike(value)


def reduce_filters(table, fn, operator=and_, **values):
    """Return a `where` expression to combine column=value criteria"""
    # Create a list of (column == value) filters and combine them using the
    # provided combinator.
    filters = [fn(table, k, v) for k, v in values.items()]
    # If we have multiple filters then combine them using AND by default,
    # otherwise use the first one as-is.
    if len(filters) == 1:
        expr = filters[0]
    else:
        expr = reduce(operator, filters)
    return expr


def select_one(table, operator=and_, **values):
    """Select one row filtered by `values` column=value criteria"""
    where_expr = where(table, operator=operator, **values)
    return fetchone(table, where_expr)


def select_all(table, operator=and_, **values):
    """Select all rows filtered by `values` column=value criteria"""
    where_expr = where(table, operator=operator, **values)
    return table.select().where(where_expr).execute().fetchall()


def update_values(table, where_expr, **values):
    """Return an update().values(...) expression for the given table"""
    return table.update().values(**values).where(where_expr)


def update(table, table_id, **values):
    """Update a specific row's values by ID"""
    return update_values(table, table.c.id == table_id, **values).execute()


def delete(table, operator=and_, **values):
    """Delete rows from a table based on the filter values"""
    where_expr = where(table, operator=operator, **values)
    return table.delete(where_expr).execute()
