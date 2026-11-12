from django.core.management.base import BaseCommand

from race.models import Passage

PASSAGES = [
    (1, "That's it, dishonor! Dishonor on your whole family! Dishonor on you, dishonor on your cow!"),
    (1, "Hello. My name is Inigo Montoya. You killed my father. Prepare to die."),
    (2, "Supreme executive power derives from a mandate from the masses, not from some farcical aquatic ceremony."),
    (2, "A Wizard is never late, Frodo Baggins. Nor is he early. He arrives precisely when he means to."),
    (3, "I'm a night-stalking, crime-fighting vigilante, and a heavy metal rapping machine. I don't feel anything emotionally, except for rage. 24/7, 365, at a million percent."),
]


class Command(BaseCommand):
    help = "Load sample typing passages"

    def handle(self, *args, **options):
        created = 0
        for difficulty, text in PASSAGES:
            _, was_created = Passage.objects.get_or_create(
                text=text, defaults={"difficulty": difficulty}
            )
            created += was_created
        self.stdout.write(self.style.SUCCESS(f"Added {created} passages"))