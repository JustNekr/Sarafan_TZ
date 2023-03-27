from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from categories.models import Category
from product.models import Product


class Command(BaseCommand):
    # help = 'Closes the specified poll for voting'
    #
    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        username = 'nekr'
        password = '123'
        if User.objects.filter(username=username).exists():
            print('Superuser creation skipped.')
        else:
            User.objects.create_superuser(username=username, password=password)
            print('Superuser created.')

        for cat_count in range(10):
            category, created = Category.objects.get_or_create(
                name=f'Category_{cat_count}', slug=slugify(f'Category_{cat_count}')
            )
            for subcat_counb in range(5):
                subcategory, created = Category.objects.get_or_create(
                    name=f'Subcategory_{subcat_counb}',
                    slug=slugify(f'{category.name}_Subcategory_{subcat_counb}'),
                    parent=category
                )
                for product_count in range(5):
                    product, created = Product.objects.get_or_create(
                        name=f'Product_{product_count}',
                        slug=slugify(f'{subcategory.slug}_Product{product_count}'),
                        sub_category=subcategory,
                        price=product_count * 1000
                    )
        # for poll_id in options['poll_ids']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)
        #
        #     poll.opened = False
        #     poll.save()
        #
        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))