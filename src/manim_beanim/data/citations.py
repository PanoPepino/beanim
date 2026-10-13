"""BibTeX parsing; importing equation tools does not require Pybtex or Manim."""
import logging
logger = logging.getLogger(__name__)

def parse_citations(bib_file, your_family_name='', initials=''):
    """Return formatted author/year citations keyed by BibTeX identifier."""
    from pybtex.database import parse_file
    bib = parse_file(str(bib_file))
    citations = {}
    for key, entry in bib.entries.items():
        names = [initials if person.last_names == [your_family_name] else ' '.join(person.last_names) for person in entry.persons.get('author', [])]
        year = entry.fields.get('year')
        if year is None:
            logger.warning('Citation %s has no year', key)
            year = 'add manually'
        names.append(year.strip())
        citations[key] = '[' + ', '.join(names) + ']'
    return citations
