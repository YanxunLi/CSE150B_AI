from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

CONFLICT = (-1, -1)

class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem) 

        # TODO: implement backtracking search. 

        # TODO: delete this block ->
        # Note that the display and test functions in the main file take domains as inputs. 
        #   So when returning the final solution, make sure to take your assignment function 
        #   and turn the value into a single element list and return them as a domain map. 
        # for spot in sd_spots:
        #     domains[spot] = [1]
        # return domains
        # <- TODO: delete this block
        assignment_func = {}
        decision_stack = []

        while True:
            assignment_func, domains = self.propagate(assignment_func, domains)
            if not CONFLICT in assignment_func:
                if self.all_assigned(assignment_func):
                    return self.solution(assignment_func)
                else:
                    assignment_func, spot = self.make_decision(assignment_func, domains)
                    decision_stack.append((copy.deepcopy(assignment_func), spot, copy.deepcopy(domains)))
            else:
                if len(decision_stack) == 0:
                    return None
                else:
                    assignment_func, domains = self.backtrack(decision_stack)

    # TODO: add any supporting function you need
    def propagate(self, assignment_func, domains):
        while True:
            for spot in domains:
                if len(domains[spot]) == 1:
                    assignment_func[spot] = domains[spot][0]

            for spot in assignment_func:
                if len(domains[spot]) > 1:
                    domains[spot] = [assignment_func[spot]]

            for spot in domains:
                if len(domains[spot]) == 0:
                    assignment_func[CONFLICT] = -1
                    return assignment_func, domains

            updated = False
            for spot in sd_spots:
                for peer in sd_peers[spot]:
                    if len(domains[peer]) == 1:
                        value = domains[peer][0]
                        if value in domains[spot]:
                            domains[spot].remove(value)
                            updated = True

            if not updated:
                return assignment_func, domains

    def all_assigned(self, assignment_func):
        for spot in sd_spots:
            if not spot in assignment_func:
                return False
        return True

    def solution(self, assignment_func):
        return {spot: [assignment_func[spot]] for spot in assignment_func}

    def make_decision(self, assignment_func, domains):
        # Choose a spot with smallest domain
        best_spot = None
        for spot in domains:
            if not spot in assignment_func:
                if best_spot is None:
                    best_spot = spot
                elif len(domains[spot]) < len(domains[best_spot]):
                    best_spot = spot

        value = random.choice(domains[best_spot])
        assignment_func[best_spot] = value
        return assignment_func, best_spot

    def backtrack(self, decision_stack):
        assignment_func, spot, domains = decision_stack.pop()
        value = assignment_func.pop(spot)
        domains[spot].remove(value)
        return assignment_func, domains

    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'
        # format: label i, j, n to each literal p 
        # where (i, j) is coordinate of the spot and n is the number filled into that spot
        # encode: the literal number for p_(i, j, n) is i*SD_SIZE**2 + j*SD_SIZE + n
        def encode(i, j, n):
            return i*SD_SIZE**2 + j*SD_SIZE + n

        num_clause = 0

        # each spot must have a number
        for i in range(SD_SIZE):
            for j in range(SD_SIZE):
                for n in range(1, SD_SIZE+1):
                    text += str(encode(i, j, n)) + " "
                text += "0\n"
                num_clause += 1
        
        # each spot has at most one number
        for i in range(SD_SIZE):
            for j in range(SD_SIZE):
                for x in range(1, SD_SIZE):
                    for y in range (x+1, SD_SIZE+1):
                        text += str(-encode(i, j, x)) + " " + str(-encode(i, j, y)) + " 0\n"
                        num_clause += 1

        # each row has every number from 1 to SD_SIZE
        for i in range(SD_SIZE):
            for n in range(1, SD_SIZE+1):
                for j in range(SD_SIZE):
                    text += str(encode(i, j, n)) + " "
                text += "0\n"
                num_clause += 1

        # each column has every number from 1 to SD_SIZE
        for j in range(SD_SIZE):
            for n in range(1, SD_SIZE+1):
                for i in range(SD_SIZE):
                    text += str(encode(i, j, n)) + " "
                text += "0\n"
                num_clause += 1

        # each block of SD_DIM by SD_DIM has every number from 1 to SD_SIZE
        for i in range(SD_DIM):
            for j in range(SD_DIM):
                for n in range(1, SD_SIZE+1):
                    for k in range(SD_DIM):
                        for l in range(SD_DIM):
                            text += str(encode(3*i+k, 3*j+l, n)) + " "
                    text += "0\n"
                    num_clause += 1

        # initial setup for pre-filled spots
        domains = init_domains()
        restrict_domain(domains, problem)
        for i, j in domains:
            if len(domains[(i, j)]) == 1:
                n = domains[(i, j)][0]
                text += str(encode(i, j, n)) + " 0\n"
                num_clause += 1

        title = "p cnf " + str(SD_SIZE**3) + " " + str(num_clause) + "\n"
        text = title + text

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains
        
        # TODO: delete this ->
        # domains = {}
        # for spot in sd_spots:
        #     domains[spot] = [1]
        # return domains
        # <- TODO: delete this

        def decode(s):
            s = s - 1
            n = s % SD_SIZE + 1
            s = s // SD_SIZE
            j = s % SD_SIZE
            s = s // SD_SIZE
            i = s % SD_SIZE
            return i, j, n

        domains = {}
        true_list = [s for s in assignments if assignments[s] == True]
        for s in true_list:
            i, j, n = decode(s)
            domains[(i, j)] = [n]

        return domains