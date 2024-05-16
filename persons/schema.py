import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from persons.models import Person, Vote
from graphql import GraphQLError
from django.db.models import Q

from .models import Person


class PersonType(DjangoObjectType):
    class Meta:
        model = Person

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    persons = graphene.List(PersonType, search=graphene.String())
    votes = graphene.List(VoteType)

    def resolve_persons(self, info, search=None, **kwargs):
        if search:
            filter = (
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
            return Person.objects.filter(filter)

        return Person.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()


class CreatePerson(graphene.Mutation):
    id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    age = graphene.Int()
    email = graphene.String()
    genre = graphene.String()
    posted_by = graphene.Field(UserType)

    #2
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        age = graphene.Int()
        email = graphene.String()
        genre = graphene.String()
        
    #3
    def mutate(self, info, first_name, last_name, age, email, genre):
        user = info.context.user or None

        person = Person(first_name=first_name,
        last_name=last_name, 
        age=age, 
        email=email, 
        genre=genre
        )
        person.save()

        return CreatePerson(
            id=person.id,
            first_name=person.first_name,
            last_name=person.last_name,
            age=person.age,
            email=person.email,
            genre=person.genre,
            posted_by=person.posted_by,
        )

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    person = graphene.Field(PersonType)

    class Arguments:
        person_id = graphene.Int()

    def mutate(self, info, person_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')


        person = Person.objects.filter(id=person_id).first()
        if not person:
            raise Exception('Invalid Person!')

        Vote.objects.create(
            user=user,
            person=person,
        )

        return CreateVote(user=user, person=person)

#4
class Mutation(graphene.ObjectType):
    create_person = CreatePerson.Field()
    create_vote = CreateVote.Field()
