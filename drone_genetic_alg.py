import random

def_p_mutation = 0.3
def_MutationAmount = 2.0
def_MutationThreshold = 0.01

def_p_swap = 0.6
def_initParamMax = 1.0
def_initParamMin = -1.0

genCount = 0
popSize = 0


Running = False
PopSorted = False

class GeneticAlgorithm:
# MUTATION OPERATORS 
    def mutateGenotype(self, genotype, p_mutation, mutationAmount):
        for i in range(len(genotype.parameterCount)):
            # If randomly generated probability is less than mutation probability threshold:
            if random.uniform(0, 1) < p_mutation:
                genotype[i] += (random.uniform(0, 1)*(mutationAmount*2) - mutationAmount)


    # Takes in a list of genotypes (constituting a population) 
    def mutateGeneration(self, newPopulation):
        for genotype in newPopulation: 
            if random.uniform(0, 1) < def_MutationThreshold:
                mutateGenotype(genotype, def_p_mutation, def_MutationAmount)


    # Randomly swaps parent and child features (genetic recombination)
    def crossover(self, parent1, parent2, p_swap):
        parameterCount = parent1.parameterCount
        off1_params = []
        off2_params = []

        for i in range(len(parameterCount)):
            if random.uniform(0, 1) < p_swap:
                off1_params[i] = parent2[i]
                off2_params[i] = parent1[i]
            else:
                off1_params[i] = parent1[i]
                off2_params[i] = parent2[i]
        
        # Instantiate new Genotype class 
        child1 = Genotype(off1_params)
        child2 = Genotype(off2_params)
        return child1, child2

    def recombination(self, intermediatePop, newPopSize):
        if len(intermediatePop) < 2:
            raise Exception("Intermediate population size must be greater than 2.")
        else:
            newPop = []
            while len(newPop) < newPopSize:
                child1, child2 = crossover(intermediatePop[0], intermediatePop[1], def_p_swap)
                newPop.append(child1)

                if len(newPop) < newPopSize:
                    newPop.append(child2)
        
        return newPop
    
    # From current generation, select 3 best candidates for intermediate population. 
    def selectCandidates(self, currentPop):
        return currentPop[:3]

    def calculateFitness(self, currentPop):
        overall_performance = 0
        for genotype in currentPop:
            overall_performance += genotype.Performance
        
        avg_performance = overall_performance / len(currentPop)
        
        for genotype in currentPop:
            genotype.Fitness = genotype.Performance / avg_performance

    # Initialize population (list of genotypes)
    def initializePopulation(self, pop):
        for genotype in pop:
            genotype.randomInitParams(def_initParamMin, def_initParamMax) 
        
        genCount = 1
        PopSorted = True
        Running = True
    
    # Initialize new algorithm instance 
    def newGenAlg(self, popSize):
        currentPop = [];
        for i in range(len(popSize)):
                genotype = Genotype()
            currentPop.append(genotype)

    def Start(self):
        Running = True
        initializePopulation(currentPop)
        Evaluate(currentPop)
    
    def PostEval(self, currentPop):
        calculateFitness(currentPop)

        if PopSorted == False:
            sortPopulation(currentPop)

        if TerminationCriteria:
            terminate(self)
        
        topCandidates = selectCandidates(currentPop)
        newPop = recombination(topCandidates, popSize)
        mutateGeneration(newPop)
        currentPop = newPop
        genCount += 1
        Evaluate(currentPop)
    
    def Evaluate(self, currentPop):
        return 
    
    def terminate(self):
        Running = False



    
    
            

    



