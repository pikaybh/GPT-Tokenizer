# Count Tokens

## Encodings

Encodings specify how text is converted into tokens. Different models use different encodings.

`tiktoken` supports three encodings used by OpenAI models:

| Encoding name | OpenAI models |
|---------------|---------------|
| o200k_base | gpt-4o, gpt-4o-mini |
| cl100k_base | gpt-4-turbo, gpt-4, gpt-3.5-turbo, text-embedding-ada-002, text-embedding-3-small, text-embedding-3-large |
| p50k_base | Codex models, text-davinci-002, text-davinci-003 |
| r50k_base (or gpt2) | GPT-3 models like davinci |

You can retrieve the encoding for a model using tiktoken.encoding_for_model() as follows:

encoding = tiktoken.encoding_for_model('gpt-4o-mini')
Note that p50k_base overlaps substantially with r50k_base, and for non-code applications, they will usually give the same tokens.