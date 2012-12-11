# -=- encoding: utf-8 -=-

from django.conf import settings
from django.db import models

MANAGED = getattr(settings, 'AUF_REFERENCES_MANAGED', False)


### Gestion des actifs/inactifs

class ActifsManager(models.Manager):
    """
    Manager pour ``ActifsModel``.
    """

    def get_query_set(self):
        return super(ActifsManager, self).get_query_set().filter(actif=True)


class ActifsModel(models.Model):
    """
    Modèle faisant la gestion des objets actifs/inactifs.

    Le manager par défaut ne liste que les objets actifs. Pour avoir tous
    les objets, utiliser le manager ``avec_inactifs``.
    """
    actif = models.BooleanField(default=True, editable=False)

    # Managers
    objects = ActifsManager()
    avec_inactifs = models.Manager()

    class Meta:
        abstract = True


### Modèles pour les données de référence

class Employe(ActifsModel):
    """
    Personne en contrat d'employé (CDD ou CDI) à l'AUF
    """
    GENRE_CHOICES = (
        (u'h', u'Homme'),
        (u'f', u'Femme'),
    )

    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    implantation = models.ForeignKey(
        'references.Implantation',
        db_column='implantation',
        related_name='lieu_travail_theorique_de'
    )
    implantation_physique = models.ForeignKey(
        'references.Implantation',
        db_column='implantation_physique',
        related_name='lieu_travail_reel_de'
    )
    courriel = models.CharField(max_length=255, null=True, blank=True)
    genre = models.CharField(max_length=3, choices=GENRE_CHOICES)
    fonction = models.CharField(max_length=255, null=True, blank=True)
    telephone_poste = models.CharField(max_length=255, blank=True)
    telephone_ip = models.CharField(max_length=255, blank=True)
    telephone_ip_nomade = models.CharField(max_length=255, blank=True)
    responsable = models.ForeignKey(
        'references.Employe',
        db_column='responsable',
        related_name='responsable_de',
        null=True, blank=True
    )
    mandat_debut = models.DateField(null=True, blank=True)
    mandat_fin = models.DateField(null=True, blank=True)
    date_entree = models.DateField(null=True, blank=True)
    service = models.ForeignKey('references.Service', db_column='service')
    poste_type_1 = models.ForeignKey(
        'references.PosteType',
        null=True, blank=True,
        db_column='poste_type_1',
        related_name='poste_type_1'
    )
    poste_type_2 = models.ForeignKey(
        'references.PosteType',
        null=True, blank=True,
        db_column='poste_type_2',
        related_name='poste_type_2'
    )

    class Meta:
        db_table = u'ref_employe'
        ordering = ['nom']
        managed = MANAGED

    def __unicode__(self):
        return u"%s, %s" % (self.nom, self.prenom)


class Authentification(ActifsModel):
    """
    Authentification
    """
    id = models.ForeignKey(
        'references.Employe', primary_key=True, db_column='id'
    )
    courriel = models.CharField(max_length=255, unique=True)
    motdepasse = models.CharField(max_length=255)

    class Meta:
        db_table = u'ref_authentification'
        ordering = ['id']
        managed = MANAGED

    def __unicode__(self):
        return self.courriel


class Service(ActifsModel):
    """
    Services (donnée de référence, source: SGRH).
    """
    nom = models.CharField(max_length=255)

    class Meta:
        db_table = u'ref_service'
        ordering = ['nom']
        managed = MANAGED

    def __unicode__(self):
        return self.nom


class PosteType(ActifsModel):
    """
    Postes types (donnée de référence, source: SGRH).
    """
    nom = models.CharField(max_length=255)

    class Meta:
        db_table = u'ref_poste_type'
        managed = MANAGED

    def __unicode__(self):
        return self.nom


class GroupeArh(ActifsModel):
    employe = models.ForeignKey('references.Employe', db_column='employe')

    class Meta:
        db_table = u'ref_groupe_arh'
        managed = MANAGED


class GroupeDirRegion(ActifsModel):
    employe = models.ForeignKey('references.Employe', db_column='employe')
    region = models.ForeignKey('references.Region', db_column='region')

    class Meta:
        db_table = u'ref_groupe_dir_region'
        managed = MANAGED


class GroupeAdmRegion(ActifsModel):
    employe = models.ForeignKey('references.Employe', db_column='employe')
    region = models.ForeignKey('references.Region', db_column='region')

    class Meta:
        db_table = u'ref_groupe_adm_region'
        managed = MANAGED


