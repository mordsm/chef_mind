'use strict';
const voiceSlot=$('coach-voice-slot'),voiceRow=el('div','','voice-row');
const voiceInput=el('button','🎙 הקלדה בקול','secondary');voiceInput.type='button';voiceInput.id='voice-input';voiceInput.setAttribute('aria-pressed','false');
const voiceRead=el('button','🔊 הקראה','secondary');voiceRead.type='button';voiceRead.id='voice-read';
const voiceStop=el('button','עצירה','secondary');voiceStop.type='button';voiceStop.id='voice-stop';
const voiceStatus=el('p','','voice-status');voiceStatus.id='voice-status';voiceStatus.setAttribute('role','status');
const voiceTools=el('details','','voice-tools');voiceTools.append(el('summary','כלי קול — הקלדה בקול והקראת ההנחיה (אופציונלי)'));
voiceRow.append(voiceInput,voiceRead,voiceStop);voiceTools.append(voiceRow,el('small','הקלדה בקול מחליפה את ההקלדה במקלדת בלבד. הטקסט אינו נשלח עד שלוחצים על שליחה. שירותי הקול של הדפדפן עשויים לעבד קול בענן.'));voiceSlot.append(voiceTools,voiceStatus);
let speechRecognizer=null,lastGuidance=null,voiceSession=null,voiceRetry=null,lastVoiceTarget='coach-question';

