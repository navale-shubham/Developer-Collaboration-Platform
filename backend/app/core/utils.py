from slugify import slugify
import uuid


def generate_slug(text: str):
    return f'{slugify(text)}-{uuid.uuid4()}'