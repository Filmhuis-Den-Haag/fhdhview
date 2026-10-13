from pathlib import Path

from fdhview.services.screenwriter.schema import AAMPos


def read_xml():
    # xml = Path('tests/data/ScreenWriter_202608181146.xml').read_text()
    xml = Path('tests/data/minimal.xml').read_text()
    data = AAMPos.from_xml(xml)

    unique_tags = set()
    unique_screen = set()

    for session in data.sessions.root:
        for tag in session.attributes:
            unique_tags.add(tag)

    print(f'Unique tags: {unique_tags}')


    for session in data.sessions.root:
        unique_screen.add(session.screen_identifier)
    print(f'Unique screen: {unique_screen}')


    for session in data.sessions.root:
        print(f'Session start: {session.start}, end: {session.end}')


read_xml()
