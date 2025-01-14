import json

from session_helper import *


def matprint(mat, fmt="g"):
    mat = np.around(mat, decimals=2)
    col_maxes = [max([len(("{:"+fmt+"}").format(x)) for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:"+str(col_maxes[i])+fmt+"}").format(y), end="  ")
        print("")


def show_state_action_tuple(state_action_tuple):
    print('Timeslot: ' + str(state_action_tuple.timeslot))
    print("")
    print('Xs:')
    matprint(state_action_tuple.Xs)
    print("")
    print('Action taken:')
    print(state_action_tuple.us)
    print("")
    print('resulting_Xs:')
    matprint(state_action_tuple.resulting_Xs)
    print("")
    print('Cost:')
    print(state_action_tuple.cost)
    print("")
    print('PV:')
    print(state_action_tuple.pv)
    print("")
    print('Next PV:')
    print(state_action_tuple.next_pv)
    print("")
    print('Next timeslot: ' + str(state_action_tuple.next_timeslot))
    print("")
    print("")
    print("")


class StateActionTuple():
    def __init__(self, state_action):
        self.timeslot = state_action['timeslot']
        self.Xs = np.reshape(state_action['Xs'], (Smax, Smax))
        self.us = state_action['us']
        self.resulting_Xs = np.reshape(state_action['resulting_Xs'], (Smax, Smax))
        self.cost = state_action['cost']
        self.next_timeslot = state_action['next_timeslot']
        self.pv = state_action['pv']
        self.next_pv = state_action['next_pv']

    def is_equal(self, state_action_tuple):
        return (self.timeslot == state_action_tuple.timeslot and
                np.array_equal(self.Xs, state_action_tuple.Xs) and
                self.us == state_action_tuple.us and
                self.pv == state_action_tuple.pv and
                self.next_pv == state_action_tuple.next_pv)


class Trajectory:
    def __init__(self, state_action_tuple):
        self.start = state_action_tuple.timeslot
        self.end = state_action_tuple.next_timeslot
        self.trajectory = [state_action_tuple]

    def add_state_action(self, state_action_tuple):
        self.trajectory.append(state_action_tuple)
        self.end = state_action_tuple.next_timeslot

    def remove_state_actions(self, n):
        self.trajectory = self.trajectory[: len(self.trajectory) - n]


def get_organized_trajectories(state_action_tuples):
    trajectories = []
    current_trajectory = Trajectory(state_action_tuples.pop(0))

    for state_action_tuple in state_action_tuples:

        if state_action_tuple.timeslot == current_trajectory.end:
            current_trajectory.add_state_action(state_action_tuple)

        else:
            difference = current_trajectory.end - state_action_tuple.timeslot
            current_trajectory.remove_state_actions(difference)
            current_trajectory.add_state_action(state_action_tuple)

        if state_action_tuple.timeslot == Smax:
            trajectories.append(current_trajectory.trajectory)

    return trajectories


def show_organized_trajectories(organized_trajectories):
    for trajectory in organized_trajectories:
        print('')
        print('')
        print('')
        print('NEW TRAJECTORY')
        print('')
        for state_action_tuple in trajectory:
            show_state_action_tuple(state_action_tuple)


def get_unique_state_action_tuples(state_action_tuples):
    unique_list = []

    for i in range(len(state_action_tuples)):
        elem = state_action_tuples[i]
        found = False
        j = i
        while not found and j < len(state_action_tuples):
            elem2 = state_action_tuples[j]

            if i != j and elem.is_equal(elem2):
                found = True

            j += 1

        if not found:
            unique_list.append(elem)

    return unique_list


def get_accumulated_cost(trajectory):
    
    return functools.reduce(lambda acc, state_action_tuple:
                            acc + state_action_tuple.cost[0], trajectory, 0)


#json_to_be_beautified = json.loads(open('../../../datasets/Trajectories/all/trajectories_2018-08-18.json').read())
#state_actions = json_to_be_beautified['trajectories']
#state_action_tuples = [StateActionTuple(state_action) for state_action in state_actions]

#for state_action_tuple in state_action_tuples:
#    show_state_action_tuple(state_action_tuple)

#unique_state_action_tuples = get_unique_state_action_tuples(state_action_tuples)
#print('Unique state action tuples: ' + str(len(unique_state_action_tuples)))

#for state_action_tuple in unique_state_action_tuples:
#    show_state_action_tuple(state_action_tuple)

#organized_trajectories = get_organized_trajectories(state_action_tuples)
#print(organized_trajectories)
#show_organized_trajectories(organized_trajectories)
#print('Number of trajectories: ' + str(len(organized_trajectories)))
