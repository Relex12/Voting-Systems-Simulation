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

def score_voting(distances, scale_size, threshold):
    results = {c: [0 for i in range(0, scale_size)] for c in distances[0]}
    for c in distances[0]:
        for v in distances:
            for i in range(0, scale_size-1):
                if i*threshold/(scale_size-1) < distances[v][c] <= (i+1)*threshold/(scale_size-1):
                    results[c][i] +=1
            if distances[v][c] > threshold:
                results[c][scale_size-1] += 1
    return results

def approval (distances, threshold):
    scale = 2
    results = score_voting(distances, scale, threshold)
    winner = [c for c in distances[0] if results[c][0] == max([results[c][0] for c in distances[0]])]
    if len(winner) == 1:
        return winner[0]

def majority_jugement (distances, threshold):
    scale = 6
    results = score_voting(distances, scale, threshold)
    cumulative = {c: [sum(results[c][:i+1]) for i in range(0, scale)] for c in results}
    majority_mentions = {c: i for i in range(scale-1, -1, -1) for c in results if cumulative[c][i] > len(distances)/2}
    winners = [c for c in majority_mentions if majority_mentions[c] == min([majority_mentions[c] for c in majority_mentions])]
    if majority_mentions[winners[0]] != scale-1:
        opposants = {c: sum(results[c][majority_mentions[c]+1:]) for c in winners}
        winners = [c for c in winners if opposants[c] == min([opposants[c] for c in winners])]
        if len(winners) == 1:
            return winners[0]
    partisants = {c: sum(results[c][:majority_mentions[c]]) for c in winners}
    winners = [c for c in winners if partisants[c] == max([partisants[c] for c in winners])]
    if len(winners) == 1:
        return winners[0]
