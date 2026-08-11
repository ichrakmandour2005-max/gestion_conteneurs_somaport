from django.db import transaction
from .models import Emplacement

NIVEAUX = "ABCDEFG"  # A = niveau 1 (sol), G = niveau 7 (sommet)


class AucunEmplacementDisponible(Exception):
    pass


class ConteneurBloque(Exception):
    """Levée quand on essaie de retirer un conteneur qui a autre chose empilé dessus."""
    pass


def _prochain_niveau_libre(zone, position):
    """Renvoie la lettre du niveau où poser un conteneur sur cette colonne (zone+position),
    ou None si la colonne est pleine ou si le sommet est un conteneur vide."""
    occupes = list(
        Emplacement.objects
        .filter(zone=zone, position=position)
        .exclude(conteneur=None)
        .select_related('conteneur')
        .order_by('rangee')
    )
    nombre = len(occupes)
    if nombre >= len(NIVEAUX):
        return None
    if nombre > 0 and occupes[-1].conteneur.etat == 'vide':
        return None
    return NIVEAUX[nombre]


def _support_valide_pour_40(zone, position, position_suivante, niveau):
    """Vérifie qu'un conteneur 40 pieds peut reposer à ce niveau : au sol (niveau A),
    ou sur un même conteneur de 40 pieds occupant déjà les deux colonnes en dessous."""
    index = NIVEAUX.index(niveau)
    if index == 0:
        return True  # niveau A : au sol, aucun support requis

    niveau_dessous = NIVEAUX[index - 1]
    e1 = Emplacement.objects.filter(zone=zone, position=position, rangee=niveau_dessous).select_related('conteneur').first()
    e2 = Emplacement.objects.filter(zone=zone, position=position_suivante, rangee=niveau_dessous).select_related('conteneur').first()

    if not e1 or not e1.conteneur or not e2 or not e2.conteneur:
        return False

    return e1.conteneur.taille == '40' and e1.conteneur_id == e2.conteneur_id


def _peut_retirer(emplacements):
    """Vérifie qu'aucun conteneur n'est empilé au-dessus des emplacements donnés."""
    for e in emplacements:
        index = NIVEAUX.index(e.rangee)
        niveaux_au_dessus = NIVEAUX[index + 1:]
        if niveaux_au_dessus and Emplacement.objects.filter(
            zone=e.zone, position=e.position, rangee__in=niveaux_au_dessus
        ).exclude(conteneur=None).exists():
            return False
    return True


def _chercher_place_dans_zone(conteneur, zone):
    positions = list(
        Emplacement.objects.filter(zone=zone)
        .values_list('position', flat=True).distinct().order_by('position')
    )

    if conteneur.taille == '20':
        for position in positions:
            niveau = _prochain_niveau_libre(zone, position)
            if niveau:
                emplacement = Emplacement.objects.select_for_update().get(
                    zone=zone, position=position, rangee=niveau
                )
                emplacement.conteneur = conteneur
                emplacement.save()
                return [emplacement]
        return None

    elif conteneur.taille == '40':
        for position in positions:
            position_suivante = position + 2
            if position_suivante not in positions:
                continue
            niveau1 = _prochain_niveau_libre(zone, position)
            niveau2 = _prochain_niveau_libre(zone, position_suivante)
            if niveau1 and niveau1 == niveau2 and _support_valide_pour_40(zone, position, position_suivante, niveau1):
                e1 = Emplacement.objects.select_for_update().get(
                    zone=zone, position=position, rangee=niveau1
                )
                e2 = Emplacement.objects.select_for_update().get(
                    zone=zone, position=position_suivante, rangee=niveau1
                )
                e1.conteneur = conteneur
                e2.conteneur = conteneur
                e1.save()
                e2.save()
                return [e1, e2]
        return None

    else:
        raise ValueError("Taille de conteneur invalide (doit être '20' ou '40').")


@transaction.atomic
def placer_conteneur(conteneur):
    zones = ['AA', 'AB', 'AC', 'AD']
    for zone in zones:
        resultat = _chercher_place_dans_zone(conteneur, zone)
        if resultat:
            return resultat
    raise AucunEmplacementDisponible(
        "Aucun emplacement libre dans tout le parc pour ce conteneur."
    )


@transaction.atomic
def liberer_emplacements(conteneur):
    """Libère les emplacements d'un conteneur, en vérifiant qu'aucun autre conteneur n'est empilé dessus."""
    emplacements = list(conteneur.emplacements.select_for_update())
    if not _peut_retirer(emplacements):
        raise ConteneurBloque(
            "Impossible de retirer ce conteneur : un autre conteneur est empilé au-dessus. "
            "Retirez d'abord le(s) conteneur(s) du dessus."
        )
    conteneur.emplacements.update(conteneur=None)


@transaction.atomic
def transferer_interne(conteneur, nouvelle_zone):
    resultat = _chercher_place_dans_zone(conteneur, nouvelle_zone)
    if not resultat:
        raise AucunEmplacementDisponible(
            f"Aucun emplacement libre dans la zone {nouvelle_zone}."
        )

    nouveaux_ids = [e.id for e in resultat]
    anciens = list(conteneur.emplacements.exclude(id__in=nouveaux_ids).select_for_update())
    if not _peut_retirer(anciens):
        # on annule le nouveau placement puisqu'on ne peut pas libérer l'ancien
        Emplacement.objects.filter(id__in=nouveaux_ids).update(conteneur=None)
        raise ConteneurBloque(
            "Impossible de transférer ce conteneur : un autre conteneur est empilé au-dessus de son emplacement actuel."
        )

    Emplacement.objects.filter(id__in=[e.id for e in anciens]).update(conteneur=None)
    conteneur.statut = 'transfert'
    conteneur.save()
    return resultat


@transaction.atomic
def transferer_externe(conteneur):
    liberer_emplacements(conteneur)
    conteneur.statut = 'transfert_externe'
    conteneur.save()