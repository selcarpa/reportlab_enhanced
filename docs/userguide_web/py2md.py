#!/usr/bin/env python
"""Convert ReportLab UserGuide Python-DSL chapter files to Markdown."""

import os
import re
import sys

CHAPTER_ORDER = [
    'ch1_intro', 'ch2_graphics', 'ch2a_fonts', 'ch3_pdffeatures',
    'ch4_platypus_concepts', 'ch5_paragraphs', 'ch6_tables', 'ch7_custom',
    'graph_intro', 'graph_concepts', 'graph_charts', 'graph_shapes',
    'graph_widgets', 'app_demos',
]


class NumberingState:
    def __init__(self):
        self.chapter = 0
        self.section = 0
        self.figure = 0
        self.list_counter = 0

    def next_chapter(self):
        self.chapter += 1
        self.section = 0
        self.figure = 0
        return self.chapter

    def next_section(self):
        self.section += 1
        return self.section

    def next_figure(self):
        self.figure += 1
        return self.figure

    def next_list_item(self):
        self.list_counter += 1
        return self.list_counter

    def reset_list(self):
        self.list_counter = 0


def convert_markup(text):
    if not text:
        return text
    text = text.replace('\\$', '\x00DOLLAR\x00')
    text = text.replace('\\^', '\x00CARET\x00')
    text = re.sub(r'\$([^$]+)\$', r'`\1`', text)
    text = re.sub(r'\^([^^]+)\^', r'*\1*', text)
    text = text.replace('\x00DOLLAR\x00', '$')
    text = text.replace('\x00CARET\x00', '^')
    text = re.sub(r'<b>(.*?)</b>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<i>(.*?)</i>', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'<super>(.*?)</super>', r'<sup>\1</sup>', text, flags=re.DOTALL)
    text = re.sub(r'<sub>(.*?)</sub>', r'<sub>\1</sub>', text, flags=re.DOTALL)
    text = re.sub(r'<a\s+href=["\']([^"\']*)["\']>(.*?)</a>', r'[\2](\1)', text, flags=re.DOTALL)
    text = re.sub(r'<font[^>]*>(.*?)</font>', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'<nobr>(.*?)</nobr>', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'<para[^/]*?/>', '', text)
    text = re.sub(r'<seq[^/]*/>', '', text)
    text = re.sub(r'<seq[^>]*>.*?</seq>', '', text, flags=re.DOTALL)
    text = re.sub(r'<bullet>.*?</bullet>', '', text, flags=re.DOTALL)
    text = re.sub(r'<br\s*/?>', '  \n', text)
    text = re.sub(r'<greek>(.*?)</greek>', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'</?(?:para|bullet|font|nobr|greek|seq)[^>]*>', '', text)
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '"')
    return text


class MarkdownWriter:
    def __init__(self):
        self.lines = []
        self.num = NumberingState()

    def _emit(self, text):
        self.lines.append(text)

    def _emit_blank(self):
        self.lines.append('')

    def heading1(self, text):
        n = self.num.next_chapter()
        self._emit(f'# {convert_markup(text)}')
        self._emit_blank()

    def heading2(self, text):
        s = self.num.next_section()
        self._emit(f'## {self.num.chapter}.{s} {convert_markup(text)}')
        self._emit_blank()

    def heading3(self, text):
        self._emit(f'### {convert_markup(text)}')
        self._emit_blank()

    def heading4(self, text):
        self._emit(f'#### {convert_markup(text)}')
        self._emit_blank()

    def Appendix1(self, text):
        letter = chr(ord('A') + self.num.chapter)
        self.num.chapter += 1
        self._emit(f'# Appendix {letter}: {convert_markup(text)}')
        self._emit_blank()

    def disc(self, text):
        self._emit(convert_markup(text))
        self._emit_blank()

    def eg(self, text, before=0.1, after=0, **kw):
        code = text.strip('\n')
        self._emit(f'```python\n{code}\n```')
        self._emit_blank()

    def npeg(self, text, before=0.1, after=0):
        code = text.strip('\n')
        self._emit(f'```\n{code}\n```')
        self._emit_blank()

    def bullet(self, text):
        self._emit(f'- {convert_markup(text)}')
        self._emit_blank()

    def list1(self, text, doBullet=1):
        n = self.num.next_list_item()
        self._emit(f'{n}. {convert_markup(text)}')
        self._emit_blank()

    def restartList(self):
        self.num.reset_list()

    def EmbeddedCode(self, code, name='t'):
        stripped = code.strip('\n')
        self._emit(f'```python\n{stripped}\n```')
        self._emit_blank()
        self._emit('*Produces:*')
        self._emit('<!-- output placeholder -->')
        self._emit_blank()

    def illust(self, operation, caption, width=None, height=None):
        n = self.num.next_figure()
        self._emit(f'<!-- Figure {self.num.chapter}-{n}: {convert_markup(caption)} -->')
        self._emit_blank()

    def draw(self, drawing, caption):
        n = self.num.next_figure()
        self._emit(f'<!-- Figure {self.num.chapter}-{n}: {convert_markup(caption)} -->')
        self._emit_blank()

    def parabox(self, text, style, caption):
        n = self.num.next_figure()
        self._emit(f'<!-- Figure {self.num.chapter}-{n}: {convert_markup(caption)} -->')
        self._emit(f'```python\n{text}\n```')
        self._emit('<!-- style rendering placeholder -->')
        self._emit_blank()

    def parabox2(self, text, caption):
        n = self.num.next_figure()
        self._emit(f'<!-- Figure {self.num.chapter}-{n}: {convert_markup(caption)} -->')
        self._emit(f'```html\n{text}\n```')
        self._emit('<!-- rendering placeholder -->')
        self._emit_blank()

    def image(self, path, width=None, height=None):
        self._emit(f'![image]({path})')
        self._emit_blank()

    def todo(self, text):
        self._emit(f'> **TODO:** {convert_markup(text)}')
        self._emit_blank()

    def centred(self, text):
        self._emit(f'<center>{convert_markup(text)}</center>')
        self._emit_blank()

    def caption(self, text):
        self._emit(f'*{convert_markup(text)}*')
        self._emit_blank()

    def CPage(self, inches):
        pass

    def newPage(self):
        self._emit('---')
        self._emit_blank()

    def nextTemplate(self, templName):
        pass

    def space(self, inches=1./6):
        pass

    def title(self, text):
        pass

    def headingTOC(self, text=None):
        pass

    def pencilnote(self):
        self._emit('<!-- pencil note annotation -->')
        self._emit_blank()

    def handnote(self, xoffset=0, size=None, fillcolor=None, strokecolor=None):
        self._emit('<!-- hand note annotation -->')
        self._emit_blank()

    def get_output(self):
        return '\n'.join(self.lines)


