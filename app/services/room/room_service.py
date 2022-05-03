from sqlalchemy import nullslast, desc, nullsfirst, asc

from app.clients.postgres_client import PostgresClient
from app.models.room import Room


class RoomService(PostgresClient):
    model = Room

    def _sort_queryset(self, queryset, sort_: str = None):
        if sort_:
            queryset = queryset.order_by(self.model.building_id)

            if sort_.startswith('-'):
                queryset = queryset.order_by(nullslast(desc(getattr(self.model, sort_[1:]))))
            else:
                queryset = queryset.order_by(nullsfirst(asc(getattr(self.model, sort_))))

        return queryset