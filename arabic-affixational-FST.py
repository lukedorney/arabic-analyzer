import nltk
"""
    Fall 2015
    This is a FST that takes Arabic text as input and returns a word segmented
    into its main root + pattern and its affixational morhpological units
    (i.e prefixes and suffixes), along with their meanings. The FST works by 
    first removing vocalization from a word, then in two passes finding these 
    afformentioned units.
    The output of the main function segment() is a a list of lists, ordered
    in the following way: prefix, main word, suffix, and morphological info
    gained from transduction.
"""

def segment(word):
    """ segments a word into its derivational and affixational morphological units"""
    word = remove_vocalization(word)
    word = long_pre_suf_find(word)
    word = short_pre_suf_find(word)
    return word

def remove_vocalization(word):
    """short vowels, case markers, geminate consonant marker removed"""
    vocalizing = ["\u064B","\u064C","\u064D","\u064E","\u064F","\u0650","\u0652","\u0670","\u0651"]
    for v in vocalizing:
        word = word.replace(v, '')
    return word

def long_pre_suf_find(word):
    """separates stem+verbal pattern from suffixes and prefixes of of size 2 or 3
    only from words that are length 5 or more (as the root minimally takes
    up 3 letters and then there could be a length one suffix or prefix)"""
    
    pre_len_3 =['\u0643\u0627\u0644', '\u0628\u0627\u0644','\u0648\u0644\u0644', '\u0648\u0627\u0644']
    pre_len_2 = ['\u0627\u0644', '\u0644\u0644']
    suf_len_3 = ['\u062a\u0645\u0627', '\u0647\u0645\u0627','\u062a\u0627\u0646', '\u062a\u064a\u0646','\u0643\u0645\u0627']
    suf_len_2 = ['\u0648\u0646','\u0627\u062a','\u0627\u0646','\u064a\u0646','\u062a\u0646', '\u0643\u0645','\u0647\u0646', '\u0646\u0627', '\u064a\u0627','\u0647\u0627', '\u062a\u0645', '\u0643\u0646','\u0646\u064a', '\u0648\u0627', '\u0645\u0627','\u0647\u0645']
    
    main = ''
    pre = ''
    suf = ''
    
    if len(word) >= 6:
        for p3 in pre_len_3:
            if word.startswith(p3):
                main = word[3:]
                pre = word[:3]
    if len(word) >= 5:
        for p2 in pre_len_2:
            if word.startswith(p2):
                main = word[2:]
                pre = word[:2]
    
    if len(word) >= 6:
        for s3 in suf_len_3:
            if word.endswith(s3):
                if main:
                    main = main[:-3]
                    suf = main[-3:]
                else:
                    main = word[:-3]
                    suf = word[-3:]
    if len(word) >= 5:
        for s2 in suf_len_2:
            if word.endswith(s2):
                if main:
                    main = main[:-2]
                    suf = main[-2:]
                else:
                    main = word[:-2]
                    suf = word[-2:]        
    """once we have stripped the main word of these longer affixes, we will
    look to see if we have found a main word, and then look to remove the
    somewhat ambiguous 'and' marker"""
    if main:
        """if the word starts with the "and" marker "waw", and the main word begins
        with that letter, then we can assume that the first "waw" corresponds to
        the affix "and" - as it is extremely uncommon to have words of such 
        len (i.e. >= 4) whose first too letters would be the consonant "w" and 
        the long vowel "uu" whose form is identical in Arabic.
        If we find this append to the prefix gathered already so far"""
        if len(main) >= 4 and main[:2] == '\u0648\u0648':
            pre = '\u0648' + pre
            main = main[1:]
    else:
        """check for the 'and' marker in the case we haven't found an seperable
        word yet"""
        if len(word) >= 4 and word[:2] == '\u0648\u0648':
            pre = '\u0648'
            main = word[1:]
    """if we haven't found any long affix so far make the main word equal to the input"""
    if not main:
        main = word

    return [["pre",pre],['main',main],['suf',suf]]
    
