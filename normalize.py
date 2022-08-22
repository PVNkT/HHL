import numpy as np

def normalize_vector(answer):
    print(answer)
    available_result = []
    for i in ["00","01","10","11"]:
        for key in answer.keys():
        
            if key[0:2] == i:
                if int(key[-1]) == 1:
                    available_result.append(answer[key])
                else:
                    pass
            else:
                pass

    available_result = np.sqrt(np.array(available_result))
    normalized_result = available_result/np.linalg.norm(available_result)
    return normalized_result