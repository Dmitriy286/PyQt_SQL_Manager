import abc

from sqlalchemy.orm import DeclarativeMeta


class DeclarativeABCMeta(DeclarativeMeta, abc.ABCMeta):
   pass