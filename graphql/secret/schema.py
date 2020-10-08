import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from django.contrib.auth.models import User


class Usermodel(DjangoObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    user_list = graphene.List(Usermodel,search=graphene.String(), first=graphene.Int(),
        skip=graphene.Int())
    me=graphene.Field(Usermodel)
    def resolve_user_list(self, info,search=None, first=None, skip=None, **kwargs):
        all_users = User.objects.all()
        if search:
            print('search arg is passed')
            return all_users.filter(Q(username__icontains= search) | Q(email__icontains=search))

        if first:
            all_users=all_users[:first]

        if skip:
            all_users=all_users[skip:]



        return all_users


  



class Create_User(graphene.Mutation):
    class Arguments:
        username = graphene.String(required= True)
        password = graphene.String(required= True)
        email    =  graphene.String(required= True)
        first_name = graphene.String()

    user = graphene.Field(Usermodel)
    def mutate(root,info,username,password,first_name,email):
        message=""
        user_instance =User(username= username,password=password,email=email, first_name=first_name)
        user_instance.save()
        return Create_User(user=user_instance,message="USer created")




class Mutation(graphene.ObjectType):
    create_user = Create_User.Field()




