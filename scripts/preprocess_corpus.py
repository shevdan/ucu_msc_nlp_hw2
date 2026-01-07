#!/usr/bin/env python3
import argparse
import re
from pathlib import Path
from tqdm import tqdm


def normalize_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # collapse multiple whitespaces into single space
    text = re.sub(r'[^\sа-яіїєґa-z0-9.,!?;:\'\"\-—–()«»""„]', '', text)  # keep only allowed chars: cyrillic, latin, digits, punctuation
    text = re.sub(r'[—–]', '-', text)  # normalize em/en dashes to hyphen
    return text.strip()


def process_corpus(input_path, output_path, max_lines=None):
    print(f"Processing: {input_path}")
    print(f"Output: {output_path}")

    line_count = 0
    valid_lines = 0

    with open(input_path, 'r', encoding='utf-8') as f_in, \
         open(output_path, 'w', encoding='utf-8') as f_out:

        for line in tqdm(f_in, desc="Processing"):
            if max_lines and line_count >= max_lines:
                break

            line = line.strip()
            if not line:
                continue

            normalized = normalize_text(line)
            words = normalized.split()

            if len(words) < 3 or len(words) > 200:
                line_count += 1
                continue

            f_out.write(normalized + '\n')
            valid_lines += 1
            line_count += 1

    print(f"Processed {line_count} lines, kept {valid_lines}")
    return valid_lines


def create_subset(input_path, output_path, fraction):
    print(f"Creating {round(fraction*100)}% subset...")

    with open(input_path, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)

    target_lines = int(total_lines * fraction)

    with open(input_path, 'r', encoding='utf-8') as f_in, \
         open(output_path, 'w', encoding='utf-8') as f_out:
        for i, line in enumerate(f_in):
            if i >= target_lines:
                break
            f_out.write(line)

    print(f"Created {target_lines} lines at {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True)
    parser.add_argument('--output', '-o', required=True)
    parser.add_argument('--max-lines', type=int, default=None)
    parser.add_argument('--create-subsets', action='store_true')
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    main_corpus = output_dir / 'corpus_full.txt'
    process_corpus(args.input, str(main_corpus), args.max_lines)

    if args.create_subsets:
        for fraction in [0.1, 0.25, 0.5]:
            subset_path = output_dir / f'corpus_{int(fraction*100)}pct.txt'
            create_subset(str(main_corpus), str(subset_path), fraction)


if __name__ == '__main__':
    main()
