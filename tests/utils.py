from faker import Faker
from faker_web import WebProvider

fake = Faker()
fake.add_provider(WebProvider)