class GroupeRespImplantation(ActifsModel):
    employe = models.ForeignKey('references.Employe', db_column='employe')
    implantation = models.ForeignKey(
        'references.Implantation', db_column='implantation'
    )
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = u'ref_groupe_resp_implantation'
        managed = MANAGED


class GroupeDirProgramme(ActifsModel):
    employe = models.ForeignKey('references.Employe', db_column='employe')
    service = models.ForeignKey('references.Service', db_column='service')

    class Meta:
        db_table = u'ref_groupe_dir_programme'
        managed = MANAGED


class GroupeDirDelegProgrammeReg(ActifsModel):
    employe = models.ForeignKey('references.Employe', db_column='employe')
    region = models.ForeignKey('references.Region', db_column='region')

    class Meta:
        db_table = u'ref_groupe_dir_deleg_programme_reg'
        managed = MANAGED


class GroupeComptable(ActifsModel):
    employe = models.ForeignKey('references.Employe', db_column='employe')

    class Meta:
        db_table = u'ref_groupe_comptable'
        managed = MANAGED


class GroupeComptableRegional(ActifsModel):
    employe = models.ForeignKey('references.Employe', db_column='employe')

    class Meta:
        db_table = u'ref_groupe_comptable_regional'
        managed = MANAGED


class GroupeComptableLocal(ActifsModel):
    employe = models.ForeignKey('references.Employe', db_column='employe')

    class Meta:
        db_table = u'ref_groupe_comptable_local'
        managed = MANAGED


class Discipline(ActifsModel):
    """
    ATTENTION: DÉSUET
    Discipline (donnée de référence, source: SQI).
    Une discipline est une catégorie de savoirs scientifiques.
    Le conseil scientifique fixe la liste des disciplines.
    """
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255)
    nom_long = models.CharField(max_length=255, blank=True)
    nom_court = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = u'ref_discipline'
        ordering = ['nom']
        managed = MANAGED

    def __unicode__(self):
        return self.nom


class Programme(ActifsModel):
    """
    ATTENTION: DÉSUET
    Programme (donnée de référence, source: SQI).
    Structure interne par laquelle l'AUF exécute ses projets et activités,
    dispense ses produits et ses services.
    """
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255)
    nom_long = models.CharField(max_length=255, blank=True)
    nom_court = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = u'ref_programme'
        managed = MANAGED

    def __unicode__(self):
        return self.nom


#PROGRAMMATION QUADRIENNALLE

class Projet(ActifsModel):
    """
    Projet (donnée de référence, source: programmation-quadriennalle).
    """
    SERVICE_CHOICES = (
        (u'1',
         u"Direction de la langue et de la communication scientifique "
         u"en français"),
        (u'2', u"Direction du développement et de la valorisation"),
        (u'3',
         u"Direction de l'innovation pédagogique et de l'économie "
         u"de la connaissance"),
        (u'4', u"Direction du renforcement des capacités scientifiques"),
    )

    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255)
    presentation = models.TextField(null=True, blank=True)
    partenaires = models.TextField(null=True, blank=True)
    service = models.CharField(
        max_length=255, choices=SERVICE_CHOICES, blank=True, null=True
    )
    objectif_specifique = models.ForeignKey(
        'references.ObjectifSpecifique',
        blank=True, null=True,
        db_column='objectif_specifique'
    )
    implantation = models.ForeignKey('references.Implantation', null=True,
                                     blank=True, db_column='implantation')
    etablissement = models.ForeignKey('references.Etablissement', null=True,
                                      blank=True, db_column='etablissement')
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)

    class Meta:
        db_table = u'ref_projet'
        ordering = ['nom']
        managed = MANAGED

    def __unicode__(self):
        return "%s - %s" % (self.code, self.nom)


class ProjetComposante(ActifsModel):
    """
    Composantes des projets (source: programmation-quadriennalle)
    """
    code = models.CharField(max_length=10)
    nom = models.CharField(max_length=255)
    nom_court = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    projet = models.ForeignKey('references.Projet', db_column='projet')

    class Meta:
        db_table = u'ref_projet_composante'
        ordering = ['nom']
        managed = MANAGED

    def __unicode__(self):
        return "%s - %s" % (self.code, self.nom)


class UniteProjet(ActifsModel):
    """
    Unités de projet (source: programmation-quadriennalle)
    """
    code = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=255)

    class Meta:
        db_table = u'ref_unite_projet'
        ordering = ['nom']
        managed = MANAGED

    def __unicode__(self):
        return "%s - %s" % (self.code, self.nom)


