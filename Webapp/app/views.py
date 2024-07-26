from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
import math
import pandas as pd
from django.http import HttpResponse

# Create your views here.
def root(request):
    return HttpResponse("<h1>Pipe Network Analysis</h1>")


def pipe_network(loops, equation:str, pipes_in_common_loops=None, K=False, error=1e-8, max_iter=100):
    results = True
    if equation not in ['darcy', 'hazen']:
        raise ValueError("The equation must either be 'hazen' for Hazen Williams or 'darcy' for Darcy Weisbach")
    
    n = 2 if equation == 'darcy' else 1.85
    
    df_list = []
    for lp in loops:
        header = lp['props'][0]
        data = lp['props'][1:]
        df = pd.DataFrame(data, columns=header)
        df['Qa'] = df['Qa'].astype(float)
        
        if 'pipe' not in df.columns:
            raise ValueError("No 'pipe' column was found. Make sure you have the names of the pipes under a column named 'pipe' ")
        elif 'Qa' not in df.columns:
            raise ValueError("No 'Qa' column was found. Make sure you have the flow rates of the pipes under a column named 'Qa' ")
        
        if not K:
            if 'length' not in df.columns:
                raise ValueError("No 'length' column was found. Make sure you have the lengths of the pipes under a column named 'length' ")
            elif 'diameter' not in df.columns:
                raise ValueError("No 'diameter' column was found. Make sure you have the Diameter of the pipes under a column named 'diameter' ")
            elif equation == 'darcy' and 'f' not in df.columns:
                raise ValueError("No 'f' column was found. Make sure you have the friction factor(f) of the pipes under a column named 'f' ")
            elif equation == 'hazen' and 'C' not in df.columns:
                raise ValueError("No 'C' column was found. Make sure you have the Hazen Williams's coefficient(C) of the pipes under a column named 'C'")
            else:
                df['length'] = df['length'].astype(float)
                df['diameter'] = df['diameter'].astype(float)
        else:
            if 'K' not in df.columns:
                raise ValueError("No 'K' column was found. Make sure you have the K values of the pipes under a column named 'K' ")
            else:
                df['K'] = df['K'].astype(float)
        
        if not K and equation == 'darcy':
            df['f'] = df['f'].astype(float)
        elif not K and equation == 'hazen':
            df['C'] = df['C'].astype(float)
            
        # Copy the assumed flow rate to a new column to be used for the calculation
        df['Qnew'] = df['Qa']
        df_list.append({'name': lp['name'], 'df': df})
        
    iterations = 1
    
    while True:
        q_list = []   
        
        # Function to calculate the head loss in each pipe
        def head_loss(a, b, c, d):
            # a=length, b=diameter, c=f/C/K, d=assumed rate
            a=float(a); b=float(b); c=float(c); d=float(d)
            
            hl = math.pow(abs(d), n)
            if not K and equation == 'darcy':
                const_A = 8*a*c; 
                const_B = 9.81*math.pow(3.143, 2)*math.pow(b, 5)
                hl = hl*(const_A/const_B)
            elif not K and equation == 'hazen':
                const_A = 10.67*a
                const_B = math.pow(c, n)*math.pow(b, 4.87)
                hl = hl*(const_A/const_B)
            else:
                hl = hl*c
            
            return hl if d > 0 else -hl
        
        for df in df_list:
            if not K and equation == 'darcy':
                df['df']['hl'] = df['df'].apply(lambda row: head_loss(row['length'], row['diameter'], row['f'], row['Qnew']), axis=1)
            elif not K and equation == 'hazen':
                df['df']['hl'] = df['df'].apply(lambda row: head_loss(row['length'], row['diameter'], row['C'], row['Qnew']), axis=1)
            else:
                df['df']['hl'] = df['df'].apply(lambda row: head_loss(1, 1, row['K'], row['Qnew']), axis=1)
            
            # Divide the head loss by the rate
            df['df']['hl/Qnew'] = abs(df['df']['hl']/(df['df']['Qnew']))
            
            # Find the sum
            hl_sum = sum(df['df']['hl'])
            hl_Qnew_sum = sum(df['df']['hl/Qnew'])
            
            # calculate the correction factor
            q = -hl_sum/(1.85*hl_Qnew_sum)
            q_list.append({'name': df['name'], 'q': q})
        
        common_loop_pipes = []
        if pipes_in_common_loops is not None:
            for com_pipe in pipes_in_common_loops:
                common_loop_pipes.append(com_pipe['name'])
                
        def correct_rate(row, df, df_q):
            Qnew = row['Qnew'] + df_q
            if pipes_in_common_loops and row['pipe'] in common_loop_pipes:
                common_p = None
                
                for com_p in pipes_in_common_loops:
                    if com_p['name'] == row['pipe']:
                        common_p = com_p
                
                if common_p:
                    common_pipe_loops = []
                    for loop_name in common_p['loops']:
                        if loop_name != df['name']:
                            common_pipe_loops.append(loop_name)
                            
                    if len(common_pipe_loops) != 0:
                        for loop_name in common_pipe_loops:
                            for q in q_list:
                                if loop_name == q['name']:
                                    Qnew = Qnew - q['q']
                
            return Qnew
        
        df_q_list = []
        for df_q in q_list:
            df_q_list.append(df_q['q'])
        
        # Check if all the correction factors are less than the error tolerance
        if all(abs(item) < error for item in df_q_list):
            break
        
        for df, df_q in zip(df_list, q_list):     
            df['df']['Qnew'] = df['df'].apply(lambda row: correct_rate(row, df, df_q['q']), axis=1)
        
        if iterations >= max_iter:
            results = False
            break

        iterations +=1
    
    if results:
        for df, df_q in zip(df_list, q_list):
            df['df']['Qnew'] = round(df['df']['Qnew'], 4)
            df['df']['hl'] = round(df['df']['hl'], 4)
            df['df']['hl/Qnew'] = round(df['df']['hl/Qnew'], 4)
            df_to_list = df['df'].values.tolist()
            df_to_list.insert(0, df['df'].columns.tolist())
            df['df'] = df_to_list
            df['props'] = df.pop('df')

        return df_list
    else:
        return f"No convergence after {max_iter} iterations. You can increase the number of iterations by modifying the 'max_iter' parameter in the function argument"



@api_view(['POST'])
def pipe_network_view(request):
    data = request.data
    loops = json.loads(data['loops'])
    equation = data['equation']
    K = True if data['K'] == 'k' else False
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
    
    
    data = {'type': 'k', 'data': []}
    try:
        result = pipe_network(loops=loops, pipes_in_common_loops=common_pipes, equation=equation, max_iter=1000, K=K, error=float(error))
        if isinstance(result, str):
            data['results'] = 'no'
            data['data'] = "Oops! No convergence after 1000 iterations. Please check the data or consider adjusting the error tolerance."
        else:
            data['results'] = 'yes'
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
    except Exception as e:
        data['data'] = "Oops! something went wrong, please check the data"
        
    return Response(data, status=200)


        
    
    

