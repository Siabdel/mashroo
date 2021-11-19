# -*- coding:utf-8 -*-
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from projects.models import Ticket, Project, Vtodo
from projects.models import Member, UProfile
from projects import models as proj_models
from core.profile  import models as profile_models
from collections import OrderedDict
from core.taxonomy.models import Category
from core.profile.models import UProfile, Service, Societe

"""
la class  TicketSerializer fait un mapping avec le models pour les colonnes definie dans fields
"""

class AsymetricRelatedField(serializers.PrimaryKeyRelatedField):

    # en lecture, je veux l'objet complet, pas juste l'id
    def to_representation(self, value):
        # le self.serializer_class.serializer_class est redondant
        # mais obligatoire
        return self.serializer_class.serializer_class(value).data

    # petite astuce perso et pas obligatoire pour permettre de taper moins
    # de code: lui faire prendre le queryset du model du serializer
    # automatiquement. Je suis lazy
    def get_queryset(self):
        if self.queryset:
            return self.queryset
        return self.serializer_class.serializer_class.Meta.model.objects.all()

    # Get choices est utilisé par l'autodoc DRF et s'attend à ce que
    # to_representation() retourne un ID ce qui fait tout planter. On
    # réécrit le truc pour utiliser item.pk au lieu de to_representation()
    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])

    # DRF saute certaines validations quand il n'y a que l'id, et comme ce
    # n'est pas le cas ici, tout plante. On désactive ça.
    def use_pk_only_optimization(self):
        return False

    # Un petit constructeur pour générer le field depuis un serializer. lazy,
    # lazy, lazy...
    @classmethod
    def from_serializer(cls, serializer, name=None, args=(), kwargs={}):
        if name is None :
            name = "{}AsymetricAutoField".format(serializer.__class__.__name__)

        return type(name, (cls,), {"serializer_class": serializer})(*args, **kwargs)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta :
        model = Project
        # fields = ('title', 'description', 'author',  'status', 'categories', )
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = '__all__'



class CategorySerializer(serializers.ModelSerializer):
    class Meta :
        model =  Category
        fields = '__all__'

class SocieteSerializer(serializers.ModelSerializer):
    class Meta :
        model = profile_models.Societe
        fields = '__all__'

class FonctionSerializer(serializers.ModelSerializer):
    class Meta :
        model = profile_models.Fonction
        fields = '__all__'


class SocieteSerializer(serializers.ModelSerializer):
    class Meta :
        model =  Societe
        #fields = '__all__'
        fields = ( 'id', 'name', )


class ServiceSerializer(serializers.ModelSerializer):
    class Meta :
        model =  Service
        #fields = '__all__'
        fields = ( 'id', 'name', )



class MemberSerializer(serializers.ModelSerializer):
    #user = serializers.StringRelatedField(many=False, read_only=False, allow_null=False)
    user        = UserSerializer()
    fonction    = FonctionSerializer ()
    service     = ServiceSerializer ()


    class Meta :
        model = UProfile
        fields = ( 'id', 'full_name', 'date_naissance', 'photo', 'user', 'fonction', 'service', 'language', )
        #fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):

    """
    fields = ('project', 'sequence',  'title', 'description', 'author', 'status', 'categories', 'type',
              'urgency', 'assignee', 'closed', 'closed', 'due_date', 'schedule_date')
    """
    author = serializers.StringRelatedField(many=False, read_only=True)

    class Meta :
        model = Ticket
        # fields = ('project', 'sequence',  'title', 'description', 'author', 'status',   )
        fields = '__all__'


class TodoTodaySerializer(serializers.ModelSerializer):
    """
    ( 'id', 'title', 'author_id',)
    """
    # author = serializers.StringRelatedField(many=False, read_only=True)

    def create(self, validated_data):
        return Vtodo.objects.create(**validated_data)

    class Meta :
        model = Vtodo
        fields = '__all__'

class TicketTimelineEventsSerializer(serializers.ModelSerializer):
    """
    """
    author = serializers.StringRelatedField(many=False, read_only=True)
    start = serializers.StringRelatedField(many=False, read_only=True)


    class Meta :
        model = Ticket
        fields = ('id', 'resourceId', 'start',  'created', 'title', 'end', 'due_date', 'status', 'author', 'eventColor' , )


class TicketTimelineResourcesSerializer(serializers.ModelSerializer):
    """
    """
    author = serializers.StringRelatedField(many=False, read_only=True)

    class Meta :
        model = Project
        fields = ( 'id', 'title', 'author',   'eventColor' ,)


class ServicesSociete(serializers.ModelSerializer):

    class Meta :
        model = Service
        fields = '__all__'

class TicketsProjectSerializer(serializers.ModelSerializer):
    author      = serializers.StringRelatedField(many=False, read_only=True)
    assignee    = UserSerializer()
    category    = CategorySerializer ()
    project     = ProjectSerializer()


    class Meta :
        model = Ticket
        #fields = '__all__'
        fields = ('id', 'project', 'sequence', 'title', 'description', 'author',
                  'type', 'urgency', 'status', 'assignee', 'created', 'modified', 'closed', 'category',
                    'due_date', 'start_date', 'end_date', 'schedule_date', 'is_manager',
                    'delai_due_date', 'delai_closed_date', 'delai_realisation',  'delai_planifie', 'nbjours_ouvrable_due_date',
                    )
