from django.core.management.base import BaseCommand
from conteneurs.models import Emplacement

class Command(BaseCommand):
    help = "Génère automatiquement tous les emplacements du parc (zones AA à AD, rangées A à G, positions 01 à 57 impaires)"

    def handle(self, *args, **kwargs):
        zones = ['AA', 'AB', 'AC', 'AD']
        rangees = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        positions = range(1, 58, 2)  # 1, 3, 5, ..., 57

        total_crees = 0
        for zone in zones:
            for rangee in rangees:
                for position in positions:
                    emplacement, cree = Emplacement.objects.get_or_create(
                        zone=zone,
                        rangee=rangee,
                        position=position
                    )
                    if cree:
                        total_crees += 1

        self.stdout.write(self.style.SUCCESS(
            f"{total_crees} emplacements créés avec succès."
        ))