def short_pre_suf_find(word):
    """length one suffixes and prefixes are separated from the 'main'
    part of the word. Depending on the length of the word, we would
    expect to find different verbal patterns (found in the extremely
    long conditionals/cases that start each different word len separation)

    in the NLTK there is a stemmer for Arabic (isri), whose algorithm I in part utilized
    in developing the patterns for Arabic's root morphology, which is not the
    type of morphology that this program analyzes, but is necessary
    to understand in order to figure out which letters are actually
    suffix or prefixes"""
    
    pre_len_1 = ['\u0644', '\u0628', '\u0641', '\u0648','\u064a', '\u062a', '\u0646', '\u0627']
    suf_len_1 = ['\u0629','\u0647','\u064a','\u0643','\u062a','\u0627','\u0646']
    five_pat = {0: ['\u0627', '\u062a'], 1: ['\u0627', '\u064a', '\u0648'], 2: ['\u0627', '\u062a', '\u0645'], 3: ['\u0645', '\u064a', '\u062a'], 4: ['\u0645', '\u062a'], 5: ['\u0627', '\u0648'], 6: ['\u0627', '\u0645']}
    s_found = False
    p_found = False
    if word[2][1] != "":
        s_found = True
    if word[0][1] != "":
        p_found = True
    #  مفعل - فاعل - فعال - فعول - فعيل - فعلة
    if len(word[1][1]) == 4 and word[1][1][0] != '\u0645' and word[1][1][1] != '\u0627' and word[1][1][2] != '\u0627' and word[1][1][2] != '\u0648' and word[1][1][2] != '\u064A' and word[1][1][3] != '\u0629':
        for s1 in suf_len_1:
            if word[1][1].endswith(s1) and s_found == False:
                word[2][1] = word[1][1][-1] + word[2][1]
                word[1][1] = word[1][1][:-1]
                s_found = True
        if len(word[1][1]) == 4:
            for p1 in pre_len_1:
                if word[1][1].startswith(p1) and p_found == False:
                    word[0][1] = word[0][1] + word[1][1][0]
                    word[1][1] = word[1][1][1:]
                    p_found == True
    # افتعل - افاعل - مفعول - مفعال - مفعيل - مفعلة - تفعلة - افعلة - مفتعل - يفتعل - تفتعل - مفاعل - تفاعل - فعولة - فعالة - انفعل - منفعل - افعال - فعلان - تفعيل - فاعول - فواعل - فعائل - فاعلة - فعالي -   
    if len(word[1][1]) == 5 and (word[1][1][2] not in five_pat[0] and word[1][1][0] != '\u0627') and (word[1][1][3] not in five_pat[1] and word[1][1][0] != '\u0645') and (word[1][1][0] not in five_pat[2] and word[1][1][4] != '\u0629') and (word[1][1][0] not in five_pat[3] and word[1][1][2] != '\u062A') and (word[1][1][0] not in five_pat[4] and word[1][1][2] != '\u0627') and (word[1][1][2] not in five_pat[5] and word[1][1][4] != '\u0629') and (word[1][1][0] not in five_pat[6] and word[1][1][1] != '\u0646') and (word[1][1][3] != '\u0627' and word[1][1][0] != '\u0627') and (word[1][1][4] != '\u0646' and word[1][1][3] != '\u0627') and (word[1][1][3] != '\u064A' and word[1][1][0] != '\u062A') and (word[1][1][3] != '\u0648' and word[1][1][1] != '\u0627') and (word[1][1][2] != '\u0627' and word[1][1][1] != '\u0648') and (word[1][1][3] != '\u0626' and word[1][1][2] != '\u0627') and (word[1][1][4] != '\u0629' and word[1][1][1] != '\u0627') and (word[1][1][4] != '\u064A' and word[1][1][2] != '\u0627'):
        for s1 in suf_len_1:
            if word[1][1].endswith(s1) and s_found == False:
                word[2][1] = word[1][1][-1] + word[2][1]
                word[1][1] = word[1][1][:-1]
                s_found = True
        if len(word[1][1]) == 5:
            for p1 in pre_len_1:
                if word[1][1].startswith(p1) and p_found == False:
                    word[0][1] = word[0][1] + word[1][1][0]
                    word[1][1] = word[1][1][1:]
                    p_found == True
    # مستفعل - استفعل - مفعالة - افتعال - افعوعل - تفاعيل - 
    if len(word[1][1]) == 6 and (word[1][1].startswith('\u0627\u0633\u062a') == False and word[1][1].startswith('\u0645\u0633\u062a') == False) and (word[1][1][0] != '\u0645' and word[1][1][3] != '\u0627' and word[1][1][5] != '\u0629') and (word[1][1][0] != '\u0627' and word[1][1][2] != '\u062A' and word[1][1][4] != '\u0627') and (word[1][1][0] != '\u0627' and word[1][1][3] != '\u0648' and word[1][1][2] != word[1][1][4]) and (word[1][1][0] != '\u062A' and word[1][1][2] != '\u0627' and word[1][1][4] != '\u0624A'):
        for s1 in suf_len_1:
            if word[1][1].endswith(s1) and s_found == False:
                word[2][1] = word[1][1][-1] + word[2][1]
                word[1][1] = word[1][1][:-1]
                s_found = True
        if len(word[1][1]) == 6:
            for p1 in pre_len_1:
                if word[1][1].startswith(p1) and p_found == False:
                    word[0][1] = word[0][1] + word[1][1][0]
                    word[1][1] = word[1][1][1:]
                    p_found == True       
    if len(word[1][1]) == 7:
        for s1 in suf_len_1:
            if word[1][1].endswith(s1) and s_found == False:
                word[2][1] = word[1][1][-1] + word[2][1]
                word[1][1] = word[1][1][:-1]
                s_found = True
        if len(word[1][1]) == 7:
            for p1 in pre_len_1:
                if word[1][1].startswith(p1) and p_found == False:
                    word[0][1] = word[0][1] + word[1][1][0]
                    word[1][1] = word[1][1][1:]
                    p_found == True
        if len(word[1][1]) == 6 and (word[1][1].startswith('\u0627\u0633\u062a') == False and word[1][1].startswith('\u0645\u0633\u062a') == False) and (word[1][1][0] != '\u0645' and word[1][1][3] != '\u0627' and word[1][1][5] != '\u0629') and (word[1][1][0] != '\u0627' and word[1][1][2] != '\u062A' and word[1][1][4] != '\u0627') and (word[1][1][0] != '\u0627' and word[1][1][3] != '\u0648' and word[1][1][2] != word[1][1][4]) and (word[1][1][0] != '\u062A' and word[1][1][2] != '\u0627' and word[1][1][4] != '\u0624A'):
            for s1 in suf_len_1:
                if word[1][1].endswith(s1) and s_found == False:
                    word[2][1] = word[1][1][-1] + word[2][1]
                    word[1][1] = word[1][1][:-1]
                    s_found = True
            if len(word[1][1]) == 6:
                for p1 in pre_len_1:
                    if word[1][1].startswith(p1) and p_found == False:
                        word[0][1] = word[0][1] + word[1][1][0]
                        word[1][1] = word[1][1][1:]
                        p_found == True
    return word

