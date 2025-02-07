num_of_ingredients, num_of_bases, num_of_questions = map(int, input().split())

price_to_add = [0 for i in range(num_of_ingredients)]
price_to_remove = [0 for i in range(num_of_ingredients)]
for i in range(num_of_ingredients):
    price_to_add[i], price_to_remove[i] = map(int, input().split())

base_sizes = [0 for i in range(num_of_bases)]
bases = [[0 for j in range(num_of_ingredients)] for i in range(num_of_bases)]
for i in range(num_of_bases):
    base_sizes[i] = int(input())
    bases[i] = list(map(int, input().split()))

goal_sizes = [0 for i in range(num_of_questions)]
goals = [[0 for j in range(num_of_ingredients)] for i in range(num_of_questions)]
for i in range(num_of_questions):
    goal_sizes[i] = int(input())
    goals[i] = list(map(int, input().split()))


def get_cost(base, goal):
    cost = 0
    #print(f'base: {base}')
    for i, ingredient in enumerate(base):
        if ingredient not in goal:
            cost += price_to_remove[ingredient]
            #print(f"-{base[i]}")

    was_counted = []
    for ingredient in goal:
        if ingredient not in was_counted:
            base_count = base.count(ingredient)
            goal_count = goal.count(ingredient)

            if base_count == goal_count:
                pass
            elif goal_count< base_count:
                cost += price_to_remove[ingredient] * (base_count-goal_count)
                #print(f"-{base_count-goal_count}* {ingredient}")
            else:
                cost += price_to_add[ingredient] * (base_count+goal_count)
                #print(f"+{base_count+goal_count}* {ingredient}")

    #print(f'goal: {goal}')
    #print(cost)
    #print()
    return cost

def get_winner_cost(goal):
    #print("\n")
    costs = [get_cost(base, goal) for base in bases]
    return min(costs)

#print()
#print(f'prices to add:    {price_to_add}')
#print(f'prices to remove: {price_to_remove}')
#print(f'bases: {bases}')
#print(f'goals: {goals}')
#print()
#print()
for goal in goals:
    print(get_winner_cost(goal))
