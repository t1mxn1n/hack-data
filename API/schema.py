from email.policy import default
import graphene
import json


class Query(graphene.ObjectType):
    is_staff = graphene.Boolean(name='is_staff')

    def resolve_is_staff(self, info):
        return True


if __name__ == '__main__':
    schema = graphene.Schema(query=Query, auto_camelcase=False)
    result = schema.execute(
        '''
        {
            is_staff
        }
        '''
    )
    items = dict(result.data.items())
    print(json.dumps(items))
