def meaning(scores):
    if len(scores)==1:
        return scores[0]
    elif len(scores)==0:
        return 0
    else:
        new_scores=[]
        for i in range(len(scores)-1):
            if scores[i]>0 and scores[i+1]>0:
                new_scores.append(scores[i]*scores[i+1])
            elif scores[i]<0 and scores[i+1]!=0:
                new_scores.append(scores[i]*scores[i+1]*(-1))
            elif scores[i]>0 and scores[i+1]<0:
                new_scores.append(scores[i]*scores[i+1])
        print(new_scores)
        return meaning(new_scores)

print(meaning([-1,0,1,-1,-1,1]))
