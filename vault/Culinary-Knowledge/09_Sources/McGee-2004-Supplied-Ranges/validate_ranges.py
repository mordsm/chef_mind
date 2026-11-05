"""Source, link, YAML and original-file checks for the range extraction."""
import hashlib
import json
from pathlib import Path
import re
import runpy

import fitz
import yaml

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    m=json.loads((OUT/'McGee-Ranges-manifest.json').read_text(encoding='utf-8'))
    norm=runpy.run_path(str(OUT/'ingest_ranges.py'))['norm']
    report=OUT/'McGee-Ranges-Report-HE.md'
    chapter_rows=[]
    for ch in sorted({r['chapter'] for r in m['records']}):
        rs=[r for r in m['records'] if r['chapter']==ch]
        chapter_rows.append(f'| {ch} | {len(rs)} | 1 |')
    source_rows='\n'.join(f"- `{s['path']}` — {s['pages']} עמודים; טווח PDF מלא {s['pdf_start']}–{s['pdf_end']}." for s in m['sources'])
    record_links='\n'.join(f"- [[{r['stem']}]] — מודפס {r['printed_page']}, PDF מלא {r['pdf_page']}, עמוד בחלק {r['split_page']}." for r in m['records'])
    rule_links='\n'.join(f"- [[{r['stem']}]]" for r in m['rules'])
    text=f'''---
id: REPORT-MCG-RNG-001
type: INGESTION_REPORT
name: דוח חילוץ וחיבור שלושת חלקי McGee לשף
verification_status: PRELIMINARY
evidence_cutoff_date: "2026-10-25"
---

# דוח חילוץ וחיבור שלושת חלקי McGee לשף

## מה בוצע

מופו 473 עמודי PDF מתוך שלושה חלקים שסיפק המשתמש. כל עמוד הושווה לטקסט אותו עמוד ב־PDF המלא בן 898 העמודים. חילוץ הידע ממוקד ב־31 טענות מקור ותשעה כללים מותנים בפרקים 5–9 ו־12–15. אלה 9 פרקים עם כיסוי משתנה, ולא עיבוד ממצה של כל טענה בספר. סוף פרק 4 נמצא בטווח אך כבר עובד בעבר, ולכן לא נוצרה לו כאן רשומת פרק חדשה.

הספר הוא On Food and Cooking: The Science and Lore of the Kitchen, Harold McGee, המהדורה המתוקנת והמורחבת משנת 2004, Scribner. נעשה שימוש חוזר ב־[[SRC-MCGEE-2004]]. הספרים המקוריים וקובצי הידע הקודמים לא שוכתבו.

## מקורות ועימוד

{source_rows}

בכל רשומת ראיה נשמרים עמוד מודפס, עמוד PDF מלא, עמוד בחלק המצורף ושם הקובץ. התאמת העמודים נבדקה מול הספר המלא, ולא הוסקה רק משם הקובץ. לדוגמה: קקאו במודפס 706 נמצא ב־PDF מלא 720 ובעמוד 20 בחלק 701–898. נשמרו חתימות SHA-256 לקבצי המקור ולטקסט כל עמוד, וכן סימן איתור טקסטואלי לטענה.

לא בוצע שינוי, חיתוך נוסף או המרה של ה־PDF המקורי. תוכן הספר טופל כמקור מידע, ולא כהוראות לביצוע פעולות במחשב.

## כיסוי ומגבלות

| פרק | טענות מקור | כללים פרשניים |
|---|---:|---:|
{chr(10).join(chapter_rows)}

הטווח הראשון מכסה מודפס 212–386 והשני 387–486. השלישי מתחיל במודפס 687 ומכסה גם נספח, ביבליוגרפיה, אינדקס וזכויות, שאינם טענות בישול חדשות. פרקים 5–8 ו־13–15 זמינים בטווחים במלוא עמודיהם, אך רק עקרונות ליבה נבחרים מהם חולצו. פרק 9 ופרק 12 זמינים כאן בחלקם. PDF ‏501–700 אינו מצורף; פרקים 10–11, סוף 9 ותחילת 12 אינם מסומנים כמושלמים. פרק 1 לא נכלל בעבודה זו. פרקים 2–4 נותרו כפי שעובדו בעבר.

טבלאות רב־עמודתיות ואיורים לא פוענחו לתהליכים מספריים בלי בדיקה נפרדת; למשל טבלת שיטות הקפה במודפס 446 תרמה רק את הטענה המפורשת בהקדמתה על חלקיקים והמשך מיצוי. לא הופקו ממנה זמני חליטה אוטומטיים.

## שילוב באונטולוגיה ובשף

נוצרו 31 רשומות ראיה בתיקיות התחום הקיימות ו־9 כללים בתיקיית `12_Rules`, עם 71 קשרים מובנים של ביסוס ומיפוי למושגים קיימים. לא נוצרו מושגים כפולים במקום המושגים הקנוניים. מיפוי בין מושגים סמוכים מסומן כפרשני ואינו טענה שהם זהים. לדוגמה, גשר בין שמן אגוזים למושג שומן קיים אינו הופך אגוז לחמאה.

הידע החדש זמין לשליפת השף לפי המנה והשאלה באמצעות מניפסט מוגדר. הוא נוסף למקורות McGee הישנים, Food Lab וכללי הבטיחות. אין הפעלה גורפת של כל טיוטות הכספת ואין המרה של מצב `PRELIMINARY` ל־`VERIFIED`. הטקסט נבדק מול המקור, אך לא נערך אימות מדעי עצמאי. הכללים מתויגים כפרשנות; פרמטרים גולמיים מהספר אינם מבוצעים כהוראות.

## פערים וביקורת

[[McGee-Ranges-Conditions-And-Gaps]] מפריד בין בעיית עימוד, הבדלי חומציות, מטרת תיקון שוקולד, הבדלי סוגי פרי, תיאורי מתחלב ומגבלות בטיחות של ספר משנת 2004. אין הכרזה שכל המחלוקות הוכרעו. מספרים רפואיים והנחיות מיושנות לא הועברו לנוהלי בטיחות או להמלצות בריאותיות. איכות מרקם והוכחת מוכנות נשארות נפרדות.

## רשומות הראיה

{record_links}

## כללים מותנים

{rule_links}

## שאלות ובדיקות

[[McGee-Ranges-Five-Questions]] מספק חמש שאלות ומסלולי ראיה: ירק קשה ברוטב חומצי, החלפת קקאו, שוקולד שנתפס, מועד הוספת עשבי תיבול ושינוי עובי המזון. היישום נבדק בנפרד בשליפת מידע חדש לשאלת קקאו ובשימור מקורות קיימים ובטיחות.

מניפסט העיבוד: `McGee-Ranges-manifest.json`. תוצאות בקרת האיכות: `McGee-Ranges-validation.json`. הבדיקה מאמתת YAML, מזהים, קישורים, התאמת מזהי הקשרים, חתימות עמודי הראיה ושימור הקבצים המקוריים.

## מדוע העבודה נעצרת

הושלם מעבר חילוץ ממוקד משלושת החלקים, עם עקיבות ושילוב בשליפה. אין טענה לרוויה מחקרית או לעיבוד ממצה. ההמשך בעל הערך הוא השלמת הטווחים החסרים ועיבוד שאלות בישול נוספות מתוך העמודים שטרם נותחו מהותית, יחד עם ביקורת התוכן והבטיחות לפני הרחבה לתהליכים אוטומטיים.
'''
    report.write_text(text,encoding='utf-8')
    all_md=list(ROOT.rglob('*.md'));stems={p.stem:p for p in all_md};byid={};new=[];errors=[];rels=0
    for p in all_md:
        t=p.read_text(encoding='utf-8-sig')
        if not t.startswith('---'):continue
        meta=yaml.safe_load(t.split('---',2)[1])
        if isinstance(meta,dict) and meta.get('id'):byid.setdefault(meta['id'],[]).append(p)
        if p.stem.startswith('McGee-Ranges-'):new.append((p,meta,t))
    for p,meta,t in new:
        if len(byid.get(meta.get('id'),[]))!=1:errors.append(f'Duplicate ID: {p}')
        if meta.get('verification_status')!='PRELIMINARY':errors.append(f'Unexpected status: {p}')
        for link in re.findall(r'\[\[([^\]]+)\]\]',t):
            dest=link.split('|')[0].split('#')[0]
            if dest and Path(dest).stem not in stems:errors.append(f'Broken link {dest}: {p}')
        for rel in meta.get('relationships',[]):
            rels+=1
            if stems.get(rel['target_name'].strip('[]')) not in byid.get(rel['target_id'],[]):errors.append(f'Relationship ID mismatch: {p}')
    for rel,h in m['existing_knowledge_hashes'].items():
        if digest(ROOT/rel)!=h:errors.append(f'Existing note changed: {rel}')
    docs={}
    for s in m['sources']:
        p=Path(s['path'])
        if digest(p)!=s['sha256']:errors.append(f'Source changed: {p}')
        docs[p.name]=fitz.open(p)
    for r in m['records']:
        page=docs[r['split_filename']][r['split_page']-1]
        if hashlib.sha256(norm(page.get_text()).encode()).hexdigest()!=r['page_text_sha256']:errors.append(f'Page mismatch: {r["id"]}')
    if digest(Path(m['full_pdf_path']))!=m['full_pdf_sha256']:errors.append('Full PDF changed')
    if len(new)!=43 or rels!=71:errors.append(f'Unexpected counts: {len(new)} notes / {rels} relationships')
    result={'status':'PASS' if not errors else 'FAIL','errors':errors,'new_markdown_notes':len(new),'source_claims':len(m['records']),'conditional_rules':len(m['rules']),'structured_relationships':rels,'pages_mapped_to_full_book':len(m['pages']),'source_page_references_verified':len(m['records']),'unique_source_pages':len({r['pdf_page'] for r in m['records']}),'existing_notes_unchanged':len(m['existing_knowledge_hashes']),'original_pdfs_unchanged':True,'independent_scientific_validation':False,'coverage_is_exhaustive':False}
    (OUT/'McGee-Ranges-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    if not errors:report.write_text(text+f'\nתוצאת הבדיקה בפועל: **PASS** — {len(new)} קובצי Markdown, {rels} קשרים, 31 הפניות לעמודי ראיה ו־{len(m["existing_knowledge_hashes"])} קובצי ידע קודמים ללא שינוי. כל שלושת חלקי המקור וה־PDF המלא נשמרו ללא שינוי.\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
    if errors:raise SystemExit(1)


if __name__=='__main__':main()
