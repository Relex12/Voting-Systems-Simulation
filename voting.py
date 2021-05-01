###############################
# N round first past the post #
###############################

def N_rounds (ranked, turns):
    """
    Function used for **plurality**, **two rounds**, **instant runoff**, **condorcet** and **borda** voting methods.

    *Prototype*:

    * **ranked** (*dict*) : keys are the electors, values are lists of candidates sorted by preferences
    * **turns** (*int*) : current turn (decreasing value)
    * **return** (*int*) : winning candidate

    *Notes*:

    * **N_rounds()** is recursive, the final return type differs from the others, while there are remaining turns

    *Algorithm*:
    ```
    if turns = 0 then
        return the winner
    else
        results <- sorted dictionary
        // keys are the candidates and values are the number of voters for
        // whom this candidate is the favourite
        if the first candidate as more than half of the votes then
            return the winner
        else
            ranked <- dictionary
            // keys are the electors, values are lists of candidates
            // sorted by preferences, last candidate is removed
            return N_rounds(ranked, turns - 1)
    ```
    """
    if turns == 0:
        return ranked[0][0]
    else:
        results = {candidate:  len([elector for elector in ranked if ranked[elector][0] == candidate]) for candidate in ranked[0]}
        results = {candidate: electors for candidate, electors in sorted(results.items(), key=lambda item: item[1], reverse=True)}
        majors = [candidate for candidate in results.keys()][:turns]
        if (results[majors[0]] > len(ranked)/2):
            return majors[0]
        else:
            ranked = {elector: [candidate for candidate in ranked[elector] if candidate in majors] for elector in ranked}
            return N_rounds (ranked, turns-1)

def condorcet(ranked):
    """
    Function used for **condorcet** and **borda** voting methods.

    *Prototype*:

    * **ranked** (*dict*) : keys are the electors, values are lists of candidates sorted by preferences
    * **return** (*int*) : winning candidate

    *Notes*:

    * In equality cases, a recursive call is performed with the winners, as long as we can remove candidates
    * In some cases of a tie, there may not be a winner (*None* returned)

    *Algorithm*:
    ```
    pairs <- list of pair of candidates
    score <- dictionary
    // keys are the candidates, values are the number of duels won
    // by this candidate
    score <- filtered dictionary, only the candidates with the most wins remain
    if there is only one winner then
        return the winner
    else
        subset_ranked <- ranked filtered
        // by weither if the candidate is one of the winners or not
        if there is less candidates in subset_ranked than in ranked then
            return condorcet(subset_ranked)
    ```
    """
    pairs = [(candidateA, candidateB) for candidateA in ranked[0] for candidateB in ranked[0] if candidateA < candidateB]
    victories = {}
    score = {candidate: 0 for candidate in ranked[0]}
    for pair in pairs:
        subset_ranked = {elector: [candidate for candidate in ranked[elector] if candidate in pair] for elector in ranked}
        victories[pair] = N_rounds(subset_ranked, 1)
        score[victories[pair]] += 1
    score = {candidate: score[candidate] for candidate in score if score[candidate] == max([value for key, value in score.items()])}
    if len(score) == 1:
        return [candidate for candidate in score.keys()][0]
    subset_ranked = {elector: [candidate for candidate in ranked[elector] if candidate in [candidate for candidate in score.keys()]] for elector in ranked}
    if sorted(set(subset_ranked[0])) != sorted(set(ranked[0])):
        return (condorcet(subset_ranked))

def borda(ranked):
    """
    Function used for **borda** voting method.

    *Prototype*:

    * **ranked** (*dict*) : keys are the electors, values are lists of candidates sorted by preferences
    * **return** (*int*) : winning candidate

    *Notes*:

    * In equality cases, **condorcet** method is called to decide
    * In some cases of a tie, there may not be a winner (*None* returned)

    *Algorithm*:
    ```
    results <- sorted dictionary
    // keys are the candidates, values are the sum of the points given by the
    // voters for this candidate, electors give as many points as there are
    // candidates to their favorite, then one point less to the second favorite
    results <- filtered dictionary
    // by weither if the candidate has the more points or not
    if there is only one winner then
        return the winner
    else
        subset_ranked <- ranked filtered
        // by weither if the candidate is one of the winners or not
        return condorcet(subset_ranked)
    ```
    """
    results = {candidate: 0 for candidate in ranked[0]}
    number_of_candidates = len(ranked[0])
    for elector in ranked:
        for i in range (0, number_of_candidates):
            results[ranked[elector][i]] += (number_of_candidates - i)
    results = {candidate: electors for candidate, electors in sorted(results.items(), key=lambda item: item[1], reverse=True)}
    results = {candidate: results[candidate] for candidate in results if results[candidate] == max([value for key, value in results.items()])}
    if len(results) == 1:
        return [candidate for candidate in results.keys()][0]
    else:
        subset_ranked = {elector: [candidate for candidate in ranked[elector] if candidate in [candidate for candidate in results.keys()]] for elector in ranked}
        return (condorcet(subset_ranked))

