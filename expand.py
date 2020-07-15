import json

def expand(videoinfo_dict, option_lst, question_lst):
    for video in videoinfo_dict:
        video_info = videoinfo_dict[video]
        q_lst = video_info['questions']
        for q in q_lst:
            
            ### expand the type
            q_type = q['type']
            if (q_type == '1' or q_type == 'd' or q_type == 'D'):
                q['type'] = 'Descriptive'
            elif (q_type == '2' or q_type == 'e' or q_type == 'E'):
                q['type'] = 'Explanatory'
            elif (q_type == '3' or q_type == 'p' or q_type == 'P'):
                q['type'] = 'Predictive'
            elif (q_type == '4' or q_type == 'r' or q_type == 'R'):
                q['type'] = 'Reverse Inference'
            elif (q_type == '5' or q_type == 'c' or q_type == 'C'):
                q['type'] = 'Counterfactual'
            elif (q_type == '6' or q_type == 'i' or q_type == 'I'):
                q['type'] = 'Introspection'
                
            ### expand the question
            q_question = q['question']
            if (q_question[0] == '#'):
                q['question'] = question_lst[int(q_question[1:])-1]
            
            ### expand the option
            q_option = q['options']
            q_options = []
            for i in q_option:
                if (i[0] == '@'):
                    q_options += option_lst[int(i[1:])-1]
                else: 
                    q_options.append(i)
            q['options'] = q_options
    return videoinfo_dict

def write_outfile(expand_dict, outfile_path):
    outfile = open(outfile_path, 'w')
    for video in expand_dict:
        video_name = expand_dict[video]
        time = video_name['time']
        view = video_name['view']
        out = f'~~~~~~{video}~~~~~~ (TIME):{time} (VIEW):{view}  '
        out = out.replace(' ','\n')
        outfile.write(out)
        
        questions = video_name['questions']
        for q in questions:
            q_type = q['type']
            q_question = q['question']
            out = f'Type:{q_type} '
            out = out.replace(' ','\n')
            outfile.write(out)
            out = f'Ques:{q_question} '
            outfile.write(out)
            out = ' '
            out = out.replace(' ','\n')
            outfile.write(out)
            
            q_options = q['options']
            out_option = ''
            for q_option in q_options:
                out_option += q_option
                out_option += ' '
            out_option = out_option.replace(' ','\n')
            outfile.write(out_option)   
             
            q_answer = q['answer']
            out = f'{q_answer}  '
            out = out.replace(' ','\n')
            outfile.write(out)
       
    

q1 = {'question':'is lynn drunk','options':['Yes','@3'],'answer':'A','type':'d'}
q2 = {'question':'is samill drunk','options':['@1','@3'],'answer':'C','type':'E'}
q3 = {'question':'#1','options':['@2','purple'],'answer':'A','type':'6'}
videoinfo_dict = {'BV90882938':{'time':'','view':'3','questions':[q1,q2]},
                  'BVsjdheoej':{'time':'','view':'1','questions':[q3]}}
option_lst = [['Yes'],['grey','blue','red'],['no','No']]
question_lst = ['what is the color']

expand_dict = expand(videoinfo_dict, option_lst, question_lst)
write_outfile(expand_dict, '/Users/linyutian/Desktop/write_out.txt')