import random as r

def solve(schedule):
    """
    Your solution of the problem
    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot. 
    """
    # Add here your agent
    solution = generate_random_solution(schedule)
    neighbourhood = colorChoiceNeighbourhood(solution)
    valid_neighbourhood = is_improving_solution(schedule, neighbourhood, solution, evaluation_function=evaluation_number_conflicts)
    
    n = 0
    
    while valid_neighbourhood:
        solution = min(valid_neighbourhood, key=lambda n: evaluation_number_conflicts(schedule, n))
        neighbourhood = colorChoiceNeighbourhood(solution)
        valid_neighbourhood = is_improving_solution(schedule, neighbourhood, solution, evaluation_function=evaluation_number_conflicts)
        n += 1
    
    return solution

#Initial solution: random assignments of the time slots to the courses
def generate_random_solution(schedule):
    solution = dict()
    for c in schedule.course_list:
        choix = r.randint(1, len(schedule.course_list))
        solution[c] = choix
    return solution

#Neighbourhood function: 
def colorChoiceNeighbourhood(solution):
    neighbourhood = []
    chosenColors = set(solution.values())
    for c in solution:
        for color in chosenColors:
            if color != solution[c]:
                neighbour = solution.copy()
                neighbour[c] = color
                neighbourhood.append(neighbour)                
    return neighbourhood

#Validation function: verify if the neighbourhood contains a better solution than the current one     
def is_improving_solution(schedule, neighbourhood, solution, evaluation_function):
    currentSolution = evaluation_function(schedule, solution)
    return [n for n in neighbourhood if evaluation_function(schedule, n) < currentSolution]

#Evaluation functions: determines the number of conflicts of the solution  
def evaluation_number_conflicts(schedule, solution):
    return sum(solution[a[0]] == solution[a[1]] for a in schedule.conflict_list)    
    
def solve_with_restarts(schedule, nb_restarts):
    best_solution = None
    
    for i in range(nb_restarts):
        solution = solve(schedule)
        if evaluation_number_conflicts(schedule, solution) < evaluation_number_conflicts(schedule, best_solution):
            best_solution = solution
        
        elif evaluation_number_conflicts(schedule, best_solution) == 0:
            break
        
        print("RESTART: ", i)
    
    return best_solution
    