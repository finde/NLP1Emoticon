import numpy as np

# decoding using viterbi algorithm
def decoding(observations, transition, emission, states=None):

    if states == None:
        states = emission.keys()

    V = {}
    path = {}
    observation_length = len(observations)

    # first calculation
    # from start symbol to observations[0]
    for state in states:
        V[state] = {}
        V[state][observations[0]] = transition["start"][state] * emission[state][observations[0]]
        path[state] = [state]

    # from observations[1] until observations[n]
    for t in range(1, observation_length):
        new_path = {}

        for state_i in states:
            temp = ()

            for state_j in states:
                temp_value = (V[state_j][observations[t - 1]] * transition[state_j][state_i] * emission[state_i][observations[t]], state_j)
                temp += (temp_value,)

            max_value, opt_state = max(temp)
            V[state_i][observations[t]] = max_value
            new_path[state_i] = path[opt_state] + [state_i]

        # update path, key is the latest column_t
        path = new_path

    # last calculation
    # from observations[n] to end symbol
    temp = ()
    for state in states:
        temp_value = (V[state][observations[len(observations) - 1]] * transition[state]["start"], state)
        temp += (temp_value,)

    # get final score and final path
    final_score, opt_state = max(temp)
    final_path = path[opt_state]

    return final_score, final_path

if __name__ == "__main__":
    states = ["N", "M", "V", "D"]
    observations = ["John", "carried", "a", "tin", "can"]

    transition_probability = {
            "start": {"start": 0.0, "N": 0.5, "M": 0.0, "V": 0.1, "D": 0.4},
            "N": {"start": 0.2, "N": 0.2, "M": 0.3, "V": 0.3, "D": 0.0},
            "M": {"start": 0.0, "N": 0.0, "M": 0.0, "V": 1.0, "D": 0.0},
            "V": {"start": 0.1, "N": 0.3, "M": 0.3, "V": 0.0, "D": 0.3},
            "D": {"start": 0.0, "N": 1.0, "M": 0.0, "V": 0.0, "D": 0.0}
            }

    emission_probability = {
            "N": {"John": 0.01, "carried": 0.0, "a": 0.0, "tin": 0.05, "can": 0.01},
            "M": {"John": 0.0, "carried": 0.0, "a": 0.0, "tin": 0.0, "can": 0.2},
            "V": {"John": 0.0, "carried": 0.02, "a": 0.0, "tin": 0.0, "can": 0.0},
            "D": {"John": 0.0, "carried": 0.0, "a": 0.5, "tin": 0.0, "can": 0.0}
            }

    final_score, final_path = decoding(
            #states,
            observations = observations,
            transition = transition_probability,
            emission = emission_probability
            )

    print final_score
    print final_path
