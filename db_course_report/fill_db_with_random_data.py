import os
import random
import string
import sys
from functools import partial
from pathlib import Path
from random import choice, choices, randint, sample

import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction

try:
    from core import models as m
except (ImportError, ImproperlyConfigured):
    project_root_dir = str(Path(__file__).resolve().parent.parent)
    if project_root_dir not in sys.path:
        sys.path.insert(0, project_root_dir)
    if not settings.configured:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_mods_simple_site.settings')
        django.setup()
    from core import models as m

DEFAULT_TEST_DATA_DIR = f"{settings.MEDIA_ROOT}/test_data"

DEFAULT_BATCH_SIZE = 100

DEFAULT_CLEAR_TABLES = False
DEFAULT_AUTOCOMMIT = False

DEFAULT_SEED = 0

DEFAULT_EMPTY_FIELDS_PROBABILITY = 0.05

DEFAULT_MIN_NUM_USERS_TO_GEN = 1
DEFAULT_MAX_NUM_USERS_TO_GEN = 100

DEFAULT_MIN_NUM_MODS_TO_GEN = 1
DEFAULT_MAX_NUM_MODS_TO_GEN = 100

NUM_GAMES = 5

NUM_MOD_CATEGORIES = 10

MIN_NUM_MOD_CATEGORIES = 0
MAX_NUM_MODS_CATEGORIES = 3

MIN_NUM_MOD_VERSIONS = 1
MAX_NUM_MOD_VERSIONS = 9

MIN_NUM_USER_COMMENTS = 0
MAX_NUM_USER_COMMENTS = 100

MIN_NUM_USER_RATINGS = 0
MAX_NUM_USER_RATINGS = 100

MIN_NUM_MOD_VERSION_IMAGES = 0
MAX_NUM_MOD_VERSION_IMAGES = 7
MIN_NUM_MOD_VERSION_DOWNLOAD_LINKS = 1
MAX_NUM_MOD_VERSION_DOWNLOAD_LINKS = 5

MAX_TRIES_TO_GEN_UNIQ_MOD_USER_RATING = 10


def truncate_path_prefix_to_media_root(path: Path, include=False):
    media_root_last_part = Path(settings.MEDIA_ROOT).parts[-1]
    media_root_last_part_idx = path.parts.index(media_root_last_part)
    parts_relative_to_media_root = path.parts[media_root_last_part_idx + (0 if include else 1):]
    return Path(*parts_relative_to_media_root)


def get_image_paths(test_data_dir, test_images_subdir):
    image_paths = []
    try:
        for entry in Path(test_data_dir).resolve().joinpath(test_images_subdir).iterdir():
            if not entry.is_file():
                continue
            image_paths.append(truncate_path_prefix_to_media_root(entry).as_posix())
    except FileNotFoundError as exc:
        raise ValueError("please give `test_data_dir` as absolute or "
                         "run script from dir that is parent to MEDIA_ROOT") from exc
    return image_paths


def random_true(prob=0.05):
    return choices((True, False), (prob, 1 - prob))[0]


def gen_random_string(prefix, pattern="{prefix}_{random_str}", random_str_chars=string.ascii_letters, random_str_len=7):
    return pattern.format(prefix=prefix, random_str="".join(choices(random_str_chars, k=random_str_len)))


def gen_version_num(length=3):
    return ".".join([str(randint(0, 9)) for _ in range(length)])


def random_bump(version_num):
    nums = [int(num) for num in version_num.split(".")]
    nums[randint(0, len(nums) - 1)] += randint(1, 9)
    return ".".join([str(num) for num in nums])


