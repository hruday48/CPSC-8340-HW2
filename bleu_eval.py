import math
import operator
import sys
def count_ngram(candidate, references, n):
    clipped_count = 0
    count = 0
    r = 0
    c = 0
    for si in range(len(candidate)):
        ref_counts = []
        ref_lengths = []
        for reference in references:
            ref_sentence = reference[si]
            ngram_d = {}
            words = ref_sentence.strip().split()
            ref_lengths.append(len(words))
            limits = len(words) - n + 1
            for i in range(limits):
                ngram = ' '.join(words[i:i+n]).lower()
                if ngram in ngram_d.keys():
                    ngram_d[ngram] += 1
                else:
                    ngram_d[ngram] = 1
            ref_counts.append(ngram_d)
        cand_sentence = candidate[si]
        cand_dict = {}
        words = cand_sentence.strip().split()
        limits = len(words) - n + 1
        for i in range(0, limits):
            ngram = ' '.join(words[i:i + n]).lower()
            if ngram in cand_dict:
                cand_dict[ngram] += 1
            else:
                cand_dict[ngram] = 1
        clipped_count += clip_count(cand_dict, ref_counts)
        count += limits
        r += best_length_match(ref_lengths, len(words))
        c += len(words)
    if clipped_count == 0:
        pr = 0
    else:
        pr = float(clipped_count) / count
    bp = brevity_penalty(c, r)
    return pr, bp


def clip_count(cand_d, ref_ds):
    count = 0
    for m in cand_d.keys():
        m_w = cand_d[m]
        m_max = 0
        for ref in ref_ds:
            if m in ref:
                m_max = max(m_max, ref[m])
        m_w = min(m_w, m_max)
        count += m_w
    return count


def best_length_match(ref_l, cand_l):
    least_diff = abs(cand_l-ref_l[0])
    best = ref_l[0]
    for ref in ref_l:
        if abs(cand_l-ref) < least_diff:
            least_diff = abs(cand_l-ref)
            best = ref
    return best


def brevity_penalty(c, r):
    if c > r:
        bp = 1
    else:
        bp = math.exp(1-(float(r)/c))
    return bp


def geometric_mean(precisions):
    return (reduce(operator.mul, precisions)) ** (1.0 / len(precisions))


def BLEU_new(predict_sentence, ground_true):

    pre = predict_sentence.strip()
    ref = ground_true.strip()
    print 'reference =>', ref
    c = len(pre.split(' ')) * 1.
    r = len(ref.split(' '))
    bp = 1. if c >= r else math.exp(1 - r/c)
    ref = ref.lower().replace('.', '').replace(',', '').split(' ')
    correct = 0.

    for word in pre.lower().split(' '):
        if word in ref:
            correct += 1
            i = ref.index(word)
            del ref[i]

    print "Score", bp * (correct/c)
    return bp * (correct/c)

def BLEU(predict_sentence, ground_true):

    score = 0.  
    count = 0
    try: 
        print 'ground_true =>', ground_true
        count += 1
        candidate = [predict_sentence.strip()]
        references = [ground_true.strip()]
        precisions = []
        pr, bp = count_ngram(candidate, references, 1)
        precisions.append(pr)
        score = geometric_mean(precisions) * bp
        print "Score", score
        return score / count
    except:
        print "Usage: python bleu_eval.py <candidate_sentence> <reference_sentence>"
