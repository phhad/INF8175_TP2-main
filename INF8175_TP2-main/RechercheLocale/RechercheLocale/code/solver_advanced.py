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
    current_solution = simulated_annealing(schedule, 1000, 0.95, 5000)
    best_solution = hill_climbing(schedule, current_solution)
    
    return best_solution

# Necessary hill climbing algorithm to improve the randomized solution.
def hill_climbing(schedule, solution):
    neighbourhood = colorChoiceNeighbourhood(solution)
    valid_neighbourhood = is_improving_solution(schedule, neighbourhood, solution)
    
    while valid_neighbourhood:
        solution = min(valid_neighbourhood, key=lambda n: evaluation_function(schedule, n))
        neighbourhood = colorChoiceNeighbourhood(solution)
        valid_neighbourhood = is_improving_solution(schedule, neighbourhood, solution)
    
    return solution
    
#Initial solution: the greedy algorithm consisting of assigning the lowest time slot possible to each course.
def initial_solution(schedule):
    solution = {}
    
    neighbours = {c: set() for c in schedule.course_list}
    for a, b, in schedule.conflict_list:
        neighbours[a].add(b)
        neighbours[b].add(a)
    
    for c in schedule.course_list:
        used_colors = {solution[n] for n in neighbours[c] if n in solution}
        color = 1
        while color in used_colors:
            color += 1
        solution[c] = color
        
    return solution

#Neighbourhood function: swaps the time slots of one course with another one. Only the ones already used decrease the neighborhood size.
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
def is_improving_solution(schedule, neighbourhood, solution):
    currentSolution = evaluation_function(schedule, solution)
    return [n for n in neighbourhood if evaluation_function(schedule, n) < currentSolution]

#Evaluation functions: determines the number of conflicts as well as the number of time_slots of the solution  
def evaluation_function(schedule, solution):
    conflict = sum(solution[a[0]] == solution[a[1]] for a in schedule.conflict_list)   
    time_slots = len(set(solution.values()))
    return conflict * (len(schedule.course_list))**2 + time_slots

#To prevent the minima problem, the simulated annealing algorithm will be applied

def simulated_annealing(schedule, init_temp, alpha, max_iteration):
    solution = initial_solution(schedule)
    neighbourhood = colorChoiceNeighbourhood(solution)
    
    temperature = init_temp
    best_solution = solution.copy()
    
    for _ in range(max_iteration):
        candidate = r.choice(neighbourhood)
        delta = evaluation_function(schedule, candidate) - evaluation_function(schedule, solution)
        probability = np.exp(-delta / temperature)
        
        if delta < 0 or r.random() < probability:
            solution = candidate

        if evaluation_function(schedule, solution) < evaluation_function(schedule, best_solution):
            best_solution = solution.copy()
        
        temperature *= alpha
        if temperature < 1e-10:
            break
        
        neighbourhood = colorChoiceNeighbourhood(solution)
    
    return best_solution