def score_voting(distances, scale_size, threshold):
    """
    Function used for **approval** and **majority judgement** voting methods.

    *Prototype*:

    * **ranked** (*dict*) : keys are the electors, values are dictionaries whose keys are candidates and values are the distance between the elector and the candidate
    * **scale_size** (*int*) : number of areas into which to divide the position space, must be strictly greater than 1
    * **threshold** (*float*) : rejection threshold
    * **return** (*dict*) : keys are the candidates, values are lists indexed by the scores, from the better to the worst, elements of the lists are the number of voters giving this score to the candidate

    *Notes*:

    * If the position space is divided into N areas, there will be N-1 areas below the rejection threshold, and one above
    * As the position space is divided in areas, it doesn't matter if it corresponds to notes or mentions

    *Algorithm*:
    ```
    for each candidate, for each elector
        for i in areas
            if the distance between the two is in this areas then
                results for this candidate for this areas increments
        if the distance is strictly greater than the rejection threshold then
            results for this candidate for the threshold increments
    return results
    ```
    """
    results = {c: [0 for i in range(0, scale_size)] for c in distances[0]}
    for c in distances[0]:
        for e in distances:
            for i in range(0, scale_size-1):
                if i*threshold/(scale_size-1) < distances[e][c] <= (i+1)*threshold/(scale_size-1):
                    results[c][i] +=1
            if distances[e][c] > threshold:
                results[c][scale_size-1] += 1
    return results

def approval (distances, threshold):
    """
    Function used for **approval** voting method.

    *Prototype*:

    * **ranked** (*dict*) : keys are the electors, values are dictionaries whose keys are candidates and values are the distance between the elector and the candidate
    * **threshold** (*float*) : rejection threshold
    * **return** (*int*) : winning candidate

    *Notes*:

    * In some cases of a tie, there may not be a winner (*None* returned)

    *Algorithm*:
    ```pseudo-code
    results <- score_voting(distances, scale=2, threshold)
    winner <- list of candidates with the most votes in the first grade
    if there is only one winner then
        return the winner
    ```
    """
    scale = 2
    results = score_voting(distances, scale, threshold)
    winner = [c for c in distances[0] if results[c][0] == max([results[c][0] for c in distances[0]])]
    if len(winner) == 1:
        return winner[0]

def majority_judgement (distances, threshold):
    """
    Function used for **majority judgement** voting method.

    *Prototype*:

    * **ranked** (*dict*) : keys are the electors, values are dictionaries whose keys are candidates and values are the distance between the elector and the candidate
    * **threshold** (*float*) : rejection threshold
    * **return** (*int*) : winning candidate

    *Notes*:

    * The number of mentions is 6, so there is no "middle mention"
    * The tie-breaking is done by minimizing the number of opponents (i.e the number of electors that gave a lesser mention that the majority mention)
    * The second tie-breaking, if necessary, is done by maximizing the number of supporters (i.e the number of electors that gave a better mention)
    * In some cases of a tie, there may not be a winner (*None* returned)
    * Because of the space of the positions, the majority mention of the best candidates can be the rejection

    *Algorithm*:
    ```
    results <- score_voting(distances, scale=6, threshold)
    cumulative <- dictionary
    // keys are the candidates, values are lists indexed by the mentions, from
    // the better to the worst, elements of the lists are the number of voters
    // giving at least this mention to the candidate
    majority_mentions <- dictionary
    // keys are the candidates, values are the majority mentions
    winner <- list of candidates with the better majority mention
    if the better majority mentions is better than rejection then
        opponents <- dictionary
        // keys are candidates, values are the number of opponents
        winner <- filtered winner
        // by weither if the candidate has the minimum of opponents
        if there is only one winner then
            return the winner
    partisants <- dictionary
    // keys are candidates, values are the number of partisants
    winner <- filtered winner
    // by weither if the candidate has the maximum of partisants
    if there is only one winner then
        return the winner
    ```
    """
    scale = 6
    results = score_voting(distances, scale, threshold)
    cumulative = {c: [sum(results[c][:i+1]) for i in range(0, scale)] for c in results}
    majority_mentions = {c: i for i in range(scale-1, -1, -1) for c in results if cumulative[c][i] > len(distances)/2}
    winners = [c for c in majority_mentions if majority_mentions[c] == min([majority_mentions[c] for c in majority_mentions])]
    if majority_mentions[winners[0]] != scale-1:
        opponents = {c: sum(results[c][majority_mentions[c]+1:]) for c in winners}
        winners = [c for c in winners if opponents[c] == min([opponents[c] for c in winners])]
        if len(winners) == 1:
            return winners[0]
    partisants = {c: sum(results[c][:majority_mentions[c]]) for c in winners}
    winners = [c for c in winners if partisants[c] == max([partisants[c] for c in winners])]
    if len(winners) == 1:
        return winners[0]
