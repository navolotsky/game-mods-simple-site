from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_LENGTH = 255


def _user_directory_path(instance, filename):
    print(f"upload_to called with instance of {type(instance)}")
    if isinstance(instance, UserProfile):
        return f"user_{instance.user_id}/profile/{filename}"
    elif isinstance(instance, ModImage):
        return f"mod_images/{filename}"
    else:
        raise TypeError(f"only accept instance either of {UserProfile, ModImage}")


class TimestampableChangeModel(models.Model):
    added_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HiddenableModel(models.Model):
    hidden = models.BooleanField(default=False)

    class Meta:
        abstract = True


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE,
                                related_name="profile", related_query_name="profile")
    avatar = models.ImageField(upload_to=_user_directory_path)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "user_profiles"


class Game(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "games"


class ModCategory(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "mod_categories"


class Mod(TimestampableChangeModel, HiddenableModel):
    game = models.ForeignKey(Game, models.PROTECT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT)
    categories = models.ManyToManyField(ModCategory, db_table="mods_n_categories")
    default_version = models.OneToOneField("ModVersion", models.PROTECT, blank=False, null=True,
                                           related_name="+")

    class Meta:
        default_related_name = "mods"
        db_table = "mods"
        ordering = ["-last_updated_at", "-pk"]


class ModImage(models.Model):
    file = models.ImageField(upload_to=_user_directory_path)

    class Meta:
        db_table = "mod_images"


class ModVersion(TimestampableChangeModel, HiddenableModel):
    mod = models.ForeignKey(Mod, models.CASCADE, related_name="versions", related_query_name="versions")
    title = models.CharField(max_length=MAX_LENGTH, db_index=True)
    short_description = models.TextField()
    full_description = models.TextField()
    main_image = models.ForeignKey(ModImage, models.PROTECT, null=True,
                                   related_name="mod_versions_having_as_main")
    images = models.ManyToManyField(ModImage, db_table="mod_versions_n_images")
    number = models.CharField(max_length=MAX_LENGTH)
    comment = models.CharField(max_length=MAX_LENGTH)

    class Meta:
        default_related_name = "mod_versions"
        db_table = "mod_versions"
        constraints = [models.UniqueConstraint(fields=("mod", "number"), name="unique_mod_version_number")]
        ordering = ["-added_at", "-pk"]
        get_latest_by = ["added_at", "pk"]


class ModDownloadLink(TimestampableChangeModel):
    mod_version = models.ForeignKey(ModVersion, models.CASCADE,
                                    related_name="download_links", related_query_name="download_links")
    url = models.URLField(max_length=MAX_LENGTH, unique=True)
    comment = models.CharField(max_length=MAX_LENGTH)

    class Meta:
        db_table = "mod_download_links"
        ordering = ["added_at", "pk"]


class ModUserRating(models.Model):
    PossibleRatingValues = models.IntegerChoices("PossibleRatingValues", " ".join([str(x + 1) for x in range(5)]))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
                             related_name="mod_ratings", related_query_name="mod_ratings")
    mod = models.ForeignKey(Mod, models.CASCADE, related_name="user_ratings", related_query_name="user_ratings")
    mod_version = models.ForeignKey(ModVersion, models.CASCADE,
                                    related_name="user_ratings", related_query_name="user_ratings")
    rating = models.PositiveSmallIntegerField(choices=PossibleRatingValues.choices)
    rated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mod_user_ratings"
        constraints = [
            models.UniqueConstraint(fields=("user", "mod"), name="one_rating_on_same_mod_per_user")
        ]


class ModUserComment(TimestampableChangeModel, HiddenableModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
                             related_name="mod_comments", related_query_name="mod_comments")
    mod = models.ForeignKey(Mod, models.CASCADE, related_name="user_comments", related_query_name="user_comments")
    mod_version = models.ForeignKey(ModVersion, models.CASCADE,
                                    related_name="user_comments", related_query_name="user_comments")
    text = models.TextField()

    class Meta:
        db_table = "mod_user_comments"
        ordering = ["-added_at", "-pk"]
