from models.data import *
from models.maltparser import Dependency

class Relation:
    def __init__(self, type: str, left: str, right: str):
        self.type = type    # e.g. AGENT
        self.left = left    # e.g. s1
        self.right = right  # e.g. đến
    
    def __str__(self) -> str:
        return f"({self.left} {self.type} {self.right})"

class SEM:
    def __init__(self, predicate: str, variable, relations=None):
        self.predicate = predicate
        self.variable = variable
        self.relations = relations if relations else []
    
    def __str__(self) -> str:
        return f"({self.predicate} {self.variable}" \
                + f"{' ' + ' '.join(map(str, self.relations)) if self.relations else ''})"

def create_sem(word, existing_vars):
    new_var = create_variable(word, existing_vars)
    if POS[word] not in [NAME]:
        return word, None
    semantic = SEM(POS[word], new_var, [word])
    return semantic, new_var

def create_variable(word: str, existing_vars: "list[str]") -> str:
    initial = word[0]
    counter = 0
    while True:
        counter += 1
        var_name = f"{initial}{counter}"
        if var_name not in existing_vars:
            return var_name

def relationalize(dependencies: "list[Dependency]") -> "list[Relation]":
    relation_list = []
    var_list = []

    for dep in dependencies:
        if dep.relation == "query":
            relation_list.append(Relation("QUERY", "s1", dep.tail))

        elif dep.relation == "noun_query":
            has_query = False
            for rel in relation_list:
                if rel.type == "QUERY":
                    has_query = True
                    break
            if has_query:
                relation_list.append(Relation("CO_QUERY", "s1", dep.head))
            else:
                relation_list.append(Relation("QUERY", "s1", dep.head))

        elif dep.relation == "root":
            var_list.append("s1")
            relation_list.append(Relation("PRED", "s1", dep.tail))

        elif dep.relation == "subj":
            if dep.tail in PRONOUN:
                relation_list.append(Relation("AGENT", "s1", dep.tail))

        elif dep.relation == "nmod":
            if POS[dep.tail] == NAME:
                sem_obj, new_var = create_sem(dep.tail, var_list)
                if new_var is not None:
                    var_list.append(new_var)
                relation_list.append(Relation("DES", "s1", sem_obj))
            else:
                sem_obj, new_var = create_sem(dep.tail, var_list)
                if new_var is not None:
                    var_list.append(new_var)
                relation_list.append(Relation("THEME", "s1", sem_obj))

        elif dep.relation == "pobj" and dep.head == "từ":
            sem_obj, new_var = create_sem(dep.tail, var_list)
            if new_var is not None:
                var_list.append(new_var)
            relation_list.append(Relation("SRC", "s1", sem_obj))

        elif dep.relation == "pobj" and dep.head == "tới":
            sem_obj, new_var = create_sem(dep.tail, var_list)
            if new_var is not None:
                var_list.append(new_var)
            relation_list.append(Relation("DES", "s1", sem_obj))

    return relation_list
