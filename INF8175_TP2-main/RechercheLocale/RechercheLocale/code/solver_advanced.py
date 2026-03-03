import random as r

def solve(schedule):
    """
    Your solution of the problem
    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot. 
    """
    # Add here your agent
    solution = generate_random_solution(schedule)
    neighbourhood = two_swap_neighbourhood(solution)
    valid_neighbourhood = is_improving_solution(schedule, neighbourhood, solution, evaluation_function=evaluation_number_conficts)
    
    while valid_neighbourhood:
        solution = min(valid_neighbourhood, key=lambda n: evaluation_number_conficts(schedule, n))
        neighbourhood = two_swap_neighbourhood(solution)
        valid_neighbourhood = is_improving_solution(schedule, neighbourhood, solution, evaluation_function=evaluation_number_conficts)
        n += 1
    
    return solution
    
def generate_random_solution(schedule):
    solution = dict()
    for c in schedule.course_list:
        choix = r.randint(1, len(schedule.course_list))
        solution[c] = choix
    return solution
    
def two_swap_neighbourhood(solution):
    neighbourhood = []
    for c1 in solution:
        for c2 in solution:
            if c1 != c2:
                n = solution.copy()
                n[c1], n[c2] = n[c2], n[c1]
                neighbourhood.append(n)
    return neighbourhood
    
def is_improving_solution(schedule, neighbourhood, solution, evaluation_function):
    return [n for n in neighbourhood if evaluation_function(schedule, n) < evaluation_function(schedule, solution)]
        
def evaluation_number_conficts(schedule, solution):
    return sum(solution[a[0]] == solution[a[1]] for a in schedule.conflict_list)    
    
