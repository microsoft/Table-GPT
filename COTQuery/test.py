import openai

openai.api_key = "oaip_bzUHFBVlVBLJPNokzGTfpFhNEokQtWHL"
openai.api_base = "https://msrgptproxy2.azurewebsites.net/v1"

response = openai.ChatCompletion.create(
    messages= [ # Change the prompt parameter to the messages parameter
        {'role': 'user', 'content': "2+2="}
    ],
    model="gpt-4",
    max_tokens=400,
)

print(response)