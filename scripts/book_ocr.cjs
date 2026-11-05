// Local OCR only. Models are cached locally; document images are never uploaded.
const fs = require('node:fs');
const path = require('node:path');
const {createWorker, createScheduler} = require('../tmp-book-ocr/node_modules/tesseract.js');

async function main() {
  const queue = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const language = process.argv[3] || 'eng';
  const scheduler = createScheduler();
  const workers = await Promise.all(Array.from({length: 4}, () => createWorker(language, 1, {
    cachePath: path.resolve('tmp-book-processing'), cacheMethod: 'readOnly',
  })));
  workers.forEach(worker => scheduler.addWorker(worker));
  let done = 0;
  try {
    await Promise.all(queue.map(async task => {
      if (!fs.existsSync(task.output)) {
        const {data} = await scheduler.addJob('recognize', task.image);
        fs.writeFileSync(task.output, JSON.stringify({text:data.text, confidence:data.confidence,
          language, engine:'Tesseract.js', engine_version:require('../tmp-book-ocr/node_modules/tesseract.js/package.json').version,
          image:task.image}, null, 2));
      }
      done++;
      if (done % 10 === 0 || done === queue.length) console.log(`${done}/${queue.length} OCR pages`);
    }));
  } finally { await scheduler.terminate(); }
}
main().catch(error => {console.error(error); process.exitCode = 1;});
