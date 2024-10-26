import json
import os
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods, EmbeddingTypes
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ibm import WatsonxEmbeddings, WatsonxLLM

load_dotenv()

my_credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": os.getenv("WATSON_API"),
}
project_id = os.getenv("PROJECT_ID")

client = APIClient(my_credentials)

ModelTypes = client.foundation_models.TextModels

documents = []
# HANDLE VECTOR FILES
filenames = ['./documents/prepare.pdf', './documents/fema-alerts.pdf', './documents/FL-emergency.pdf', './documents/pets.pdf', ]

for (i, filename) in enumerate(filenames):
  # Load and process documents
    loader = PyPDFLoader(filename)
    loaded_docs = loader.load()
    documents.extend(loaded_docs)

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_chunks = []

for doc in documents:
    chunks = text_splitter.split_documents([doc])
    all_chunks.extend(chunks)

embeddings = WatsonxEmbeddings(
    model_id=EmbeddingTypes.IBM_SLATE_30M_ENG,
    url=my_credentials["url"],
    apikey=my_credentials["apikey"],
    project_id=project_id
    )

docsearch = Chroma.from_documents(all_chunks, embeddings)

gen_parms = {
    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
    GenParams.MAX_NEW_TOKENS: 250,

    GenParams.STOP_SEQUENCES: ["<|endoftext|>"],
    GenParams.REPETITION_PENALTY: 1.05
}
model_id = ModelTypes.LLAMA_3_1_70B_INSTRUCT

model = WatsonxLLM(
    model_id=model_id.value,
    url=my_credentials.get("url"),
    apikey=my_credentials.get("apikey"),
    params=gen_parms,
    project_id=project_id,
)

examples = """
The user has a household size of 4, and lives in a single family home. They live in evacuation zone 1, which is under mandatory evacuation. Hurricane-force winds arrive in 36 hours. The user will evacuate to a hotel 2 hours away via car. A state of emergency has been declared. The user takes prescription medications. The user has two small pets.
- Install shutters or boards if you have them. Remember that taping windows does not prevent them from breaking.
- Turn your refrigerator and freezer to the coldest setting and keep the doors closed as much as possible.
- Fill your car's gas tank before you leave. Gas stations may be closed after the storm.
- Bring your emergency kit with you.
- Make sure your pets are in a secure carrier or crate.
- Never drive through standing water. It may be deeper than you think.
- Follow the evacuation route as described. Do not take shortcuts or defer to a GPS.
- Pack enough clothes for 3 days.
- Bring your important documents such as your driver's license passport and insurance information.
- Bring your medications and any medical equipment you need.
- Bring enough food and water for 3 days.
- Bring your pets' food and water as well as any medications they need.
- Under a state of emergency Floridians are permitted to receive early prescription refills. If needed check if your pharmacy is open before you leave.
<|endoftext|>

The user has a household size of 2, and lives in an apartment. They live in evacuation zone 3, which is under advisory evacuation. Hurricane-force winds arrive in 48 hours. The user will shelter in place, but may evacuate to family who live 4 hours away if forecasts worsen. A state of emergency has been declared. The user has no pets.
- Before you leave, bring in anything on your balcony or patio that could become a projectile.
- Close and lock all windows and doors.
- Turn your refrigerator and freezer to the coldest setting.
- Fill your car's gas tank before you leave. Gas stations may be closed after the storm.
- Bring your emergency kit with you.
- Make sure your pets are in a secure carrier or crate.
- Never drive through standing water. It may be deeper than you think.
- Pack enough clothes for 3 days.
- Bring your important documents, such as your driver's license, passport, and insurance information.
- Bring your medications and any medical equipment you need.
- Bring enough food and water for 3 days.
<|endoftext|>

The user has a household size of 1, and is homeless. They live in evacuation zone 4, which is not under evacuation. Tropical-storm-force winds arrive in 24 hours. The user will evacuate to a shelter via bus. A state of emergency has not been declared. The user does not take prescription medications. The user has no pets.
- Bring your belongings with you.
- Bring your important documents, such as your driver's license, passport, and insurance information.
- Bring food and water, if possible.
- Bring a change of clothes and a blanket or sleeping bag.
- Bring a phone charger and a portable charger.
- Bring a small amount of cash, if possible.
- Bring a small amount of personal hygiene items.
- Bring a small amount of non-perishable snacks.
- RTS bus service will be suspended once area winds reach 35 mph. Make sure you're at the shelter before then.
<|endoftext|>
"""
# GENERATE

#generated_response = model.generate_prompt(prompt=prompt_txt)

# qa = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=docsearch.as_retriever())
# generated_response = qa.invoke(new_prompt)

# Manually query the vector data
new_query = "The user has a household size of 1, and is homeless. They live in evacuation zone 2, which is under mandatory evacuation. Hurricane-force winds arrive in 18 hours. The user will evacuate to a shelter via bus. A state of emergency has been declared. The user does take prescription medications. The user has no pets."
retrieved_docs = docsearch.similarity_search(new_query, 3)

# Generate response based on retrieved documents
retrieved_texts = " ".join([doc.page_content for doc in retrieved_docs])

combined_prompt = f"""
Based on the provided user profile, and the provided context, generate advise for how to prepare for a hurricane. Consider the specifics of each user's scenario, and consider the provided documents as starting points to ground your response in.
The bullet points will be used to display supplementary information in an application. The following information is coded in, and does not need to be covered in your response: Available shelters, transit options. Also, do not include any sort of explanation for why you included or excluded certain information. The response should be a list of bullet points, each starting with a dash. The response should be tailored to the user's specific scenario.
### CONTEXT
{retrieved_texts}
###
### EXAMPLES
{examples}
###
### YOUR QUERY
{new_query}
###
### YOUR RESPONSE
"""

generated_response = model.invoke(combined_prompt)

print("Output from generate() method:")
print(json.dumps(generated_response, indent=2))