function isWhyVoiceCommand(text){return /^(?:(?:השף|שף)\s+)?למה(?:\s+עושים\s+את\s+זה)?$/.test(text.replace(/[,.!?״"׳']/g,' ').replace(/\s+/g,' ').trim());}
document.addEventListener('focusin',event=>{if(['coach-question','work-report'].includes(event.target.id))lastVoiceTarget=event.target.id;});
function placeVoiceStatus(input){const cockpit=$('cockpit-voice');if(cockpit&&document.body.classList.contains('cooking-live'))cockpit.append(voiceStatus);else input.insertAdjacentElement('afterend',voiceStatus);}
function stopDictation(){clearTimeout(voiceRetry);voiceRetry=null;voiceSession=null;const old=speechRecognizer;speechRecognizer=null;if(old){try{old.abort();}catch{}}voiceInput.textContent='🎙 הקלדה בקול';voiceInput.setAttribute('aria-pressed','false');}
function stopCoachVoice(){stopDictation();window.speechSynthesis?.cancel();}
function startRecognizer(session){
 if(voiceSession!==session)return;
 const Recognition=window.SpeechRecognition||window.webkitSpeechRecognition;
 try{const recognizer=new Recognition();speechRecognizer=recognizer;recognizer.lang=document.documentElement.lang==='he'?'he-IL':'en-US';recognizer.continuous=true;recognizer.interimResults=true;const seen=new Map();
   recognizer.onstart=()=>{if(speechRecognizer!==recognizer)return;voiceInput.textContent='מקשיב… לחץ לעצירה';voiceInput.setAttribute('aria-pressed','true');voiceStatus.textContent=session.target==='work-report'?'דבר עכשיו. הטקסט יתווסף לדיווח.':'דבר עכשיו. הטקסט יתווסף לשאלה.';};
   recognizer.onresult=event=>{if(speechRecognizer!==recognizer)return;const input=$(session.target);if(!input){stopDictation();voiceStatus.textContent='שדה ההקלדה נסגר. פתח אותו ונסה שוב.';return;}const finals=[],interim=[];for(let index=event.resultIndex||0;index<event.results.length;index++){const result=event.results[index],text=result[0].transcript.trim();if(result.isFinal){if(!seen.has(index)){seen.set(index,text);finals.push(text);}}else interim.push(text);}if(interim.length)document.dispatchEvent(new CustomEvent('chef-voice-transcript',{detail:{text:interim.join(' '),final:false}}));if(finals.length){const heard=finals.join(' ');document.dispatchEvent(new CustomEvent('chef-voice-transcript',{detail:{text:heard,final:true}}));if(isWhyVoiceCommand(heard)){document.dispatchEvent(new Event('chef-why-requested'));return;}input.value=(input.value.trim()+' '+finals.join(' ')).trim().slice(0,2000);input.dispatchEvent(new Event('input',{bubbles:true}));session.received=true;}voiceStatus.textContent=interim.length?'שומע: '+interim.join(' '):'הטקסט נוסף. אפשר להמשיך לדבר, לעצור, לערוך ולשלוח.';};
   recognizer.onerror=event=>{if(speechRecognizer!==recognizer)return;if(event.error==='no-speech'){voiceStatus.textContent='לא זוהה דיבור. מנסה להקשיב שוב…';return;}const message=['not-allowed','service-not-allowed'].includes(event.error)?'אין הרשאה למיקרופון או לשירות הזיהוי. אפשר לאפשר גישה בהגדרות האתר, או להשתמש במיקרופון של המקלדת.':event.error==='audio-capture'?'לא נמצא מיקרופון זמין. בדוק את חיבור המיקרופון והרשאות המכשיר.':event.error==='network'?'שירות זיהוי הדיבור של הדפדפן אינו זמין ברשת. אפשר להקליד או להשתמש במיקרופון של המקלדת.':'זיהוי הדיבור נעצר. אפשר לנסות שוב או להשתמש במיקרופון של המקלדת.';stopDictation();voiceStatus.textContent=message;};
   recognizer.onend=()=>{if(speechRecognizer!==recognizer||voiceSession!==session)return;speechRecognizer=null;if(session.restarts<2&&!document.hidden){session.restarts++;voiceRetry=setTimeout(()=>startRecognizer(session),300);}else{const received=session.received;stopDictation();voiceStatus.textContent=received?'ההקלדה בקול הסתיימה. הטקסט נשמר בשדה; אפשר לערוך ולשלוח.':'הדפדפן סגר את שירות הזיהוי בלי טקסט. בדוק הרשאות מיקרופון או השתמש במיקרופון של המקלדת.';}};recognizer.start();
 }catch{stopDictation();voiceStatus.textContent='לא ניתן להפעיל זיהוי דיבור בדפדפן הזה כרגע. אפשר להשתמש במיקרופון של המקלדת.';}
}
function dictate(event){
 const target=event?.detail?.target||lastVoiceTarget;
 if(voiceSession){const sameTarget=voiceSession.target===target;stopDictation();if(sameTarget)return;}
 const Recognition=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!window.isSecureContext){voiceStatus.textContent='להפעלת המיקרופון פתח דרך localhost או HTTPS.';return;}
 if(!Recognition){voiceStatus.textContent='הדפדפן אינו תומך בהכתבה כאן. אפשר להשתמש במיקרופון של המקלדת.';return;}
 if(!['coach-question','work-report'].includes(target)||!$(target)){voiceStatus.textContent='פתח קודם שדה שאלה או דיווח.';return;}
 placeVoiceStatus($(target));
 clearTimeout(voiceRetry);window.speechSynthesis?.cancel();voiceSession={target,restarts:0,received:false};startRecognizer(voiceSession);
}
voiceInput.addEventListener('click',dictate);document.addEventListener('coach-dictate',dictate);
document.addEventListener('coach-stop-dictation',stopDictation);
voiceRead.addEventListener('click',()=>{
 stopDictation();
 const text=lastGuidance?.instruction||mentor.state?.messages.filter(message=>message.role==='chef').at(-1)?.text;
 if(!text){voiceStatus.textContent='בחר מנה כדי להתחיל לקבל הנחיות.';return;}
 if(!window.speechSynthesis||!window.SpeechSynthesisUtterance){voiceStatus.textContent='הקראה אינה נתמכת בדפדפן הזה.';return;}
 const locale=/[\u0590-\u05ff]/.test(text)?'he':'en';const voices=window.speechSynthesis.getVoices().filter(voice=>voice.lang.toLowerCase().startsWith(locale));const voice=voices.find(candidate=>candidate.localService)||voices[0];
 if(!voice){voiceStatus.textContent='לא נמצא קול מתאים. התקן קול בעברית במכשיר או נסה דפדפן אחר.';return;}
 window.speechSynthesis.cancel();const utterance=new SpeechSynthesisUtterance(text.replace(/https?:\/\/\S+/g,''));utterance.voice=voice;utterance.lang=voice.lang;utterance.onerror=()=>{voiceStatus.textContent='ההקראה לא הושלמה.';};window.speechSynthesis.speak(utterance);voiceStatus.textContent='מקריא את ההנחיה.';
});
voiceStop.addEventListener('click',()=>{stopCoachVoice();voiceStatus.textContent='הקול נעצר.';});
document.addEventListener('coach-guidance',event=>{window.speechSynthesis?.cancel();lastGuidance=event.detail;if(voiceSession&&$(voiceSession.target))placeVoiceStatus($(voiceSession.target));});
document.addEventListener('chef-decision',event=>{window.speechSynthesis?.cancel();lastGuidance=event.detail;});
document.addEventListener('chef-session-reset',()=>{stopCoachVoice();lastGuidance=null;voiceStatus.textContent='';});
document.addEventListener('visibilitychange',()=>{if(document.hidden)stopCoachVoice();});window.addEventListener('pagehide',stopCoachVoice);
