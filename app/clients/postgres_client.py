import itertools
import logging
from typing import Dict, List, Any

import sqlalchemy
from flask import g
from sqlalchemy import desc, asc
from sqlalchemy import or_, and_, nullslast, nullsfirst
from sqlalchemy.orm import sessionmaker, Load

from app.main import CONFIG


class PostgresClient:
    """
    1. _get_queryset
        1.1 _filter_queryset
            1.1.1 _get_select_clause
            1.1.2 _search_queryset
        1.2 _paginate_queryset
            1.2.1 _sort_queryset
    """

    def __init__(self):
        self.pg_db = CONFIG.PG_DB

    @property
    def model(self):
        raise NotImplemented

    @property
    def select_fields_settings(self):
        """
        <relationship_name>: {
            <hybrid_property_name>: <a list of fields from the relationship to select>
        }
        """
        return {}

    def _get_select_clause(self, fields_: List[str] = None):
        """
        Trims unnecessary fields from SELECT statement.
        """
        if fields_:
            strategies = []

            load_only_params = [_ for _ in fields_ if _ in self.model.__table__.columns]
            if load_only_params:
                strategies.append(Load(self.model).load_only(*load_only_params))

            for relationship, options in self.select_fields_settings.items():
                if set(options.keys()).intersection(set(fields_)):
                    load = set(itertools.chain(*[v for k, v in options.items() if k in fields_]))
                    if relationship == self.model.__tablename__:
                        strategies.append(
                            Load(self.model).load_only(*load)
                        )
                    else:
                        strategies.append(
                            Load(self.model).joinedload(relationship).load_only(*load)
                        )

            queryset = self.pg_db.query(self.model).options(*strategies)
        else:
            queryset = self.pg_db.query(self.model)

        return queryset

    def _filter_queryset(self,
                         not_: Dict = None,
                         in_and_: Dict = None,
                         in_or_: Dict = None,
                         lt_: Dict[str, Any] = None,
                         gt_: Dict[str, Any] = None,
                         lte_: Dict[str, Any] = None,
                         gte_: Dict[str, Any] = None,
                         contains_: Dict[str, List] = None,
                         fields_: List[str] = None,
                         search_: str = None,
                         sort_: str = None,
                         limit_: int = None,
                         offset_: int = None,
                         **kwargs):
        queryset = self._get_select_clause(fields_=fields_)

        if kwargs:
            queryset = queryset.filter_by(**kwargs)

        if not_:
            for k, v in not_.items():
                queryset = queryset.filter(sqlalchemy.not_(getattr(self.model, k) == v))

        if in_and_:
            and_clause = []
            for k, v in in_and_.items():
                and_clause.append(getattr(self.model, k).in_(v))

            queryset = queryset.filter(and_(*and_clause))

        if in_or_:
            or_clause = []
            for k, v in in_or_.items():
                or_clause.append(getattr(self.model, k).in_(v))

            queryset = queryset.filter(or_(*or_clause))

        if lt_:
            for k, v in lt_.items():
                queryset = queryset.filter(getattr(self.model, k) < v)

        if gt_:
            for k, v in gt_.items():
                queryset = queryset.filter(getattr(self.model, k) > v)

        if lte_:
            for k, v in lte_.items():
                queryset = queryset.filter(getattr(self.model, k) <= v)

        if gte_:
            for k, v in gte_.items():
                queryset = queryset.filter(getattr(self.model, k) >= v)

        if contains_:
            for k, v in contains_.items():
                queryset = queryset.filter(getattr(self.model, k).contains(v))

        if search_:
            queryset = self._search_queryset(queryset, search_)

        return queryset

    def _search_queryset(self, queryset, search_: str = None):
        raise NotImplemented

    def _sort_queryset(self, queryset, sort_: str = None):
        if sort_:
            if sort_.startswith('-'):
                queryset = queryset.order_by(nullslast(desc(getattr(self.model, sort_[1:]))))
            else:
                queryset = queryset.order_by(nullsfirst(asc(getattr(self.model, sort_))))

        return queryset

    def _paginate_queryset(self,
                           queryset,
                           sort_: str = None,
                           limit_: int = None,
                           offset_: int = None):

        queryset = self._sort_queryset(queryset, sort_)

        if limit_ is not None:
            queryset = queryset.limit(limit_)

        if offset_ is not None:
            queryset = queryset.offset(offset_)

        return queryset

    def _get_queryset(self,
                      not_: Dict = None,
                      in_and_: Dict[str, List] = None,
                      in_or_: Dict[str, List] = None,
                      lt_: Dict[str, Any] = None,
                      gt_: Dict[str, Any] = None,
                      lte_: Dict[str, Any] = None,
                      gte_: Dict[str, Any] = None,
                      contains_: Dict[str, List] = None,
                      fields_: List = None,
                      search_: str = None,
                      sort_: str = None,
                      limit_: int = None,
                      offset_: int = None,
                      *args, **kwargs):
        queryset = self._filter_queryset(
            not_,
            in_and_,
            in_or_,
            lt_,
            gt_,
            lte_,
            gte_,
            contains_,
            fields_,
            search_,
            **kwargs)

        queryset = self._paginate_queryset(queryset, sort_, limit_, offset_)

        return queryset

    def count(self, *args, **kwargs):
        return self._filter_queryset(*args, **kwargs).count()

    def exists(self, *args, **kwargs):
        return self.pg_db.query(self._get_queryset(*args, **kwargs).exists()).scalar()

    def fetch(self, *args, **kwargs):
        return self._get_queryset(*args, **kwargs).first()

    def fetch_all(self, *args, **kwargs):
        return self._get_queryset(*args, **kwargs).all()

    def fetch_all_query(self, *args, **kwargs):
        return self._get_queryset(*args, **kwargs)

    def create(self, **kwargs):
        instance = self.model(**kwargs)

        self.pg_db.add(instance)
        self.pg_db.flush()

        return instance

    def update(self, pk: int, **kwargs):
        self.pg_db.query(self.model).filter(self.model.id == pk).update(kwargs)
        self.pg_db.flush()

    def delete(self, pk: int, **kwargs):
        self.pg_db.query(self.model).filter(self.model.id == pk).delete()
        self.pg_db.flush()

    def bulk_create(self, mappings: List[Dict]):
        engine = self.pg_db.session.get_bind(mapper=None, shard_id=g.tenant_host)

        Session = sessionmaker(bind=engine)
        session = Session()

        session.execute(f"set role {g.tenant_dbname}")
        session.execute(f"set schema '{g.tenant_dbname}'")

        instances = [self.model(**_) for _ in mappings]

        session.bulk_save_objects(instances, return_defaults=True)
        session.commit()
        session.close()

        return instances

    def bulk_update(self, mappings: List[Dict]):
        engine = self.pg_db.session.get_bind(mapper=None, shard_id=g.tenant_host)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.execute(f"set role {g.tenant_dbname}")
        session.execute(f"set schema '{g.tenant_dbname}'")

        session.bulk_update_mappings(self.model, mappings)
        session.commit()
        session.close()

    def commit(self):
        self.pg_db.commit()

    def get_ddl(self):
        table_name = self.model.__tablename__
        columns = self.model.metadata.tables[table_name].columns

        return [{'name': k, 'type': v.type.__repr__().upper()} for k, v in columns.items()]
