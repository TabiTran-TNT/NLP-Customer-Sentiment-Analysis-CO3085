from models.semantic_procedure import Procedure
from models.data import *

def answer(procedure: Procedure):
    TOUR_DATA, ATIME_DATA, DTIME_DATA, RUNTIME_DATA, BY_DATA = load_data()
    
    q_type = None
    tour_query = []
    
    if procedure.name == "PRINT-ALL":
        for instruction in procedure.args:
            if isinstance(instruction, Procedure) and "TOUR" in instruction.name:
                route_parts = instruction.name.split(" ")
                if len(route_parts) > 1:
                    tour_query = [route_parts[1]]
                    q_type = "TOUR"
                else:
                    tour_query = [x for x in TOUR_DATA]
                    q_type = "TOUR"

            elif isinstance(instruction, Procedure) and instruction.name == "ATIME":
                params = instruction.args
                if "?" not in params[1]:
                    tour_query.append(params[1])

            elif isinstance(instruction, Procedure) and instruction.name == "DTIME":
                params = instruction.args
                if "?" not in params[1]:
                    tour_query.append(params[1])

            elif isinstance(instruction, Procedure) and instruction.name == "RUN-TIME":
                q_type = "RUN-TIME"

            elif isinstance(instruction, Procedure) and "BY" in instruction.name:
                route_parts = instruction.name.split(" ")
                if len(route_parts) > 1:
                    tour_query = [route_parts[1]]
                    q_type = "BY"
                else:
                    tour_query = [x for x in TOUR_DATA]
                    q_type = "BY"

            elif isinstance(instruction, Procedure) and "DATE" in instruction.name:
                route_parts = instruction.name.split(" ")
                if len(route_parts) > 1:
                    tour_query = [route_parts[1]]
                    q_type = "DATE"
                else:
                    tour_query = [x for x in TOUR_DATA]
                    q_type = "DATE"

    ans_string = ""

    if q_type == "TOUR" and tour_query:
        def ignore_escape(string: str) -> str:
            return string.replace("\"", "")
        
        count = 0
        list_tour = []
        for (dt_key, dt_value), (at_key, at_value) in zip(DTIME_DATA.items(), ATIME_DATA.items()):
            if dt_key not in tour_query:
                continue
            for schedule in zip(dt_value, at_value):
                list_tour.append("Tour " + (TOUR_DATA[dt_key] if dt_key in TOUR_DATA else dt_key) 
                                 + " - " + (TOUR_DATA[schedule[0][0]] if schedule[0][0] in TOUR_DATA else schedule[0][0]) 
                                 + " khởi hành lúc " + ignore_escape(schedule[0][1])
                                 + " và đến nơi lúc " + ignore_escape(schedule[1][1]))
                count += 1
        ans_string += "Có " + str(count) + " tour. \n"
        ans_string += ",\n".join(list_tour) + "."
        
    elif q_type == "TOUR":
        ans_string += "Không tìm thấy."

    elif q_type == "RUN-TIME":
        if tour_query[0] in RUNTIME_DATA and RUNTIME_DATA[tour_query[0]][0] == tour_query[1]:
            ans_string += "Đi từ " + (TOUR_DATA[tour_query[0]] if tour_query[0] in TOUR_DATA else tour_query[0]) + " đến " + (TOUR_DATA[tour_query[1]] if tour_query[1] in TOUR_DATA else tour_query[1])
            ans_string += " mất " + RUNTIME_DATA[tour_query[0]][1] + "."

        elif tour_query[1] in RUNTIME_DATA and RUNTIME_DATA[tour_query[1]][0] == tour_query[0]:
            ans_string += "Đi từ " + (TOUR_DATA[tour_query[0]] if tour_query[0] in TOUR_DATA else tour_query[0]) + " đến " + (TOUR_DATA[tour_query[1]] if tour_query[1] in TOUR_DATA else tour_query[1])
            ans_string += " mất " + RUNTIME_DATA[tour_query[1]][1] + "."
        else:
            ans_string += "Không tìm thấy."
    
    elif q_type == "BY" and tour_query:
        for tour in tour_query:
            ans_string += "Tour " + (TOUR_DATA[tour] if tour in TOUR_DATA else tour) + " đi bằng " + (ENGLISH_WORD[BY_DATA[tour]])  + "."

    elif q_type == "DATE" and tour_query:
        def get_date(string: str) -> str:
            string = string.replace("\"", "")
            parts = string.split(" ")
            for part in parts:
                if '/' in part:
                    return part
            return ""
        
        list_tour = []
        for at_key, at_value in ATIME_DATA.items():
            if at_key not in tour_query:
                continue
            list_tour.append("Tour " + (TOUR_DATA[at_key] if at_key in TOUR_DATA else at_key) 
                                 + " có thể đi vào các ngày ")
            dates = []
            for schedule in at_value:
                dates.append(get_date(schedule[1]))
            list_tour[-1] += ", ".join(dates)
        ans_string += ",\n".join(list_tour) + "."

    return ans_string

def load_data(path=None):
    TOUR = {}
    ATIME = {}
    DTIME = {}
    RUNTIME = {}
    BY = {}
    default_path = "../input/database.txt"
    path = path or default_path
    
    with open(path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            line = line.strip().replace('(', '').replace(')', '').replace('HCMC', 'HCM').replace("\n", "")
            elements = line.split(" ")

            if elements[0] == "TOUR":
                for i in range(len(elements)):
                    if elements[i] == 'TOUR':
                        TOUR.update({elements[i+1]: elements[i+2]})
                        i += 2
                        continue

            if elements[0] == "DTIME":
                for i in range(len(elements)):
                    if elements[i] == 'DTIME':
                        if elements[i+1] not in DTIME:
                            DTIME.update({elements[i+1]: [(elements[i+2], elements[i+3] + " " + elements[i+4])]}) 
                        else:
                            DTIME[elements[i+1]].append((elements[i+2], elements[i+3] + " " + elements[i+4]))
                        i += 3
                        continue
                    elif elements[i] == 'ATIME':
                        if elements[i+1] not in ATIME:
                            ATIME.update({elements[i+1]: [(elements[i+2], elements[i+3] + " " + elements[i+4])]}) 
                        else:
                            ATIME[elements[i+1]].append((elements[i+2], elements[i+3] + " " + elements[i+4]))
                        i += 3
                        continue

            if elements[0] == "RUN-TIME":
                RUNTIME.update({elements[1]: (elements[2], elements[4] + " " + elements[5])})

            if elements[0] == "BY":
                BY.update({elements[1]: elements[2]})
                
    return TOUR, ATIME, DTIME, RUNTIME, BY
