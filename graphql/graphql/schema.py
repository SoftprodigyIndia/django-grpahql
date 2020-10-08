import graphene
import secret.schema
import graphql_jwt


class Query(secret.schema.Query, graphene.ObjectType):
    pass

class Mutation(secret.schema.Mutation,graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query,mutation=Mutation,auto_camelcase=False)