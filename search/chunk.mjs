// Line-preserving Markdown section parser. Fences are opaque to heading detection.
export function sections(source, path) {
  const lines=source.split('\n'), out=[]; let start=0, heading=path, title=path, fence=null, math=null;
  if(lines[0]?.trim()==='---') { const end=lines.findIndex((l,i)=>i>0&&l.trim()==='---'); if(end>=0) start=end+1; }
  let begin=start;
  function emit(end) {
    let a=begin,b=end;
    while(a<b&&!lines[a].trim()) a++;
    while(b>a&&!lines[b-1].trim()) b--;
    if(a<b) out.push({path,title,heading,start:a+1,end:b,text:lines.slice(a,b).join('\n')});
  }
  for(let i=start;i<lines.length;i++) {
    const line=lines[i], f=line.match(/^\s{0,3}(`{3,}|~{3,})/);
    if(f) { if(!fence) fence=f[1]; else if(f[1][0]===fence[0]&&f[1].length>=fence.length) fence=null; continue; }
    if(fence) continue;
    const trimmed=line.trim();
    if(math) { if(trimmed===math) math=null; continue; }
    if(trimmed==='$$'||trimmed==='\\[') {math=trimmed==='$$'?'$$':'\\]';continue;}
    const h=line.match(/^ {0,3}(#{1,6})\s+(.+?)(?:\s+#+)?\s*$/);
    const setext=i+1<lines.length && line.trim() && /^ {0,3}(=+|-+)\s*$/.test(lines[i+1]);
    // Keep H3-H6 subsections with their H2 parent so assumptions and definitions retain context.
    if((h && h[1].length<=2)||setext) {
      emit(i); heading=h?h[2]:line.trim(); if(h?.[1]==='#'||(setext&&lines[i+1].trim()[0]==='=')) title=heading;
      begin=i; if(setext)i++;
    }
  }
  emit(lines.length); return out;
}
// Tokenizer-aware subdivision; text remains an exact contiguous source excerpt.
export function splitSection(section, tokenizer, limit) {
  const result=[], lines=section.text.split('\n'); let begin=0;
  const fits=text=>tokenizer('passage: '+section.title+'\n'+text,{truncation:false}).input_ids.size<=limit;
  while(begin<lines.length) {
    let end=begin+1;
    if(!fits(lines[begin])) throw Error(`Single source line exceeds token limit: ${section.path}:${section.start+begin}`);
    while(end<lines.length&&fits(lines.slice(begin,end+1).join('\n'))) end++;
    if(end<lines.length) {
      for(let k=end-1;k>begin+Math.floor((end-begin)/2);k--) if(!lines[k].trim()) {end=k+1;break;}
    }
    const text=lines.slice(begin,end).join('\n');
    if(text.trim()) result.push({...section,text,start:section.start+begin,end:section.start+end-1});
    begin=end;
  }
  return result;
}
