import random as r
import numpy as np

def solve(schedule):
    """
    Your solution of the problem
    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot. 
    """
    # Add here your agent
    
    best_solution = None
    current_solution = simulated_annealing(schedule, 1000, 0.95, 10)
    best_solution = hill_climbing(schedule, current_solution)
    
    return best_solution

# Necessary hill climbing algorithm to improve the randomized solution.
def hill_climbing(schedule, solution):
    neighbourhood = colorChoiceNeighbourhood(solution)
    valid_neighbourhood = is_improving_solution(schedule, neighbourhood, solution, evaluation_function=evaluation_function)
    
    while valid_neighbourhood:
        solution = min(valid_neighbourhood, key=lambda n: evaluation_function(schedule, n))
        neighbourhood = colorChoiceNeighbourhood(solution)
        valid_neighbourhood = is_improving_solution(schedule, neighbourhood, solution, evaluation_function=evaluation_function)
    
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

#Evaluation functions: determines the number of conflicts as well as the number of time_slots of the solution  
def evaluation_function(schedule, solution):
    conflict = sum(solution[a[0]] == solution[a[1]] for a in schedule.conflict_list)   
    time_slots = len(set(solution.values()))
    return conflict * len(schedule.course_list) + time_slots

#To prevent the minima problem, the simulated annealing algorithm will be applied

def simulated_annealing(schedule, init_temp, alpha, max_iteration):
    solution = generate_random_solution(schedule)
    neighbourhood = colorChoiceNeighbourhood(solution)
    
    i = 0
    temperature = init_temp
    best_solution = solution
    
    for i in range(max_iteration):
        candidate = r.choice(neighbourhood)
        delta = evaluation_function(schedule, candidate) - evaluation_function(schedule, solution)
        probability = max(np.exp(-delta / temperature), 0.01)
        
        if delta < 0:
            solution = candidate
        
        elif np.random.binomial(1, probability):
            solution = candidate
        
        if evaluation_function(schedule, solution) < evaluation_function(schedule, best_solution):
            best_solution = solution
        
        temperature *= alpha
        neighbourhood = colorChoiceNeighbourhood(solution)
    
    return best_solution