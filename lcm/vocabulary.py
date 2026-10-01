"""Language vocabulary used by the deterministic chemistry parser."""
TERMS={
'en':{'what is':'lookup','balance':'balance','reaction':'reaction','oxidation state':'oxidation','molar mass':'molar_mass','titration':'titration','equilibrium':'equilibrium'},
'sw':{'ni nini':'lookup','sawazisha':'balance','mmenyuko':'reaction','hali ya oksidishaji':'oxidation','uzito wa moli':'molar_mass','titration':'titration','usawaziko':'equilibrium'},
'ar':{'ما هو':'lookup','وازن':'balance','تفاعل':'reaction','حالة الأكسدة':'oxidation','الكتلة المولية':'molar_mass','معايرة':'titration','اتزان':'equilibrium'}
}

def detect_language(text):
    low=text.lower()
    for lang,terms in TERMS.items():
        if any(k in low for k in terms): return lang
    return 'en'

def classify(text):
    lang=detect_language(text); low=text.lower()
    for key,intent in TERMS[lang].items():
        if key in low: return intent
    return 'unknown'