def analyze(word):
    """returns the input with the meaning of the separated morphological units"""
    
    non_verbal_p_3 = ['\u0643\u0627\u0644', '\u0628\u0627\u0644','\u0648\u0644\u0644', '\u0648\u0627\u0644']
    non_verbal_p_2 = ['\u0627\u0644', '\u0644\u0644']
    non_verbal_p_1 = ['\u0648', '\u0644', '\u0628', '\u0641']
    non_verbal_s_3 = ['\u0643\u0645\u0627', '\u0647\u0645\u0627']
    non_verbal_s_2 = ['\u0643\u0645', '\u0643\u0646', '\u0647\u0627', '\u0647\u0645', '\u0647\u0646', '\u0646\u064a']
    non_verbal_s_1 = ['\u064a', '\u0643', '\u0647']
    pres_verbal_p = ['\u064A','\u062A','\u0644','\u0628']
    pres_verbal_s_2 = ['\u064A\u0646','\u0627\u0646','\u0648\u0646']
    pres_verbal_s_1 = ['\u0646']
    past_verbal_s_3 = ['\u062a\u0645\u0627']
    past_verbal_s_2 = ['\u0646\u0627', '\u062a\u0645', '\u062a\u0646', '\u062a\u0627', '\u0648\u0627']
    past_verbal_s_1 = ['\u062a', '\u0627', '\u0646']

    """check for pres prefix
       if so check for suffix if applicable
    if no pres prefix check if there is a past tense suffix
    
    if prefix not already found check non verbals
    if suffix not already found check non verbals
    
    if no morphological info found - state this

    note: Arabic possesive markers are identical to the
    object pronouns that appear on verbs """
    
    info = ['info',[]]
    p_found = False
    s_found = False
    verbal = False
    
    if word[0][1] != "" and word[0][1] in pres_verbal_p:
        verbal = True
        if word[0][1] == "\u064a": #ي
            if word[2][1] != "" and word[2][1] in pres_verbal_s_2:
                if word[2][1] == "\u0627\u0646": #ان
                    info[1].append("p+s: 3rd du m non-past")
                    p_found = True
                    s_found = True
                elif word[2][1] == "\u0648\u0646": #ون
                    info[1].append("p+s: 3rd pl m non-past")
                    p_found = True
                    s_found = True                    
            elif word[2][1] != "" and word[2][1] in pres_verbal_s_1:
                if word[2][1] == "\u0646": #ن
                    info[1].append("p+s: 3rd pl f non-past")
                    p_found = True
                    s_found = True                   
            else:
                info[1].append("P: 3rd s m non-past")
                p_found == True
        elif word[0][1] == "\u062a": #ت
            if word[2][1] != "" and word[2][1] in pres_verbal_s_2:
                if word[2][1] == "\u0627\u0646": #ان
                    info[1].append("p+s: 2nd du m/f non-past OR 3rd du f non-past")
                    p_found = True
                    s_found = True
                elif word[2][1] == "\u0648\u0646": #ون
                    info[1].append("p+s: 2nd pl m non-past")
                    p_found = True
                    s_found = True
                elif word[2][1] == "\u064a\u0646": #ين
                    info[1].append("p+s: 2nd s f non-past")
                    p_found = True
                    s_found = True
            elif word[2][1] != "" and word[2][1] in pres_verbal_s_1:
                if word[2][1] == "\u0646": #ن
                    info[1].append("p+s: 2nd pl f non-past")
                    p_found = True
                    s_found = True
            else:
                info[1].append("p: 2nd s m non-past OR 3rd s f non-past")
                p_found == True
        elif word[0][1] == "\u0627": #ا
            info[1].append("p: 1st m/f s non-past")
            p_found = True
        elif word[0][1] == "\u0646": #ن
            info[1].append("p: 1st m/f pl non-past")
            p_found = True
    elif word[2][1] != "" and word[2][1] in past_verbal_s_3: #تما
        verbal == True
        info[1].append("s: 2nd du m/f past")
        s_found == True
    elif word[2][1] !="" and word[2][1] in past_verbal_s_2:
        verbal == True
        if word[2][1] == "\u0646\u0627": #نا
            info[1].append("s: 1st pl m/f past")
            s_found = True
        elif word[2][1] == "\u062a\u0645": #تم
            info[1].append("s: 2nd p m past")
            s_found = True
        elif word[2][1] == "\u062a\u0646": #تن
            info[1].append("s: 2nd p f past")
            s_found = True
        elif word[2][1] == "\u062a\u0627": #تا
            info[1].append("s: 3rd du f past")
            s_found = True
        elif word[2][1] == "\u0648\u0627": #وا
            info[1].append("s: 3rd pl m past")
            s_found = True
    elif word[2][1] !="" and word[2][1] in past_verbal_s_1:
        verbal = True
        if word[2][1] == "\u062a": #ت
            info[1].append("s: 1st s m/f past OR 2nd s m/f past OR 3rd s f past")
            s_found = True
        elif word[2][1] == "\u0627": #ا
            info[1].append("s: 3rd du m past")
            s_found = True
        elif word[2][1] == "\u0646": #ن
            info[1].append("s: 3rd pl f")
            s_found = True

    if p_found == False and word[0][1] != "":
        if word[0][1] in non_verbal_p_3:
            if word[0][1] == "\u0643\u0627\u0644": #كال
                info[1].append("p: as + def")
                p_found = True
            elif word[0][1] == "\u0628\u0627\u0644": #بال
                info[1].append("p: by + def")
                p_found = True
            elif word[0][1] == "\u0648\u0644\u0644": #ولل
                info[1].append("p: and + to + def")
                p_found = True
            elif word[0][1] == "\u0648\u0627\u0644": #وال
                info[1].append("p: and + def")
                p_found = True
        elif word[0][1] in non_verbal_p_2:
            if word[0][1] == "\u0627\u0644": #ال
                info[1].append("p: def")
                p_found = True
            elif word[0][1] == "\u0644\u0644": #لل
                info[1].append("p: to + def")
                p_found = True
        elif word[0][1] in non_verbal_p_1:
            if word[0][1] == "\u0648": #و
                info[1].append("p: and")
                p_found = True
            elif word[0][1] == "\u0644": #ل
                info[1].append("p: to")
                p_found = True
            elif word[0][1] == "\u0628": #ب
                info[1].append("p: by")
                p_found = True
            elif word[0][1] == "\u0641": #ف
                info[1].append("p: so")
                p_found = True
    if s_found == False and word[2][1] !="":
        if word[2][1] in non_verbal_s_3:
            if verbal:
                if word[2][1] == "\u0643\u0645\u0627": #كما
                    info[1].append("s: 2nd du m/f object")
                    s_found = True
                elif word[2][1] == "\u0647\u0645\u0627": #هما
                    info[1].append("s: 3rd du m/f object")
                    s_found = True
            else:
                if word[2][1] == "\u0643\u0645\u0627": #كما
                    info[1].append("s: 2nd du m/f possessive")
                    s_found = True
                elif word[2][1] == "\u0647\u0645\u0627": #هما
                    info[1].append("s: 3rd du m/f possesive")
                    s_found = True
        elif word[2][1] in non_verbal_s_2:
            if verbal:
                if word[2][1] == "\u0643\u0645": #كم
                    info[1].append("s: 2nd pl m object")
                    s_found = True
                elif word[2][1] == "\u0643\u0646": #كن
                    info[1].append("s: 2rd pl f object")
                    s_found = True
                elif word[2][1] == "\u0647\u0627": #ها
                    info[1].append("s: 3rd s f object")
                    s_found = True
                elif word[2][1] == "\u0647\u0645": #هم
                    info[1].append("s: 3rd pl m object")
                    s_found = True
                elif word[2][1] == "\u0647\u0646": #هن
                    info[1].append("s: 3rd pl f object")
                    s_found = True
                elif word[2][1] == "\u0646\u0627": #نا
                    info[1].append("s: 1st pl m/f object")
                    s_found = True
                elif word[2][1] == "\u0646\u064a": #ني
                    info[1].append("s: 1st s m/f object")
                    s_found = True
            else:
                if word[2][1] == "\u0643\u0645": #كم
                    info[1].append("s: 2nd pl m possesive")
                    s_found = True
                elif word[2][1] == "\u0643\u0646": #كن
                    info[1].append("s: 2rd pl f possesive")
                    s_found = True
                elif word[2][1] == "\u0647\u0627": #ها
                    info[1].append("s: 3rd s f possesive")
                    s_found = True
                elif word[2][1] == "\u0647\u0645": #هم
                    info[1].append("s: 3rd pl m possesive")
                    s_found = True
                elif word[2][1] == "\u0647\u0646": #هن
                    info[1].append("s: 3rd pl f possesive")
                    s_found = True
                elif word[2][1] == "\u0646\u0627": #نا
                    info[1].append("s: 1st pl m/f possesive")
                    s_found = True
        elif word[2][1] in non_verbal_s_1:
            if verbal:
                if word[2][1] == "\u0647": #ه
                    info[1].append("s: 3rd s m object")
                    s_found = True
                elif word[2][1] == "\u0643": #ك
                    info[1].append("s: 2nd s m/f object")
                    s_found = True
            else:
                if word[2][1] == "\u0647": #ه
                    info[1].append("s: 3rd s m possesive")
                    s_found = True
                elif word[2][1] == "\u064a": #ي
                    info[1].append("s: 1st s m/f possessive")
                    s_found = True
                elif word[2][1] == "\u0643": #ك
                    info[1].append("s: 2nd s m/f possesive")
                    s_found = True
    if info[1] == []:
        info[1].append("no morphological information")
    word.append(info)
    return word
    

