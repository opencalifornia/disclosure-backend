from django.test import TestCase

from locality.models import City, County, Locality, State


class LocalityTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(LocalityTest, cls).setUpClass()
        cls.state, _ = State.objects.get_or_create(name='California')
        cls.city, _ = City.objects.get_or_create(name='San Diego', state=cls.state)
        cls.county, _ = County.objects.get_or_create(name='San Diego', state=cls.state)


class LocalityStringTest(LocalityTest):
    def test_strings(self):
        """
        Smoke tests on str() and unicode()
        """
        for obj in [self.state, self.city, self.county]:
            cls = obj.__class__
            self.assertNotIn('Object', str(obj), cls.__name__)
            self.assertNotIn('Object', unicode(obj), cls.__name__)

            self.assertNotEqual('', str(obj), cls.__name__)
            self.assertNotEqual('', unicode(obj), cls.__name__)


class LocalityAliasTest(LocalityTest):
    def test_clean(self):
        self.city.aliases = 'my_alias, your_alias'
        self.city.save()
        self.assertNotIn(' ', self.city.aliases, "Remove spaces.")

        self.city.aliases = 'my_alias, my_alias'
        self.city.save()
        self.assertEqual('my_alias', self.city.aliases,
                         "Remove duplicates." + self.city.aliases)

        self.city.aliases = ','
        self.city.save()
        self.assertEqual(None, self.city.aliases,
                         "Convert empty list to None")

        self.city.aliases = ''
        self.city.save()
        self.assertEqual(None, self.city.aliases,
                         "Convert blank to None")

    def test_avoid_adding_city_with_alias(self):
        self.city.aliases = 'my_alias, your_alias'
        self.city.save()
        n_cities = City.objects.all().count()

        city = City(name='my_alias')
        self.assertRaises(Exception, city.save,
                          "Don't allow 'save' on city with aliased name")
        self.assertEqual(n_cities, City.objects.all().count(),
                         "# of cities does not change.")

    def test_get_alias(self):
        self.city.aliases = 'my_alias, your_alias'
        self.city.save()

        city = City.aliased_objects.get(name='my_alias')
        self.assertEqual(city.name, self.city.name)
        self.assertNotEqual(city.name, 'my_alias')

    def test_set_alias_None(self):
        self.city.aliases = 'my_alias, your_alias'
        self.city.save()

        self.city.aliases = None
        self.city.save()

    def test_merge_on_alias(self):
        self.city.aliases = None
        self.city.save()

        city = City(name='my_alias', state=State.objects.all()[0])
        city.save()
        n_cities = City.objects.all().count()

        # Should merge
        self.city.aliases = 'my_alias'
        self.city.save()

        # No city named 'my_alias'
        self.assertRaises(City.DoesNotExist, City.objects.get, name='my_alias'),
        self.assertEqual(n_cities - 1, City.objects.all().count(),
                         "Saving with alias should merge city info.")

    def test_merge_flipped(self):
        self.city.aliases = 'a1,a2,a3'
        self.city.save()

        # New city, no alias.
        city = City(name='new_city', state=State.objects.all()[0])
        city.save()

        # New city, add alias to existing city.
        city.aliases = self.city.name
        city.save()

        # Should delete the city.
        self.assertRaises(City.DoesNotExist, City.objects.get, id=city.id)
        self.assertIn('new_city', City.objects.get(id=self.city.id).aliases.split(','),
                      "New city should have alias of saved city.")


class LocalityAliasManagerTest(LocalityTest):
    def test_not_found(self):
        self.assertRaises(Locality.DoesNotExist, Locality.aliased_objects.get,
                          name='xxxxxxxx')

    def test_not_implemented(self):
        self.assertRaises(NotImplementedError, Locality.aliased_objects.get,
                          name__iequals='xxxxxxxx')