class ObjectifSpecifique(ActifsModel):
    nom = models.CharField(max_length=255)
    objectif_strategique = models.ForeignKey(
        'references.ObjectifStrategique', db_column='objectif_strategique'
    )

    class Meta:
        db_table = u'ref_objectif_specifique'
        ordering = ['nom']
        managed = MANAGED

    def __unicode__(self):
        return "%s - %s" % (self.id, self.nom)


class ObjectifStrategique(ActifsModel):
    nom = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = u'ref_objectif_strategique'
        ordering = ['nom']
        managed = MANAGED

    def __unicode__(self):
        return "%s - %s" % (self.id, self.nom)


class Thematique(ActifsModel):
    nom = models.CharField(max_length=255)

    class Meta:
        db_table = u'ref_thematique'
        ordering = ['nom']
        managed = MANAGED

    def __unicode__(self):
        return "%s - %s" % (self.id, self.nom)


class ProjetUp(ActifsModel):
    """
    Projet-unité de projet (source: coda)
    => codes budgétaires
    """
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255)
    nom_court = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = MANAGED


class Poste(ActifsModel):
    """
    ATTENTION: DÉSUET
    Poste (donnée de référence, source: CODA).
    Un poste est une catégorie destinée à venir raffiner un projet.
    """
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = u'ref_poste'
        managed = MANAGED

    def __unicode__(self):
        return "%s - %s (%s)" % (self.code, self.nom, self.type)


class ProjetPoste(ActifsModel):
    """
    ATTENTION: DÉSUET
    Projet-poste (donnée de référence, source: CODA).
    Un projet-poste consiste en une raffinement d'un projet par un poste
    (budgétaire).  Subdivision utile pour le suivi budgétaire et comptable.
    """
    code = models.CharField(max_length=255, unique=True)
    code_projet = models.ForeignKey(
        'references.Projet', to_field='code', db_column='code_projet'
    )
    code_poste = models.ForeignKey(
        'references.Poste', to_field='code', db_column='code_poste'
    )
    code_bureau = models.ForeignKey(
        'references.Bureau', to_field='code', db_column='code_bureau'
    )
    code_programme = models.ForeignKey(
        'references.Programme', to_field='code', db_column='code_programme'
    )

    class Meta:
        db_table = u'ref_projet_poste'
        managed = MANAGED

    def __unicode__(self):
        return self.code


class Region(ActifsModel):
    """
    Région (donnée de référence, source: referentiels_spip).
    Une région est une subdivision géographique du monde pour la gestion de
    l'AUF.
    """
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255, db_index=True)
    implantation_bureau = models.ForeignKey(
        'references.Implantation', db_column='implantation_bureau',
        related_name='gere_region', null=True, blank=True
    )

    class Meta:
        db_table = u'ref_region'
        ordering = ['nom']
        verbose_name = u"région"
        verbose_name_plural = u"régions"
        managed = MANAGED

    def __unicode__(self):
        return self.nom


class ZoneAdministrative(ActifsModel):
    """
    Les implantations sont classées par zone administrative pour fins de
    ressources humaines et de comptabilité. Pour les implantations
    régionales, la zone administrative est équivalente à la région. Pour les
    services centraux, la zone administrative est soit "Services centraux
    Montréal" ou "Services centraux Paris".
    """
    code = models.CharField(max_length=4, primary_key=True)
    nom = models.CharField(max_length=100)

    class Meta:
        db_table = 'ref_zoneadministrative'
        ordering = ['nom']
        verbose_name = u'zone administrative'
        verbose_name_plural = u'zones administratives'
        managed = MANAGED

    def __unicode__(self):
        return self.nom


class Bureau(ActifsModel):
    """
    Bureau (donnée de référence, source: SQI).

    Référence legacy entre la notion de région et celle d'implantation
    responsable des régions et du central.

    Un bureau est :
    - soit le bureau régional d'une région (implantations de type 'Bureau')
    - soit la notion unique de Service central pour les 2 implantations
      centrales (implantations de type 'Service central' et 'Siege').

    Ne pas confondre avec les seuls 'bureaux régionaux'.
    """
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255)
    nom_court = models.CharField(max_length=255, blank=True)
    nom_long = models.CharField(max_length=255, blank=True)
    implantation = models.ForeignKey(
        'references.Implantation', db_column='implantation'
    )
    region = models.ForeignKey('references.Region', db_column='region')

    class Meta:
        db_table = u'ref_bureau'
        ordering = ['nom']
        verbose_name = u"bureau"
        verbose_name_plural = u"bureaux"
        managed = MANAGED

    def __unicode__(self):
        return self.nom


