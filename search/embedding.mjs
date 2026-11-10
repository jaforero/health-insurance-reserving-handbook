import modelConfig from './config.json' with {type:'json'};
export const modelRevision=modelConfig.revision;
import {env, pipeline} from '@huggingface/transformers';
export async function encoder(base, progress_callback) {
  env.allowRemoteModels=false;
  env.allowLocalModels=true;
  env.localModelPath=base+'models/';
  env.backends.onnx.wasm.wasmPaths=base+'runtime/';
  env.backends.onnx.wasm.numThreads=1;
  env.useBrowserCache=typeof caches !== 'undefined';
  const model=await pipeline('feature-extraction','e5-'+modelRevision, {device:'auto',dtype:'q8', local_files_only:true, progress_callback, session_options:{executionProviders:['wasm']}});
  const embed=async (text,kind='query')=>Array.from((await model(kind+': '+text,{pooling:'mean',normalize:true,truncation:true,max_length:512})).data);
  return {embed,tokenizer:model.tokenizer};
}
