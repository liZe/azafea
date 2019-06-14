# Copyright (c) 2019 - Endless
#
# This file is part of Azafea
#
# Azafea is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Azafea is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Azafea.  If not, see <http://www.gnu.org/licenses/>.


from sqlalchemy.orm.session import Session as DbSession
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Unicode

from azafea.model import Base, NullableBoolean


class Event(Base):
    __tablename__ = 'nullableboolean_event'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    value = Column(NullableBoolean, nullable=False)


def process(dbsession: DbSession, record: bytes) -> None:
    pass