from models.maltparser import *
from models.grammar_relation import relationalize
from models.logical_form import logicalize
from models.semantic_procedure import proceduralize
from models.answer import answer

def load_input_queries(path):
    query_list = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            line = line.replace("\n", "")
            query_list.append(line)
    return query_list

def append_text_to_file(content, path):
    with open(path, "a", encoding="utf-8") as file:
        file.write(content)

def process_queries():
    input_queries = load_input_queries("../input/questions.txt")

    for i in range(1,6):
        file_path = f"../output/p2-q-{i}.txt"
        with open(file_path, "w", encoding="utf-8"):
            pass

    result1 = "Đầu tiên ta định nghĩa RIGHT_ARC và LEFT_ARC như sau:\n\n"
    result1 += "RIGHT_ARC: \nCó dạng A R B, nghĩa là, từ bên trái là A, từ bên phải là B, mối quan hệ RIGHT_ARC của chúng là R\n"
    for i in RIGHT_ARC:
        if len(RIGHT_ARC[i]) > 0:
            for j in RIGHT_ARC[i]:
                result1 += ''.join([f"{i:{18}}", f"{RIGHT_ARC[i][j]:{18}}", f"{j:{18}}"]) + "\n"
    result1 += "\n\nLEFT_ARC: \nCó dạng A R B, nghĩa là, từ bên trái là A, từ bên phải là B, mối quan hệ LEFT_ARC của chúng là R\n"
    for i in LEFT_ARC:
        if len(LEFT_ARC[i]) > 0:
            for j in LEFT_ARC[i]:
                result1 += ''.join([f"{i:{18}}", f"{LEFT_ARC[i][j]:{18}}", f"{j:{18}}"]) + "\n"
    result1 += "\nSau khi đã định nghĩa, sử dụng giải thuật MaltParser như đã học để phân tích câu."
    append_text_to_file(result1, f"../output/p2-q-1.txt")

    for query in input_queries:
        formatted_query = "Câu hỏi: " + query + "\n"

        parsed_deps = malt_parse(query)
        result2 = ""
        for item in parsed_deps:
            result2 += str(item) + "\n"
        result2 += "\n\n"
        append_text_to_file(formatted_query + result2, f"../output/p2-q-2.txt")

        result3 = ""
        grammar_relations = relationalize(parsed_deps)
        for rel in grammar_relations:
            result3 += str(rel) + "\n"
        result3 += "\n\n"
        append_text_to_file(formatted_query + result3, f"../output/p2-q-3.txt")

        logical_form = logicalize(grammar_relations)
        result4 = str(logical_form) + "\n"
        semantic_proc = proceduralize(logical_form)
        result4 += str(semantic_proc) + "\n\n\n"
        append_text_to_file(formatted_query + result4, f"../output/p2-q-4.txt")

        result5 = "Trả lời: " + answer(semantic_proc) + "\n\n\n"
        append_text_to_file(formatted_query + result5, f"../output/p2-q-5.txt")

if __name__ == "__main__":
    process_queries()