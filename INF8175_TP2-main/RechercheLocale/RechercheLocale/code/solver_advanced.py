import random as r

def solve(schedule):
    """
    Your solution of the problem
    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot. 
    """
    # Add here your agent
    solution = generate_random_solution(schedule)
    
    def generate_random_solution(schedule):
        solution = dict()
        for c in schedule.course_list:
            choix = r.randint(1, len(schedule.course_list))
            solution[c] = choix
        schedule.get_n_creneaux(solution)
        return solution
    
    def two_swap_neighborhood(solution):
        neighbourhood = []
    
    return solution