class Implantation(ActifsModel):
    """
    Implantation (donnée de référence, source: Implantus)

    Une implantation est un endroit où l'AUF est présente et offre des
    services spécifiques. Deux implantations peuvent être au même endroit
    physique.
    """
    STATUT_CHOICES = (
        (0, u'Fermée ou jamais ouverte'),
        (1, u'Ouverte'),
        (2, u'Ouverture imminente'),
        (3, u'En projet')
    )

    nom = models.CharField(max_length=255)
    nom_court = models.CharField(max_length=255, blank=True)
    nom_long = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255)
    bureau_rattachement = models.ForeignKey(
        'references.Implantation', db_column='bureau_rattachement'
    )
    region = models.ForeignKey('references.Region', db_column='region')
    zone_administrative = models.ForeignKey('references.ZoneAdministrative')
    fuseau_horaire = models.CharField(max_length=255, blank=True)
    code_meteo = models.CharField(max_length=255, blank=True)
    # responsable
    responsable_implantation = models.IntegerField(null=True, blank=True)
    # adresse postale
    adresse_postale_precision_avant = models.CharField(
        max_length=255, blank=True, null=True
    )
    adresse_postale_no = models.CharField(max_length=30, blank=True, null=True)
    adresse_postale_rue = models.CharField(
        max_length=255, blank=True, null=True
    )
    adresse_postale_bureau = models.CharField(
        max_length=255, blank=True, null=True
    )
    adresse_postale_precision = models.CharField(
        max_length=255, blank=True, null=True
    )
    adresse_postale_boite_postale = models.CharField(
        max_length=255, blank=True, null=True
    )
    adresse_postale_ville = models.CharField(max_length=255)
    adresse_postale_code_postal = models.CharField(
        max_length=20, blank=True, null=True
    )
    adresse_postale_code_postal_avant_ville = models.NullBooleanField()
    adresse_postale_region = models.CharField(
        max_length=255, blank=True, null=True
    )
    adresse_postale_pays = models.ForeignKey(
        'references.Pays', to_field='code',
        db_column='adresse_postale_pays',
        related_name='impl_adresse_postale'
    )
    # adresse physique
    adresse_physique_precision_avant = models.CharField(
        max_length=255, blank=True
    )
    adresse_physique_no = models.CharField(max_length=30, blank=True)
    adresse_physique_rue = models.CharField(max_length=255, blank=True)
    adresse_physique_bureau = models.CharField(max_length=255, blank=True)
    adresse_physique_precision = models.CharField(max_length=255, blank=True)
    adresse_physique_ville = models.CharField(max_length=255)
    adresse_physique_code_postal = models.CharField(max_length=30, blank=True)
    adresse_physique_code_postal_avant_ville = models.NullBooleanField()
    adresse_physique_region = models.CharField(max_length=255, blank=True)
    adresse_physique_pays = models.ForeignKey(
        'references.Pays', to_field='code',
        db_column='adresse_physique_pays',
        related_name='impl_adresse_physique'
    )
    # autres coordonnées
    telephone = models.CharField(max_length=255, blank=True)
    telephone_interne = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    fax_interne = models.CharField(max_length=255, blank=True)
    courriel = models.EmailField(blank=True)
    courriel_interne = models.EmailField(blank=True)
    url = models.URLField(verify_exists=False, max_length=255, blank=True)
    # traitement
    statut = models.IntegerField(choices=STATUT_CHOICES)
    date_ouverture = models.DateField(null=True, blank=True)
    date_inauguration = models.DateField(null=True, blank=True)
    date_extension = models.DateField(null=True, blank=True)
    date_fermeture = models.DateField(null=True, blank=True)
    hebergement_etablissement = models.CharField(max_length=255, blank=True)
    hebergement_convention = models.NullBooleanField()
    hebergement_convention_date = models.DateField(null=True, blank=True)
    remarque = models.TextField()
    commentaire = models.CharField(max_length=255, blank=True)
    # meta
    modif_date = models.DateField()

    class Managers:

        class Ouvertes(ActifsManager):

            def get_query_set(self):
                return super(Implantation.Managers.Ouvertes, self) \
                        .get_query_set() \
                        .filter(statut=1)

    objects = ActifsManager()
    ouvertes = Managers.Ouvertes()

    class Meta:
        db_table = u'ref_implantation'
        ordering = ['nom']
        managed = MANAGED

    def __unicode__(self):
        return self.nom


