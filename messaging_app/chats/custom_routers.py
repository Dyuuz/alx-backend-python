from rest_framework.routers import SimpleRouter, Route

class NestedDefaultRouter(SimpleRouter):
    routes = [
       Route(
           url=r'^{prefix}/{lookup}$',
           mapping={'get': 'retrieve'},
           name='{basename}-detail',
           detail=True,
           initkwargs={'suffix': 'Detail'}
       ),

       Route(
           url=r'^{prefix}$',
           mapping={'get': 'list'},
           name='{basename}-list',
           detail=False,
           initkwargs={'suffix': 'List'}
       ) 
    ]

