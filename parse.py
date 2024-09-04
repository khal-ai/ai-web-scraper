from langchain_openai import ChatOpenAI  # Use ChatOpenAI for chat models
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return this string 'Désolé. Aucune donnée ne correspond à la requête.'."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Initialize the ChatOpenAI model; you may need to specify the API key if not set globally
model = ChatOpenAI(model_name="gpt-4o-mini")  # Use ChatOpenAI for chat models

def parse_with_openai(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        input_data = {
            "dom_content": chunk,
            "parse_description": parse_description
        }
        
        messages = prompt.format_prompt(**input_data).to_messages()
        response = model(messages)

        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response.content)

    return "\n".join(parsed_results)
