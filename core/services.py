from django.db.models import Count

from core.models import Game


def get_games_queryset_for_menu():
    return (
        Game.objects
            .filter(mod__hidden=False, mod__showed_version__hidden=False)
            .annotate(mods_number=Count("mod"))
            .filter(mods_number__gte=0)
            .values("id", "name", "mods_number")
            .order_by("name")
    )
