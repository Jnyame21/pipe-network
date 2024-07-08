from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from bolcan import pipeline_eng
from django.http import HttpResponse

# Create your views here.
def root(request):
    return HttpResponse("<h1>Hello!</h1>")


@api_view(['POST'])
def pipe_network(request):
    data = request.data
    loops = json.loads(data['loops'])
    equation = data['equation']
    K = True if data['K'] == 'k' else False
    max_iter = data['maxIter'] if data['maxIter'] != 'false' else 100
    common_pipes = json.loads(data['commonPipes']) if data['commonPipes'] != 'false' else None
    error = data['error'] if data['error'] != 'false' else 1e-8
    
    if K:
        for loop in loops:
            loop['props'].insert(0, ['pipe', 'K', 'Qa'])
    else:
        if equation == 'darcy':
            for loop in loops:
                loop['props'].insert(0, ['pipe', 'length', 'diameter', 'f', 'Qa'])
        elif equation == 'hazen':
            for loop in loops:
                loop['props'].insert(0, ['pipe', 'length', 'diameter', 'C', 'Qa'])
            
    result = pipeline_eng.pipe_network(loops=loops, pipes_in_common_loops=common_pipes, equation=equation, K=K, max_iter=int(max_iter), error=float(error))
    data = {'type': 'k', 'data': []}
    pipe_names = []
    if not K:
        data['type'] = equation
    
    for loop in result:
        del loop['props'][0]
        for pipe in loop['props']:
            pipe.pop(-1)
            if pipe[0] not in pipe_names:
                pipe_names.append(pipe[0])
                data['data'].append(pipe)
    
    return Response(data, status=200)


        
    
    

