import os
from flask import Flask, request, render_template
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    outputs = []
    if request.method == 'POST':
        # Initialize OpenAI LLM
        llm = OpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'))

        # Get list of all form inputs
        prompts = request.form.getlist('prompts')

        # Run the prompts
        try:
            for i, prompt_text in enumerate(prompts):
                # Include the outputs of the previous prompts in the next prompt
                if outputs:
                    prompt_text = outputs[-1] + ' ' + prompt_text
                
                prompt = PromptTemplate.from_template(prompt_text)
                chain = LLMChain(llm=llm, prompt=prompt)

                # Run the chain with the previous output as input
                output = chain.run({'text': outputs[-1]} if outputs else {'text': ''})

                # Append prompt and output to outputs
                outputs.append(f"Prompt {i+1}: {prompts[i]}\n\n{output}")
        except Exception as e:
            outputs = ['Error: ' + str(e)]

    return render_template('index.html', output='\n\n'.join(outputs))

if __name__ == '__main__':
    app.run(debug=True)