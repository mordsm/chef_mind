"""Validate the new knowledge artifacts and unchanged originals, read-only except reports."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def main():
    manifest=json.loads((OUT/'FoodLab-2015-manifest.json').read_text(encoding='utf-8'))
    report=OUT/'FoodLab-2015-Report-HE.md'
    records=manifest['records']
    canonical_count=len({r['canonical_id'] for r in records})
    chapter_counts=Counter(f['chapter'] for f in manifest['files'] if f['chapter'])
    kind_counts=Counter(r['kind'] for r in records)
    chapters='\n'.join(f'| {i} | {title[2:]} | 4 | 1 | {chapter_counts[i]} |' for i,(_,title) in enumerate(manifest['chapter_boundaries'],1))
    files=sorted(p for p in ROOT.rglob('*') if p.is_file() and ('FoodLab-2015' in p.parts or p.stem.startswith('FoodLab-CH') or p.stem=='FoodLab-2015-Conflicts-And-Gaps'))
    # Include the report and the validation JSON that this validator generates.
    expected=set(files)|{report,OUT/'FoodLab-2015-validation.json'}
    md_count=sum(p.suffix=='.md' for p in expected)
    filelist='\n'.join(f'- `{p.relative_to(ROOT).as_posix()}`' for p in sorted(expected))
    report_text=f'''---
id: REPORT-FLB-2015-001
type: INGESTION_REPORT
name: דוח חילוץ ידע מכל תשעת פרקי The Food Lab
verification_status: PRELIMINARY
evidence_cutoff_date: "2026-10-25"
---

# דוח חילוץ ידע מכל תשעת פרקי The Food Lab

## תוצאה והיקף

עובדו כל תשעת הפרקים הממוספרים לשכבה ראשונה של ידע מובנה: **36 טענות מקור נבחרות, 9 ניסוחי כלל מותנה, 9 מפות פרק ו־{canonical_count} מושגים קיימים שאליהם קושרו הראיות**. זהו חילוץ סלקטיבי של עקרונות ליבה מכל פרק, ולא טענה שכל משפט, מתכון, איור או טענה מספרית בספר קודדו ונבדקו. קובצי המבוא, האינדקס והנספחים נסרקו מבנית; לא נוצר מהם פרק נוסף של טענות.

זוהו 11 עקרונות קולינריים, 6 עקרונות מדעיים, 8 תכונות חומרי גלם, 5 תצפיות ניסוי מטבח, 4 טכניקות ו־2 תכונות ציוד. תשעת הכללים הם **פרשנות מותנית** של הראיות; לא הוצגו כציטוטים. לא נוצרו השערות מדעיות חדשות. קישור מושגי מסומן כפרשנות, ולא כהוכחה לסיבתיות.

## ספר ומהדורה

The Food Lab: Better Home Cooking Through Science, J. Kenji López-Alt, First Edition, W. W. Norton & Company, 2015. פורמט המקור בפועל הוא EPUB; אין PDF מצורף של הספר הזה. ISBN אלקטרוני: `9780393249866`. מידע הכותרת נבדק ב־`content.opf`, ומהדורה וזכויות ב־`text/part0458.html`. [[FoodLab-2015-Source-Audit]] מתעד את הבדיקה. הספר האחר, On Food and Cooking של McGee, לא עובד מחדש במסגרת משימה זו.

מקור מקומי: `{manifest['book_path']}`

חתימת המקור: `{manifest['book_sha256']}`

## שיטת העבודה והכיסוי

מופו **459 קובצי HTML פנימיים**, מהם {sum(chapter_counts.values())} משויכים לפרקים 1–9 לפי תוכן העניינים. הסריקה מדדה מבנה, מספר פסקאות, כמות טקסט וחתימות. אין להסיק מכך שנערכה ביקורת מהותית לכל כ־{sum(f['characters'] for f in manifest['files'] if f['chapter']):,} תווי טקסט בפרקים. בפועל נבחרו ונבדקו 36 פסקאות ראיה, ועוד פסקאות נקודתיות לצורך ביקורת פערים והקשר.

| פרק | שם לפי תוכן העניינים | טענות | כללים | קבצים במיפוי המבני |
|---|---|---:|---:|---:|
{chapters}

לכל טענה מזהה יציב `CLM-FLB-CHxx-nnn`, רשומת ראיה `EVD-FLB-CHxx-nnn`, נתיב פנימי, מספר פסקה וחתימת הפסקה. אין עימוד EPUB אמין בעותק: `pdf_page` ו־`printed_page` הם `UNKNOWN`. שיטת המיקום ניתנת לשחזור ומוגדרת במניפסט ובביקורת המקור. לא הומצאו עמודים.

## שילוב, כפילויות וקשרים

הראיות פוזרו בתיקיות התחום הקיימות, וכל כלל בתיקיית `12_Rules`. נוצרו 36 **רשומות ראיה**, ולא 36 מושגי ליבה חלופיים. נעשה שימוש חוזר ב־{canonical_count} מזהי מושג קיימים וב־`SRC-FOODLAB-2015`; 3 מהכללים מציינים במפורש מזהי כלל קנוניים קיימים (`RUL-MEAT-001`, `RUL-MEAT-002`, `RUL-MEAT-003`). 6 האחרים הם כללי טיוטה חדשים בהקשר מוגדר. אין אומדן מומצא של מספר כפילויות מילוליות שנמנעו: הנתון המדיד הוא 36 מיפויי ראיה ל־21 יעדים קיימים.

נוצרו **90 קשרים מובנים ב־YAML** ברשומות הראיה והכללים: ביסוס במקור, מיפוי למושג קיים וביסוס כלל בראיה. קשרי המיפוי הם מותנים ופרשניים. החיבור לשמונת התחומים, כולל מגבלות הבטיחות והטעם, מוצג ב־[[FoodLab-2015-Domain-Map]]. גלוטן ופקטין אינם ממוזגים עם עמילן: אלה פערים בטקסונומיה המתועדים לבחינה.

## סתירות, תנאים ואי־ודאות

[[FoodLab-2015-Conflicts-And-Gaps]] כולל 9 ממצאי ביקורת. שניים הם אי־התאמות מפורשות: שיוך פסטה לפרק 9 ברשומה הישנה מול פרק 7 בפועל, ותיאור שדה מגנטי מול שדה חשמלי בשני מקומות בספר. יתר הממצאים מפרידים הבדלי תחולה, גבולות ניסוי ופערי אימות; אין להציג את כל תשעתם כסתירות מוכחות.

כל 36 הטענות נבדקו מול פסקת המקור שסומנה, אך **לא אומתו עצמאית מול מחקרים חיצוניים או ניסויים חדשים**. כל הרשומות החדשות מסומנות `PRELIMINARY`; רמת העקיבות גבוהה, וההכללה מותנית. Confidence מתאר ביטחון בייחוס ובהתאמה, לא הסתברות מדעית. חסרים נתוני מדגם, סמיות וסטטיסטיקה לחלק ממבחני המטבח (`UNKNOWN`). לא נבדקו errata של המו״ל או מהדורות אחרות.

טמפרטורות, חיי מדף ותהליכי בטיחות לא נגזרו אוטומטית מהעדפות המרקם בספר. מספרים שלא נבדקו בהקשר מתאים אינם מוצגים כקבועים אוניברסליים. אין כאן חיבור חדש למנוע השף, הפעלת טיוטות, שינוי בממשק או הבטחה למנוע הסקה אוטומטי.

## שאלות בדיקה

[[FoodLab-2015-Five-Questions]] מציג חמש שאלות, תשובות מוגבלות ושרשראות ראיה: בשר יבש בתבשיל לח, מרקם בשר טחון, נפח מים בירקות לעומת פסטה, יציבות ויניגרט, ופרישת עוף/מאוורר תנור. אלה בדיקות ידניות של הידע וקשריו.

## בקרת איכות ושימור

תוצאות הבדיקה נרשמות ב־`FoodLab-2015-validation.json`: מזהים חדשים ייחודיים, YAML תקין, קישורים חדשים פתירים, מזהי קשר תואמים ליעדיהם, עקיבות לכל פסקת ראיה, 9 פרקים ו־8 תחומים, אי־שינוי המקור, אי־שינוי קובצי הידע הקודמים ואי־שינוי קובצי היישום. בדיקות Chef אינן נדרשות כאן כי קוד היישום לא השתנה. אין הסתמכות על קישור שאינו פתיר או על מספר עמוד מומצא.

## קבצים

נוצרו {md_count} קובצי Markdown חדשים; כולל 36 רשומות ראיה, 9 כללים, 9 מפות פרק, ביקורת מקור, ביקורת סתירות ופערים, מפת תחומים, חמש שאלות והדוח הזה. נוסף מניפסט JSON, דוח בדיקות JSON ושני סקריפטי שחזור/אימות, כולם בתוך אזור הידע הקיים. **לא שונה אף קובץ ידע שהיה קיים לפני העבודה; לא שונה יישום השף.**

{filelist}

## מדוע העבודה נעצרת ומה מומלץ הלאה

הסתיים מעבר החילוץ המובנה המוגדר מכל תשעת הפרקים, והתקבלו ראיות, כללים וקשרים שניתנים לבדיקה. לא הוכרזה רוויה מדעית או סקירה ממצה של הספר. נותרו מתכונים, איורים וטענות נוספות שלא נותחו מהותית; הם ניתנים לאיתור דרך המניפסט.

מומלץ לבדוק ידנית תחילה את תשעת הכללים ואת שתי אי־ההתאמות, להחליט כיצד לתקן את הפניות הפסטה בלי לאבד היסטוריה, להשלים מקור לפיזיקת המיקרוגל ולמנגנון הלציטין, ולהפריד גלוטן ופקטין בטקסונומיה. לפני שימוש אוטומטי נדרשת סקירת התוכן ובטיחות התהליכים. ההרחבה העתידית תהיה לפי שאלות בעלות ערך, ולא באמצעות הכרזה שכל הספר כבר אומת.
'''
    report.write_text(report_text,encoding='utf-8')
    errors=[];ids={};paths_by_stem={};new_notes=[];relationships=0
    for p in ROOT.rglob('*.md'):
        paths_by_stem.setdefault(p.stem,[]).append(p)
        t=p.read_text(encoding='utf-8-sig')
        if not t.startswith('---'):continue
        try:m=yaml.safe_load(t.split('---',2)[1])
        except Exception as e:errors.append(f'YAML: {p}: {e}');continue
        if isinstance(m,dict) and m.get('id'):ids.setdefault(str(m['id']),[]).append(p)
        if p in expected:new_notes.append((p,m,t))
    for p,m,t in new_notes:
        if not isinstance(m,dict):errors.append(f'Missing YAML: {p}');continue
        if len(ids.get(str(m.get('id')),[]))!=1:errors.append(f'Duplicate/missing id: {p}')
        if m.get('verification_status')!='PRELIMINARY':errors.append(f'Unexpected activation status: {p}')
        for raw in re.findall(r'\[\[([^\]]+)\]\]',t):
            dest=raw.split('|')[0].split('#')[0]
            if not dest:continue
            stem=Path(dest).stem
            if len(paths_by_stem.get(stem,[]))!=1:errors.append(f'Unresolved/ambiguous link {dest}: {p}')
        for rel in m.get('relationships',[]):
            relationships+=1
            dest=rel['target_name'].strip('[]'); target=paths_by_stem.get(dest,[])
            if len(target)!=1 or target[0] not in ids.get(rel['target_id'],[]):errors.append(f'Relationship id mismatch: {p}')
    with zipfile.ZipFile(manifest['book_path']) as z:
        for r in records:
            loc=r['locator'];root=ET.fromstring(z.read(loc['internal_path']));ps=[' '.join(e.itertext()).strip() for e in root.find('{*}body').iter() if e.tag.rsplit('}',1)[-1]=='p']
            if hashlib.sha256(ps[loc['paragraph_index']-1].encode()).hexdigest()!=loc['paragraph_sha256']:errors.append(f'Source mismatch: {r["id"]}')
    for rel,digest in manifest['existing_knowledge_hashes'].items():
        if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=digest:errors.append(f'Existing knowledge changed: {rel}')
    for rel,digest in manifest['application_hashes'].items():
        if hashlib.sha256((ROOT.parents[1]/'backend'/rel).read_bytes()).hexdigest()!=digest:errors.append(f'Application changed: {rel}')
    if hashlib.sha256(Path(manifest['book_path']).read_bytes()).hexdigest()!=manifest['book_sha256']:errors.append('Original book changed')
    for p in OUT.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'))
    if len(new_notes)!=59:errors.append(f'Expected 59 Markdown notes, got {len(new_notes)}')
    if relationships!=90:errors.append(f'Expected 90 relationships, got {relationships}')
    result={'status':'PASS' if not errors else 'FAIL','errors':errors,'new_markdown_files':len(new_notes),'claims':len(records),'conditional_rules':9,'chapters':len(chapter_counts),'structured_relationships':relationships,'canonical_concepts_reused':canonical_count,'claim_type_counts':dict(kind_counts),'source_paragraph_hashes_verified':len(records),'original_knowledge_files_unchanged':len(manifest['existing_knowledge_hashes']),'application_files_unchanged':len(manifest['application_hashes']),'book_unchanged':True,'all_new_records_preliminary':True,'coverage_is_exhaustive':False,'bibliographic_and_scientific_independent_review':'NOT_PERFORMED'}
    (OUT/'FoodLab-2015-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    if not errors:
        report.write_text(report_text.replace('## קבצים\n', f'תוצאת הבדיקה בפועל: **PASS**. אומתו {len(new_notes)} רשומות Markdown, {relationships} קשרים ו־{len(records)} חתימות פסקה; {len(manifest["existing_knowledge_hashes"])} קובצי ידע קודמים ו־{len(manifest["application_hashes"])} קובצי יישום נשארו ללא שינוי.\n\n## קבצים\n'),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
    if errors:raise SystemExit(1)


if __name__=='__main__':main()
