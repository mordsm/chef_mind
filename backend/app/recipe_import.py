"""Bounded recipe snapshots. Source content is data, never executable instructions."""
import hashlib
import json
import re
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlsplit, urljoin

from pydantic import Field, field_validator
from app.schemas import StrictModel
from app.knowledge import DomainError

HOSTS={'mako.co.il','www.mako.co.il','www.hashulchan.co.il','hashulchan.co.il',
       'imaot.co.il','www.imaot.co.il','food.walla.co.il','www.bbcgoodfood.com'}


class RecipeStep(StrictModel):
    id: str = Field(max_length=80)
    text: str = Field(min_length=1,max_length=1000)
    action_type: str = Field(default='',max_length=80)


class RecipeSnapshot(StrictModel):
    id: str = Field(max_length=80)
    title: str = Field(min_length=1,max_length=200)
    url: str = Field(default='',max_length=2000)
    ingredients: list[str] = Field(default_factory=list,max_length=100)
    steps: list[RecipeStep] = Field(min_length=1,max_length=30)
    acquisition: str = Field(pattern='^(structured_web|pasted)$')

    @field_validator('url')
    @classmethod
    def safe_reference(cls,value):
        if value:
            parsed=urlsplit(value)
            if parsed.scheme not in ('https','http') or not parsed.hostname or parsed.username or parsed.password:
                raise ValueError('Expected a public recipe reference URL')
        return value


class RecipeImport(StrictModel):
    url: str = Field(default='',max_length=2000)
    text: str = Field(default='',max_length=20000)
    title: str = Field(default='המתכון שבחרתי',max_length=200)


def clean(value):
    return unescape(re.sub('<[^>]*>',' ',str(value))).strip()


def classify_step(text):
    # Only labels a referenced instruction. It does not infer times or measurements.
    for action,terms in [('grill',['גריל','מנגל','grill']),('bake',['אפייה','אופים','לאפות','bake']),
                         ('roast',['צלייה','צולים','לצלות','roast']),('fry',['מטגנים','לטגן','טיגון','fry']),
                         ('boil',['מרתיחים','להרתיח','רתיחה']),('cut',['חותכים','לחתוך','קוצצים','cut']),
                         ('stir',['מערבבים','לערבב','stir']),('season',['מתבלים','לתבל','season']),
                         ('cook',['מבשלים','לבשל','cook'])]:
        if any(term in text.lower() for term in terms):return action
    return ''


def snapshot(title,url,ingredients,instructions,acquisition):
    instructions=[clean(x) for x in instructions if clean(x)]
    if not instructions or len(instructions)>30 or any(len(x)>1000 for x in instructions):
        raise DomainError('RECIPE_IMPORT_FAILED','לא נמצאו עד 30 שלבים באורך מתאים. אפשר להדביק רק את הוראות ההכנה, שלב בכל שורה.',422)
    digest=hashlib.sha256(json.dumps([title,url,instructions],ensure_ascii=False).encode()).hexdigest()[:32]
    return RecipeSnapshot(id='recipe_'+digest,title=clean(title)[:200] or 'המתכון שבחרתי',url=url,
        ingredients=[clean(x)[:200] for x in ingredients[:100]],
        steps=[RecipeStep(id=f'recipe_step_{digest}_{index}',text=text,action_type=classify_step(text)) for index,text in enumerate(instructions)],acquisition=acquisition)


class RecipeHTML(HTMLParser):
    def __init__(self):super().__init__();self.inside=False;self.parts=[];self.scripts=[]
    def handle_starttag(self,tag,attrs):
        if tag=='script' and dict(attrs).get('type','').split(';')[0].strip()=='application/ld+json':self.inside=True;self.parts=[]
    def handle_data(self,data):
        if self.inside:self.parts.append(data)
    def handle_endtag(self,tag):
        if tag=='script' and self.inside:self.scripts.append(''.join(self.parts));self.inside=False


def recipe_nodes(value):
    if isinstance(value,list):
        for item in value:yield from recipe_nodes(item)
    elif isinstance(value,dict):
        types=value.get('@type',[]);types=[types] if isinstance(types,str) else types
        if 'Recipe' in types:yield value
        for item in value.values():
            if isinstance(item,(dict,list)):yield from recipe_nodes(item)


def instruction_text(value):
    if isinstance(value,str):return [value]
    if isinstance(value,list):return [text for item in value for text in instruction_text(item)]
    if isinstance(value,dict):
        types=value.get('@type',[]);types=[types] if isinstance(types,str) else types
        return instruction_text(value.get('itemListElement') or value.get('text') or (value.get('name',[]) if 'HowToStep' in types else []))
    return []


def from_html(html,url):
    parser=RecipeHTML();parser.feed(html)
    for script in parser.scripts:
        try:data=json.loads(script)
        except ValueError:continue
        for recipe in recipe_nodes(data):
            instructions=instruction_text(recipe.get('recipeInstructions',[]))
            if instructions:return snapshot(recipe.get('name','המתכון שבחרתי'),url,recipe.get('recipeIngredient',[]),instructions,'structured_web')
    raise DomainError('RECIPE_IMPORT_FAILED','האתר לא סיפק הוראות בפורמט שניתן לקלוט. הדבק את הוראות ההכנה, שלב בכל שורה.',422)


def allowed_url(url):
    try:
        parsed=urlsplit(url)
        valid=parsed.scheme=='https' and parsed.hostname in HOSTS and not parsed.username and not parsed.password and parsed.port in (None,443)
    except ValueError:valid=False
    if not valid:
        raise DomainError('RECIPE_IMPORT_FAILED','קליטת קישור נתמכת כרגע באתרי המתכונים שבחיפוש. לאתר אחר: הדבק את הוראות ההכנה.',422)
    return url


def import_recipe(body):
    if body.text.strip():
        if body.url:
            parsed=urlsplit(body.url)
            if parsed.scheme not in ('https','http') or not parsed.hostname or parsed.username or parsed.password:
                raise DomainError('RECIPE_IMPORT_FAILED','הקישור אינו תקין.',422)
        return snapshot(body.title,body.url,[],body.text.splitlines(),'pasted')
    import httpx
    from app.model import tls_context
    url=allowed_url(body.url)
    try:
        with httpx.Client(verify=tls_context(),trust_env=False,timeout=12,follow_redirects=False) as client:
            for _ in range(4):
                with client.stream('GET',url,headers={'Accept':'text/html'}) as response:
                    if response.is_redirect:
                        url=allowed_url(urljoin(url,response.headers.get('Location','')));continue
                    response.raise_for_status();parts=[];size=0
                    for part in response.iter_bytes():
                        size+=len(part)
                        if size>2_000_000:raise ValueError('Recipe page too large')
                        parts.append(part)
                    return from_html(b''.join(parts).decode('utf-8',errors='replace'),url)
    except DomainError:raise
    except (httpx.HTTPError,ValueError,OSError):pass
    raise DomainError('RECIPE_IMPORT_FAILED','לא ניתן לקרוא את האתר כרגע. אפשר להדביק את הוראות ההכנה כאן במקום הקישור.',422)
