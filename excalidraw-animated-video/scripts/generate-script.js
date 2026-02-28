#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function generateScript(storyboardPath, outputPath) {
  const storyboard = JSON.parse(fs.readFileSync(storyboardPath, 'utf-8'));
  
  let markdown = `# ${storyboard.title}\n\n`;
  
  let currentTime = 0;
  
  for (const scene of storyboard.scenes) {
    const startTime = formatTime(currentTime);
    const endTime = formatTime(currentTime + scene.duration);
    
    markdown += `## Scene: ${scene.title} (${startTime} - ${endTime})\n\n`;
    
    if (scene.voiceover) {
      markdown += `${scene.voiceover}\n\n`;
    }
    
    currentTime += scene.duration;
  }
  
  markdown += `---\n\n总时长: ${storyboard.duration}秒\n`;
  
  fs.writeFileSync(outputPath, markdown);
  console.log(`Generated: ${outputPath}`);
}

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

const args = process.argv.slice(2);

if (args.length < 2) {
  console.log('Usage: node generate-script.js <storyboard.json> <output.script.md>');
  process.exit(1);
}

const storyboardPath = path.resolve(args[0]);
const outputPath = path.resolve(args[1]);

generateScript(storyboardPath, outputPath);