def main(*, test_data_dir=DEFAULT_TEST_DATA_DIR, seed=DEFAULT_SEED, batch_size=DEFAULT_BATCH_SIZE,
         min_num_users_to_gen=DEFAULT_MIN_NUM_USERS_TO_GEN, max_num_users_to_gen=DEFAULT_MAX_NUM_USERS_TO_GEN,
         min_num_mods_to_gen=DEFAULT_MIN_NUM_MODS_TO_GEN, max_num_mods_to_gen=DEFAULT_MAX_NUM_MODS_TO_GEN,
         empty_fields_prob=DEFAULT_EMPTY_FIELDS_PROBABILITY,
         clear_tables=DEFAULT_CLEAR_TABLES, autocommit=DEFAULT_AUTOCOMMIT):
    random_empty = partial(random_true, empty_fields_prob)

    err_msg = "`test_data_dir` must match format MEDIA_ROOT/your_dir"
    try:
        if (Path(test_data_dir).parent != Path(settings.MEDIA_ROOT) and
                truncate_path_prefix_to_media_root(
                    Path(test_data_dir).resolve(), include=True).parent != Path(settings.MEDIA_ROOT)):
            raise ValueError(err_msg)
    except ValueError:
        raise ValueError(err_msg)

    if not autocommit:
        transaction.set_autocommit(False)

    if clear_tables:
        m.ModUserRating.objects.all().delete()
        m.ModUserComment.objects.all().delete()
        m.ModDownloadLink.objects.all().delete()
        m.ModVersion.objects.all().delete()
        m.Mod.objects.all().delete()
        m.ModImage.objects.all().delete()
        m.User.objects.filter(is_superuser=False).delete()
        m.UserProfile.objects.all().delete()
        m.Game.objects.all().delete()
        m.ModCategory.objects.all().delete()

    test_avatars = get_image_paths(test_data_dir, "avatars")
    test_mod_images = get_image_paths(test_data_dir, "mod_images")

    random.seed(seed)

    # Generate models.User & models.UserProfile
    users = []
    user_profiles = []
    for i in range(randint(min_num_users_to_gen, max_num_users_to_gen)):
        user = m.User(username=(username := gen_random_string("username")))
        user.set_password("password")
        users.append(user)
        user_profiles.append(m.UserProfile(user=user, avatar=None if not test_avatars else choice(test_avatars),
                                           description="" if random_empty() else f"description of user {username}"))
    m.User.objects.bulk_create(users, batch_size)
    m.UserProfile.objects.bulk_create(user_profiles, batch_size)

    # Generate models.Game
    games = []
    for i in range(NUM_GAMES):
        games.append(m.Game(name=(name := gen_random_string("game")),
                            description="" if random_empty() else f"description of game {name}"))
    m.Game.objects.bulk_create(games, batch_size)

    # Generate ModCategory
    mod_categories = []
    for i in range(NUM_MOD_CATEGORIES):
        mod_categories.append(m.ModCategory(name=(name := gen_random_string("category")),
                                            description="" if random_empty() else f"description of category {name}"))
    m.ModCategory.objects.bulk_create(mod_categories, batch_size)

    # Generate models.Mod
    mods = []
    for _ in range(randint(min_num_mods_to_gen, max_num_mods_to_gen)):
        mods.append(m.Mod(game=choice(games), author=choice(users), hidden=random_empty()))
    m.Mod.objects.bulk_create(mods, batch_size)

    # Choose categories (models.ModCategory) for models.Mod
    for mod in mods:
        mod.categories.set(sample(mod_categories,
                                  k=randint(MIN_NUM_MOD_CATEGORIES, min(MAX_NUM_MODS_CATEGORIES, len(mod_categories)))))

    # Generate other models.* related to models.Mod
    for mod in mods:
        # Generate models.ModVersion
        mod_versions = []
        for i in range(randint(MIN_NUM_MOD_VERSIONS, MAX_NUM_MOD_VERSIONS)):
            hidden = random_empty()
            prefix = "hidden " if hidden else ""
            mod_versions.append(
                m.ModVersion(mod=mod, title=f"title of {prefix}mod_version{i + 1} of mod_{mod.pk}",
                             short_description="" if random_empty() else f"short_description of mod_version{i + 1}",
                             full_description="" if random_empty() else f"full_description of mod_version{i + 1}",
                             number=gen_version_num() if not mod_versions else random_bump(mod_versions[-1].number),
                             comment="" if random_empty() else f"comment of {prefix}mod_version{i + 1}",
                             hidden=hidden))
        if not mod_versions:
            raise ValueError("mod must has at least one version")
        m.ModVersion.objects.bulk_create(mod_versions, batch_size)

        # Generate models.ModUserComment
        mod_user_comments = []
        for i in range(randint(MIN_NUM_USER_COMMENTS, MAX_NUM_USER_COMMENTS)):
            user = choice(users)
            mod_version = choice(mod.versions.all())
            text = ("" if random_empty() else
                    f"text of comment of user_{user.pk} on mod_version_{mod_version.pk} of mod_{mod.pk}")
            mod_user_comments.append(
                m.ModUserComment(user=user, mod=mod, mod_version=mod_version, text=text, hidden=random_empty()))
        m.ModUserComment.objects.bulk_create(mod_user_comments)

        # Generate models.ModUserRating
        mod_user_ratings = []
        mod_user_ratings_uniq_user_mod = set()
        mod_rated_by_no_one = random_empty()
        if mod_rated_by_no_one:
            continue
        for i in range(randint(MIN_NUM_USER_RATINGS, MAX_NUM_USER_RATINGS)):
            tries_left = MAX_TRIES_TO_GEN_UNIQ_MOD_USER_RATING
            while tries_left > 0:
                user = choice(users)
                if (user, mod) not in mod_user_ratings_uniq_user_mod:
                    break
                tries_left -= 1
            else:
                break  # possibly, too few users and/or mods to generate given number of unique ratings
            mod_user_ratings_uniq_user_mod.add((user, mod))
            mod_user_ratings.append(m.ModUserRating(user=user, mod=mod, mod_version=choice(mod.versions.all()),
                                                    rating=choice(m.ModUserRating.PossibleRatingValues.values)))
        m.ModUserRating.objects.bulk_create(mod_user_ratings, batch_size)

        # Generate other models.* related to models.ModVersion
        prev_mod_version_images = []
        for mod_version in mod_versions:
            # Generate models.ModDownloadLink
            mod_version_downloads_links = []
            for i in range(randint(MIN_NUM_MOD_VERSION_DOWNLOAD_LINKS, MAX_NUM_MOD_VERSION_DOWNLOAD_LINKS)):
                mod_version_downloads_links.append(
                    m.ModDownloadLink(mod_version=mod_version,
                                      url=f"https://cdn.host.xy/mod_{mod.pk}_mod_version_{mod_version.pk}_link{i + 1}",
                                      comment="" if random_empty() else f"comment of download_link{i + 1}"))
            m.ModDownloadLink.objects.bulk_create(mod_version_downloads_links, batch_size)

            # Generate models.ModImage
            if not test_mod_images:
                continue

            mod_version_has_own_images = not prev_mod_version_images or random_empty()
            if not mod_version_has_own_images:
                mod_version.images.set(prev_mod_version_images)
                mod_version.main_image = None if random_empty() else choice(prev_mod_version_images)
                continue

            last_mod_version_images = []
            last_mod_version_images_to_create = []
            for image in prev_mod_version_images:
                delete_image = random_empty()
                if delete_image:
                    continue
                replace_image = random_empty()
                if replace_image:
                    image = m.ModImage(file=choice(test_mod_images))
                    last_mod_version_images.append(image)
                    last_mod_version_images_to_create.append(image)
                else:  # leave an image from a previous version
                    last_mod_version_images.append(image)
            if not last_mod_version_images:
                for path in choices(test_mod_images, k=randint(MIN_NUM_MOD_VERSION_IMAGES, MAX_NUM_MOD_VERSION_IMAGES)):
                    last_mod_version_images.append(m.ModImage(file=path))
                last_mod_version_images_to_create = last_mod_version_images
            m.ModImage.objects.bulk_create(last_mod_version_images_to_create, batch_size)

            mod_version.images.set(last_mod_version_images)
            mod_version.main_image = (
                None if random_empty() or not last_mod_version_images else choice(last_mod_version_images))

            prev_mod_version_images = last_mod_version_images

        m.ModVersion.objects.bulk_update(mod_versions, ("main_image",), batch_size)
        mod.showed_version = None if random_empty() else choice(mod_versions)

    m.Mod.objects.bulk_update(mods, ("showed_version",), batch_size)

    if not autocommit:
        transaction.commit()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Fill `default` database defined in Django settings file with randomly generated data.")
    parser.add_argument("--test_data_dir", type=str, default=DEFAULT_TEST_DATA_DIR,
                        help="directory that must contains both folders `avatars` & `mod_images` that contain images. "
                             "Must match format MEDIA_ROOT/your_dir where `MEDIA_ROOT` defined in Django settings file "
                             "(default: %(default)s)")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED,
                        help="seed value passed to random.seed() (default: %(default)s)")
    parser.add_argument("--batch_size", type=int, default=DEFAULT_BATCH_SIZE,
                        help="batch size to bulk creating table rows (default: %(default)s)")
    parser.add_argument("--min_num_users_to_gen", type=int, default=DEFAULT_MIN_NUM_USERS_TO_GEN,
                        help="first argument passed to random.randint() which used to choose how many users "
                             "to generate (default: %(default)s)")
    parser.add_argument("--max_num_users_to_gen", type=int, default=DEFAULT_MAX_NUM_USERS_TO_GEN,
                        help="second argument passed to random.randint() (default: %(default)s)")
    parser.add_argument("--min_num_mods_to_gen", type=int, default=DEFAULT_MIN_NUM_MODS_TO_GEN,
                        help="first argument passed to random.randint() which used to choose how many mods "
                             "to generate (default: %(default)s)")
    parser.add_argument("--max_num_mods_to_gen", type=int, default=DEFAULT_MAX_NUM_MODS_TO_GEN,
                        help="second argument passed to random.randint() (default: %(default)s)")
    parser.add_argument("--empty_fields_prob", type=int, default=DEFAULT_EMPTY_FIELDS_PROBABILITY,
                        help="probability of that some fields will be empty or hidden (default: %(default)s)")
    parser.add_argument("--clear_tables", const=True, default=False, action="store_const",
                        help="if presented, all previous table rows will be deleted")
    parser.add_argument("--autocommit", const=True, default=False, action="store_const",
                        help="if presented, autocommit will be used instead of atomic")
    args = parser.parse_args()

    main(**vars(args))
