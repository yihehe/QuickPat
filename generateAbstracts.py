import lib.openaiapi as openaiapi
import pandas as pd
import lib.constants as constants
import lib.evaluate as evaluate

patents_df = pd.read_parquet(constants.PROCESSED_FILE)

# Open AI API parameters
temp_value = 1
max_tokens_value = 256
top_p_value = 1
frequency_penalty_value = 0
presence_penalty_value = 0

abstract_system = 'Generate a patent abstract from the provided claim that is suitable for use in a patent application. In the abstract, do not make reference to the words "abstract", "invention", "patent", "patent application", or "document". Do not discuss the advantages or improvements. Use simple and plain language, but avoid using slang. Limit the abstract to 150 words.'

df = pd.DataFrame(columns=['i', 'title', 'ground_truth_abstract', 'generated_abstract'])

for i in constants.PATENT_INDICES:
    print("--------------------------------------------------")
    patent = patents_df.iloc[i]
    # print(patent)

    ground_truth_abstract = patent["abstract"]
    first_claim = patent["claim_data"][0]

    api_response = openaiapi.sendAPIRequest(abstract_system, first_claim, temp_value, max_tokens_value, top_p_value, frequency_penalty_value, presence_penalty_value)
    generated_abstract = api_response.choices[0].message.content

    print('Ground truth abstract: ', ground_truth_abstract)
    print('Generated abstract: ' , generated_abstract)

    df = df._append({
        'i': i,
        'title': patent["title"],
        'ground_truth_abstract': ground_truth_abstract,
        'generated_abstract': generated_abstract,
    }, ignore_index=True)

print("writing to file", constants.GENERATED_ABSTRACTS_FILE)
df.to_csv(constants.GENERATED_ABSTRACTS_FILE, index=False)
