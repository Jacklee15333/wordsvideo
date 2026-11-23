"""配音稿里的英文缩写念全（Don't → Do not），免得配音把缩写念丢、意思弄反"""
import json, re, sys, os
PAIRS = [("can't", 'cannot'), ("Can't", 'Cannot'), ("couldn't", 'could not'), ("Couldn't", 'Could not'), ("don't", 'do not'), ("Don't", 'Do not'),
         ("doesn't", 'does not'), ("Doesn't", 'Does not'), ("didn't", 'did not'), ("Didn't", 'Did not'), ("won't", 'will not'), ("Won't", 'Will not'),
         ("isn't", 'is not'), ("Isn't", 'Is not'), ("aren't", 'are not'), ("wasn't", 'was not'), ("weren't", 'were not'), ("haven't", 'have not'),
         ("hasn't", 'has not'), ("shouldn't", 'should not'), ("wouldn't", 'would not'), ("I'm", 'I am'), ("I've", 'I have'), ("I'll", 'I will'),
         ("you're", 'you are'), ("You're", 'You are'), ("we're", 'we are'), ("We're", 'We are'), ("they're", 'they are'), ("They're", 'They are'),
         ("let's", 'let us'), ("Let's", 'Let us'), ("that's", 'that is'), ("That's", 'That is'), ("what's", 'what is'), ("What's", 'What is'),
         ("there's", 'there is'), ("It's", 'It is'), ("it's", 'it is'), ("You'll", 'You will'), ("you'll", 'you will'),
         ("We'll", 'We will'), ("we'll", 'we will'), ("Here's", 'Here is'), ("here's", 'here is'), ("Who's", 'Who is'), ("who's", 'who is'),
         ("You've", 'You have'), ("you've", 'you have'), ("We've", 'We have'), ("we've", 'we have'), ("There's", 'There is'), ("he's", 'he is'), ("He's", 'He is'), ("she's", 'she is'), ("She's", 'She is')]
for w in sys.argv[1:]:
    p = os.path.expanduser(f'~/wordfilm-work/{w}/brief/plan.json')
    if not os.path.exists(p): continue
    s = open(p, encoding='utf-8').read(); n = 0
    for a, b in PAIRS:
        for q in (a, a.replace("'", '’')):
            n += s.count(q); s = s.replace(q, b)
    if n: open(p, 'w', encoding='utf-8').write(s)
    print(w, n)
