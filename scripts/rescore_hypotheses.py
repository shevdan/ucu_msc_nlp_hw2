import argparse
import json
import re

import kenlm
from tqdm import tqdm


def load_hypotheses(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data


def normalize_for_scoring(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # collapse multiple whitespaces into single space
    text = re.sub(r'[—–]', '-', text)  # normalize em/en dashes to hyphen
    return text.strip()


def sentence_logprob(model, sentence, unigram_only=False):
    if unigram_only:
        total = 0.0
        for word in sentence.split():
            total += model.score(word, bos=False, eos=False)
        return total
    return model.score(sentence, bos=True, eos=True)


def sentence_perplexity(model, sentence, unigram_only=False):
    logprob = sentence_logprob(model, sentence, unigram_only=unigram_only)
    num_words = len(sentence.split())
    if num_words == 0:
        return float('inf')
    return 10 ** (-logprob / num_words)


def select_best_hypothesis(model, hypotheses, unigram_only=False):
    best_idx, best_hyp, best_ppl = 0, hypotheses[0], float('inf')

    for idx, hyp in enumerate(hypotheses):
        ppl = sentence_perplexity(model, normalize_for_scoring(hyp), unigram_only)
        if ppl < best_ppl:
            best_ppl = ppl
            best_idx = idx
            best_hyp = hyp

    return best_idx, best_hyp, best_ppl




def evaluate(model, data, verbose=False, unigram_only=False):
    correct = 0
    results = []

    for record in tqdm(data, desc="Evaluating"):
        ref = record['reference']
        hypotheses = record['hypotheses']

        best_idx, best_hyp, best_ppl = select_best_hypothesis(model, hypotheses, unigram_only)

        is_correct = ref.strip() == best_hyp.strip()

        if is_correct:
            correct += 1

        results.append({
            'utt_id': record['utt_id'],
            'reference': ref,
            'selected': best_hyp,
            'selected_idx': best_idx,
            'perplexity': best_ppl,
            'correct': is_correct
        })

        if verbose and not is_correct:
            print(f"\n--- {record['utt_id']} ---")
            print(f"Reference: {ref}")
            print(f"Selected:  {best_hyp}")

    return {
        'accuracy': correct / len(data),
        'correct': correct,
        'total': len(data),
        'results': results
    }
