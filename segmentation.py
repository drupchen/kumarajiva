from pathlib import Path
import re

from botok import Text

def chinese_tokenizer(text):
    """Tokenizes string on Chinese punctuation: 。！？
    """
    punct_regex = r'([。！？])'
    parts = re.split(punct_regex, text.replace('\n', ''))
    i = 0
    while i < len(parts):
        p = parts[i]
        if i >= 0 and p in '。！？':
            parts[i-1] += p
            del parts[i]
        i += 1
    return parts

def chinese_format(sents, sep="\n"):
    tokens = [t.replace(" ", "_") for t in sents]
    return sep.join(tokens)

def segment():
    for f in in_files.rglob('*.txt'):
        print('processing:', f)
        if f.parts[1] == 'chinese':
            out = out_files / Path('/'.join(f.parts[1:]))
            out.parent.mkdir(parents=True, exist_ok=True)

            t = Text(f, out_file=out)
            t.custom_pipeline("basic_cleanup", chinese_tokenizer, "dummy", chinese_format)

        elif f.parts[1] == 'tibetan':
            out = out_files / Path('/'.join(f.parts[1:]))
            out.parent.mkdir(parents=True, exist_ok=True)

            t = Text(f, out_file=out)
            t.custom_pipeline("basic_cleanup", "sentence_tok", "dummy", "plaintext_sent_par")


if __name__ == '__main__':
    in_files = Path('to_segment')
    if not in_files.is_dir():
        in_files.mkdir()
        (in_files / 'tibetan').mkdir()
        (in_files / 'chinese').mkdir()
    out_files = Path('segmented')
    if not out_files.is_dir():
        out_files.mkdir()
    segment()