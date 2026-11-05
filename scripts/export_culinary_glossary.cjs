// Export the UI dictionary to an Obsidian note from the same definitions.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const source=fs.readFileSync(path.join(root,'backend/app/static/culinary-glossary.js'),'utf8');
const terms=vm.runInNewContext(source.split('let culinaryGlossaryDialog')[0]+';culinaryTerms');
const text='---\nid: Culinary-Plain-Language-Glossary\ntype: glossary\nname: מילון בישול בשפה פשוטה\ndomain: food_science\ntags: [culinary/glossary]\n---\n\n# מילון בישול בשפה פשוטה\n\n'+terms.map(t=>'## '+t.term+'\n\n'+t.meaning+'\n'+(t.aliases?'\nשמות נוספים: '+t.aliases.join(', ')+'\n':'')).join('\n');
fs.writeFileSync(path.join(root,'vault/Culinary-Knowledge/00_Ontology/Culinary-Plain-Language-Glossary.md'),text,'utf8');
console.log(`Exported ${terms.length} glossary entries.`);
