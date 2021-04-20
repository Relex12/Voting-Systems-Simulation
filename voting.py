###############################
# N round first past the post #
###############################

def N_rounds (ranked, turns):
    if turns == 0:
        return ranked[0][0]
    else:
        results = {candidate:  len([voter for voter in ranked if ranked[voter][0] == candidate]) for candidate in ranked[0]}
        results = {candidate: voters for candidate, voters in sorted(results.items(), key=lambda item: item[1], reverse=True)}
        majors = [candidate for candidate in results.keys()][:turns]
        if (results[majors[0]] > len(ranked)):
            return majors[0]
        else:
            ranked = {voter: [candidate for candidate in ranked[voter] if candidate in majors] for voter in ranked}
            return N_rounds (ranked, turns-1)

def condorcet(ranked):
    pairs = [(candidateA, candidateB) for candidateA in ranked[0] for candidateB in ranked[0] if candidateA < candidateB]
    victories = {}
    score = {candidate: 0 for candidate in ranked[0]}
    for pair in pairs:
        subset_ranked = {voter: [candidate for candidate in ranked[voter] if candidate in pair] for voter in ranked}
        victories[pair] = N_rounds(subset_ranked, 1)
        score[victories[pair]] += 1
    score = {candidate: score[candidate] for candidate in score if score[candidate] == max([value for key, value in score.items()])}
    if len(score) == 1:
        return [candidate for candidate in score.keys()][0]
    subset_ranked = {voter: [candidate for candidate in ranked[voter] if candidate in [candidate for candidate in score.keys()]] for voter in ranked}
    if sorted(set(subset_ranked[0])) != sorted(set(ranked[0])):
        return (condorcet(subset_ranked))

def borda(ranked):
    results = {candidate: 0 for candidate in ranked[0]}
    number_of_candidates = len(ranked[0])
    for voter in ranked:
        for i in range (0, number_of_candidates):
            results[ranked[voter][i]] += (number_of_candidates - i)
    results = {candidate: voters for candidate, voters in sorted(results.items(), key=lambda item: item[1], reverse=True)}
    results = {candidate: results[candidate] for candidate in results if results[candidate] == max([value for key, value in results.items()])}
    if len(results) == 1:
        return [candidate for candidate in results.keys()][0]
    else:
        subset_ranked = {voter: [candidate for candidate in ranked[voter] if candidate in [candidate for candidate in results.keys()]] for voter in ranked}
        if (len([candidate for candidate in results.keys()]) >= 3):
            print ([candidate for candidate in results.keys()])
        return (condorcet(subset_ranked))
