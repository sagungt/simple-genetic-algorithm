import random
import copy
import os
import numpy as np


def genetic(target):
    result = ''
    for i in range(len(target)):
        result += chr(random.randint(32, 126))
    return result


def fitness(genetic, target):
    data = []
    for i, x in enumerate(target):
        data.append(x == genetic[i])
    result = (sum(x == True for x in data) / len(target)) * 100
    return result


def populations(populationsNumber, target):
    result = []
    for x in range(populationsNumber):
        gen = genetic(target)
        poplulation = {'gen': gen, 'fitness': fitness(gen, target)}
        result.append(poplulation)
    return result


def selections(populations):
    result, fitnessData = [], []
    population = populations.copy()
    for i, x in enumerate(population):
        fitnessData.append(x['fitness'])
    for i in range(int(len(population) / 2)):
        mini = fitnessData.index(max(fitnessData))
        result.append(populations[mini])
        del fitnessData[mini]
    return result


def crossover(parent):
    result = []
    child = copy.deepcopy(parent)
    subChild = ''
    cp = round(len(child[0]['gen']) / 2)
    for i, x in enumerate(child):
        if i > 0:
            subChild += child[i - 1]['gen'][:cp]
            subChild += x['gen'][cp:]
            x['gen'] = subChild
            result.append(x)
            subChild = ''
        subChild += child[-1]['gen'][:cp]
        subChild += x['gen'][cp:]
        x['gen'] = subChild
        result.append(x)
        subChild = ''
    return result


def mutations(childs, mRate, target):
    result = []
    child = copy.deepcopy(childs)
    mutant = ''
    for x in child:
        for i, y in enumerate(x['gen']):
            if random.random() <= mRate:
                if y == target[i]:
                    mutant += y
                else:
                    mutant += chr(random.randint(32, 126))
            else:
                mutant += y
        x['gen'] = mutant
        x['fitness'] = fitness(mutant, target)
        mutant = ''
        result.append(x)
    return result


def regeneration(populations, children):
    population = populations.copy()
    fit = []
    for i, x in enumerate(population):
        fit.append(x['fitness'])
    for i in range(len(children)):
        mini = fit.index(min(fit))
        del population[mini]
    for x in children:
        population.append(x)
    return population


def solutions(population):
    best = max(range(len(population)),
               key=lambda index: population[index]['fitness'])
    return population[best]


def termination(isLooping, populations):
    solution = solutions(populations)
    isLooping = False if solution['gen'] == target else True
    return isLooping


def logging(populations, target, solution, generation):
    os.system('cls')
    print('Target\t\t:', target)
    print('Solution\t:', solution['gen'])
    print('Generation\t:', generation)
    for i, x in enumerate(populations):
        print('Gen {0} : {1} | Fitness : {2}%'.format(
            i + 1, x['gen'], x['fitness']))


def simpleGA(target, populationSize, mRate):
    isLooping = True
    generations = 0
    newPopulations = populations(populationSize, target)
    while isLooping:
        parent = selections(newPopulations)
        child = crossover(parent)
        mutant = mutations(child, mRate, target)
        children = mutant.copy()
        newPopulations = regeneration(newPopulations, children)
        generations += 1
        solution = solutions(newPopulations)
        isLooping = termination(isLooping, newPopulations)
        logging(newPopulations, target, solution, generations)


os.system('cls')
target = input('Input Target (String)\t\t: ')
mRate = float(input('Input Mutation Rate (0-1)\t: '))
popNumber = int(input('Input Populations Size\t\t: '))

simpleGA(target, popNumber, mRate)
