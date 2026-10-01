from dataclasses import dataclass

@dataclass(frozen=True)
class Term:
    concept: str
    language: str
    text: str
    definition: str = ''
    source: str = ''

class Terminology:
    def __init__(self, terms=()): self._terms=list(terms)
    def add(self, term): self._terms.append(term)
    def find(self, concept, language): return tuple(t for t in self._terms if t.concept==concept and t.language.lower()==language.lower())
    def translate(self, concept, language):
        matches=self.find(concept,language)
        return matches[0].text if matches else None

DEFAULT_TERMS=Terminology([
 Term('atom','en','atom'), Term('atom','sw','atomi'), Term('atom','ar','ذرة'),
 Term('molecule','en','molecule'), Term('molecule','sw','molekuli'), Term('molecule','ar','جزيء'),
 Term('bond','en','chemical bond'), Term('bond','sw','kifungo cha kemikali'), Term('bond','ar','رابطة كيميائية'),
 Term('reaction','en','chemical reaction'), Term('reaction','sw','mmenyuko wa kemikali'), Term('reaction','ar','تفاعل كيميائي'),
 Term('equilibrium','en','chemical equilibrium'), Term('equilibrium','sw','usawaziko wa kemikali'), Term('equilibrium','ar','اتزان كيميائي'),
])
