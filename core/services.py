from typing import List, Optional, Union

from django.db.models import Count, Model, Q

from core.models import Game, ModCategory


def _get_queryset_for_menu(filters: List[Q], model: Model, mods_number__gte: Optional[int] = None):
    return (model.objects
            .filter(mods__hidden=False, mods__showed_version__hidden=False, *filters)
            .annotate(mods_number=Count("mods"))
            .filter(mods_number__gte=1 if mods_number__gte is None else mods_number__gte)
            .values("id", "name", "mods_number")
            .order_by("name"))


def get_games_queryset_for_menu(mods_category: Optional[Union[ModCategory, int]] = None,
                                mods_number__gte: Optional[int] = None):
    return _get_queryset_for_menu([Q(mods__categories=mods_category)] if mods_category else [],
                                  model=Game, mods_number__gte=mods_number__gte)


def get_mod_categories_queryset_for_menu(game: Optional[Union[Game, int]] = None,
                                         mods_number__gte: Optional[int] = None):
    return _get_queryset_for_menu([Q(mods__game=game)] if game else [],
                                  model=ModCategory, mods_number__gte=mods_number__gte)