class Pays(ActifsModel):
    """
    Pays (donnée de référence, source: SQI).

    Liste AUF basée sur la liste ISO-3166-1.
    """
    NORD_SUD_CHOICES = (
        (u'Nord', u'Nord'),
        (u'Sud', u'Sud'),
    )
    DEVELOPPEMENT_CHOICES = (
        (u'Elevé', u'Elevé'),
        (u'Faible', u'Faible'),
        (u'Intermédiaire', u'Intermédiaire'),
        (u'inconnu', u'Inconnu'),
    )

    code = models.CharField(max_length=2, unique=True)
    code_iso3 = models.CharField(max_length=3, unique=True)
    nom = models.CharField(max_length=255)
    region = models.ForeignKey('references.Region', db_column='region')
    code_bureau = models.ForeignKey('references.Bureau', to_field='code',
                                    db_column='code_bureau', blank=True,
                                    null=True)
    nord_sud = models.CharField(
        max_length=255, blank=True, null=True,
    )
    developpement = models.CharField(max_length=255, blank=True, null=True)
    monnaie = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = u'ref_pays'
        ordering = ['nom']
        verbose_name = u"pays"
        verbose_name_plural = u"pays"
        managed = MANAGED

    def __unicode__(self):
        return self.nom


class _Etablissement(ActifsModel):
    """
    Superclasse pour les modèles ``Etablissement`` et ``EtablissementBase``
    """
    STATUT_CHOICES = (
        ('T', 'Titulaire'),
        ('A', 'Associé'),
        ('C', 'Candidat'),
    )
    QUALITE_CHOICES = (
        ('ESR', "Établissement d'enseignement supérieur et de recherche"),
        ('CIR', "Centre ou institution de recherche"),
        ('RES', "Réseau"),
    )

    # Infos de base
    nom = models.CharField(max_length=255)
    sigle = models.CharField(max_length=16, blank=True)
    pays = models.ForeignKey(
        'references.Pays', to_field='code', db_column='pays',
        related_name='+'
    )
    region = models.ForeignKey(
        'references.Region', db_column='region', blank=True, null=True,
        related_name='+', verbose_name='région'
    )
    implantation = models.ForeignKey(
        'references.Implantation', db_column='implantation',
        related_name='+', blank=True, null=True
    )
    description = models.TextField(blank=True)
    historique = models.TextField(blank=True)

    # Membership
    membre = models.BooleanField()
    membre_adhesion_date = models.DateField(
        u"date d'adhésion", null=True, blank=True
    )
    statut = models.CharField(
        max_length=1, choices=STATUT_CHOICES, blank=True, null=True
    )
    qualite = models.CharField(
        u'qualité', max_length=3, choices=QUALITE_CHOICES, blank=True,
        null=True
    )

    # Responsable
    responsable_genre = models.CharField(u'genre', max_length=1, blank=True)
    responsable_nom = models.CharField(u'nom', max_length=255, blank=True)
    responsable_prenom = models.CharField(
        u'prénom', max_length=255, blank=True
    )
    responsable_fonction = models.CharField(
        u'fonction', max_length=255, blank=True
    )
    responsable_courriel = models.EmailField(u'courriel', blank=True)

    # Adresse
    adresse = models.CharField(max_length=255, blank=True)
    code_postal = models.CharField(u'code postal', max_length=20, blank=True)
    cedex = models.CharField(u'CEDEX', max_length=20, blank=True)
    ville = models.CharField(max_length=255, blank=True)
    province = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(u'téléphone', max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    url = models.URLField(
        u'URL', verify_exists=False, max_length=255, blank=True
    )

    # Meta-données
    date_modification = models.DateField(
        u'date de modification', blank=True, null=True
    )
    commentaire = models.TextField(blank=True)

    class Meta:
        abstract = True
        ordering = ['pays__nom', 'nom']
        managed = MANAGED

    def __unicode__(self):
        return "%s - %s" % (self.pays.nom, self.nom)


class Etablissement(_Etablissement):
    """
    Établissement (donnée de référence, source: GDE).

    Un établissement peut être une université, un centre de recherche, un
    réseau d'établissement... Un établissement peut être membre de l'AUF ou
    non.
    """
    class Meta(_Etablissement.Meta):
        db_table = u'ref_etablissement'
        managed = MANAGED


class EtablissementBase(_Etablissement):
    """
    Modèle de base pour créer des établissements locaux pouvant être
    liés à des établissements des données de référence.
    """
    ref = models.OneToOneField(Etablissement, blank=True, null=True,
                               related_name='%(app_label)s_%(class)s')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.ref and not self.pk:
            # Nouvel établissement faisant référence à un établissement dans
            # les références. On copie tous les champs.
            for f in self.ref._meta.fields:
                if f.attname != 'id':
                    setattr(self, f.attname, getattr(self.ref, f.attname))
        super(EtablissementBase, self).save(*args, **kwargs)
