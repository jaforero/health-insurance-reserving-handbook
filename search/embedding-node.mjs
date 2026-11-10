// Transformers.js 3.8.1 exposes an ONNX runtime injection hook. Pinning the same
// WASM runtime in Node and browsers avoids native CPU quantization discrepancies.
import * as ort from 'onnxruntime-web';
globalThis[Symbol.for('onnxruntime')] = ort;
export const {encoder} = await import('./embedding.mjs');