def resolve_chapter_files(chapter_dir, name):
    single = os.path.join(chapter_dir, f'{name}.py')
    if os.path.isfile(single):
        return [single]
    files = []
    i = 1
    while True:
        split = os.path.join(chapter_dir, f'{name}_{i}.py')
        if not os.path.isfile(split):
            break
        files.append(split)
        i += 1
    return files


def convert_chapters(lang='en'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.dirname(script_dir)
    top_dir = os.path.dirname(docs_dir)
    sys.path.insert(0, str(top_dir))
    sys.path.insert(0, str(docs_dir))

    userguide_dir = os.path.join(docs_dir, 'userguide')

    if lang != 'en':
        chapter_dir = os.path.join(userguide_dir, lang)
    else:
        chapter_dir = userguide_dir

    output_dir = os.path.join(script_dir, 'docs', lang)
    os.makedirs(output_dir, exist_ok=True)

    writer = MarkdownWriter()
    G = {}

    overrides = {
        'heading1': writer.heading1,
        'heading2': writer.heading2,
        'heading3': writer.heading3,
        'heading4': writer.heading4,
        'Appendix1': writer.Appendix1,
        'disc': writer.disc,
        'eg': writer.eg,
        'npeg': writer.npeg,
        'bullet': writer.bullet,
        'list1': writer.list1,
        'restartList': writer.restartList,
        'EmbeddedCode': writer.EmbeddedCode,
        'illust': writer.illust,
        'draw': writer.draw,
        'parabox': writer.parabox,
        'parabox2': writer.parabox2,
        'image': writer.image,
        'todo': writer.todo,
        'centred': writer.centred,
        'caption': writer.caption,
        'CPage': writer.CPage,
        'newPage': writer.newPage,
        'nextTemplate': writer.nextTemplate,
        'space': writer.space,
        'title': writer.title,
        'headingTOC': writer.headingTOC,
        'pencilnote': writer.pencilnote,
        'handnote': writer.handnote,
    }
    G.update(overrides)

    import tools.docco.rl_doc_utils as dsl
    for name, func in overrides.items():
        setattr(dsl, name, func)

    for chapter_name in CHAPTER_ORDER:
        chapter_files = resolve_chapter_files(chapter_dir, chapter_name)
        if not chapter_files:
            print(f'Warning: Chapter not found: {chapter_name}')
            continue

        writer.lines = []
        writer.num.reset_list()

        print(f'Processing: {chapter_name} ({len(chapter_files)} file(s))')

        for fpath in chapter_files:
            with open(fpath, 'r', encoding='utf-8') as f:
                source = f.read()
            exec(source, G, G)

        out_path = os.path.join(output_dir, f'{chapter_name}.md')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(writer.get_output())
        print(f'  Generated: {out_path}')

    _generate_index(output_dir)
    print(f'\nDone. Output in: {output_dir}')


def _generate_index(output_dir):
    lines = ['# ReportLab User Guide', '']
    for chapter_name in CHAPTER_ORDER:
        md_path = os.path.join(output_dir, f'{chapter_name}.md')
        if os.path.isfile(md_path):
            title = chapter_name.replace('_', ' ').replace('graph ', 'Graphics - ').title()
            lines.append(f'- [{title}]({chapter_name}.md)')
    lines.append('')
    index_path = os.path.join(output_dir, 'index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'  Generated: {index_path}')


if __name__ == '__main__':
    lang = 'en'
    if len(sys.argv) > 1 and sys.argv[1] == '--zh-CN':
        lang = 'zh-CN'
    convert_chapters(lang=lang)