print(analyze(segment("يريدكم")))# he likes you all
print(analyze(segment("والكتب"))) #and the books
print(analyze(segment("ووجه"))) #and a face
print(analyze(segment("كتاب")))#a book
print(analyze(segment("يكتبون"))) #they (pl,m) write
print(analyze(segment("يكتب"))) # he writes
print(analyze(segment("عائلتي"))) #my family
print(analyze(segment("يسكنان"))) #they (2,m) reside
print(analyze(segment("جدته"))) #his grandmother
print(analyze(segment("اليوم"))) #today/the day
print(analyze(segment("للدرس"))) #to the lesson

v = ["\u064B","\u064C","\u064D","\u064E","\u064F","\u0650","\u0652","\u0670","\u0651",'.']
arabic_text= "يولد جميع الناس أحراراً متساوين في الكرامة والحقوق. وقد وهبوا عقلاً وضميراً وعليهم ان يعامل بعضهم بعضاً بروح اﻹخاء."
seg = nltk.tokenize.wordpunct_tokenize(arabic_text)
for i in seg:
    """ check if the unit is actually a word"""
    if i not in v:
        print(i + "\n" + str(analyze(segment(i))))
        
"""
    next steps could include getting functionality for the digraph "lam+alif",
    trying to account for the accusative indefinate case marker which is identical
    to some verbal affixes (especially in the case that we are removing all 
    vocalization/case type units) and is extremely common in written arabic, 
    and developing measures of success on hand annotated data(f1, etc)
    
    this analyzer does not make use of statistical methods or a root dictionary,
    and also belies a greater issue in Arabic morphological computational
    analysis, which is that a given word could have a number of potential
    possible analyses, but what this parser tries to acomplish, is regardless
    of root/form possibilties to return the appropriate affixes regardless.
"""