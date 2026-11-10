import fs from 'node:fs/promises';
const r=JSON.parse(await fs.readFile('artifacts/semantic-report.json'));
const b=JSON.parse(await fs.readFile('artifacts/semantic-browser.json'));
const m=JSON.parse(await fs.readFile('docs/pregunta/manifest.json'));
const pct=x=>(100*x).toFixed(1)+' %';
const times=r.results.map(x=>x.embeddingMs+x.hybridSearchMs).sort((a,b)=>a-b);
const lines=[
 '# Validación de búsqueda híbrida estática',
 '',`Commit documental: \`${r.commit}\`. Corpus: ${m.documents.length} documentos, ${m.chunks} fragmentos.`,
 '', 'Resultados reales de la ejecución registrada; evaluación exploratoria de regresión, sin revisión independiente ni etiquetas exhaustivas.',
 '', '| Métrica | BM25 | Híbrida |','|---|---:|---:|',
 `| Recall@5 del extracto de referencia (${r.supported} preguntas) | ${pct(r.bm25RecallAt5)} | ${pct(r.hybridRecallAt5)} |`,
 `| Recall@5 del documento de referencia | ${pct(r.bm25DocumentRecallAt5)} | ${pct(r.hybridDocumentRecallAt5)} |`,
 `| Abstenciones correctas (${r.unsupported} sin respuesta) | ${r.bm25CorrectAbstentions}/${r.unsupported} | ${r.correctAbstentions}/${r.unsupported} |`,
 `| Abstenciones incorrectas (${r.supported} respaldadas) | ${r.bm25FalseAbstentions} | ${r.falseAbstentions} |`,
 '', `Semántica sola, como diagnóstico: Recall@5 estricto ${pct(r.semanticRecallAt5)}. La fusión no se presume superior a cada componente.`,
 '',`Calibración: 12 preguntas separadas; umbral ${r.calibration.threshold.toFixed(6)}; exactitud balanceada en calibración ${pct(r.calibration.balanced)}. Este ajuste no demuestra generalización.`,
 '',`Latencia Node WASM, modelo caliente: mediana ${(times[Math.floor(times.length/2)]).toFixed(1)} ms; p95 ${times[Math.ceil(times.length*.95)-1].toFixed(1)} ms. No incluye descarga ni representa un teléfono.`,
 '',`Navegador Chromium: ${b.cosines.length} comparaciones de embeddings; coseno mínimo ${Math.min(...b.cosines).toFixed(9)}; máxima diferencia por coordenada ${Math.max(...b.maxErrors).toExponential(3)}. Solicitudes a terceros: ${b.externalRequests}. Solicitudes de pesos durante la prueba: ${b.modelRequests}. Tiempo del escenario completo local: ${b.secondsIncludingColdLoad.toFixed(2)} s; no es una medición de descarga por Internet.`,
 '',`Ruta validada: \`${b.prefix}pregunta/\`. Se comprobaron citas al SHA y líneas, abstención, ausencia de desbordamiento móvil y reutilización del modelo. Todos los fragmentos se compararon byte a byte con sus intervalos de origen.`,
 '', 'Pruebas incrementales: archivos intactos, nuevos, modificados, eliminados, caché JSON corrupto y reconstrucción completa. El workflow impide desplegar si fallan.',
 '', 'Limitaciones: la recuperación de evidencia exacta sigue siendo baja; un documento relevante no garantiza respuesta completa. El umbral y las reglas de alcance pueden fallar ante preguntas nuevas. La descarga inicial ronda 160 MB y la inferencia depende de la RAM/CPU del dispositivo. No se validaron Safari/iOS ni Android reales.',
 '', 'Las consultas usan únicamente recursos del mismo origen y cómputo local; no requieren APIs pagas. Esto no garantiza capacidad ilimitada ni la factura global de la cuenta de GitHub. Véase README para límites de Pages/Actions y mantenimiento.',
 '', '| Pregunta | Recall@5 BM25 | Recall@5 híbrida | Abstiene |','|---|---:|---:|---|',
 ...r.results.map(x=>`| ${x.id}: ${x.query.replaceAll('|','/')} | ${x.bm25.recall===null?'—':pct(x.bm25.recall)} | ${x.hybrid.recall===null?'—':pct(x.hybrid.recall)} | ${x.abstain?'Sí':'No'} |`),''
];
await fs.writeFile('artifacts/semantic-report.md',lines.join('\n'));
console.log('Wrote artifacts/semantic-report.md');
