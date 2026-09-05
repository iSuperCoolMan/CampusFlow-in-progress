from enum import StrEnum
from typing import get_args, Any, Annotated
from uuid import UUID

from annotated_types import Interval
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


def _extract_constraints(column_name: str, annotation: Any) -> CheckConstraint | None:
    """
    Анализирует аннотацию поля и возвращает CheckConstraint,
    если находит ограничения типа Interval или подкласс StrEnum.
    """
    args = get_args(annotation)
    if not args:
        target_type = annotation
    else:
        target_type = args[0]

    base_type = target_type
    if getattr(target_type, "__origin__", None) is Annotated:
        base_type = get_args(target_type)[0]

    if isinstance(base_type, type) and issubclass(base_type, StrEnum):
        allowed_values = [f"'{item.value}'" for item in base_type]
        if allowed_values:
            values_str = ", ".join(allowed_values)
            return CheckConstraint(
                f"{column_name} IN ({values_str})",
                name=f"check_{column_name}_enum_values"
            )

    interval_meta = None

    for arg in args:
        if isinstance(arg, Interval):
            interval_meta = arg
            break

        if getattr(arg, "__origin__", None) is Annotated:
            for sub_arg in get_args(arg):
                if isinstance(sub_arg, Interval):
                    interval_meta = sub_arg
                    break

    if not interval_meta and getattr(target_type, "__origin__", None) is Annotated:
        for arg in get_args(target_type):
            if isinstance(arg, Interval):
                interval_meta = arg
                break

    if interval_meta:
        conditions = []
        if interval_meta.ge is not None:
            conditions.append(f"{column_name} >= {interval_meta.ge}")
        elif interval_meta.gt is not None:
            conditions.append(f"{column_name} > {interval_meta.gt}")

        if interval_meta.le is not None:
            conditions.append(f"{column_name} <= {interval_meta.le}")
        elif interval_meta.lt is not None:
            conditions.append(f"{column_name} < {interval_meta.lt}")

        if conditions:
            sql_expression = " AND ".join(conditions)
            return CheckConstraint(sql_expression, name=f"check_{column_name}_interval")

    return None


class BaseORM(DeclarativeBase):
    __abstract__ = True

    uuid: Mapped[UUID] = mapped_column(primary_key=True)


    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = cls.__name__[:-3]
        upper_indices = [i for i, c in enumerate(name) if c.isupper()]
        space_indices = []

        for i in range(1, len(upper_indices)):
            if upper_indices[i] >= len(name):
                continue

            if name[upper_indices[i]+1].islower():
                space_indices.append(upper_indices[i])

        for i in range(len(space_indices)):
            name = name[:space_indices[i] + i] + "_" + name[space_indices[i] + i:]

        if name.endswith("s"):
            name += "es"
        elif name.endswith("y"):
            name = name[:-1] + "ies"
        else:
            name += "s"

        return name.lower()


    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not hasattr(cls, "__annotations__"):
            return

        constraints = []

        for attr_name, annotation in cls.__annotations__.items():
            if getattr(annotation, "__origin__", None) is Mapped:
                constraint = _extract_constraints(attr_name, annotation)
                if constraint:
                    constraints.append(constraint)

        if constraints:
            current_table_args = getattr(cls, "__table_args__", None)

            if current_table_args is None:
                cls.__table_args__ = tuple(constraints)
            elif isinstance(current_table_args, tuple):
                cls.__table_args__ = current_table_args + tuple(constraints)
            elif isinstance(current_table_args, dict):
                cls.__table_args__ = tuple(constraints) + (current_table_args,)
