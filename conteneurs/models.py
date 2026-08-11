from django.db import models
from django.core.validators import RegexValidator

# Validateur pour le nom du conteneur : 4 lettres majuscules + 7 chiffres (norme ISO 6346)
nom_conteneur_validator = RegexValidator(
    regex=r'^[A-Z]{4}\d{7}$',
    message="Le nom du conteneur doit contenir exactement 4 lettres majuscules suivies de 7 chiffres (ex: MSCU1234567)."
)


class Conteneur(models.Model):

    TAILLE_CHOICES = [
        ('20', "20 pieds"),
        ('40', "40 pieds"),
    ]

    ETAT_CHOICES = [
        ('plein', "Plein"),
        ('vide', "Vide"),
    ]

    STATUT_CHOICES = [
        ('entree', "Entrée"),
        ('transfert', "En transfert"),
        ('transfert_externe', "Transfert externe"),
        ('sortie_terrestre', "Sortie terrestre"),
        ('sortie_maritime', "Sortie maritime"),
    ]

    nom = models.CharField(
        max_length=11,
        unique=True,
        validators=[nom_conteneur_validator],
        help_text="4 lettres + 7 chiffres, ex: MSCU1234567"
    )
    taille = models.CharField(max_length=2, choices=TAILLE_CHOICES)
    etat = models.CharField(max_length=5, choices=ETAT_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='entree')

    date_entree = models.DateTimeField(auto_now_add=True)
    date_sortie = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nom

    def code_emplacement(self):
        """Code d'affichage : position unique pour 20 pieds, position paire médiane pour 40 pieds."""
        emplacements = list(self.emplacements.order_by('position'))
        if not emplacements:
            return "—"
        if self.taille == '20' or len(emplacements) == 1:
            return emplacements[0].code
        e1, e2 = emplacements[0], emplacements[1]
        position_moyenne = (e1.position + e2.position) // 2
        return f"{e1.zone}{position_moyenne:02d}{e1.rangee}"


class Emplacement(models.Model):

    RANGEE_CHOICES = [(l, l) for l in "ABCDEFG"]

    zone = models.CharField(max_length=2)  # ex: "AA", "AB", "AC", "AD"
    rangee = models.CharField(max_length=1, choices=RANGEE_CHOICES)  # ex: "A" à "G"
    position = models.PositiveIntegerField()  # ex: 1, 3, 5, ... 57 (numéros impairs)

    conteneur = models.ForeignKey(
        Conteneur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='emplacements'
    )

    class Meta:
        unique_together = ('zone', 'rangee', 'position')
        ordering = ['zone', 'rangee', 'position']

    @property
    def code(self):
        """Ex: AA01A, AB03G... (zone + position + rangée, unique)"""
        return f"{self.zone}{self.position:02d}{self.rangee}"

    @property
    def est_occupe(self):
        return self.conteneur is not None

    def __str__(self):
        return f"{self.code} ({'Occupé' if self.est_occupe else 'Libre'})"